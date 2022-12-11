from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from logic.table_models import PersonModel, InventoryModel
from views.base_classes import OptionsEditorDialog, TableDialog
from views.dataContainerDialogs import AccessHistoryDialog
from views.helpers import load_ui_file
from views.inventory import InventoryWidget
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
        self.optionsButton = self.widget.optionsButton

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

        self.tabview.currentChanged.connect(self.reload_current_widget)

    def reload_current_widget(self):
        current: QWidget = self.tabview.currentWidget()
        if isinstance(current, TableDialog):
            search = current.searchLine.text()
            if isinstance(current, PersonWidget):
                current.reload_table_contents(PersonModel(search))
            if isinstance(current, InventoryWidget):
                current.reload_table_contents(InventoryModel(search))

    def configure_buttons(self):
        self.widget.loadDbButton.clicked.connect(self.load_access_history)
        self.optionsButton.clicked.connect(self.open_options)

    def load_access_history(self):
        self.accessHistoryDialog.exec_()

    def open_options(self):
        self.options_dialog.exec_()
