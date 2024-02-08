from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QActionEvent
from PySide6.QtCore import QPoint, QSettings, QSize, QEvent, Qt, Slot, Signal
from MarketGaze.Toolbar import Toolbar
from MarketGaze.MainWidget import MainWidget
from MarketGaze.ConfigDialog import ConfigDialog
from MarketGaze.ConfigHandler import ConfigHandler
from MarketGaze.MarketEvent import MarketEvent

class AppWindow(QMainWindow):
  dc_only_mode = Signal(bool, name="DcOnlyMode")
  consider_history = Signal(bool, name="ConsiderHistory")

  def __init__(self):
    super().__init__(objectName="MainWindow")
    self.handler = ConfigHandler(self)
    toolbar = Toolbar(self)
    widget = MainWidget(self)
    self.addToolBar(toolbar)
    self.setCentralWidget(widget)
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
  
  def event(self, event):
    if event.type() == MarketEvent.Type.ConfigChanged.value:
      return True
    return super().event(event)