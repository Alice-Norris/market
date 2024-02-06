from PyQt6.QtWidgets import QToolBar, QWidget
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt

class Toolbar(QToolBar):

  def __init__(self, parent: QWidget=None):
    super().__init__(parent)

    help_action = QAction(QIcon("./data/icons/active_help.png"), "", parent)
    
    cfg_action = QAction(QIcon("./data/icons/system_configuration.png"), "", parent)
    cfg_action.triggered.connect(parent.cfg_dialog.show)
    
    self.addAction(help_action)
    self.addAction(cfg_action)

    self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)