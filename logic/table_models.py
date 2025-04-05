from PySide6.QtCore import QAbstractTableModel, QModelIndex
from PySide6.QtGui import Qt

from logic.config import properties
from logic.crypt import decrypt_string
from logic.database import find_all_of, find_by_id
from logic.model import Person, InventoryItem, LendingHistory
from views.helpers import filter_by_search


class SearchTableModel(QAbstractTableModel):
    def __init__(self, col_count, search: str = "", items=None):
        super(SearchTableModel, self).__init__()
        self.col_count = col_count
        self.search = search.lower()  # Normalize to lowercase for easier matching
        if items is None:
            items = []
        self.all_items = items  # Store full, unfiltered list of items
        self.items = self.filter_items()  # Start with filtered list

    def set_search(self, search: str):
        """Update the search string and reapply filtering."""
        self.search = search.lower()
        self.items = self.filter_items()
        self.layoutChanged.emit()  # Notify the view that the data has changed

    def filter_items(self):
        """Filter items based on the search string. Must be implemented by subclasses."""
        return self.all_items

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        return self.col_count

    def data(self, index, role=Qt.DisplayRole):
        """Must be implemented by subclass."""
        pass

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Must be implemented by subclass."""
        pass


class PersonModel(SearchTableModel):
    def __init__(self, search: str = ""):
        items = find_all_of(Person)
        super(PersonModel, self).__init__(4, search, items)

    def filter_items(self):
        """Filter persons based on the search string."""
        if not self.search:
            return self.all_items  # No search; return all items

        key = properties.encryption_key
        # Normalize search value to lowercase for case-insensitive matching
        search_lower = self.search
        filtered = []
        for person in self.all_items:
            # Decrypt fields when necessary and match them against the search string
            first_name = decrypt_string(key, person.firstname).lower() if key else person.firstname.lower()
            last_name = decrypt_string(key, person.lastname).lower() if key else person.lastname.lower()
            email = decrypt_string(key, person.email).lower() if key and person.email else person.email.lower()

            if (search_lower in first_name or
                    search_lower in last_name or
                    (email and search_lower in email)):
                filtered.append(person)

        return filtered

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            person: Person = self.items[index.row()]
            column = index.column()
            key = properties.encryption_key
            if column == 0:
                return person.id
            elif column == 1:
                if key is not None:
                    return decrypt_string(key, person.firstname)
                else:
                    return person.firstname
            elif column == 2:
                if key is not None:
                    return decrypt_string(key, person.lastname)
                else:
                    return person.lastname
            elif column == 3:
                email = person.email
                if key is not None and email is not None:
                    return decrypt_string(key, email)
                else:
                    return email
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return "ID"
            elif section == 1:
                return self.tr("First Name")
            elif section == 2:
                return self.tr("Last Name")
            elif section == 3:
                return self.tr("E-Mail")
        return None


class InventoryModel(SearchTableModel):
    def __init__(self, search: str = ""):
        items = find_all_of(InventoryItem)
        super(InventoryModel, self).__init__(7, search, items)

    def filter_items(self):
        """Filter inventory items based on the search string."""
        return filter_by_search(
            all_items=self.all_items,
            search=self.search,
            key=properties.encryption_key,
            fields=("category", "name", "lender")
        )

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            item: InventoryItem = self.items[index.row()]
            column = index.column()
            key = properties.encryption_key
            if column == 0:
                return item.id
            elif column == 1:
                return item.category
            elif column == 2:
                return item.name
            elif column == 3:
                return item.available
            elif column == 4:
                return item.lending_date
            elif column == 5:
                lender: Person = find_by_id(item.lender_id, Person)
                if lender:
                    return lender.get_full_name()
            elif column == 6:
                return item.next_mot
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return "ID"
            elif section == 1:
                return self.tr("Category")
            elif section == 2:
                return self.tr("Name")
            elif section == 3:
                return self.tr("Available")
            elif section == 4:
                return self.tr("Lending Date")
            elif section == 5:
                return self.tr("Lender")
            elif section == 6:
                return self.tr("Next Mot")
        return None



class LendingHistoryModel(SearchTableModel):
    def __init__(self, search: str = ""):
        items = find_all_of(LendingHistory)
        super(LendingHistoryModel, self).__init__(5, search, items)

    def filter_items(self):
        """Filter lending history based on the search string."""
        return filter_by_search(
            all_items=self.all_items,
            search=self.search,
            key=properties.encryption_key,
            fields=("item_name", "lender_name")  # Specify item name and lender name fields
        )

    def data(self, index, role=Qt.DisplayRole):

        if role == Qt.DisplayRole:
            item: LendingHistory = self.items[index.row()]
            column = index.column()
            key = properties.encryption_key
            if column == 0:
                return item.id
            elif column == 1:
                return item.item.name
            elif column == 2:
                return item.lender.get_full_name()
            elif column == 3:
                return item.lending_date
            elif column == 4:
                return item.return_date
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return "ID"
            elif section == 1:
                return self.tr("Item Name")
            elif section == 2:
                return self.tr("Lender")
            elif section == 3:
                return self.tr("Lending Date")
            elif section == 4:
                return self.tr("Return Date")
            return None
