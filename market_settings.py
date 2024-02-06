from PyQt6.QtCore import QSettings

class MarketSettings(QSettings):

  def __init__(self, parent=None):
    super().__init__(parent=parent)
