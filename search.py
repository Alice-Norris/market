from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QFrame, QComboBox, QTreeView

class Search(QFrame):
  def __init__(cls, parent):
    super().__init__(parent)
    cls.layout = QHBoxLayout(cls)
    cls.show()
    cls.mk_widgets()
    

  def mk_widgets(cls):
    cls.btn = QPushButton("Search", cls)
    cls.btn.show()
    cls.btn.clicked.connect(cls.collect_search_data)
    cls.layout.addWidget(cls.btn)

  def collect_search_data(cls):
    dc_sel = cls.parent().findChild(QComboBox, "dc_sel")
    world_sel = cls.parent().findChild(QComboBox, "world_sel")
    jobs = cls.parent().findChild(QFrame, "JobSelect").job_sel
    recipes: QTreeView = cls.parent().findChild(QFrame, "RecipeList")
    dc_name = dc_sel.currentText()
    world_name = world_sel.currentText()
    recipe_comps = [item.data() for item in recipes.selectedIndexes()]
    print("DC: " + dc_name)
    print("World: " + world_name)
    print("Selected Jobs: ", jobs.keys())
    if len(recipe_comps) == 3:
      print("Recipe Name: " + recipe_comps[1])
      print("Recipe Item Id: " + recipe_comps[2])