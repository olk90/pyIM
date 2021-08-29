import sys

from PySide6.QtSql import QSqlRelationalTableModel, QSqlDatabase
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QHBoxLayout, QHeaderView

from logic.model import inventoryTableName
from views.editorDialogs import InventoryEditorWidget
from views.helpers import load_ui_file


class InventoryWidget(QWidget):

    def __init__(self):
        super().__init__()

        loader = QUiLoader()

        table_ui_name = "ui/inventoryView.ui"
        table_file = load_ui_file(table_ui_name)
        self.table_widget = loader.load(table_file)
        table_file.close()

        editor_ui_name = "ui/inventoryEditor.ui"
        editor_file = load_ui_file(editor_ui_name)
        self.editor = InventoryEditorWidget()
        editor_file.close()

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.table_widget, stretch=2)
        self.layout.addWidget(self.editor, stretch=1)

        self.create_connection()
        self.setup_table()

    def get_table(self):
        return self.table_widget.table  # noqa -> loaded from ui file

    def create_connection(self):
        database = QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName("pyIM.db")

        if not database.open():
            print("Unable to open database")
            sys.exit(1)

    def setup_table(self):
        model = QSqlRelationalTableModel()
        model.setTable(inventoryTableName)
        tableview = self.get_table()
        tableview.setModel(model)
        model.select()
