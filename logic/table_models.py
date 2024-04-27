from PySide6.QtCore import QAbstractTableModel, QModelIndex
from PySide6.QtGui import Qt

from logic.config import properties
from logic.crypt import decrypt_string
from logic.database import find_all_off
from logic.model import Person


class SearchTableModel(QAbstractTableModel):
    def __init__(self, col_count, search: str = "", items=None):
        super(SearchTableModel, self).__init__()
        self.col_count = col_count
        self.search = search
        if items is None:
            items = []
        self.items = items

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        return self.col_count

    def data(self, index, role=Qt.DisplayRole):
        """Must be implemented by subclass"""
        pass

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Must be implemented by subclass"""
        pass


class PersonModel(SearchTableModel):
    def __init__(self, search: str = ""):
        super(PersonModel, self).__init__(search)
        query = person_query(self.search)
        self.setQuery(query)
        self.setHeaderData(0, Qt.Horizontal, "ID")
        self.setHeaderData(1, Qt.Horizontal, self.tr("First Name"))
        self.setHeaderData(2, Qt.Horizontal, self.tr("Last Name"))
        self.setHeaderData(3, Qt.Horizontal, self.tr("E-Mail"))


class InventoryModel(SearchTableModel):
    def __init__(self, search: str = ""):
        super(InventoryModel, self).__init__(search)
        query = inventory_query(self.search)
        self.setQuery(query)
        self.setHeaderData(0, Qt.Horizontal, "ID")
        self.setHeaderData(1, Qt.Horizontal, self.tr("Category"))
        self.setHeaderData(2, Qt.Horizontal, self.tr("Device"))
        self.setHeaderData(3, Qt.Horizontal, self.tr("Available"))
        self.setHeaderData(4, Qt.Horizontal, self.tr("Lending Date"))
        self.setHeaderData(5, Qt.Horizontal, self.tr("Lend to"))
        self.setHeaderData(6, Qt.Horizontal, self.tr("Next MOT"))


class LendingHistoryModel(SearchTableModel):
    def __init__(self, search: str =""):
        super(LendingHistoryModel, self).__init__(search)
        query = lending_history_query(search)
        self.setQuery(query)
        self.setHeaderData(0, Qt.Horizontal, "ID")
        self.setHeaderData(1, Qt.Horizontal, self.tr("Device"))
        self.setHeaderData(2, Qt.Horizontal, self.tr("Lent to"))
        self.setHeaderData(3, Qt.Horizontal, self.tr("Lending Date"))
        self.setHeaderData(4, Qt.Horizontal, self.tr("Return Date"))
