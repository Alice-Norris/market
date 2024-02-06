from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QRect, QSettings, QCoreApplication, QPoint, QSize, pyqtSignal
from cfg_dialog import ConfigDialog
from marketsearch import MarketSearch
from toolbar import Toolbar
from sys import exit

class AppWindow(QMainWindow):
  settings = None
  dc_only_mode = pyqtSignal(bool)
  consider_history = pyqtSignal(bool)

  def __init__(self):
    super().__init__()
    QCoreApplication.setApplicationName("MarketGaze")
    QCoreApplication.setOrganizationName("Aresu Nereru")
    self.settings = QSettings(self)
    self.cfg_dialog = ConfigDialog(self)
    self.addToolBar(Toolbar(self))
    self.setWindowTitle("MarketGaze")
    self.setCentralWidget(MarketSearch(self))
    self.read_settings()
  
  def calc_win_geometry(self):
    cent = self.screen().geometry().center()
    size = self.screen().availableSize()
    half_h = size.height() // 2
    half_w = size.width() // 2
    quart_x = cent.x() // 2
    quart_y = cent.y() // 2
    return (QPoint(quart_x, quart_y), QSize(half_h, half_w))

  def read_settings(cls):
    if cls.settings.contains("AppWindow"):
      cls.settings.beginGroup("AppWindow")
    
      position: QPoint = cls.settings.value("position")
      size: QSize = cls.settings.value("size")
    
      cls.settings.endGroup()

      cls.move(position)
      cls.resize(size)

    else:
      cls.write_settings  

  def write_settings(cls):
    pos, size = cls.calc_win_geometry()

    cls.settings.beginGroup("AppWindow")

    cls.settings.setValue("position", pos)
    cls.settings.setValue("size", size)

    cls.settings.endGroup()

  def cfg_update(cls, name, val):
    match name:
      case "dc_only":
        cls.dc_only_mode.emit(val)
      case "consider_history":
        cls.consider_history.emit(val)