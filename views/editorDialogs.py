from PySide6 import QtCore
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QHBoxLayout

from views.helpers import load_ui_file, get_min_date


class PersonEditorWidget(QWidget):

    def __init__(self):

        super().__init__()
        ui_file_name = "ui/personEditor.ui"
        ui_file = load_ui_file(ui_file_name)

        loader = QUiLoader()
        self.widget = loader.load(ui_file)
        ui_file.close()

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.widget)


class InventoryEditorWidget(QWidget):

    def __init__(self):

        super().__init__()
        ui_file_name = "ui/inventoryEditor.ui"
        ui_file = load_ui_file(ui_file_name)

        loader = QUiLoader()
        self.widget = loader.load(ui_file)
        ui_file.close()

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.widget)
        
        self.configure_next_mot()

    def configure_next_mot(self):
        combo = self.widget.monthCombo  # noqa -> loaded from ui file
        spinbox = self.widget.yearSpinner  # noqa -> loaded from ui file
        min_date = get_min_date()
        index = combo.findText(min_date[0], QtCore.Qt.MatchFixedString)
        if index >= 0:
            combo.setCurrentIndex(index)
        spinbox.setMinimum(min_date[1])
