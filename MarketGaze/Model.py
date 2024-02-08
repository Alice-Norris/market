from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QAbstractItemModel, QSortFilterProxyModel
from pathlib import Path
from json import load
from MarketGaze.ModelClass import Dc, Job, Recipe, World

class ServerModel(QAbstractTableModel):
  def __init__(cls):
    super().__init__()
    cls.dcs = []
    cls.dc_index = 0
    cls.load_data()
  
  def load_data(cls):
    fp = Path("./data/json/dc.json")
    dc_data = None

    if fp.is_file():
      with fp.open() as file:
        dc_data = load(file)

    for dc in dc_data.items():
      cls.dcs.append(Dc(dc[0], **dc[1]))

  def index(cls, row: int, column: int, parent: QModelIndex = QModelIndex()):  
    if column == 0:
      dc = cls.dcs[row]
      return cls.createIndex(row, column, dc)
    elif column > 0 and column <= len(cls.dcs):
      return cls.createIndex(row, column, cls.dcs[column-1].getWorld(row))
  
  def rowCount(cls, index: QModelIndex = QModelIndex()):
    row, col = index.row(), index.column()
    count = 0

    if not index.isValid():
      if cls.dc_index > 0:
        count = cls.dcs[cls.dc_index-1].numWorlds()
      else:
        count = len(cls.dcs)
    else:
      if col == 0:
        count = len(cls.dcs)
      else:
        count = cls.dcs[col-1].numWorlds()
    
    print(f"Row Count returned {count} for row {row}, column {col}")
    return count
    
  def columnCount(cls, index: QModelIndex = QModelIndex()):
    return len(cls.dcs)+1
    
  def data(cls, index, role):
    col = index.column()

    cls.dc_index = col  

    item = index.internalPointer()
    
    match role:
      case Qt.ItemDataRole.DisplayRole:
        return item.name
      case Qt.ItemDataRole.UserRole:
        return item.id
      case _:
        return None
      
class RecipeModel(QAbstractItemModel):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.jobs = []
    self.load_data()

  def flags(self, index: QModelIndex):
    if not index.parent().isValid():
      return Qt.ItemFlag.ItemIsEnabled
    
    match index.column():
      case 1:
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
      case 2:
        return Qt.ItemFlag.ItemIsEnabled
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
      job: Job = index.internalPointer()
      return job.data(role)
    else:
      recipe: Recipe = index.internalPointer()
      return recipe.data(index.column(), role)
    
class RecipeFilterModel(QSortFilterProxyModel):

  def __init__(cls, parent):
    super().__init__(parent)
    cls.setSourceModel(RecipeModel())
    cls.setupJobs()
  
  def setupJobs(cls):
    src_model = cls.sourceModel()
    top_lvl_rows = src_model.rowCount()
    cls.jobs = {}
    for row_num in range(0, top_lvl_rows):
      job_index = src_model.index(row_num, 0)
      job_name = src_model.data(job_index, Qt.ItemDataRole.DisplayRole)
      cls.jobs.update({job_name : {"select": False, "min": 1, "max": 1}})

  def updateSort(self, name, sort_data):
    self.jobs[name] = sort_data
    self.invalidateFilter()

  def filterAcceptsRow(cls, row: int, parent: QModelIndex):
    src_model = cls.sourceModel()
    if not parent.isValid():
      job_index = src_model.index(row, 0, parent)
      job_name = src_model.data(job_index, Qt.ItemDataRole.DisplayRole)
      return cls.jobs[job_name]["select"]
    else:
      job_name = src_model.data(parent, Qt.ItemDataRole.DisplayRole)
      recipe_index = src_model.index(row, 2, parent)
      recipe_lvl = src_model.data(recipe_index, Qt.ItemDataRole.DisplayRole)
      return recipe_lvl >= cls.jobs[job_name]["min"] and recipe_lvl <= cls.jobs[job_name]["max"]
  
  def headerData(self, section: int, orientation, role):
    return self.sourceModel().headerData(section, orientation, role)

class JobModel(QAbstractTableModel):
  
  def __init__(self):
    self.job_min_lvl: [int] = [0] * 8
    self.job_max_lvl: [int] = [90] * 8
    self.job_select: [bool] = [False] * 8
    
  def rowCount(self, index):
    return 3
  
  def columnCount(self, index):
    return 8
  
  def data(self, index):
    row, col = index.row(), index.column()
    match col:
      case 0:
        return self.dc
      case 1:
        return self.world
      case 2:
        if col >= 0 and col < 8:
          return self.job_select[row]
      case 3:
        if col >= 0 and col < 8:
          return self.job_min_lvl[row]
      case 4:
        if col >= 0 and col < 8:
          return self.job_max_lvl[row]
  
  def setData(self, index, value, role=None):
    row, col = index.row(), index.column()

    match col:
      case 0 | 1:
        if value is int and col == 0:
          self.dc = value
        elif col == 1:
          self.world = value
      case 2 | 3:
        if value is int and col == 2:
          self.job_min_lvl[row] = value
        elif col == 3:
          self.job_max_lvl[row] = value
      case 4:
        if value is bool:
          self.job_select[row] = value

          