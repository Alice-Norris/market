from PySide6.QtWidgets import QFileSystemModel
from PySide6.QtCore import QDir, QJsonDocument, QObject, Slot

class MarketFileSystemModel(QFileSystemModel):
  def __init__(self, parent: QObject=None):
    sup = super()
    sup.__init__(parent)
    sup.setRootPath(QDir().currentPath())
  
  @Slot(QJsonDocument | None)
  def chk_file(self):
    pass