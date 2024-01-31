from app_window import AppWindow
from PyQt6.QtWidgets import QApplication, QComboBox, QComboBox, QLabel, QFrame
from job_select import JobSelect
from data_handler import DataHandler
from sys import exit

#TODO: Subclass this from QApplication
class MarketGaze(QApplication):
  
  def __init__(cls):
    super().__init__([])
    cls.handler = DataHandler()
    cls.ui = AppWindow()
    cls.start()
    cls.exit()

  def connect_widgets(cls):
    dc_sel = cls.ui.findChild(QComboBox, "dc_sel")
    dc_sel.currentTextChanged.connect(cls.dc_sel_chg)
    job_sel_frame:JobSelect = cls.ui.findChild(QFrame, "JobSelect")
    job_sel_frame.showEvent.connect(cls.set_dc_data)

  def start(cls):
    cls.ui.show_win()
  
  def exit(cls):
    exit(cls.exec())

  def dc_sel_chg(cls, text):
    world_sel = cls.ui.findChild(QComboBox, "world_sel")
    world_sel_lbl = cls.ui.findChild(QLabel, "world_sel_lbl")
    dc_sel = cls.ui.findChild(QComboBox, "dc_sel")
    
    if not world_sel.isEnabled():
      world_sel_lbl.setEnabled(True)
      world_sel.setEnabled(True)
    
    world_sel.clear()
    for world in cls.handler.get_worlds(dc_sel.currentText()):
      world_sel.addItem(world["Name"], world["ID"])

  def set_dc_data(cls):
    dc_data = cls.handler.get_dcs()
    dc_sel: QComboBox = cls.ui.find_child(QComboBox, "dc_sel")
    dc_sel.addItems(dc_data)

  def get_world_dc(cls):
    print("World Data Signal Received")
