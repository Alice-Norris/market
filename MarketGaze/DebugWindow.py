from PySide6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QDialog

class DebugWindow(QDialog):
  def __init__(self, parent=None):
    super().__init__(parent, objectName="DebugLog")
    self.setWindowTitle("Debug Log")
    self.setLayout(QVBoxLayout())
    dbg_log = QPlainTextEdit(self, readOnly=True)
    #dbg_log.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
    font_info = dbg_log.fontMetrics()
    dbg_log.setFixedWidth(font_info.averageCharWidth()*80)
    dbg_log.setFixedHeight(font_info.lineSpacing()*6)
    self.layout().addWidget(dbg_log)

  #def error_event(self, event: QErrorEvent):