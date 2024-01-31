from PyQt6.QtCore import QAbstractTableModel, Qt
from pathlib import Path 
from enum import IntEnum
from json import load

class JobModel(QAbstractTableModel):
  
  def __init__(cls):
    cls.job_min_lvl: [int] = [0] * 8
    cls.job_max_lvl: [int] = [90] * 8
    cls.job_select: [bool] = [False] * 8
    
  
  def rowCount(cls, index):
    match index.column():
      case 0 | 1:
        return 1
      case 2 | 3 | 4:
        return 8
  
  def columnCount(cls, index):
    return 5
  
  def data(cls, index):
    row, col = index.row(), index.column()
    match col:
      case 0:
        return cls.dc
      case 1:
        return cls.world
      case 2:
        if col >= 0 and col < 8:
          return cls.job_select[row]
      case 3:
        if col >= 0 and col < 8:
          return cls.job_min_lvl[row]
      case 4:
        if col >= 0 and col < 8:
          return cls.job_max_lvl[row]
  
  def setData(cls, index, value, role=None):
    row, col = index.row(), index.column()

    match col:
      case 0 | 1:
        if value is int and col == 0:
          cls.dc = value
        elif col == 1:
          cls.world = value
      case 2 | 3:
        if value is int and col == 2:
          cls.job_min_lvl[row] = value
        elif col == 3:
          cls.job_max_lvl[row] = value
      case 4:
        if value is bool:
          cls.job_select[row] = value

          