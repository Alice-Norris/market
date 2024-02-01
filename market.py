from app_window import AppWindow
from PyQt6.QtWidgets import QApplication, QComboBox, QComboBox, QLabel, QFrame
from job_select import JobSelect
from data_handler import DataHandler
from sys import exit

class MarketGaze(QApplication):
  def __init__(self):
    super().__init__([])
    self.handler = DataHandler()
    ui = AppWindow()
    ui.show()
    #self.start()
    exit(self.exec())
    #self.exit()

  # def start(self):
  #   self.ui.show_win()
  
  # def exit(self):
  #   exit(self.exec())
