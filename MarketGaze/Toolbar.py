from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt

class Toolbar(QToolBar):

  def __init__(self, parent=None):
    super().__init__(parent)
    self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    help_action = QAction(QIcon("./data/icons/active_help.png"), "", parent)
    help_action.triggered.connect(parent.help_mode)

    cfg_action = QAction(QIcon("./data/icons/system_configuration.png"), "", parent)
    cfg_action.triggered.connect(parent.show_cfg)

    self.addAction(help_action)
    self.addAction(cfg_action)
    