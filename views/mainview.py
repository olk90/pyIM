from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QVBoxLayout

from views.helpers import load_ui_file
from views.inventorywidget import InventoryWidget
from views.personwidget import PersonWidget


class MainWindow(QMainWindow):

    def __init__(self, form):
        super().__init__(parent=form)
        self.adjustSize()

        form.setWindowTitle("pyIM")

        self.layout = QVBoxLayout(form)

        ui_file_name = "ui/main.ui"
        ui_file = load_ui_file(ui_file_name)

        loader = QUiLoader()
        loader.registerCustomWidget(InventoryWidget)
        self.widget = loader.load(ui_file, form)
        ui_file.close()

        self.configure_tabview()

        self.layout.addWidget(self.widget)

        form.resize(1600, 900)

    def configure_tabview(self):
        tabview = self.widget.tabview  # noqa -> tabview is loaded from ui file

        person_widget = PersonWidget()
        tabview.addTab(person_widget, "Persons")

        inventory_widget = InventoryWidget()
        tabview.addTab(inventory_widget, "Inventory")
