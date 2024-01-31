from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QSpinBox, QGridLayout, QLabel
from PyQt6.QtGui import QIcon
from job_model import JobModel
from PyQt6.QtCore import QSize, Qt
from pathlib import Path
from json import load

class JobSelect(QFrame):
  job_sel = {}

  def __init__(cls, parent):
    super().__init__(parent)
    cls.setObjectName("JobSelect")
    cls.job_sel_layout = QGridLayout(cls)
    cls.model = JobModel()
    cls.show()
    cls.mk_widgets()
    job_sel = {}

  def get_jobs(cls):
    with open("./data/json/class_job.json") as file:
      return load(file)
    
  # creates a checkable button for each job.
  def mk_widgets(cls):
    cls.job_sel_layout.addWidget(QLabel(text="Job:"), 0, 0, Qt.AlignmentFlag.AlignRight)
    cls.job_sel_layout.addWidget(QLabel(text ="Level:"), 1, 0, Qt.AlignmentFlag.AlignRight)
    jobs = cls.get_jobs()
    for index, item in enumerate(jobs.items()):
        lvl_spin = QSpinBox(cls)
        lvl_spin.setMaximum(90)
        lvl_spin.setMinimum(1)
        lvl_spin.setWrapping(True)
        icon = QIcon("data/icons/" + item[0] + ".png")
        btn = QPushButton(icon, "", cls, checkable=True, objectName=item[0], iconSize=QSize(56, 56))
        btn.toggled.connect(cls.update_job_sel)
        #cls.job_sel[icon_file.stem] = False
        # btn.show()
        # lvl_spin.show()
        cls.job_sel_layout.addWidget(btn, 0, index+1)
        cls.job_sel_layout.addWidget(lvl_spin, 1, index+1)
        #cls.job_sel_layout.addLayout(btn_layout)
    
  # Updates the job selection when a job button's state changes
  def update_job_sel(cls, toggled):
    job_name = cls.sender().objectName()
    cls.job_sel[job_name] = True