from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QHBoxLayout, QHeaderView

from views.editorwidgets import PersonEditorWidget
from views.helpers import load_ui_file


class PersonWidget(QWidget):

    def __init__(self):
        super().__init__()

        loader = QUiLoader()

        table_ui_name = "ui/personView.ui"
        table_file = load_ui_file(table_ui_name)
        self.table_widget = loader.load(table_file)
        table_file.close()

        editor_ui_name = "ui/personEditor.ui"
        editor_file = load_ui_file(editor_ui_name)
        self.editor = PersonEditorWidget()
        editor_file.close()

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.table_widget, stretch=2)
        self.layout.addWidget(self.editor, stretch=1)

        table = self.get_table()

        header = table.horizontalHeader()
        for i in range(0, 3):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def get_table(self):
        return self.table_widget.table  # noqa -> loaded from ui file
