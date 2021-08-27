from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog, QHBoxLayout, QListWidgetItem

from logic.objectStore import access_records
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

        view = self.widget.accessHistoryView  # noqa -> view loaded from ui file
        for record in access_records:
            item = QListWidgetItem(record["filePath"])
            view.addItem(item)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.widget)

        self.configure_buttons()

    def configure_buttons(self):
        self.widget.cancelLoadButton.clicked.connect(self.close)  # noqa -> button loaded from ui file
