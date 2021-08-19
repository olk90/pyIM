from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget

from views.helpers import load_ui_file


class InventoryEditorWidget(QWidget):

    def __init__(self, form):

        super().__init__(parent=form)
        ui_file_name = "ui/inventoryEditor.ui"
        ui_file = load_ui_file(ui_file_name)

        loader = QUiLoader()
        self.widget = loader.load(ui_file, form)
        ui_file.close()
