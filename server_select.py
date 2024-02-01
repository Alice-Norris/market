from PyQt6.QtWidgets import QFrame, QComboBox, QLabel, QHBoxLayout, QVBoxLayout, QDataWidgetMapper, QWidget, QGridLayout
from PyQt6.QtCore import Qt, QModelIndex
from world_dc_model import DcModel
from PyQt6.QtGui import QStandardItemModel
from sys import exit

# selection for datacenter and server. 
# Once a selection is made, the server list populates,
# and the user can select the server.
class ServerSelect(QWidget):
  def __init__(self, parent):
    super().__init__(parent)

    self.model = DcModel()

    layout = QHBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    self.setLayout(layout)
    
    self.mk_widgets()
    
  # creates a layout, placing all widgets in it.
  def mk_layout(cls, widgets):
    layout = QGridLayout(cls)
    layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    for widget in widgets:
      layout.addWidget(widget)
      widget.show()
    cls.show()

  # creates widgets
  def mk_widgets(self):
    #datacenter selection
    dc_sel = QComboBox(self, objectName="dc_sel", placeholderText="--- Select ---")
    dc_sel.setModel(self.model)
    dc_sel.setModelColumn(0)
    dc_sel.currentIndexChanged.connect(self.update_worlds)
    #self.layout().addWidget(dc_sel, 0, 1)
    self.layout().addWidget(dc_sel)

    # Setting up datacenter selection label
    dc_sel_lbl = QLabel(self, text='Datacenter:')
    dc_sel_lbl.setBuddy(dc_sel)
    #self.layout().addWidget(dc_sel_lbl, 0, 0)
    
    self.layout().insertWidget(0, dc_sel_lbl)

    #make world selection
    self.world_sel = QComboBox(self, objectName="world_sel", enabled=False, placeholderText="--- Select ---")
    self.layout().addWidget(self.world_sel)
    #self.layout().addWidget(self.world_sel, 1, 1)

    # Make world selection label
    world_sel_lbl = QLabel(self, text='World: ', objectName="world_sel_lbl", enabled=False)
    world_sel_lbl.setBuddy(self.world_sel)
    self.layout().insertWidget(2, world_sel_lbl)
    # self.layout().addWidget(world_sel_lbl, 1, 0)
    #cls.mk_layout([dc_sel_lbl, dc_sel, world_sel_lbl, cls.world_sel])

  def update_worlds(self, new_index):
    if not self.world_sel.isEnabled():
      self.world_sel.setModel(self.model)
      self.world_sel.setEnabled(True)
    self.world_sel.setModelColumn(new_index+1)
