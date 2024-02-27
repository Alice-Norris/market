from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt
from MarketGaze.Constants import RequestType
from typing import Any

class ResultModel(QAbstractItemModel):
  items = {}

  def __init__(self, parent=None):
    super().__init__(parent)

  def index(self, row: int, column: int, parent: QModelIndex):
    if not self.hasIndex(row, column, parent):
      return QModelIndex()
    
    if not parent.isValid():
      item_id = self.items.keys([row])
      return self.createIndex(row, column, )
    pass

  def parent(self, index: QModelIndex):
    pass

  def rowCount(self, parent: QModelIndex):
    pass

  def columnCount(self, parent: QModelIndex):
    pass

  def data(self, index: QModelIndex, role: Qt.ItemDataRole):
    pass

  def hasChildren(self, parent: QModelIndex):
    pass

  def flags(self, index: QModelIndex):
    pass

  def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
    pass

  def insertRows(self, row: int, count: int, parent: QModelIndex):
    self.beginInsertRows(parent, row, row+count)
    self.endInsertRows()
    pass

  def insertColumns(self, column: int, count: int, parent: QModelIndex):
    self.beginInsertColumns(parent, column, column+count)
    self.endInsertColumns()
    pass

  def add_item(self, id: int, data: dict, req_type: RequestType):
    id = data.pop("itemID") 
    # removing recentHistory (we don't need it!)
    data.pop("recentHistory", None)
    
    if "worldID" in data:
      world_id = data.pop("worldID")
      world_name = data.pop("worldName")
      self.insert_world_data(world_id, world_name, data, req_type)

    if not id in self.items:
      self.items[id] = {}

    self.items[id][req_type.value] = data    
    
  def add_items(self, data: dict, req_type: RequestType):
    ids = data.pop("itemIDs")
    for id in ids:
      item_data = data["items"][str(id)]
      self.add_item(id, item_data, req_type)
      
  x=1
  
  def insert_world_data(self, world_id, world_name, data: dict, type: RequestType):
    key = "listings" if type == RequestType.CURRENT else "entries"
    for item in data[key]:
      item["worldID"] = world_id
      item["worldName"] = world_name
  
  def process_item_history(self, items: dict):    
    pass
  def process_item_current(self, data):
    pass

class ItemResult:
  def __init__(self, id: int, data: dict):
    self.item_id = id
    self.entries = data.pop("entries")
