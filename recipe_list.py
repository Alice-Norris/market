from PyQt6.QtWidgets import QFrame, QTreeView, QHeaderView, QVBoxLayout
from recipe_model import RecipeModel

#from PyQt6.QtGui import QList

class RecipeList(QFrame):
  def __init__(cls, parent):
    super().__init__(parent)
    cls.show()
    cls.layout = QVBoxLayout(cls)
    cls.model = RecipeModel()
    cls.mk_widgets()
    
    
  def mk_widgets(cls):
    cls.recipe_list = QTreeView(cls)
    cls.recipe_list.setModel(cls.model)
    cls.recipe_list.setObjectName("RecipeList")
    cls.recipe_list.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    cls.recipe_list.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    cls.layout.addWidget(cls.recipe_list)
    cls.recipe_list.show()    
