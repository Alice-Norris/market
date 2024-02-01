from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QSpinBox, QGridLayout, QLabel
from PyQt6.QtGui import QIcon
from job_model import JobModel
from PyQt6.QtCore import QSize, Qt, QMargins
from pathlib import Path
from json import load

class JobSelect(QFrame):
  job_sel = {}

  def __init__(cls, parent):
    super().__init__(parent)
    cls.setObjectName("JobSelect")
    cls.setLayout(QHBoxLayout(cls))
    cls.layout().setSpacing(0)
    cls.setFrameShape(cls.Shape.NoFrame)
    cls.setLineWidth(0)
    cls.model = JobModel()
    cls.mk_widgets()
    cls.show()


  def get_jobs(cls):
    with open("./data/json/class_job.json") as file:
      return load(file)
    
  # creates a checkable button for each job.
  def mk_widgets(cls):
    jobs = cls.get_jobs()
    for index, item in enumerate(jobs.items()):
        icon = QIcon("data/icons/" + item[0] + ".png")
        job_w = JobWidget(cls, icon)
        cls.layout().addWidget(job_w)
    
  # Updates the job selection when a job button's state changes
  def update_job_sel(cls, toggled):
    job_name = cls.sender().objectName()
    cls.job_sel[job_name] = True

class JobWidget(QFrame):
  def __init__(cls, parent, icon: QIcon):
    super().__init__(parent)
    btn = QPushButton(icon, "", cls, checkable=True, iconSize=QSize(48, 48))
    cls.min_lvl = QSpinBox(cls, minimum=1, maximum=90, wrapping=True)
    cls.max_lvl = QSpinBox(cls, minimum=1, maximum=90, wrapping=True)
    cls.setLayout(QGridLayout(cls, spacing=0, contentsMargins=QMargins(0,0,0,0)))
    cls.layout().addWidget(cls.min_lvl, 0, 0)
    cls.layout().addWidget(btn, 1, 0)
    cls.layout().addWidget(cls.max_lvl, 2, 0)

    cls.min_lvl.valueChanged.connect(cls.set_max_min)
    cls.max_lvl.valueChanged.connect(cls.set_min_max)

  def set_max_min(cls, val):
    if cls.max_lvl.value() < val:
      cls.max_lvl.setValue(val)
  
  def set_min_max(cls, val):
    if cls.min_lvl.value() > val:
      cls.min_lvl.setValue(val)
    