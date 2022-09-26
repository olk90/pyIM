from PySide6.QtSql import QSqlQueryModel


class SearchTableModel(QSqlQueryModel):
    def __init__(self, search: str = ""):
        super(SearchTableModel, self).__init__()
        self.search = search
