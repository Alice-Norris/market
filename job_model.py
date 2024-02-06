from PyQt6.QtCore import QAbstractTableModel, Qt
from pathlib import Path 
from enum import IntEnum
from json import load

class JobModel(QAbstractTableModel):
  
  def __init__(self):
    self.job_min_lvl: [int] = [0] * 8
    self.job_max_lvl: [int] = [90] * 8
    self.job_select: [bool] = [False] * 8
    
  def rowCount(self, index):
    return 3
  
  def columnCount(self, index):
    return 8
  
  def data(self, index):
    row, col = index.row(), index.column()
    match col:
      case 0:
        return self.dc
      case 1:
        return self.world
      case 2:
        if col >= 0 and col < 8:
          return self.job_select[row]
      case 3:
        if col >= 0 and col < 8:
          return self.job_min_lvl[row]
      case 4:
        if col >= 0 and col < 8:
          return self.job_max_lvl[row]
  
  def setData(self, index, value, role=None):
    row, col = index.row(), index.column()

    match col:
      case 0 | 1:
        if value is int and col == 0:
          self.dc = value
        elif col == 1:
          self.world = value
      case 2 | 3:
        if value is int and col == 2:
          self.job_min_lvl[row] = value
        elif col == 3:
          self.job_max_lvl[row] = value
      case 4:
        if value is bool:
          self.job_select[row] = value

          