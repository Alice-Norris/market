from PySide6.QtCore import QModelIndex, Qt, QAbstractItemModel
from pathlib import Path
from json import load
from MarketGaze.ModelClass import Job, Recipe
      
class RecipeModel(QAbstractItemModel):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.jobs = []
    self.load_data()

  def flags(self, index: QModelIndex):
    if not index.parent().isValid():
      match index.column():
        case 0:
          return Qt.ItemFlag.ItemIsEnabled
        case _:
          return Qt.ItemFlag.NoItemFlags
    else:
      match index.column():
        case 1:
          return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemNeverHasChildren
        case 2:
          return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemNeverHasChildren
        case _:
          return Qt.ItemFlag.NoItemFlags
    
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

  def hasChildren(self, index):
    if not index.parent().isValid():
      return True
    else:
      return False

  def index(self, row: int, column: int, parent: QModelIndex=QModelIndex()):
    if not self.hasIndex(row, column, parent):
      return QModelIndex()
    
    if not parent.isValid():
      if column == 0:
        job = self.jobs[row]
        return self.createIndex(row, 0, job)
      else:
        return QModelIndex()
    else:
      job = parent.internalPointer()
      recipe = job.get_recipe(row)
      
      if recipe is not None:
        return self.createIndex(row, column, recipe)
          
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
    
  def setData(self, index, val, role):
    if role == Qt.ItemDataRole.CheckStateRole:
      if not index.parent().isValid() and index.column() == 0:
        index.internalPointer().setData(val, role)
      
      if index.parent().isValid() and index.column() == 1:
        index.internalPointer().setData(val, role)
      return True
    return False
  
  def data(cls, index, role):
    if not index.isValid():
      return None
    
    if not index.parent().isValid():
      job: Job = index.internalPointer()
      return job.data(role)
    else:
      recipe: Recipe = index.internalPointer()
      return recipe.data(index.column(), role)
