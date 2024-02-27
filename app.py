from PySide6.QtCore import Signal, QDir, QEvent, QFile, QByteArray, QSaveFile, QIODevice, QDataStream
from PySide6.QtWidgets import QApplication, QFileSystemModel
from app_window import AppWindow
from MarketGaze.MarketEvent import MarketEvent
from MarketGaze.Constants import App_Data, FFData
from MarketGaze.Network import MarketNetworkManager


class MarketGaze(QApplication):
  fetch_data = Signal(FFData, name="FetchData")

  def __init__(self):
    super().__init__([])
    net_mgr: MarketNetworkManager = MarketNetworkManager(self)
    # self.file_model = QFileSystemModel()
    # self.file_model.setRootPath(QDir.currentPath())
    # self.fetch_data.connect(net_mgr.fetch_data)
    self.fetch_data.connect(net_mgr.fetch_data)
    net_mgr.data_send.connect(self.write_data)

    self.register_events()
    self.chk_dir()
    self.chk_data()
    self.setApplicationName(App_Data.NAME)
    self.setOrganizationName(App_Data.ORG)

    ui = AppWindow()
    ui.show()

    exit(self.exec())

  def register_events(self):
    for event_code in MarketEvent.Type:
      QEvent.registerEventType(event_code.value)

  # TODO: Add check for empty files
  def chk_data(self):
    # for entry in FFData:
    #   file = QFile(entry.value["dir"] + entry.value["filename"])
    #   if not file.exists():
    #     self.fetch_data.emit(entry)
    self.fetch_data.emit(FFData.RECIPES)
    
  def chk_dir(self):
    dirs = ["data", "data/json", "data/icon"]
    for dir in [QDir(dir) for dir in dirs]:
      if not dir.exists():
        dir.mkpath(".")    

  def write_data(self, data: QByteArray, info: FFData):
    dir = info.value["dir"] 
    filename = info.value["filename"]
    file = QSaveFile(dir + filename)
    file.open(QIODevice.OpenModeFlag.WriteOnly)
    print(data)
    file.write(data)

if __name__ == "__main__":
  MarketGaze().start()
  #mg.start()


