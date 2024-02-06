from app_window import AppWindow
from PyQt6.QtWidgets import QApplication, QComboBox, QComboBox, QLabel, QFrame
from job_select import JobSelect
from data_handler import DataHandler
from sys import exit

class MarketGaze(QApplication):
  def __init__(self):
    super().__init__([])
    #self.handler = DataHandler()
    ui = AppWindow()
    ui.show()
    exit(self.exec())

