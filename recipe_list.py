from PyQt6.QtWidgets import QFrame, QTreeView, QHeaderView, QVBoxLayout
from PyQt6.QtCore import QItemSelectionModel, QSortFilterProxyModel
from recipe_filter_model import RecipeFilterModel
from recipe_model import RecipeModel

#from PyQt6.QtGui import QList

class RecipeList(QFrame):
  def __init__(cls, parent):
    super().__init__(parent)
    cls.show()
    cls.layout = QVBoxLayout(cls)
    cls.model = RecipeModel(cls)
    cls.filter_model = RecipeFilterModel(cls, cls.model)
    #cls.filter_model.setSourceModel(cls.model)
    cls.mk_widgets()
    
    
  def mk_widgets(cls):
    cls.recipe_list = QTreeView(cls)
    cls.recipe_list.setModel(cls.filter_model)
    cls.recipe_list.setObjectName("RecipeList")
    cls.recipe_list.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    cls.recipe_list.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    cls.recipe_list.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    cls.recipe_list.header().setStretchLastSection(False)
    cls.recipe_list.setSelectionMode(QTreeView.SelectionMode.MultiSelection)
    #cls.recipe_list.mouseReleaseEvent()
    cls.layout.addWidget(cls.recipe_list)
    cls.recipe_list.show()    
