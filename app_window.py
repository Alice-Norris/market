from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QPoint, QSettings, Slot
from MarketGaze.Toolbar import Toolbar
from MarketGaze.MainWidget import MainWidget
from MarketGaze.ConfigDialog import ConfigDialog
from MarketGaze.ConfigHandler import ConfigHandler
from MarketGaze.DebugWindow import DebugWindow
from MarketGaze.Network import MarketNetworkManager

class AppWindow(QMainWindow):
  def __init__(self):
    super().__init__(objectName="MainWindow")
    self.handler = ConfigHandler(self)
    self.addToolBar(Toolbar(self))
    self.setCentralWidget(MainWidget(self))
    self.init_win()

  def init_win(self):
    settings = QSettings()
    self.move(settings.value("AppWindow/Position"))
    self.resize(settings.value("AppWindow/Size"))

  @Slot()
  def help_mode(self):
    pass
  
  @Slot()
  def show_cfg(self):
    ConfigDialog(self).show()

  @Slot()
  def show_dbg(self):
    DebugWindow(self).show()