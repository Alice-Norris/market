from PySide6.QtCore import QSize, QMargins, Signal, QSettings, Qt, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QSpinBox, QWidget, QVBoxLayout, QLabel
from json import load

class JobWidget(QWidget):
  val_changed = Signal(str, str, int)

  def __init__(self, parent, name: str, icon: QIcon, data: dict):
    super().__init__(parent, objectName=name)
    self.data = data
    self.setLayout(QVBoxLayout(self, spacing=0, contentsMargins=QMargins(0,0,0,0)))

    self.max_lvl = QSpinBox(self, minimum=1, maximum=90, wrapping=True, objectName="max")
    self.max_lvl.setValue(data["max"])
    self.layout().addWidget(self.max_lvl)

    self.layout().addWidget(self.max_lvl)
    btn = QPushButton(icon, "", self, checkable=True, iconSize=QSize(48, 48), objectName="select")
    btn.setChecked(data["select"])
    self.layout().addWidget(btn)

    self.min_lvl = QSpinBox(self, minimum=1, maximum=90, wrapping=True, objectName="min")
    self.min_lvl.setValue(data["min"])
    self.layout().addWidget(self.min_lvl)

    self.max_lvl.valueChanged.connect(self.max_val_changed)
    self.max_lvl.valueChanged.connect(lambda val: self.val_changed.emit(self.objectName(), self.max_lvl.objectName(), val))

    btn.toggled.connect(lambda checked: self.val_changed.emit(self.objectName(), btn.objectName(), int(checked)))

    self.min_lvl.valueChanged.connect(self.min_val_changed)
    self.min_lvl.valueChanged.connect(lambda val: self.val_changed.emit(self.objectName(), self.min_lvl.objectName(), val))

  @Slot(int, name="MinChanged")   
  def min_val_changed(self, val):
    self.max_lvl.setMinimum(val)
    if self.max_lvl.value() < val:
      self.max_lvl.setValue(val)
    
  @Slot(int, name="MaxChanaged")
  def max_val_changed(self, val):
    self.min_lvl.setMaximum(val)
    if self.min_lvl.value() > val:
      self.min_lvl.setValue(val)
    
class JobSelect(QWidget):
  sortUpdate = Signal(str, dict, name="sortUpdate")

  def __init__(self, parent):
    super().__init__(parent, objectName="JobSelect")
    self.data = {}
    self.setLayout(QHBoxLayout(self, spacing=0, contentsMargins=QMargins(0,0,0,0)))
    self.mk_lbls()
    self.mk_widgets()

  def mk_lbls(self):
    layout = QVBoxLayout(spacing=0, contentsMargins=QMargins(0,0,8,0))
    layout.addWidget(QLabel("Max Lvl:", alignment = Qt.AlignmentFlag.AlignCenter))
    layout.addWidget(QLabel("Job:", alignment = Qt.AlignmentFlag.AlignCenter))
    layout.addWidget(QLabel("Min Lvl:", alignment = Qt.AlignmentFlag.AlignCenter))
    self.layout().addLayout(layout)
  
  # creates a checkable button for each job.
  def mk_widgets(self):   
    cfg = QSettings()
    cfg.beginGroup("JobSelect")
    for job in cfg.allKeys():
      job_data = cfg.value(job)
      self.data[job] = job_data
      job_w = JobWidget(self, job, QIcon(f"data/icons/{job}.png"), job_data)
      job_w.val_changed.connect(self.change)
      self.layout().addWidget(job_w)
    cfg.endGroup()
  
  def change(self, job_name, attr_name, val):
    job_dict = self.data[job_name]
    job_dict[attr_name] = val
    cfg = QSettings()
    cfg.setValue(f"JobSelect/{job_name}", job_dict)
    self.sortUpdate.emit(job_name, job_dict)
