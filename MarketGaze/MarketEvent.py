from PySide6.QtCore import QEvent
from enum import IntEnum, Enum

class MarketEvent(QEvent):
  
  class Type(Enum):
    ConfigChanged = QEvent.Type(QEvent.Type.User + 1)
  
  def __init__(self, type):
    super().__init__(type.value)

  

