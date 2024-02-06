from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton
from recipe_list import RecipeList
from server_select import ServerSelect
from job_select import JobSelect
from marketrequest import MarketRequest
from result_display import ResultDisplay

class MarketSearch(QWidget):

  def __init__(self, parent):
    super().__init__(parent, objectName="MarketSearch")
    self.setLayout(QGridLayout(self))
    
    # Creating widgets
    mr = MarketRequest(self)
    server_select = ServerSelect(self)
    parent.dc_only_mode.connect(server_select.dc_only_mode)
    recipe_list = RecipeList(self)
    job_select = JobSelect(self)
    output = ResultDisplay(self)
    
    # Forming connections
    mr.sendParams.connect(server_select.get_selected)
    mr.sendParams.connect(recipe_list.get_selected)
    
    server_select.returnParams.connect(mr.set_server)
    
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
    
  
