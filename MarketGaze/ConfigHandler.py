from PySide6.QtCore import QObject, QSettings, QSize, QPoint

class ConfigHandler(QObject):
  
  SETTINGS = {
    "AppWindow" : {
      "Position":QPoint(479, 269),
      "Size": QSize(540, 960)
    },
    "Config" : {
      "DcOnly" : False,
      "ConsiderHistory" : False,
      "EnableLogging" : False
    }
  }

  def __init__(cls, parent=None):
    super().__init__(parent, objectName="ConfigHandler")
    cls.chk_cfg()
  
  def chk_cfg(cls):
    cfg = QSettings()

    for grp_name in cls.SETTINGS.keys():

      cfg.beginGroup(grp_name)

      for (key, val) in cls.SETTINGS[grp_name].items():
        if not cfg.contains(key):
          cfg.setValue(key, val)

      cfg.endGroup()

    cfg.sync()

  def get_cfg(self, grp_name: str, key_name: str=None):
    cfg = QSettings()
    output = {}

    if key_name is not None:
      key = f"{grp_name}/{key_name}"
      val_type = type(self.SETTINGS[grp_name][key_name])
      output[key] = cfg.value(key, type=val_type)
    else:
      cfg.beginGroup(grp_name)

      for key in cfg.allKeys():
        val_type = type(self.SETTINGS[grp_name][key])
        output[key] = cfg.value(key, type=val_type)

      cfg.endGroup()

    return output
  
    