from PyQt6.QtCore import QSettings, QCoreApplication, Qt, QSettings, pyqtSignal
from PyQt6.QtWidgets import QDialog, QCheckBox, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup
from constants import APPLICATION_DATA

class ConfigDialog(QDialog):
  update = pyqtSignal(str, bool)

  def __init__(self, parent=None):
    super().__init__(parent)
    self.setLayout(QGridLayout())
    self.setWindowTitle("Search Settings")
    self.add_buttons()
    self.add_checks()
    self.update.connect(parent.cfg_update)
  
  def add_checks(self):
    sel_grp_layout = QVBoxLayout()
    self.sel_grp = QButtonGroup(self)
    self.sel_grp.setExclusive(False)
    
    self.sel_grp.addButton(QCheckBox("Search Datacenter Only", self, objectName="dc_only"))
    self.sel_grp.addButton(QCheckBox("Consider Market History", self, objectName="consider_history"))
    
    for button in self.sel_grp.buttons():
      sel_grp_layout.addWidget(button)
    
    self.layout().addLayout(sel_grp_layout, 0, 0, Qt.AlignmentFlag.AlignLeft)

  def add_buttons(self):
    btn_layout = QHBoxLayout()

    cancel = QPushButton("Cancel", self)
    cancel.clicked.connect(self.close)
    btn_layout.addWidget(cancel)

    apply = QPushButton("Apply", self)
    apply.clicked.connect(self.save)
    btn_layout.addWidget(apply)

    row = self.layout().rowCount() + 1
    col_span = self.layout().columnCount()

    self.layout().addLayout(btn_layout, row, 0, row, col_span)

  def save(self):
    update = {}
    settings = QSettings()
    setting_update = [(btn.objectName(), btn.isChecked()) for btn in self.sel_grp.buttons()]

    settings.beginGroup("search")

    for key, val in setting_update:
      if settings.value(key) != val:
        settings.setValue(key, val)
        self.update.emit(key, val)

    settings.endGroup()

  def close(self):
    self.reject()