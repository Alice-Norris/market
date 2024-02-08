from PySide6.QtWidgets import QTreeView, QHeaderView
from PySide6.QtCore import Signal, Qt
from MarketGaze.Model import RecipeFilterModel

class RecipeList(QTreeView):
  def __init__(self, parent):
    super().__init__(parent)
    self.show()
    filter_model = RecipeFilterModel(self)
    self.setModel(filter_model)
    self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    self.header().setStretchLastSection(False)
    self.setSelectionMode(QTreeView.SelectionMode.MultiSelection)
    
  def receive_sort_update(self, name, sort_data):
    self.model().updateSort(name, sort_data)

  def get_selected(self):
    items = self.selectionModel().selectedIndexes()
    item_id1 = items[0].data(Qt.ItemDataRole.UserRole)
    item_ids = [item.data(Qt.ItemDataRole.UserRole)[0] for item in items]
    self.returnParams.emit(item_ids)
