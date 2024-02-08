from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import QAbstractTableModel, QSettings, Qt, Signal, QEvent, Slot
from MarketGaze.Model import ServerModel
from MarketGaze.MarketEvent import MarketEvent

class ServerSelect(QWidget):
  returnParams = Signal(int, int)
  update_world_list = Signal(int)
  dc_mode = False

  def __init__(self, parent):
    super().__init__(parent, objectName="ServerSelect")
    self.model = ServerModel()

    layout = QHBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    self.setLayout(layout)
    
    self.mk_widgets()
  
  # creates widgets
  def mk_widgets(self):
    # #datacenter selection
    self.dc_sel = DcSelect(self, self.model)
    self.layout().addWidget(self.dc_sel)

    # Setting up datacenter selection label
    dc_sel_lbl = QLabel(self, text='Datacenter:')
    dc_sel_lbl.setBuddy(self.dc_sel)
    self.layout().insertWidget(0, dc_sel_lbl)

    #make world selection
    self.world_sel = WorldSelect(self, self.model)
    self.parent().ui_update.connect(self.world_sel.toggle_dc_mode)
    self.layout().addWidget(self.world_sel)

    self.dc_sel.currentIndexChanged.connect(self.world_sel.update_worlds)

    # Make world selection label
    world_sel_lbl = QLabel(self, text='World: ', objectName="world_sel_lbl", enabled=False)
    world_sel_lbl.setBuddy(self.world_sel)
    self.layout().insertWidget(2, world_sel_lbl)
  
  # def get_selected(self):
  #   dc_id = self.dc_sel.currentData(Qt.ItemDataRole.UserRole)
  #   world_id = self.world_sel.currentData(Qt.ItemDataRole.UserRole)
  #   self.returnParams.emit(dc_id, world_id)

# Combobox to select the data center to search. It also uses its 
# currentIndexChanged signals to the World selection box which column
# of its model to use.
class DcSelect(QComboBox):
  def __init__(self, parent: QWidget, model: QAbstractTableModel):
    super().__init__(parent, objectName="dc_sel", placeholderText="--- Select ---")
    self.setModel(model)

# Selects the specific world to search
class WorldSelect(QComboBox):
  def __init__(self, parent, model: QAbstractTableModel):
    self.dc_only_mode = QSettings().value("Config/DcOnly", type=bool)
    self.dc_index = 1
    self.last_world_index = 0
    super().__init__(parent, objectName="world_sel", placeholderText="--- Select ---")
    self.setEnabled(False)
    self.model = model
  
  @Slot(int, name="UpdateWorlds", result=None)
  def update_worlds(self, new_index: int):
    self.last_world_index = 0
    self.dc_index = new_index + 1

    if not self.dc_only_mode:
      if not self.isEnabled():
        self.setEnabled(True)
        self.setModel(self.model)
      self.setModelColumn(self.dc_index)
  
  @Slot(name="ToggleDcMode")
  def toggle_dc_mode(self):
    self.dc_only_mode = QSettings().value("Config/DcOnly", type=bool)

    # disable and block signals so it can't be put in an undefined state.
    self.setEnabled(not self.dc_only_mode)
    # self.blockSignals(self.dc_only_mode)

    # If DcOnly mode is on, make sure we change to a valid index and model 
    # column, or else the invalid index / weird model column will cause problems.
    # Setting current index to -1 so placeholder text will show again.
    # Otherwise, make sure we save the world index and set the new model column.
    if self.dc_only_mode:
      self.last_world_index = self.currentIndex()
      self.setCurrentIndex(-1)  
    else:
      self.setCurrentIndex(self.last_world_index)
      self.setModelColumn(self.dc_index)