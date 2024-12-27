from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from logic.table_models import PersonModel, InventoryModel, LendingHistoryModel
from views.base_classes import OptionsEditorDialog, TableDialog, EncryptEditorDialog
from views.dataContainerDialogs import AccessHistoryDialog
from views.helpers import load_ui_file
from views.inventory import InventoryWidget
from views.lendingHistory import LendingHistoryWidget
from views.person import PersonWidget


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

        self.tabview = self.widget.tabview
        self.encrypt_dialog = EncryptEditorDialog(self)

        self.optionsButton = self.widget.optionsButton
        self.encrypt_button = self.widget.encryptButton

        self.configure_buttons()
        self.configure_tabview()

        self.layout.addWidget(self.widget)

        form.resize(1600, 900)

    def configure_tabview(self):
        tabview = self.widget.tabview

        person_widget = PersonWidget()
        self.accessHistoryDialog.person_widget = person_widget
        tabview.addTab(person_widget, self.tr("Persons"))

        inventory_widget = InventoryWidget()
        self.accessHistoryDialog.inventory_widget = inventory_widget
        tabview.addTab(inventory_widget, self.tr("Inventory"))

        lh_widget = LendingHistoryWidget()
        self.accessHistoryDialog.lh_widget = lh_widget
        tabview.addTab(lh_widget, self.tr("Lending History"))

        self.tabview.currentChanged.connect(self.reload_current_widget)

    def reload_current_widget(self):
        current: QWidget = self.tabview.currentWidget()
        if isinstance(current, TableDialog):
            search = current.searchLine.text()
            # example
            if isinstance(current, PersonWidget):
                current.reload_table_contents(PersonModel(search))
            if isinstance(current, InventoryWidget):
                current.reload_table_contents(InventoryModel(search))
            if isinstance(current, LendingHistoryWidget):
                current.reload_table_contents(LendingHistoryModel(search))

    def configure_buttons(self):
        self.widget.loadDbButton.clicked.connect(self.load_access_history)
        self.encrypt_button.clicked.connect(self.open_encrypt)
        self.optionsButton.clicked.connect(self.open_options)

    def load_access_history(self):
        self.accessHistoryDialog.exec_()

    def open_options(self):
        self.options_dialog.exec_()

    def open_encrypt(self):
        self.encrypt_dialog.exec_()
        self.reload_current_widget()
