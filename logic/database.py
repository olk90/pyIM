import sys

from PySide6.QtGui import Qt
from sqlalchemy.orm import Session

from PySide6.QtSql import QSqlDatabase, QSqlQueryModel
from sqlalchemy import create_engine as ce

from logic.model import create_tables, Person, InventoryItem
from logic.queries import personQuery, inventoryQuery

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


def configure_person_model():
    model = QSqlQueryModel()
    model.setQuery(personQuery)
    model.setHeaderData(0, Qt.Horizontal, "First Name")
    model.setHeaderData(1, Qt.Horizontal, "Last Name")
    model.setHeaderData(2, Qt.Horizontal, "E-Mail")
    return model


def configure_inventory_model():
    model = QSqlQueryModel()
    model.setQuery(inventoryQuery)
    model.setHeaderData(0, Qt.Horizontal, "Device")
    model.setHeaderData(1, Qt.Horizontal, "Category")
    model.setHeaderData(2, Qt.Horizontal, "Available")
    model.setHeaderData(3, Qt.Horizontal, "Lending Date")
    model.setHeaderData(4, Qt.Horizontal, "Lend to")
    model.setHeaderData(5, Qt.Horizontal, "Next MOT")
    return model


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
                lending_date=i["lendingDate"],
                lender_id=i["lender"],
                info=i["info"],
                category=i["category"],
                mot_required=i["motRequired"],
                next_mot=i["nextMot"]
            )
            session.add(inventory_item)
        session.commit()
