from PyQt6.QtWidgets import QWidget, QGridLayout
from recipe_list import RecipeList
from server_select import ServerSelect
from job_select import JobSelect
class MarketSearch(QWidget):

  def __init__(self, parent):
    super().__init__(parent)
    self.setupLayout()
    self.layout().addWidget(ServerSelect(self), 0, 0)
    self.layout().addWidget(JobSelect(self), 1, 0)
    self.layout().addWidget(RecipeList(self), 2, 0)

  def setupLayout(self):
    layout = QGridLayout(self)
    self.setLayout(layout)
  
