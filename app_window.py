from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import QRect, Qt
from server_select import ServerSelect
from job_select import JobSelect
from recipe_list import RecipeList
from search import Search
from sys import exit

class AppWindow(QWidget):
  serv_sel = None
  job_btns = None

  def __init__(cls):
    super().__init__()
    cls.serv_sel = ServerSelect(cls)
    cls.job_btns = JobSelect(cls)
    cls.recipe_list = RecipeList(cls)
    cls.search = Search(cls)
    cls.mk_layout()
    
  def show_win(cls):
    win_rect = QRect(*cls.calc_win_geometry())
    cls.setGeometry(win_rect)
    cls.setWindowTitle("MarketGaze")
    cls.show()
  
  def calc_win_geometry(cls):
    cent = cls.screen().geometry().center()
    size = cls.screen().availableSize()
    half_h = size.height() // 2
    half_w = size.width() // 2
    return (cent.x() // 2, cent.y() // 2, half_h, half_w)
  
  def mk_layout(cls):
    layout = QVBoxLayout(cls)
    layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    layout.addWidget(cls.serv_sel)
    layout.addWidget(cls.job_btns)
    layout.addWidget(cls.recipe_list)
    layout.addWidget(cls.search)
  
