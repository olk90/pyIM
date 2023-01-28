import json

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog, QHBoxLayout

from logic.database import load_persons, load_inventory
from views.helpers import load_ui_file
from views.inventory import InventoryWidget
from views.lendingHistory import LendingHistoryWidget
from views.person import PersonWidget


class AccessHistoryDialog(QDialog):

    def __init__(self, person_widget: PersonWidget = None, inventory_widget: InventoryWidget = None,
                 lh_widget: LendingHistoryWidget = None):
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
        self.lh_widget = lh_widget

        self.view = self.widget.accessHistoryView
        # for record in access_records:
        #     item = str(record["filePath"])
        #     self.view.addItem(item)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.widget)

        self.configure_buttons()

    def configure_buttons(self):
        self.widget.confirmLoadButton.clicked.connect(self.load_contents)
        self.widget.cancelLoadButton.clicked.connect(self.close)

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
