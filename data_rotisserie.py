from collections import ChainMap
class DataRotisserie(ChainMap):

  def __init__(cls, **maps: dict[str, map]):
    cls.names = [*maps.keys()]
    super().__init__(*maps.values())
    x=1

  def __setitem__(cls, name, value):
    index = cls.names.index(name)
    cls.maps[index].__setitem__(name, value)

  def sel_map(cls, name: str):
    index = cls.names.index(name)
    cls.maps = cls.maps[index:] + cls.maps[0:index]
    cls.names = cls.names[index:] + cls.names[0:index]

  def insert(cls, name:str, key, val):
    index = cls.names.index(name)
    cls.maps[index][key] = val
  
  def get_map(cls, key:str):
    index = cls.names.index(key)
    return cls.maps[index]

  def add_map_front(cls, name: str, map: map):
    cls.names.insert(0, name)
    cls.maps.insert(0, name)

  def add_map_rear(cls, name: str, map: map):
    cls.names.append(name)
    cls.maps.append(name)

  def rotate_left(cls):
    (name_front, map_front) = cls.names.pop(0), cls.maps.pop(0)
    cls.names.append(name_front)
    cls.maps.append(map_front)
  
  def rotate_right(cls):
    name_rear, map_rear = cls.names.pop(), cls.maps.pop()
    cls.names.insert(0, name_rear)
    cls.maps.insert(0, map_rear)
  
  def get_names(cls):
    return cls.names