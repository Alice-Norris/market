from PySide6.QtCore import QSize, QMargins, Signal, QEvent, QSettings
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QPushButton, QSpinBox, QWidget
from json import load
from MarketGaze.Model import JobModel

class JobWidget(QWidget):
  update = Signal(str, dict, name="Update")

  def __init__(self, parent, name: str, icon: QIcon, select=False, min=1, max=1):
    super().__init__(parent, objectName=name)
    self.setLayout(QGridLayout(self, spacing=0, contentsMargins=QMargins(0,0,0,0)))
    self.data = {"min": min, "max": max, "select": select}

    btn = QPushButton(icon, "", self, checkable=True, iconSize=QSize(48, 48))
    btn.toggled.connect(lambda checked: self.send_update(checked, "select"))
    btn.setChecked(select)
    self.layout().addWidget(btn, 1, 0)    

    self.min_lvl = QSpinBox(self, minimum=1, maximum=90, wrapping=True)
    self.min_lvl.valueChanged.connect(lambda val: self.send_update(val, "min"))
    self.min_lvl.setValue(min)
    self.layout().addWidget(self.min_lvl, 0, 0)

    self.max_lvl = QSpinBox(self, minimum=1, maximum=90, wrapping=True)
    self.max_lvl.valueChanged.connect(lambda val: self.send_update(val, "max"))
    self.max_lvl.setValue(max)
    self.layout().addWidget(self.max_lvl, 2, 0)

  def min_val_changed(self, val):
    if self.max_lvl.value() < val:
      self.max_lvl.setValue(val)
  
  def max_val_changed(self, val):
    if self.min_lvl.value() > val:
      self.min_lvl.setValue(val)
  
  def job_toggled(self, checked: bool):
    self.data["select"] = not self.data["select"]

  def send_update(self, val, name):
    self.data[name] = val
    
    if name == "min":
      self.min_val_changed(val)
    elif name == "max":
      self.max_val_changed(val)

    self.update.emit(self.objectName(), self.data)

class JobSelect(QWidget):
  sortUpdate = Signal(str, dict, name="sortUpdate")

  def __init__(self, parent):
    super().__init__(parent, objectName="JobSelect")
    self.setLayout(QHBoxLayout(self, spacing=0, contentsMargins=QMargins(0,0,0,0)))
    self.mk_widgets()

  # creates a checkable button for each job.
  def mk_widgets(self):
    
    cfg = QSettings()
    cfg.beginGroup("JobSelect")
    for job in cfg.allKeys():
      job_w = JobWidget(self, job, QIcon(f"data/icons/{job}.png"), **cfg.value(job))
      job_w.update.connect(self.update_job_sel)
      self.layout().addWidget(job_w)
    cfg.endGroup()
        
  # Updates the job selection when a job widget's state changes
  def update_job_sel(cls, job_name, sort_data):
    cfg = QSettings()

    cfg.beginGroup("JobSelect")    
    cfg.setValue(job_name, sort_data)
    cfg.endGroup()

    cls.sortUpdate.emit(job_name, sort_data)
