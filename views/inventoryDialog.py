from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QHBoxLayout, QHeaderView, QTableView

from logic.database import configure_inventory_model
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

        self.setup_table()

    def get_table(self):
        return self.table_widget.table  # noqa -> loaded from ui file

    def setup_table(self):
        model = configure_inventory_model()

        tableview = self.get_table()
        tableview.setModel(model)
        tableview.setSelectionBehavior(QTableView.SelectRows)

        header = tableview.horizontalHeader()
        for i in range(0, 6):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def reload_table_contents(self):
        model = configure_inventory_model()
        tableview = self.get_table()
        tableview.setModel(model)
