from PyQt6.QtCore import QSortFilterProxyModel, QModelIndex, Qt
from recipe_model import RecipeModel
class RecipeFilterModel(QSortFilterProxyModel):
  def __init__(cls, parent, model):
    super().__init__(parent)
    cls.setSourceModel(model)
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

