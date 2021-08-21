from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QVBoxLayout

from views.editorwidgets import InventoryEditorWidget
from views.helpers import load_ui_file


class InventoryWidget(QWidget):

    def __init__(self):

        super().__init__()
        ui_file_name = "ui/inventoryView.ui"
        ui_file = load_ui_file(ui_file_name)

        loader = QUiLoader()
        loader.registerCustomWidget(InventoryEditorWidget)
        self.widget = loader.load(ui_file)
        ui_file.close()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.widget)
