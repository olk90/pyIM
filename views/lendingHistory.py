from typing import Union

from PySide6.QtCore import QModelIndex, QPersistentModelIndex
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QStyleOptionViewItem, QTableView

from logic.table_models import LendingHistoryModel
from views.base_classes import TableDialog, EditorWidget, DateItemDelegate


class LendingHistoryWidget(TableDialog):

    def __init__(self):
        super(LendingHistoryWidget, self).__init__(has_editor=False)
        self.setup_table(LendingHistoryModel(), range(1, 5))

        tableview: QTableView = self.get_table()
        delegate: LendingHistoryItemDelegate = LendingHistoryItemDelegate()
        tableview.setItemDelegate(delegate)

    def get_editor_widget(self) -> EditorWidget:
        return EditorWidget("")

    def configure_search(self):
        self.searchLine.textChanged.connect(
            lambda x: self.reload_table_contents(LendingHistoryModel(self.searchLine.text())))


class LendingHistoryItemDelegate(DateItemDelegate):

    def __init__(self):
        super(LendingHistoryItemDelegate, self).__init__()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: Union[QModelIndex, QPersistentModelIndex]):
        if index.column() in [3, 4]:
            self.format_ymd(index, option, painter)
        else:
            super(LendingHistoryItemDelegate, self).paint(painter, option, index)
