from PySide6.QtCore import QSize, QMargins, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QPushButton, QSpinBox, QWidget
from json import load
from MarketGaze.Model import JobModel

class JobWidget(QWidget):
  update = Signal(str, dict, name="update")

  def __init__(self, parent, name: str, icon: QIcon):
    self.data={"select": False, "min": 1, "max": 1}
    super().__init__(parent, objectName=name)
    btn = QPushButton(icon, "", self, checkable=True, iconSize=QSize(48, 48))
    btn.toggled.connect(self.job_toggled)
    
    self.min_lvl = QSpinBox(self, minimum=1, maximum=90, wrapping=True)
    self.min_lvl.valueChanged.connect(self.min_val_changed)

    self.max_lvl = QSpinBox(self, minimum=1, maximum=90, wrapping=True)
    self.max_lvl.valueChanged.connect(self.max_val_changed)
    
    self.setLayout(QGridLayout(self, spacing=0, contentsMargins=QMargins(0,0,0,0)))

    self.layout().addWidget(self.min_lvl, 0, 0)
    self.layout().addWidget(btn, 1, 0)
    self.layout().addWidget(self.max_lvl, 2, 0)

  def min_val_changed(self, val):
    if self.max_lvl.value() < val:
      self.max_lvl.setValue(val)
    self.data["min"] = val
    self.update.emit(self.objectName(), self.data)
  
  def max_val_changed(self, val):
    if self.min_lvl.value() > val:
      self.min_lvl.setValue(val)
    self.data["max"] = val
    self.update.emit(self.objectName(), self.data)
  
  def job_toggled(self, checked: bool):
    self.data["select"] = not self.data["select"]
    self.update.emit(self.objectName(), self.data)


class JobSelect(QWidget):
  sortUpdate = Signal(str, dict, name="sortUpdate")

  def __init__(self, parent):
    super().__init__(parent)
    self.setObjectName("JobSelect")
    self.setLayout(QHBoxLayout(self, spacing=0, contentsMargins=QMargins(0,0,0,0)))
    self.mk_widgets()

  # creates a checkable button for each job.
  def mk_widgets(self):
    jobs = load(open("./data/json/class_job.json"))
    for item in jobs.items():
        icon = QIcon("data/icons/" + item[0] + ".png")
        job_w = JobWidget(self, item[0], icon)
        job_w.update.connect(self.update_job_sel)
        self.layout().addWidget(job_w)
    
  # Updates the job selection when a job button's state changes
  def update_job_sel(cls, job_name, sort_data):
    cls.sortUpdate.emit(job_name, sort_data)



