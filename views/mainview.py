from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow

from views.helpers import load_ui_file
from views.inventorywidget import InventoryWidget
from views.personwidget import PersonWidget


class MainWindow(QMainWindow):

    def __init__(self, form):
        super().__init__(parent=form)
        self.adjustSize()

        form.setWindowTitle("pyIM")

        ui_file_name = "ui/main.ui"
        ui_file = load_ui_file(ui_file_name)

        loader = QUiLoader()
        loader.registerCustomWidget(PersonWidget)
        loader.registerCustomWidget(InventoryWidget)
        self.widget = loader.load(ui_file, form)
        ui_file.close()

        form.resize(1600, 900)
