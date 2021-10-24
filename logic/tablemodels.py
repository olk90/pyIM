from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlTableModel, QSqlQuery


class InventoryTableModel(QSqlTableModel):

    def __init__(self, *args, **kwargs):
        QSqlTableModel.__init__(self, *args, **kwargs)

    def setQuery(self, query_str: str) -> None:
        query = QSqlQuery(query_str)
        super().setQuery(query)

    def flags(self, index) -> Qt.ItemFlags:
        if self.headerData(index.column(), Qt.Horizontal) in ("Available", "Console", "Accessory",
                                                              "Box", "Manual"):
            return Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            return super().flags(index)
