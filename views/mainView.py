from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QVBoxLayout

from views.dataContainerDialogs import AccessHistoryDialog
from views.editorDialogs import OptionsEditorDialog
from views.helpers import load_ui_file
from views.inventoryDialog import InventoryWidget
from views.personDialog import PersonWidget


class MainWindow(QMainWindow):

    def __init__(self, form):
        super().__init__(parent=form)
        self.adjustSize()

        form.setWindowTitle("pyIM")
        form.setWindowIcon(QIcon("icon.svg"))

        self.layout = QVBoxLayout(form)

        self.options_dialog = OptionsEditorDialog(self)
        self.accessHistoryDialog = AccessHistoryDialog()

        ui_file_name = "ui/main.ui"
        ui_file = load_ui_file(ui_file_name)

        loader = QUiLoader()
        self.widget = loader.load(ui_file, form)
        ui_file.close()

        self.optionsButton = self.widget.optionsButton  # noqa

        self.configure_buttons()
        self.configure_tabview()

        self.layout.addWidget(self.widget)

        form.resize(1600, 900)

    def configure_tabview(self):
        tabview = self.widget.tabview  # noqa -> tabview is loaded from ui file

        person_widget = PersonWidget()
        self.accessHistoryDialog.person_widget = person_widget
        tabview.addTab(person_widget, "Persons")

        inventory_widget = InventoryWidget()
        self.accessHistoryDialog.inventory_widget = inventory_widget
        tabview.addTab(inventory_widget, "Inventory")

    def configure_buttons(self):
        self.widget.loadDbButton.clicked.connect(self.load_access_history)  # noqa -> button loaded from ui file
        self.optionsButton.clicked.connect(self.open_options)

    def load_access_history(self):
        self.accessHistoryDialog.exec_()

    def open_options(self):
        self.options_dialog.exec_()
