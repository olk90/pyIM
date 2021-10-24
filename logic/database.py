import sys
from datetime import datetime

from PySide6.QtGui import Qt
from PySide6.QtSql import QSqlDatabase, QSqlQueryModel
from sqlalchemy import create_engine as ce
from sqlalchemy.orm import Session

from logic.model import create_tables, Person, InventoryItem
from logic.queries import personQuery, inventoryQuery
from logic.tablemodels import InventoryTableModel

db = ce("sqlite:///pyIM.db")


def init_database():
    print("Connecting to database {}".format(db))
    db.connect()

    print("Initializing database")
    create_tables(db)

    print("Connect database to PySide")
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName("pyIM.db")

    if not database.open():
        print("Unable to open database")
        sys.exit(1)


def configure_person_model() -> QSqlQueryModel:
    model = QSqlQueryModel()
    model.setQuery(personQuery)
    model.setHeaderData(0, Qt.Horizontal, "First Name")
    model.setHeaderData(1, Qt.Horizontal, "Last Name")
    model.setHeaderData(2, Qt.Horizontal, "E-Mail")
    return model


def configure_inventory_model() -> InventoryTableModel:
    model = InventoryTableModel()
    model.setQuery(inventoryQuery)
    model.setHeaderData(0, Qt.Horizontal, "Device")
    model.setHeaderData(1, Qt.Horizontal, "Category")
    model.setHeaderData(2, Qt.Horizontal, "Available")
    model.setHeaderData(3, Qt.Horizontal, "Lending Date")
    model.setHeaderData(4, Qt.Horizontal, "Lend to")
    model.setHeaderData(5, Qt.Horizontal, "Next MOT")
    return model


def find_inventory_by_name(name: str) -> InventoryItem:
    with Session(db) as session:
        return session.query(InventoryItem).filter(InventoryItem.name == name).one()


def load_persons(persons):
    with Session(db) as session:
        for p in persons:
            person = Person(
                id=p["id"] + 1,
                firstname=p["firstName"],
                lastname=p["lastName"],
                email=p["email"]
            )
            session.add(person)
        session.commit()


def load_inventory(inventory):
    with Session(db) as session:
        for i in inventory:
            inventory_item = InventoryItem(
                id=i["id"] + 1,
                name=i["name"],
                available=i["available"],
                lending_date=convert_date(i["lendingDate"]),
                lender_id=i["lender"],
                info=i["info"],
                category=i["category"],
                mot_required=i["motRequired"],
                next_mot=convert_date(i["nextMot"])
            )
            session.add(inventory_item)
        session.commit()


def convert_date(date_str: str):
    date_pattern = "%Y-%m-%d"
    if len(date_str) > 0:
        return datetime.strptime(date_str, date_pattern)
    else:
        return None
