class Job:
  def __init__(cls, abbr, id):
    cls.abbr, cls.id = abbr, id
    cls.recipes = []
  
  def get_abbr(cls):
    return cls.abbr
  
  def get_id(cls):
    return cls.id
    
  def get_recipe(cls, row):
    return cls.recipes[row]

  def num_recipes(cls):
    return len(cls.recipes)
  
  def append_recipe(cls, recipe: 'Recipe'):
    cls.recipes.append(recipe)

class Recipe:
  def __init__(cls, name, lvl, id, job):
    cls.name, cls.lvl, cls.id, cls.job = name, lvl, id, job
  
  def get_name(cls):
    return cls.name
  
  def get_lvl(cls):
    return cls.lvl
  
  def get_id(cls):
    return cls.id
  
  def get_job(cls):
    return cls.job