from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from pathlib import Path
from json import load

class Dc:
  def __init__(cls, name, id, worlds):
    cls.name, cls.id = name, id
    cls.worlds = [World(*world, cls) for world in worlds.items()]

  def numWorlds(cls):
    return len(cls.worlds)
  
  def getWorld(cls, world_index):
    world = cls.worlds[world_index]
    return world
  
  def appendWorld(cls, world:'World'):
    cls.worlds.append(world)

class World:
  def __init__(cls, name, id, dc):
    cls.name, cls.id, cls.dc = name, id, dc


class DcModel(QAbstractTableModel):
  
  def __init__(cls):
    super().__init__()
    cls.dcs = []
    cls.load_data()
    cls.dc_index = 0
  
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
      if cls.dc_index != 0:
        count = cls.dcs[cls.dc_index].numWorlds()
      else:
        count = len(cls.dcs)
    else:
      if index.column() == 0:
        count = len(cls.dcs)
      else:
        count = cls.dcs[col-1].numWorlds()
    
    print(f"Row Count returned {count} for row {row}, column {col}")
    return count
    
  def columnCount(cls, index: QModelIndex = QModelIndex()):
    return len(cls.dcs)+1
    

  def data(cls, index, role):
    row, col = index.row(), index.column()
    cls.dc_index = col # CLUE: changing this from cls.dc_index = col -1 fixed everything
    item = index.internalPointer()
    
    match role:
      case Qt.ItemDataRole.DisplayRole:
        print(item.name)
        return item.name
      case Qt.ItemDataRole.UserRole:
        print(item.id)
        return item.id
      case _:
        return None