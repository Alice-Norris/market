from enum import StrEnum, Enum

class FFData(Enum):
  RECIPES = {
    "dir": "data/json/",
    "filename":"recipes.json",
    "url": "https://xivapi.com/search",
    "payload": {"indexes": "Recipe",
    "columns": ",".join(["AmountIngredient*",
        "ClassJob.ID",
        "ItemIngredient0TargetID",
        "ItemIngredient1TargetID",
        "ItemIngredient2TargetID",
        "ItemIngredient3TargetID",
        "ItemIngredient4TargetID",
        "ItemIngredient5TargetID",
        "ItemIngredient6TargetID",
        "ItemIngredient7TargetID",
        "ItemIngredient8TargetID",
        "ItemIngredient9TargetID",
        "ItemResult.ID",
        "ItemResult.Name",
        "RecipeLevelTable.ClassJobLevel"
      ]),
      "body": {
        "sort": {
          "ClassJob.ID": "asc"
        },
        "size": 1
      }
    }
  }

  JOBS = {
    "dir": "data/json/",
    "filename": "jobs.json",
    "url": "https://xivapi.com/ClassJob",
    "payload": {
      "columns": ",".join(["ID", "Abbreviation", "DohDolJobIndex"]),
      "body": {}
    }
  }
  
  DATACENTERS = {
    "dir": "data/json/",
    "filename": "datacenters.json",
    "url": "https://universalis.app/api/v2/data-centers"
  }
  WORLDS = {
    "dir": "data/json/",
    "filename": "worlds.json",
    "url":"https://universalis.app/api/v2/worlds"
  }
  ALC = {
    "dir": "data/icon/",
    "filename": "ALC.png",
    "url": "https://xivapi.com/cj/1/alchemist.png"
  }
  ARM = {
    "dir": "data/icon/",
    "filename": "ARM.png",
    "url": "https://xivapi.com/cj/1/armorer.png"
  }
  BSM = {
    "dir": "data/icon/",
    "filename": "BSM.png",
    "url": "https://xivapi.com/cj/1/blacksmith.png"
  }
  BTN = {
    "dir": "data/icon/",
    "filename": "BTN.png",
    "url": "https://xivapi.com/cj/1/botanist.png"
  }
  CRP = {
    "dir": "data/icon/",
    "filename": "CRP.png",
    "url": "https://xivapi.com/cj/1/carpenter.png"
  }
  CUL = {
    "dir": "data/icon/",
    "filename": "CUL.png",
    "url": "https://xivapi.com/cj/1/culinarian.png"
  }
  FSH = {
    "dir": "data/icon/",
    "filename": "FSH.png",
    "url": "https://xivapi.com/cj/1/fisher.png",
  }
  GSM = {
    "dir": "data/icon/",
    "filename": "GSM.png",
    "url": "https://xivapi.com/cj/1/goldsmith.png",
  }
  LTW = {
    "dir": "data/icon/",
    "filename": "LTW.png",
    "url": "https://xivapi.com/cj/1/leatherworker.png"
  }
  MIN = {
    "dir": "data/icon/",
    "filename": "MIN.png",
    "url": "https://xivapi.com/cj/1/miner.png"
  }
  WVR = {
    "dir": "data/icon/",
    "filename": "WVR.png",
    "url": "https://xivapi.com/cj/1/botanist.png"
  }

class App_Data(StrEnum):
  ORG = "Aresu Nereru"
  NAME = "MarketGaze"

class Files(Enum):
  JSON = {
    "dir":"./data/json/",
    "filenames": [
    "class_job.json",
    "dc.json",
    "recipes.json"
    ]
  }
  ICON = {
    "dir":"./data/icons/",
    "filenames": [
    "ALC.png", "ARM.png", "BSM.png", "BTN.png",
    "CRP.png", "CUL.png", "FSH.png", "GSM.png", 
    "LTW.png", "MIN.png", "WVR.png"
    ]
  }

class FiltOp(StrEnum):
  LTE = "lte"
  LT = "lt"
  GT = "gt"
  GTE = "gte"

class SortType(StrEnum):
  ASC = "asc"
  DESC = "desc"

class BoolQuery(StrEnum):
  MUST = "must"
  FILT = "filter"
  SHOULD = "should"
  MUSTNT = "must_not"
  
class TermQuery(StrEnum):
  #TERM = "term"
  TERMS = "terms"
  TERMS_SET = "terms_set"
  RANGE = "range"
  EXISTS = "exists"
  WILDCARD = "wildcard"
  IDS = "ids"

class FullTextQuery(StrEnum):
  MATCH = "match"
  PHRASE = "match_phrase"
  PHRASE_PRE = "match_phrase_prefix"
  MULTI = "multi_match"
  COMM = "common"
  Q_STRING = "query_string"
  S_Q_STRING = "simple_query_string"

# TODO: Remove this
class TermsLookup(StrEnum):
  IND = "index"
  TYPE = "type"
  ID = "id"
  PATH = "path"

class RequestType(StrEnum):
  CURRENT = "current"
  HISTORY = "history"
