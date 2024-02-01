from PyQt6.QtWidgets import QFrame, QComboBox, QLabel, QHBoxLayout, QDataWidgetMapper
from PyQt6.QtCore import Qt, QModelIndex
from world_dc_model import DcModel
from PyQt6.QtGui import QStandardItemModel
from sys import exit

# selection for datacenter and server. 
# Once a selection is made, the server list populates,
# and the user can select the server.
class ServerSelect(QFrame):
  def __init__(cls, parent):
    super().__init__(parent)
    cls.model = DcModel()
    cls.mk_widgets()
    
  # creates a layout, placing all widgets in it.
  def mk_layout(cls, widgets):
    layout = QHBoxLayout(cls)
    layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    for widget in widgets:
      layout.addWidget(widget)
      widget.show()
    cls.show()

  # creates widgets
    
  def mk_widgets(cls):
    #datacenter selection
    dc_sel_lbl = QLabel(cls, text='Datacenter:')
    
    cls.dc_sel = QComboBox(cls, objectName="dc_sel", placeholderText="--- Select ---")
    dc_sel_lbl.setBuddy(cls.dc_sel)
    cls.dc_sel.setModel(cls.model)
    cls.dc_sel.setModelColumn(0)
    cls.dc_sel.currentIndexChanged.connect(cls.update_worlds)
    #make world selection
    world_sel_lbl = QLabel(cls, text='World: ', objectName="world_sel_lbl", enabled=False)
    cls.world_sel = QComboBox(cls, objectName="world_sel", enabled=False, placeholderText="--- Select ---")
    world_sel_lbl.setBuddy(cls.world_sel)
    cls.mk_layout([dc_sel_lbl, cls.dc_sel, world_sel_lbl, cls.world_sel])

  def update_worlds(cls, new_index):
    if not cls.world_sel.isEnabled():
      cls.world_sel.setModel(cls.model)
      cls.world_sel.setEnabled(True)
    cls.world_sel.setModelColumn(new_index+1)
