from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget

from views.editorwidgets import InventoryEditorWidget
from views.helpers import load_ui_file


class InventoryWidget(QWidget):

    def __init__(self, form):

        super().__init__(parent=form)
        ui_file_name = "ui/inventoryView.ui"
        ui_file = load_ui_file(ui_file_name)

        loader = QUiLoader()
        loader.registerCustomWidget(InventoryEditorWidget)
        self.widget = loader.load(ui_file, form)
        ui_file.close()
