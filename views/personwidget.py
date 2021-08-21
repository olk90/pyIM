from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QHBoxLayout

from views.helpers import load_ui_file


class PersonWidget(QWidget):

    def __init__(self):
        super().__init__()

        loader = QUiLoader()

        table_ui_name = "ui/personView.ui"
        table_file = load_ui_file(table_ui_name)
        self.table = loader.load(table_file)
        table_file.close()

        editor_ui_name = "ui/personEditor.ui"
        editor_file = load_ui_file(editor_ui_name)
        self.editor = loader.load(editor_file)
        editor_file.close()

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.table, stretch=2)
        self.layout.addWidget(self.editor, stretch=1)
