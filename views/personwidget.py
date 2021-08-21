from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QVBoxLayout

from views.helpers import load_ui_file


class PersonWidget(QWidget):

    def __init__(self):
        super().__init__()

        ui_file_name = "ui/personView.ui"
        ui_file = load_ui_file(ui_file_name)

        loader = QUiLoader()
        self.widget = loader.load(ui_file)
        ui_file.close()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.widget)
