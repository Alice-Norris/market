from PyQt6.QtCore import Qt

class Job:
  def __init__(cls, abbr, id):
    cls.abbr, cls.id = abbr, id
    cls.recipes = []

  def get_recipe(cls, row):
    return cls.recipes[row]

  def num_recipes(cls):
    return len(cls.recipes)
  
  def append_recipe(cls, recipe: 'Recipe'):
    cls.recipes.append(recipe)
  
  def data(cls, role: Qt.ItemDataRole):
    match role:
      case Qt.ItemDataRole.DisplayRole:
        return cls.abbr
      case Qt.ItemDataRole.UserRole:
        return cls.id
      case _:
        return None


class Recipe:
  def __init__(cls, name, lvl, id, job):
    cls.name, cls.lvl, cls.id, cls.job = name, lvl, id, job

  def get_job(self):
    return self.job
  
  def data(cls, column: int, role: Qt.ItemDataRole):
    match role:
      case Qt.ItemDataRole.DisplayRole:
        match column:
          case 1:
            return cls.name
          case 2:
            return cls.lvl
          case _:
            return None
      case Qt.ItemDataRole.UserRole:
        return cls.id
