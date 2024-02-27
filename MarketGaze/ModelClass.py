from PySide6.QtCore import Qt

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

class Job:
  def __init__(self, abbr, id):
    self.abbr, self.id = abbr, id
    self.recipes = []
    self.checked = Qt.CheckState.Unchecked
  def get_recipe(self, row):
    return self.recipes[row]

  def num_recipes(self):
    return len(self.recipes)
  
  def append_recipe(self, recipe: 'Recipe'):
    self.recipes.append(recipe)
  
  def data(self, role: Qt.ItemDataRole):
    match role:
      case Qt.ItemDataRole.DisplayRole:
        return self.abbr
      case Qt.ItemDataRole.UserRole:
        return self.id
      # case Qt.ItemDataRole.CheckStateRole:
      #   return self.checked
      case _:
        return None
  
  # def setData(self, val, role: Qt.ItemDataRole):
  #   if role == Qt.ItemDataRole.CheckStateRole:
  #     self.checked = val
  
class Recipe:
  def __init__(self, name, lvl, id, job):
    self.name, self.lvl, self.id, self.job = name, lvl, id, job
    self.checked = Qt.CheckState.Unchecked

  def get_job(self):
    return self.job
  
  def data(self, column: int, role: Qt.ItemDataRole):
    match role:
      case Qt.ItemDataRole.DisplayRole:
        match column:
          case 1:
            return self.name
          case 2:
            return self.lvl
          case _:
            return None
      case Qt.ItemDataRole.UserRole:
        return self.id
      # case Qt.ItemDataRole.CheckStateRole:
      #   match column:
      #     case 1:
      #       return self.checked

  # def setData(self, val, role: Qt.ItemDataRole):
  #   if role == Qt.ItemDataRole.CheckStateRole:
  #     self.checked = val