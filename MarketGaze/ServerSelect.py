from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import QAbstractTableModel, QSettings, Qt, Signal, QEvent, Slot
from MarketGaze.ServerSelectModel import ServerModel
from MarketGaze.MarketEvent import MarketEvent

class ServerSelect(QWidget):
  dc_id_changed = Signal(int, name="dcIdChanged")
  world_id_changed = Signal(int, name="worldIdChanged")
  
  def __init__(self, parent):
    super().__init__(parent, objectName="ServerSelect")
    model = ServerModel()
    
    self.dc_mode = QSettings().value("Config/DcOnly")
    self.setLayout(QHBoxLayout(Alignment=Qt.AlignmentFlag.AlignHCenter))
    self.mk_widgets(model)
    cfg = QSettings()
    cfg.beginGroup("Search")
  
  # creates widgets
  def mk_widgets(self, model):
    # #datacenter selection
    dc_sel = DcSelect(self, model)
    self.layout().addWidget(dc_sel)

    # Setting up datacenter selection label
    dc_sel_lbl = QLabel(self, text='Datacenter:')
    dc_sel_lbl.setBuddy(dc_sel)
    self.layout().insertWidget(0, dc_sel_lbl)
    
    #make world selection
    world_sel = WorldSelect(self, model)
    self.parent().ui_update.connect(world_sel.toggle_dc_mode)
    self.layout().addWidget(world_sel)

    dc_sel.currentIndexChanged.connect(world_sel.update_worlds)

    # Make world selection label
    world_sel_lbl = QLabel(self, text='World: ', objectName="world_sel_lbl", enabled=False)
    world_sel_lbl.setBuddy(world_sel)
    self.layout().insertWidget(2, world_sel_lbl)

  # @Slot(name="SendIds")
  # def send_search_info(self):
  #   self.send_server_ids.emit(self.dc_id, self.world_id)

# Combobox to select the data center to search. It also uses its 
# currentIndexChanged signals to the World selection box which column
# of its model to use.
    
class DcSelect(QComboBox):
  id_changed = Signal(int, name="DcIdChanged")
  
  def __init__(self, parent: QWidget, model: QAbstractTableModel):
    super().__init__(parent, objectName="dc_sel", placeholderText="--- Select ---")
    self.setModel(model)
    self.currentIndexChanged.connect(self.update_index)
    index = QSettings().value("ServerSelect/DcIndex", type=int)
    self.setCurrentIndex(index)

  def update_index(self, index):
    QSettings().setValue("ServerSelect/DcIndex", index)
    QSettings().setValue("Search/DcId", self.currentData(Qt.ItemDataRole.UserRole))
    new_id = self.currentData(Qt.ItemDataRole.UserRole)
    self.parent().dc_id_changed.emit(new_id)
    #self.id_changed.emit(new_id)

# Selects the specific world to search
class WorldSelect(QComboBox):
  id_changed = Signal(int, name="DcIdChanged")
  dc_index = 1
  last_world_index = 0

  def __init__(self, parent, model: QAbstractTableModel):
    super().__init__(parent, objectName="world_sel", placeholderText="--- Select ---")
    self.dc_only_mode = QSettings().value("Config/DcOnly", type=bool)
    self.setEnabled(not self.dc_only_mode)
    self.setModel(model)
    self.setModelColumn(QSettings().value("ServerSelect/WorldColumn", type=int))
    self.currentIndexChanged.connect(self.update_index)
    self.setCurrentIndex(QSettings().value("ServerSelect/WorldIndex", type=int))
    
  def update_index(self, index):
    QSettings().setValue("ServerSelect/WorldIndex", index)
    QSettings().setValue("ServerSelect/WorldColumn", self.modelColumn())
    new_id = self.currentData(Qt.ItemDataRole.UserRole)
    QSettings().setValue("Search/WorldId", new_id)
    self.parent().world_id_changed.emit(new_id)
    #self.id_changed.emit(self.currentData(Qt.ItemDataRole.UserRole))

  @Slot(int, name="UpdateWorlds", result=None)
  def update_worlds(self, new_index: int):
    self.last_world_index = 0
    self.dc_index = new_index + 1

    if not self.dc_only_mode:
      if not self.isEnabled():
        self.setEnabled(True)
      self.setModelColumn(self.dc_index)
      
    QSettings().setValue("ServerSelect/WorldIndex", self.currentIndex())
    QSettings().setValue("ServerSelect/WorldColumn", self.modelColumn())

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