from PySide6.QtGui import Qt
from PySide6.QtSql import QSqlQueryModel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QHBoxLayout, QHeaderView, QTableView

from logic.queries import personQuery
from views.editorDialogs import PersonEditorWidget
from views.helpers import load_ui_file


class PersonWidget(QWidget):

    def __init__(self):
        super(PersonWidget, self).__init__()

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

        self.setup_table()

    def get_table(self):
        return self.table_widget.table  # noqa -> loaded from ui file

    def setup_table(self):
        model = QSqlQueryModel()
        model.setQuery(personQuery)
        model.setHeaderData(0, Qt.Horizontal, "First Name")
        model.setHeaderData(1, Qt.Horizontal, "Last Name")
        model.setHeaderData(2, Qt.Horizontal, "E-Mail")

        tableview = self.get_table()
        tableview.setModel(model)
        tableview.setSelectionBehavior(QTableView.SelectRows)
        tableview.setSortingEnabled(True)

        header = tableview.horizontalHeader()
        for i in range(0, 3):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
