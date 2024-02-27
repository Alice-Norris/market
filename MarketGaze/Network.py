from math import ceil
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QEventLoop, QFile, QJsonDocument, QUrl, Signal, Slot, QSettings, QByteArray
from MarketGaze.Constants import RequestType, FFData
from MarketGaze.ResultModel import ResultModel

# TODO: HTTP Error handling
# TODO: Add warning if unresolved items in responses
class MarketNetworkManager(QNetworkAccessManager):
  active_reqs = 0
  data_send = Signal(QByteArray, FFData)
  market_url = QUrl("https://universalis.app/api/v2/")
  search_complete = Signal(name="searchComplete")
  results = ResultModel()

  def __init__(self, parent):
    super().__init__(parent)
    self.dc_id = QSettings().value("Search/DcId")
    self.world_id = QSettings().value("Search/WorldId")
    self.dc_only = QSettings().value("Config/DcOnly", type=bool)
    self.recipe_list = []
    # self.finished.connect(self.parse_reply)

  @Slot(name="Search")
  def search(self, ids):
    self.recipe_list = ids
    server_id = 0
    pos = 0

    if self.dc_only:
      server_id = self.dc_id
    else:
      server_id = self.world_id

    while pos < len(self.recipe_list):
      batch = self.recipe_list[pos:pos+100]
      pos += 100
      
      item_str = ','.join([str(id) for id in batch])

      self.send_reqs(server_id, item_str)
      x=1

  @Slot(list, name="FetchData")
  def fetch_data(self, entry: FFData) -> QJsonDocument:
    url = QUrl(entry.value["url"])
    json = None 
    if "payload" in entry.value:
      self.multi_fetch(entry)
    #req.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
    loop = QEventLoop(self)
    reply = self.post(QNetworkRequest(url), json)
    reply.finished.connect(loop.quit)
    loop.exec()
    #reply.finished.connect(self.write_to_file)
    if reply.isFinished():
      loop.exit()
      self.data_send.emit(reply.readAll(), entry)
  
  def num_results(self, url: QUrl, payload_dict: dict) -> int:
    payload_dict["body"]["size"] = 0
    payload = QJsonDocument.fromVariant(payload_dict).toJson()
    response: QByteArray = self.synch_request(QNetworkRequest(url), payload)
    object = QJsonDocument.fromJson(response).object()
    return object["Pagination"]["ResultsTotal"]
    
  def multi_fetch(self, entry:FFData):
    url = QUrl(entry.value["url"])
    payload_dict = entry.value["payload"]
    num_res = self.num_results(url, payload_dict)
    payload_dict["body"]["size"] = 2500
    request: QNetworkRequest = QNetworkRequest(url)
    
    for i in range(0, ceil(num_res / 2500)):
      payload_dict["body"]["from"] = i*2500
      payload = QJsonDocument.fromVariant(payload_dict).toJson(QJsonDocument.JsonFormat.Compact)
      self.post(QNetworkRequest(url), payload)
      self.active_reqs += 1
    x=1

  def check_cache(self, reply):
    self.active_reqs -= 1
    if self.active_reqs == 0:
      x = 1

  def synch_request(self, req: QNetworkRequest, payload: QJsonDocument) -> QByteArray:
    loop = QEventLoop(self)
    reply: QNetworkReply = self.post(req, payload)
    reply.finished.connect(loop.quit)
    loop.exec()
    return reply.readAll()


  def send_reqs(self, server_id, item_str):
    
    url = QUrl(f"http://universalis.app/api/v2/{server_id}/{item_str}")
    
    self.get(QNetworkRequest(url))
    
    url = QUrl(f"http://universalis.app/api/v2/history/{server_id}/{item_str}")

    self.get(QNetworkRequest(url))
  
  @Slot(list, name="SetRecipeIds")
  def set_recipe_ids(self, recipe_list: list[int]):
    self.recipe_list = recipe_list

  @Slot(int, name="SetDcId")
  def set_dc_id(self, id):
    self.dc_id = id

  @Slot(int, name="SetWorldId")
  def set_world_id(self, id):
    self.world_id = id

  def curr_resp(self, resp):
    x=1

  def parse_reply(self, reply: QNetworkReply):
    data = QJsonDocument.fromJson(reply.readAll()).toVariant()
    path = reply.url().path()

    req_type = RequestType.HISTORY if "history" in path else RequestType.CURRENT

    if "itemID" in data:
      self.results.add_item(data, req_type)
    else:
      self.results.add_items(data, req_type)

# class MarketRequest(QNetworkRequest):
#   base_url = "http::/universalis.app/api/v2"

#   def __init__(self, server_id: int, item_ids: list[int], type: RequestType=RequestType.CURRENT):
#     # Set list of item ids, a server id, and request type
#     # Creating URL components

#     super().__init__(self.url)

# class MarketReply(QNetworkReply):
#   def __init__(self, item_ids: list[int], type: RequestType):
#     super().__init__()
#     self.items = item_ids
#     self.type = type

#   def get_num_items(self: MarketNetworkManager) -> int:
#     return len(self.items)
  
#   def get_type(self: MarketNetworkManager) -> RequestType:
#     return self.type
