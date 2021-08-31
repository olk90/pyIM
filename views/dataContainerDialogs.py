import json

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog, QHBoxLayout

from logic.database import load_persons
from logic.files import access_records
from views.helpers import load_ui_file


class AccessHistoryDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.setMinimumWidth(450)
        self.setWindowTitle("Load recent file")
        ui_file_name = "ui/accessHistory.ui"
        ui_file = load_ui_file(ui_file_name)

        loader = QUiLoader()
        self.widget = loader.load(ui_file)
        ui_file.close()

        self.view = self.widget.accessHistoryView  # noqa -> view loaded from ui file
        for record in access_records:
            item = str(record["filePath"])
            self.view.addItem(item)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.widget)

        self.configure_buttons()

    def configure_buttons(self):
        self.widget.confirmLoadButton.clicked.connect(self.load_contents)  # noqa -> button loaded from ui file
        self.widget.cancelLoadButton.clicked.connect(self.close)  # noqa -> button loaded from ui file

    def load_contents(self):
        item = self.view.currentItem()
        file = open(item.text())
        dictionary = json.load(file)
        load_persons(dictionary["persons"])

        items = dictionary["items"]
        for i in items:
            print(i)

        self.close()
