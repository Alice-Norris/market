from PySide6.QtCore import QModelIndex, Qt, QSortFilterProxyModel, QSettings
from json import load
from MarketGaze.RecipeListModel import RecipeModel

class RecipeFilterModel(QSortFilterProxyModel):
  def __init__(self, parent):
    super().__init__(parent)
    self.jobs ={}
    self.setSourceModel(RecipeModel())
    self.setupJobs()
  
  def setupJobs(self):
    cfg = QSettings()
    cfg.beginGroup("JobSelect")
    jobs = cfg.allKeys()
    for job in jobs:
      self.jobs[job] = cfg.value(job)
    cfg.endGroup()
  
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
