from urllib3 import PoolManager
from pathlib import Path
from math import ceil
from constants import BoolQuery, SortType, TermQuery, FILE_NAMES, FILE_DIRS
from req_builder import RequestBuilder
import json
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

class DataHandler:
  def __init__(cls):
    cls.pool = PoolManager()
    cls.req_builder = RequestBuilder()
    cls.chk_files()

  # --- File Operations --- #
    
  # Checks if each file is present. If the file is present,
  # the file is loaded. Otherwise, the appropriate function
  # is called.
  def chk_files(cls):
    for name in FILE_NAMES["json"]:
      dir = FILE_DIRS["json"]

      fp = Path(dir + name)

      if not fp.is_file() or fp.stat().st_size == 0:
        cls.fetch_data(fp)

  def fetch_data(cls, path):
    match path.stem:
      case "dc" | "world" | "dc_world_id":
        cls.fetch_dcs()
      case "class_job":
        cls.fetch_jobs()
      case "craft_type":
        cls.fetch_crafts()
      case "recipes":
        cls.fetch_recipes()

  # writes data from data handler's dictionary to a file.
  def write_data(cls, name: str, data: dict[str:str]):
    """Writes DataHandler's data to the appropriate files."""
    path = Path("./data/json/" + name + ".json")
    file_mode = "r"

    if not path.is_file():
      file_mode = "x"
    else:
      file_mode = "w"
    
    with open(path, file_mode) as file:
      json.dump(data, file, indent=2)

  # Creates data directory (and subfolders) if needed.
  def mk_dirs(cls):
    data_path = Path("data")
    if not data_path.is_dir():
      data_path.mkdir()
      for folder_name in ["icons", "json"]:
        sub_data_path = Path("data/" + folder_name)
        if not sub_data_path.is_dir():
          sub_data_path.mkdir()
    
  # This should be run only when cache is cleared by user.
  def delete_data(cls):
    for name in FILE_NAMES["json"]:
      dir = FILE_DIRS["json"]
      Path(dir+name).unlink()
    cls.chk_files()

  # --- Network Data Request Functions --- #
  # Requests datacenter info from server and puts the data in the dictionary
  def fetch_dcs(cls):
    base_url = "https://xivapi.com/search"
    cls.req_builder.new_req(["World"], ["Name", "ID", "DataCenter.Name", "DataCenter.ID"], 83)
    cls.req_builder.add_sort(SortType.ASC, "DataCenter.ID")
    cls.req_builder.add_term_query(BoolQuery.MUST, TermQuery.EXISTS, {"field_name":"DataCenter"})
    cls.req_builder.add_term_query(BoolQuery.FILT, TermQuery.TERMS, {"field":"IsPublic", "values":"1"})
    num_results = cls.get_result_size(base_url)
    resp_data = cls.get_results(base_url, num_results)
    cls.process_dcs(resp_data)
    
  def fetch_jobs(cls):
    base_url = "https://xivapi.com/classjob"
    cls.req_builder.new_req(columns=["ID","Abbreviation","DohDolJobIndex"])
    num_results = cls.get_result_size(base_url)
    resp_data = cls.get_results(base_url, num_results)
    cls.process_jobs(resp_data)

  # Requests recipe data, putting each job's data in the dictionary
  def fetch_recipes(cls):
    base_url = "https://xivapi.com/search"
    cls.req_builder.new_req(indexes=["Recipe"], columns=["ItemResultTargetID","Name","ID","ClassJob.ID","RecipeLevelTable.ClassJobLevel"])
    cls.req_builder.add_sort(SortType.ASC, "ClassJob.ID")
    cls.req_builder.add_sort(SortType.ASC, "RecipeLevelTable.ClassJobLevel")
    num_results = cls.get_result_size(base_url)
    results = cls.get_results(base_url, num_results)
    cls.process_recipes(results)

  def fetch_crafts(cls):
    base_url = "https://xivapi.com/CraftType"
    cls.req_builder.new_req(indexes = [], columns=["Name", "ID"])
    num_results = cls.get_result_size(base_url)
    results = cls.get_results(base_url, num_results)
    cls.process_crafts(results)
  
  def process_dcs(cls, data):
    dc_data = {}
    for world in data:
      dc_info = world.pop("DataCenter")
      dc_name = dc_info["Name"]
      dc_id = dc_info["ID"]
      if dc_info["Name"] not in dc_data:
        dc_data[dc_name] = { "id": dc_id, "worlds": {world["Name"] : world["ID"]}}
      else:
        dc_data[dc_name]["worlds"].update({world["Name"]:world["ID"]})
    cls.write_data("dc", dc_data)

  # def process_dcs(cls, data):
  #   dc_data = {}
  #   world_data = []
  #   for world in data:
  #     dc_info = world.pop("DataCenter")
  #     if dc_info["Name"] not in dc_data:
  #       dc_data[dc_info["Name"]] = dc_info["ID"]
  #       world_data.append({})
  #     world_data[-1][world["Name"]] = world["ID"]
  #   cls.write_data("dc", dc_data)

  def process_jobs(cls, data):
    job_data = {}
    for job in data:
      if len(job["Abbreviation"]) != 0 and int(job["DohDolJobIndex"]) >= 0:
        abbr = job["Abbreviation"]
        id = job["ID"]
        job_data[abbr] = id
    cls.write_data("class_job", job_data)
  
  def process_recipes(cls, data):
    recipe_data = {}
    
    for recipe in data:
      class_id = recipe["ClassJob"]["ID"]
      craft_lvl = recipe["RecipeLevelTable"]["ClassJobLevel"]
      item = {"lvl":craft_lvl, "id": recipe["ID"], "name": recipe["Name"]}
    
      if class_id not in recipe_data:
        recipe_data["recipes"][class_id] = [item]
      else:
        recipe_data["recipes"][class_id].append(item)
    
    cls.write_data("recipes", recipe_data)

  def process_crafts(cls, data):
    crafts_data = {}
    for craft_data in data:
      craft_name = craft_data["Name"]
      craft_id = craft_data["ID"]
      crafts_data[craft_id] = craft_name

    cls.write_data("craft_type")

  def get_result_size(cls, url: str):
    headers={"ContentType":"application/json"}
    query = cls.req_builder.gen_query()
    resp = cls.pool.request("GET", url, headers, body=query)
    page_data = json.loads(resp.data)["Pagination"]
    return page_data["ResultsTotal"]
  
  def get_results(cls, url:str, size:int):
    result_data = []
    header = {"ContentType":"application/json"}
    cls.req_builder.set_size(500)
    
    num_queries = ceil(size / 500)
    start_index = 0
    
    for x in range(0,num_queries):
      cls.req_builder.set_start(start_index)
      resp = cls.pool.request("GET", url, header, body=cls.req_builder.gen_query())
      results = json.loads(resp.data)["Results"]
      result_data.extend(results)
      start_index += 500
    return result_data