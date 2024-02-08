from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication
from PySide6.QtCore import Signal, QEvent
from MarketGaze.Network import MarketRequest
from MarketGaze.ServerSelect import ServerSelect
from MarketGaze.JobSelect import JobSelect
from MarketGaze.RecipeList import RecipeList
from MarketGaze.ResultDisplay import ResultDisplay
from MarketGaze.ConfigDialog import ConfigDialog
from MarketGaze.MarketEvent import MarketEvent


class MainWidget(QWidget):
  ui_update = Signal(name="UiUpdate")

  def __init__(self, parent):
    super().__init__(parent, objectName="MarketSearch")
    self.setLayout(QGridLayout(self))
    self.layout()

    self.installEventFilter(self)

    # Creating widgets
    mr = MarketRequest(self)
    server_select = ServerSelect(self)
    #self.ui_update.connect(server_select.toggle_dc_mode)
    recipe_list = RecipeList(self)
    job_select = JobSelect(self)
    output = ResultDisplay(self)
    
    # Forming connections
    #mr.sendParams.connect(server_select.get_selected)
    mr.sendParams.connect(recipe_list.get_selected)
    
    #server_select.returnParams.connect(mr.set_server)
    
    recipe_list.returnParams.connect(mr.set_ids)
    
    job_select.sortUpdate.connect(recipe_list.receive_sort_update)
    
    # TODO: Put this in its own widget?
    search_button = QPushButton("Search", self)
    search_button.pressed.connect(mr.search)

    # Placing widgets in layout    
    self.layout().addWidget(server_select, 0, 0)
    self.layout().addWidget(job_select, 1, 0)
    self.layout().addWidget(recipe_list, 2, 0)
    self.layout().addWidget(search_button, 3, 0)
    self.layout().addWidget(output, 4, 0)  

  def event(self, event: QEvent):
    if event.type() == MarketEvent.Type.ConfigChanged.value:
      self.ui_update.emit()
      return True
    return super().event(event)