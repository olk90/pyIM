from datetime import date
from typing import Union

from PySide6.QtCore import QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QSpinBox, QPlainTextEdit, QCheckBox, \
    QLineEdit, QDialogButtonBox, QLabel, QStyleOptionViewItem, QStyleOptionButton, QTableView, QMessageBox, QToolButton

from logic.database import persist_item, find_by_id, update_inventory, delete_item, configure_query_model, \
    check_and_return
from logic.model import InventoryItem, Person
from logic.queries import person_fullname_query
from logic.table_models import InventoryModel, SearchTableModel
from views.base_classes import TableDialog, EditorDialog, EditorWidget, DateItemDelegate
from views.base_functions import configure_month_box, configure_year_box, get_day_range, get_date
from views.confirmationDialogs import ConfirmDeletionDialog
from views.helpers import configure_next_mot, calculate_background


class AddInventoryDialog(EditorDialog):

    def __init__(self, parent: QWidget):
        super(AddInventoryDialog, self).__init__(parent=parent, ui_file_name="ui/inventoryEditor.ui")
        self.get_widget(QLabel, "editorTitle").setText(self.tr("Add Device"))

        self.name_edit: QLineEdit = self.get_widget(QLineEdit, "nameEdit")
        self.category_edit: QLineEdit = self.get_widget(QLineEdit, "categoryEdit")

        self.name_edit.textChanged.connect(self.widget.validate)
        self.category_edit.textChanged.connect(self.widget.validate)

        self.widget.append_validation_fields(self.name_edit, self.category_edit)

        self.mot_checkbox: QCheckBox = self.get_widget(QCheckBox, "motCheckBox")
        self.month_combobox: QComboBox = self.get_widget(QComboBox, "monthCombo")
        self.year_spinner: QSpinBox = self.get_widget(QSpinBox, "yearSpinner")

        configure_next_mot(self.month_combobox, self.year_spinner)

        self.available_checkbox: QCheckBox = self.get_widget(QCheckBox, "availableCheckbox")
        self.info_edit: QPlainTextEdit = self.get_widget(QPlainTextEdit, "infoEdit")

        # lending options not needed here
        lender_label = self.get_widget(QLabel, "lenderLabel")
        lender_box = self.get_widget(QComboBox, "lenderBox")
        return_button = self.get_widget(QToolButton, "returnButton")
        lender_label.deleteLater()
        lender_box.deleteLater()
        return_button.deleteLater()

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.widget)
        self.button_box: QDialogButtonBox = self.widget.buttonBox

        self.configure_widgets()

    def commit(self):
        name: str = self.name_edit.text()
        category: str = self.category_edit.text()
        available: bool = self.available_checkbox.isChecked()
        info: str = self.info_edit.toPlainText()

        mot_required: bool = self.mot_checkbox.isChecked()
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

        self.name_edit.textChanged.connect(self.validate)
        self.category_edit.textChanged.connect(self.validate)

        self.append_validation_fields(self.name_edit, self.category_edit)

        self.available_checkbox: QCheckBox = self.widget.availableCheckbox
        self.mot_checkbox: QCheckBox = self.widget.motCheckBox
        self.month_combobox: QComboBox = self.widget.monthCombo
        self.year_spinner: QSpinBox = self.widget.yearSpinner
        self.info_edit: QPlainTextEdit = self.widget.infoEdit

        self.lender_combobox: QComboBox = self.widget.lenderBox
        self.return_button: QToolButton = self.widget.returnButton

        self.lender_id: int = -1
        self.lender_combobox.currentIndexChanged.connect(self.update_lender_id)
        self.lender_combobox.currentIndexChanged.connect(self.validate)

        self.reload_lender_box()

        configure_next_mot(self.month_combobox, self.year_spinner)
        configure_month_box(self.month_combobox)
        configure_year_box(self.year_spinner)

        self.year = self.year_spinner.value()
        self.month = self.month_combobox.currentIndex() + 1

        self.month_combobox.currentTextChanged.connect(self.update_mot)
        self.year_spinner.valueChanged.connect(self.update_mot)

    def reload_lender_box(self):
        query: str = person_fullname_query()
        configure_query_model(self.lender_combobox, query)

    def fill_fields(self, item: InventoryItem):
        self.item_id = item.id
        self.name_edit.setText(item.name)
        self.category_edit.setText(item.category)
        self.info_edit.setPlainText(item.info)
        self.available_checkbox.setChecked(item.available)
        self.mot_checkbox.setChecked(item.mot_required)

        if item.mot_required:
            mot_date = item.next_mot
            self.month_combobox.setCurrentIndex(mot_date.month - 1)
            self.year_spinner.setValue(mot_date.year)

        if item.lender_id:
            self.lender_id = item.lender_id
            lender: Person = find_by_id(self.lender_id, Person)
            if lender:
                self.lender_combobox.setCurrentText(lender.get_full_name())
        else:
            self.lender_combobox.setCurrentIndex(-1)

    def get_values(self) -> dict:
        mot_required: bool = self.mot_checkbox.isChecked()
        return {
            "item_id": self.item_id,
            "name": self.name_edit.text(),
            "category": self.category_edit.text(),
            "info": self.info_edit.toPlainText(),
            "mot_required": mot_required,
            "next_mot": get_date(mot_required, self.month, self.year),
            "available": self.available_checkbox.isChecked(),
            "lender": self.lender_id
        }

    def validate(self) -> bool:
        enable: bool = super(InventoryEditorWidget, self).validate()
        if enable:
            item: InventoryItem = find_by_id(self.item_id, InventoryItem)
            mot = item.next_mot
            mot_expired: bool = date.today() >= mot if mot else False
            selected_index: int = self.lender_combobox.currentIndex()
            enable = (mot_expired and selected_index < 0) or not mot_expired
        self.toggle_buttons(enable)
        return enable

    def update_mot(self):
        self.year = self.year_spinner.value()
        self.month = self.month_combobox.currentIndex() + 1

    def update_lender_id(self):
        index = self.lender_combobox.currentIndex()
        selected_id = self.lender_combobox.model().index(index, 1).data()
        self.lender_id = selected_id

    def clear_fields(self):
        self.name_edit.setText("")
        self.category_edit.setText("")
        self.available_checkbox.setChecked(False)
        self.mot_checkbox.setChecked(False)
        self.info_edit.insertPlainText("")
        self.toggle_buttons(False, False)
        self.lender_combobox.setCurrentIndex(-1)


class InventoryWidget(TableDialog):

    def __init__(self):
        super(InventoryWidget, self).__init__()
        self.add_dialog = AddInventoryDialog(self)
        self.setup_table(InventoryModel(), range(1, 7))

        tableview: QTableView = self.get_table()
        delegate: InventoryItemDelegate = InventoryItemDelegate()
        tableview.setItemDelegate(delegate)

    def get_editor_widget(self) -> EditorWidget:
        return InventoryEditorWidget()

    def configure_search(self):
        self.searchLine.textChanged.connect(
            lambda x: self.reload_table_contents(InventoryModel(self.searchLine.text())))

    def configure_widgets(self):
        super().configure_widgets()
        self.editor.return_button.clicked.connect(self.return_item)

    def return_item(self):
        self.editor.lender_combobox.setCurrentIndex(-1)
        item_id = super().get_selected_item()
        check_and_return(item_id)
        search = self.searchLine.text()
        self.reload_table_contents(model=InventoryModel(search))

    def delete_item(self):
        dialog = ConfirmDeletionDialog(self)
        button = dialog.exec_()
        if button == QMessageBox.AcceptRole:
            item: InventoryItem = self.get_selected_item()
            delete_item(item)
            search = self.searchLine.text()
            self.reload_table_contents(model=InventoryModel(search))
            self.editor.clear_fields()

    def get_selected_item(self):
        item_id = super().get_selected_item()
        item = find_by_id(item_id, InventoryItem)
        return item

    def commit_changes(self):
        value_dict: dict = self.editor.get_values()
        update_inventory(value_dict)
        search = self.searchLine.text()
        self.reload_table_contents(model=InventoryModel(search))
        self.editor.clear_fields()

    def revert_changes(self):
        item: InventoryItem = find_by_id(self.editor.item_id, InventoryItem)
        self.editor.fill_fields(item)

    def reload_table_contents(self, model: SearchTableModel):
        super().reload_table_contents(model)
        self.editor.reload_lender_box()


class InventoryItemDelegate(DateItemDelegate):

    def __init__(self):
        super(InventoryItemDelegate, self).__init__()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: Union[QModelIndex, QPersistentModelIndex]):
        self.format_background(index, option, painter)

        # available
        if index.column() == 3:
            self.format_checkbox(index, option, painter)
        # lending date
        elif index.column() == 4:
            self.format_ymd(index, option, painter)
        # MOT date
        elif index.column() == 6:
            self.formal_ym(index, option, painter)
        else:
            super(InventoryItemDelegate, self).paint(painter, option, index)

    @staticmethod
    def format_background(index, option, painter):
        model = index.model()
        mot_date = model.index(index.row(), 6).data()
        if mot_date:
            calculate_background(mot_date, option, painter)

    def format_checkbox(self, index, option, painter):
        model = index.model()
        data = model.index(index.row(), index.column()).data()
        opt: QStyleOptionButton = QStyleOptionButton()
        opt.rect = option.rect
        if data:
            value = Qt.Checked
        else:
            value = Qt.Unchecked
        self.drawCheck(painter, option, option.rect, value)
        self.drawFocus(painter, option, option.rect)
