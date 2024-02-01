from PyQt6.QtCore import QAbstractItemModel, QModelIndex
from PyQt6.QtCore import Qt
from enum import IntEnum
from json import load
from pathlib import Path
from recipe_classes import Job, Recipe

class RecipeModel(QAbstractItemModel):
  def __init__(cls, parent=None):
    super().__init__(parent)
    cls.jobs = []
    
    cls.load_data()
    x=1

  def headerData(cls, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
    if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
      match section:
        case 0:
          return "Job"
        case 1:
          return "Recipe Name"
        case 2:
          return "Recipe Level"
    
  def load_data(cls):
    path = Path("./data/json/class_job.json")

    with open(path) as file:
      cls.insert_jobs(load(file))
    
    path = Path("./data/json/recipes.json")

    with open(path) as file:
      cls.insert_recipes(load(file))
  
  def insert_jobs(cls, jobs: dict[str, int]):
    for job_data in [*jobs.items()][0:8]:
      job_item = Job(*job_data)
      cls.jobs.append(job_item)
  
  def insert_recipes(cls, recipes: dict[str:str, str:int, str:int]):
    for row_num, job_recipes in enumerate(recipes.values()):
      job_index = cls.index(row_num, 0)
      job_item = job_index.internalPointer()
      for recipe in job_recipes:
        recipe_item = Recipe(**recipe, job=job_item)
        job_index.internalPointer().append_recipe(recipe_item)

  def index(cls, row: int, column: int, parent: QModelIndex=QModelIndex()):
    if not cls.hasIndex(row, column, parent):
      return QModelIndex()
    
    if not parent.isValid():
      if column == 0:
        job = cls.jobs[row]
        return cls.createIndex(row, 0, job)
      else:
        return QModelIndex()
    else:
      job = parent.internalPointer()
      recipe = job.get_recipe(row)
      
      if recipe is not None:
        return cls.createIndex(row, column, recipe)
          
  def parent(cls, index):
    if not index.isValid():
      return QModelIndex()
    
    item = index.internalPointer()

    if item in cls.jobs:
      return QModelIndex()
    else:
      job = index.internalPointer().get_job()
      return cls.createIndex(cls.jobs.index(job), 0, job)
    
  def rowCount(cls, parent: QModelIndex=QModelIndex()):
    parent_item = None

    if not parent.isValid():
      return len(cls.jobs)
    else:
      parent_item = parent.internalPointer()
      if parent_item in cls.jobs:
        return parent_item.num_recipes()
      else:
        return 0
    
  def columnCount(cls, parent: QModelIndex = QModelIndex()):
    if not parent.isValid():
      return 3
    parent_item = parent.internalPointer()
    if parent_item in cls.jobs:
      return 3

  def data(cls, index, role):
    if not index.isValid():
      return None
    
    if not index.parent().isValid():
      job = index.internalPointer()
      match role:
        case Qt.ItemDataRole.DisplayRole:
          return job.get_abbr()
        case Qt.ItemDataRole.UserRole:
          return job.get_id()
    else:
      recipe = index.internalPointer()
      match role:
        case Qt.ItemDataRole.DisplayRole:
          match index.column():
            case 1:
              return recipe.get_name()
            case 2:
              return recipe.get_lvl()
        case Qt.ItemDataRole.UserRole:
          return recipe.get_id()