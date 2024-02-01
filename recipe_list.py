from PyQt6.QtWidgets import QTreeView, QHeaderView
from recipe_filter_model import RecipeFilterModel
from recipe_model import RecipeModel

class RecipeList(QTreeView):
  def __init__(cls, parent):
    super().__init__(parent)
    cls.show()
    cls.model = RecipeModel(cls)
    cls.filter_model = RecipeFilterModel(cls, cls.model)
    cls.setModel(cls.filter_model)
    cls.setObjectName("RecipeList")
    cls.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    cls.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    cls.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    cls.header().setStretchLastSection(False)
    cls.setSelectionMode(QTreeView.SelectionMode.MultiSelection)
    
    
    
