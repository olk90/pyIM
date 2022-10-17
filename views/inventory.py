from datetime import date

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox, QSpinBox, QPlainTextEdit, QCheckBox, \
    QLineEdit, QDialogButtonBox, QLabel

from logic.database import persist_item, find_by_id
from logic.model import InventoryItem
from logic.table_models import InventoryModel
from views.base_classes import TableDialog, EditorDialog, EditorWidget
from views.base_functions import configure_month_box, configure_year_box, get_day_range, get_date
from views.helpers import configure_next_mot


class AddInventoryDialog(EditorDialog):

    def __init__(self, parent: QWidget):
        super(AddInventoryDialog, self).__init__(parent=parent, ui_file_name="ui/inventoryEditor.ui")
        self.get_widget(QLabel, "editorTitle").setText(self.tr("Add Device"))

        self.name_edit: QLineEdit = self.get_widget(QLineEdit, "nameEdit")
        self.category_edit: QLineEdit = self.get_widget(QLineEdit, "categoryEdit")

        self.name_edit.textChanged.connect(self.widget.validate)
        self.category_edit.textChanged.connect(self.widget.validate)

        self.widget.append_validation_fields(self.name_edit)
        self.widget.append_validation_fields(self.category_edit)

        self.next_mot_button: QPushButton = self.get_widget(QPushButton, "nextMotButton")
        self.month_combobox: QComboBox = self.get_widget(QComboBox, "monthCombo")
        self.year_spinner: QSpinBox = self.get_widget(QSpinBox, "yearSpinner")

        configure_next_mot(self.month_combobox, self.year_spinner)

        self.available_checkbox: QCheckBox = self.get_widget(QCheckBox, "availableCheckbox")
        self.info_edit: QPlainTextEdit = self.get_widget(QPlainTextEdit, "infoEdit")

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.widget)
        self.button_box: QDialogButtonBox = self.widget.buttonBox

        self.configure_widgets()

    def commit(self):
        name: str = self.name_edit.text()
        category: str = self.category_edit.text()
        available: bool = self.available_checkbox.isChecked()
        info: str = self.info_edit.toPlainText()

        mot_required: bool = self.next_mot_button.isChecked()
        mot_date = None
        if mot_required:
            month: int = self.month_combobox.currentIndex() + 1
            year: int = self.year_spinner.value()
            day: int = get_day_range(month, year)[-1]
            mot_date = date(year, month, day)

        item = InventoryItem(name=name, category=category, available=available, info=info, mot_required=mot_required)
        if mot_date:
            item.next_mot = mot_date
        persist_item(item)
        self.parent.reload_table_contents(model=InventoryModel())
        self.close()

    def configure_widgets(self):
        super(AddInventoryDialog, self).configure_widgets()
        configure_month_box(self.month_combobox)
        configure_year_box(self.year_spinner)


class InventoryEditorWidget(EditorWidget):

    def __init__(self, item_id=None):
        super(InventoryEditorWidget, self).__init__(ui_file_name="ui/inventoryEditor.ui", item_id=item_id)

        self.name_edit: QLineEdit = self.widget.nameEdit
        self.category_edit: QLineEdit = self.widget.categoryEdit
        self.available_checkbox: QCheckBox = self.widget.availableCheckbox
        self.next_mot_button: QPushButton = self.widget.nextMotButton
        self.month_combobox: QComboBox = self.widget.monthCombo
        self.year_spinner: QSpinBox = self.widget.yearSpinner
        self.info_edit: QPlainTextEdit = self.widget.infoEdit

        self.year = self.year_spinner.value()
        self.month = self.month_combobox.currentIndex() + 1

        configure_next_mot(self.month_combobox, self.year_spinner)
        configure_month_box(self.month_combobox)
        configure_year_box(self.year_spinner)

        self.month_combobox.currentTextChanged.connect(self.update_mot)
        self.year_spinner.valueChanged.connect(self.update_mot)

    def fill_fields(self, item: InventoryItem):
        self.item_id = item.id
        self.name_edit.setText(item.name)
        self.category_edit.setText(item.category)
        self.info_edit.setPlainText(item.info)
        self.available_checkbox.setChecked(item.available)

        if item.mot_required:
            mot_date = item.next_mot
            self.month_combobox.setCurrentIndex(mot_date.month - 1)
            self.year_spinner.setValue(mot_date.year)

    def get_values(self) -> dict:
        return {
            "item_id": self.item_id,
            "name": self.name_edit.text(),
            "category": self.category_edit.text(),
            "info": self.info_edit.toPlainText(),
            "next_mot": get_date(self.month, self.year),
            "available": self.available_checkbox.isChecked()
        }

    def update_mot(self):
        self.year = self.year_spinner.value()
        self.month = self.month_combobox.currentIndex() + 1

    def clear_fields(self):
        self.name_edit.setText("")
        self.category_edit.setText("")
        self.available_checkbox.setChecked(False)
        self.info_edit.insertPlainText("")


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

    def get_selected_item(self):
        item_id = super().get_selected_item()
        item = find_by_id(item_id, InventoryItem)
        return item
