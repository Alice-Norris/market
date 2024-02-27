from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton
from PySide6.QtCore import Signal, QEvent
from MarketGaze.Network import MarketNetworkManager
from MarketGaze.ServerSelect import ServerSelect
from MarketGaze.JobSelect import JobSelect
from MarketGaze.RecipeList import RecipeList
from MarketGaze.ResultDisplay import ResultDisplay
from MarketGaze.MarketEvent import MarketEvent

class MainWidget(QWidget):
  ui_update = Signal(name="UiUpdate")

  def __init__(self, parent):
    super().__init__(parent, objectName="MarketSearch")
    self.setLayout(QGridLayout(self))
    self.layout()
    # Creating widgets
    mr = MarketNetworkManager(self)
    recipe_list = RecipeList(self)
    server_select = ServerSelect(self)
    job_select = JobSelect(self)
    result_display = ResultDisplay(self)

    # TODO: Put this in its own widget?
    search_button = QPushButton("Search", self)
    search_button.pressed.connect(recipe_list.send_search_ids)
    recipe_list.send_recipe_ids.connect(mr.search)
    server_select.world_id_changed.connect(mr.set_world_id)
    server_select.dc_id_changed.connect(mr.set_dc_id)

    job_select.sortUpdate.connect(recipe_list.receive_sort_update)
    
    # Placing widgets in layout    
    self.layout().addWidget(server_select, 0, 0)
    self.layout().addWidget(job_select, 1, 0)
    self.layout().addWidget(recipe_list, 2, 0)
    self.layout().addWidget(search_button, 3, 0)
    self.layout().addWidget(result_display, 4, 0)  

  def event(self, event: QEvent):
    if event.type() == MarketEvent.Type.ConfigChanged.value:
      self.ui_update.emit()
      return True
    return super().event(event)