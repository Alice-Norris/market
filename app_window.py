from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QMainWindow, QToolBar
from PyQt6.QtCore import QRect, Qt
from server_select import ServerSelect
from job_select import JobSelect
from recipe_list import RecipeList
from marketsearch import MarketSearch
from search import Search
from sys import exit

class AppWindow(QMainWindow):
  serv_sel = None
  job_btns = None

  def __init__(self):
    super().__init__()
    #toolbar = QToolBar(self, movable=False)
    #toolbar.insertWidget(None, ServerSelect(self))
    #toolbar.insertWidget(None, JobSelect(self))
    #self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)
    self.setCentralWidget(MarketSearch(self))
    #cls.serv_sel = ServerSelect(cls)
    #cls.job_btns = JobSelect(cls)
    #cls.recipe_list = RecipeList(cls)
    #cls.search = Search(cls)
    #cls.mk_layout()
    
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
