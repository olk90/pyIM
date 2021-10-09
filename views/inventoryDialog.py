from PySide6.QtCore import QItemSelectionModel, QModelIndex
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QHBoxLayout, QHeaderView, QTableView

from logic.database import configure_inventory_model, find_inventory_by_name
from logic.model import InventoryItem
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
        tableview.selectionModel().selectionChanged.connect(lambda x: self.reload_editor())

        header = tableview.horizontalHeader()
        for i in range(0, 6):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def reload_table_contents(self):
        model = configure_inventory_model()
        tableview = self.get_table()
        tableview.setModel(model)

    def reload_editor(self):
        tableview: QTableView = self.get_table()
        selection_model: QItemSelectionModel = tableview.selectionModel()
        indexes: QModelIndex = selection_model.selectedRows()
        model = tableview.model()
        for index in indexes:
            name: str = model.data(model.index(index.row(), 0))
            item: InventoryItem = find_inventory_by_name(name)
            category = item.category
            available = item.available
            info = item.info
            mot_required = item.mot_required
            next_mot = item.next_mot

            self.editor.fill_fields(name, category, available, mot_required, next_mot, info)
