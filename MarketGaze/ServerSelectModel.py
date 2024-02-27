from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from pathlib import Path
from json import load
from MarketGaze.ModelClass import Dc

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
    
    #print(f"Row Count returned {count} for row {row}, column {col}")
    return count
    
  def columnCount(cls, index: QModelIndex = QModelIndex()):
    return len(cls.dcs)+1
    
  def data(cls, index, role):
    col = index.column()

    if col > 0:
      cls.dc_index = col  

    item = index.internalPointer()
    
    match role:
      case Qt.ItemDataRole.DisplayRole:
        return item.name
      case Qt.ItemDataRole.UserRole:
        return item.id
      case _:
        return None
