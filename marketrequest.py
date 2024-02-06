from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt6.QtCore import QJsonDocument
from PyQt6.QtCore import QUrl, pyqtSignal

# TODO: HTTP Error handling
# TODO: Add warning if unresolved items in responses
class MarketRequest(QNetworkAccessManager):
  sendParams = pyqtSignal()
  def __init__(self, parent):
    super().__init__(parent)
    #self.setUrl(QUrl("https://"))

  def search(self):
    self.sendParams.emit()
    item_ids = ','.join([str(id) for id in self.ids])
    url = QUrl(f"https://universalis.app/api/v2/{self.world}/{item_ids}")
    self.finished.connect(self.parse_reply)
    self.get(QNetworkRequest(url))

  def parse_reply(self, reply):
    print(reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute))
    result = QJsonDocument.fromJson(reply.readAll())
    reply = MarketReply(result)

  def set_url(self, url):
    self.url = url
    
  # Qt slots
  def set_ids(self, id_list: [int]):
    self.ids = id_list

  def set_server(self, dc_id, world_id):
    self.dc = dc_id
    self.world = world_id

class MarketReply:
  def __init__(self, data: QJsonDocument):
    data_object = data.object()
    x = 1
