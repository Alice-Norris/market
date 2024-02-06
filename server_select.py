from PyQt6.QtWidgets import QFrame, QComboBox, QLabel, QHBoxLayout, QVBoxLayout, QDataWidgetMapper, QWidget, QGridLayout
from PyQt6.QtCore import Qt, QModelIndex, pyqtSignal
from server_model import ServerModel
from PyQt6.QtGui import QStandardItemModel
from sys import exit

# selection for datacenter and server. 
# Once a selection is made, the server list populates,
# and the user can select the server.
class ServerSelect(QWidget):
  returnParams = pyqtSignal(int, int)
  update_world_list = pyqtSignal(int)

  def __init__(self, parent):
    super().__init__(parent, objectName="ServerSelect")
    self.dc_only = False
    self.model = ServerModel()

    layout = QHBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    self.setLayout(layout)
    
    self.mk_widgets()
    
  # creates widgets
  def mk_widgets(self):
    #datacenter selection
    self.dc_sel = DcSelect(self, self.model)
    self.layout().addWidget(self.dc_sel)

    # Setting up datacenter selection label
    dc_sel_lbl = QLabel(self, text='Datacenter:')
    dc_sel_lbl.setBuddy(self.dc_sel)
    self.layout().insertWidget(0, dc_sel_lbl)

    #make world selection
    self.world_sel = WorldSelect(self, self.model)
    self.layout().addWidget(self.world_sel)

    self.dc_sel.updateWorldColumn.connect(self.world_sel.update_worlds)
    # Make world selection label
    world_sel_lbl = QLabel(self, text='World: ', objectName="world_sel_lbl", enabled=False)
    world_sel_lbl.setBuddy(self.world_sel)
    self.layout().insertWidget(2, world_sel_lbl)
    
  def update_worlds(self, new_index):
    if not self.world_sel.isEnabled():
      self.world_sel.setModel(self.model)
      self.world_sel.setEnabled(True)
    self.world_sel.setModelColumn(new_index+1)

  def get_selected(self):
    dc_id = self.dc_sel.currentData(Qt.ItemDataRole.UserRole)
    world_id = self.world_sel.currentData(Qt.ItemDataRole.UserRole)
    self.returnParams.emit(dc_id, world_id)
  
  def dc_only_mode(self, val):
    if self.dc_only != val:
      self.dc_only = val
      self.world_sel.setEnabled(not val)
      self.world_sel.blockSignals(not val)

class DcSelect(QComboBox):
  updateWorldColumn = pyqtSignal(int)

  def __init__(self, parent, model):
    super().__init__(parent, objectName="dc_sel", placeholderText="--- Select ---")
    self.currentIndexChanged.connect(self.updateWorldColumn.emit)
    self.setModel(model)
    self.setModelColumn(0)

class WorldSelect(QComboBox):
  def __init__(self, parent, model):
    super().__init__(parent, objectName="world_sel", placeholderText="--- Select ---")
    self.setModel(model)
    self.setModelColumn(1)
  
  def update_worlds(self, col_num: int):
    self.setModelColumn(col_num)