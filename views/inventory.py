from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox, QSpinBox, QPlainTextEdit, QCheckBox, \
    QLineEdit, QDialogButtonBox, QLabel

from logic.database import persist_item
from logic.model import InventoryItem
from logic.table_models import InventoryModel
from views.base_classes import TableDialog, EditorDialog, EditorWidget
from views.helpers import get_min_date


class AddInventoryDialog(EditorDialog):

    def __init__(self, parent: QWidget):
        super(AddInventoryDialog, self).__init__(parent=parent, ui_file_name="ui/inventoryEditor.ui")
        self.get_widget(QLabel, "editorTitle").setText(self.tr("Add Device"))

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.widget)
        self.button_box: QDialogButtonBox = self.widget.buttonBox

        self.configure_widgets()

    def commit(self):
        name: str = self.widget.nameEdit.text()
        category: str = self.widget.categoryEdit.text()
        available: bool = self.widget.availableCheckbox.checked()
        info: str = self.widget.infoEdit.text()

        item = InventoryItem(name=name, category=category, available=available, info=info)
        persist_item(item)
        self.parent.reload_table_contents(model=InventoryModel())

    def clear_fields(self):
        self.widget.nameEdit.setText("")
        self.widget.categoryEdit.setText("")
        self.widget.availableCheckbox.setChecked(False)
        self.widget.infoEdit.setText("")


class InventoryEditorWidget(EditorWidget):

    def __init__(self, item_id=None):
        super(InventoryEditorWidget, self).__init__(ui_file_name="ui/inventoryEditor.ui", item_id=item_id)

        self.nameEdit: QLineEdit = self.widget.nameEdit
        self.categoryEdit: QLineEdit = self.widget.categoryEdit
        self.availableCheckbox: QCheckBox = self.widget.availableCheckbox
        self.nextMotButton: QPushButton = self.widget.nextMotButton
        self.monthCombo: QComboBox = self.widget.monthCombo
        self.yearSpinner: QSpinBox = self.widget.yearSpinner
        self.infoEdit: QPlainTextEdit = self.widget.infoEdit

        self.configure_next_mot()

    def configure_next_mot(self):
        combo = self.widget.monthCombo
        spinbox = self.widget.yearSpinner
        min_date = get_min_date()
        index = combo.findText(min_date[0], QtCore.Qt.MatchFixedString)
        if index >= 0:
            combo.setCurrentIndex(index)
        spinbox.setMinimum(min_date[1])

    def fill_fields(self, item: InventoryItem):
        # self.nameEdit.setText(name)
        # self.categoryEdit.setText(category)
        #
        # if available:
        #     self.availableCheckbox.setCheckState(QtCore.Qt.CheckState.Checked)
        # else:
        #     self.availableCheckbox.setCheckState(QtCore.Qt.CheckState.Unchecked)
        #
        # self.nextMotButton.setChecked(mot_required)
        # if mot_required:
        #     month = next_mot.month
        #     year = next_mot.year
        #     self.monthCombo.setCurrentIndex(month - 1)
        #     self.yearSpinner.setValue(year)
        #
        # self.infoEdit.setPlainText(info)
        pass


class InventoryWidget(TableDialog):

    def __init__(self):
        super(InventoryWidget, self).__init__(table_ui_name="ui/inventoryView.ui")
        self.add_dialog = AddInventoryDialog(self)
        self.setup_table(InventoryModel(), range(1, 7))

    def get_editor_widget(self) -> EditorWidget:
        return InventoryEditorWidget()

    def configure_search(self):
        self.searchLine.textChanged.connect(
            lambda x: self.reload_table_contents(InventoryModel(self.searchLine.text())))
