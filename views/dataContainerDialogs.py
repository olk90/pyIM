import json

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog, QHBoxLayout

from logic.database import load_persons, load_inventory
from logic.files import access_records
from views.helpers import load_ui_file
from views.inventoryDialog import InventoryWidget
from views.personDialog import PersonWidget


class AccessHistoryDialog(QDialog):

    def __init__(self, person_widget: PersonWidget = None, inventory_widget: InventoryWidget = None):
        super().__init__()
        self.setModal(True)
        self.setMinimumWidth(450)
        self.setWindowTitle("Load recent file")
        ui_file_name = "ui/accessHistory.ui"
        ui_file = load_ui_file(ui_file_name)

        loader = QUiLoader()
        self.widget = loader.load(ui_file)
        ui_file.close()

        self.person_widget = person_widget
        self.inventory_widget = inventory_widget

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
        persons = dictionary["persons"]
        load_persons(persons)
        self.person_widget.reload_table_contents()

        items = dictionary["items"]
        load_inventory(items)
        self.inventory_widget.reload_table_contents()

        self.close()
