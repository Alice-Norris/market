from PySide6.QtWidgets import QButtonGroup, QCheckBox, QDialog, QGridLayout, QHBoxLayout, QPushButton, QVBoxLayout, QApplication
from PySide6.QtCore import Qt, QSettings, QEvent, Signal
from MarketGaze.ConfigHandler import ConfigHandler
from MarketGaze.MarketEvent import MarketEvent

class ConfigDialog(QDialog):
  config_changed = Signal(name="ConfigChanged")

  def __init__(self, parent):
    super().__init__(parent, objectName="ConfigDialog")
    #self.config_changed.connect(parent.send_cfg_event)
    self.setWindowTitle("Search Settings")
    self.setLayout(QGridLayout())
    self.cfg_setup()
    self.btn_setup()

  def cfg_setup(self):
    sel_grp = QButtonGroup(self, objectName="Config")
    sel_grp.setExclusive(False)

    sel_grp.addButton(QCheckBox("Search Datacenter Only", self, objectName="DcOnly"))
    sel_grp.addButton(QCheckBox("Consider Market History", self, objectName="ConsiderHistory"))
    sel_grp.addButton(QCheckBox("Enable Error Log", self, objectName="EnableLogging"))
    chk_layout = QVBoxLayout()
    cfg = self.get_cfg()

    for chk in sel_grp.buttons():
      chk_layout.addWidget(chk)
      chk.setChecked(cfg[chk.objectName()])

    self.layout().addLayout(chk_layout, 0, 0, Qt.AlignmentFlag.AlignLeft)
  
  def btn_setup(self):
    cancel_btn = QPushButton("Close", self)
    cancel_btn.clicked.connect(self.close)
    
    apply_btn = QPushButton("Apply", self)
    apply_btn.clicked.connect(self.apply)
    
    btn_layout = QHBoxLayout()
    btn_layout.addWidget(cancel_btn)
    btn_layout.addWidget(apply_btn)
    
    self.layout().addLayout(btn_layout, 1, 0, Qt.AlignmentFlag.AlignRight)

  def get_cfg(self) -> dict:
    cfg = QSettings()
    output = {}

    cfg.beginGroup("Config")

    for key in cfg.allKeys():
      output[key] = cfg.value(key, type=bool)
    
    cfg.endGroup()

    return output
    
  def apply(self):
    cfg = QSettings()
  
    cfg.beginGroup("Config")
    
    for chk in self.findChild(QButtonGroup, "Config").buttons():
      cfg.setValue(chk.objectName(), chk.isChecked())

    event_type = MarketEvent.Type.ConfigChanged
    QApplication.sendEvent(self.parent().centralWidget(), MarketEvent(event_type))

    self.hide()
