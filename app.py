from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import QEvent, QSettings, Slot
from app_window import AppWindow
from MarketGaze.Toolbar import Toolbar
from MarketGaze.MainWidget import MainWidget
from MarketGaze.MarketEvent import MarketEvent

class MarketGaze(QApplication):  
  def __init__(self):
    super().__init__([])
    self.register_events()
    self.setApplicationName("MarketGaze")
    self.setOrganizationName("Aresu Nereru")
    ui = AppWindow()
    ui.show()

    exit(self.exec())

  def register_events(self):
    for event_code in MarketEvent.Type:
      QEvent.registerEventType(event_code.value)

  @Slot()
  def config_update(cls):
    cls.sendEvent(QEvent(QEvent.Type.User+1))

  @Slot()
  def open_cfg(self):
    self.findChild(QDialog, "ConfigDialog")
      
if __name__ == "__main__":
  MarketGaze().start()
  #mg.start()

