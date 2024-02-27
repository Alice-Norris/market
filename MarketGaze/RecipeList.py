from PySide6.QtWidgets import QTreeView, QHeaderView
from PySide6.QtCore import Signal, Qt, Slot, QModelIndex, QItemSelection, QItemSelectionModel
from PySide6.QtGui import QMouseEvent
from MarketGaze.RecipeFilterModel import RecipeFilterModel

class RecipeList(QTreeView):
  send_recipe_ids = Signal(list, name="SendRecipeIds")
  
  def __init__(self, parent):
    super().__init__(parent)
    self.show()
    #self.setSelectionBehavior(self.SelectionBehavior.SelectItems)
    filter_model = RecipeFilterModel(self)
    self.setModel(filter_model)
    self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    self.header().setStretchLastSection(False)
    self.setSelectionMode(QTreeView.SelectionMode.MultiSelection)
  
  @Slot(str, dict, name="ReceiveSortUpdate")
  def receive_sort_update(self, name, sort_data):
    self.model().updateSort(name, sort_data)

  @Slot(name="SendIds")
  def send_search_ids(self):
    items = self.selectionModel().selectedIndexes()
    item_ids = [item.data(Qt.ItemDataRole.UserRole)[0] for item in items]
    self.send_recipe_ids.emit(item_ids)

  def mousePressEvent(self, m_event: QMouseEvent):
    event_point = m_event.position().toPoint()
    index = self.indexAt(event_point)
    
    if index.column() == 0:
      last_row = self.model().rowCount(index)
      last_col = self.model().columnCount(index)
      start = self.model().index(0, 1, index)
      end = self.model().index(last_row, last_col, index)
      child_items = QItemSelection(start, end)
      self.selectionModel().selection().merge(child_items, QItemSelectionModel.SelectionFlag.Current)
      self.selectionChanged(child_items, QItemSelection())
    super().mousePressEvent(m_event)
    
  def job_clicked(self, index: QModelIndex):
    job_checked = None
    match index.data(Qt.ItemDataRole.CheckStateRole):
      case Qt.CheckState.Checked:
        job_checked = Qt.CheckState.Unchecked
      case Qt.CheckState.PartiallyChecked | Qt.CheckState.UnChecked:
        job_checked = Qt.CheckState.Checked
    print(index.row(), ", ", index.column())
    rows = self.model().rowCount(index)
    for row in range(0, rows):
      item_index = self.model().index(row, 1, index)
      self.model().setData(item_index, True, Qt.ItemDataRole.CheckStateRole)
      
  #     x=1
      