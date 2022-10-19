import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

from PySide6.QtSql import QSqlDatabase
from sqlalchemy import create_engine as ce
from sqlalchemy.orm import Session

from logic import configure_file_handler
from logic.config import properties
from logic.model import create_tables, Person, InventoryItem, Base

db = ce("sqlite:///pyIM.db")

rfh: RotatingFileHandler = configure_file_handler("database")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(rfh)

logger.info("Logger initialised")


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


def find_by_id(identifier: int, entities):
    s = properties.open_session()
    result = s.query(entities).filter_by(id=identifier).first()
    s.close()
    return result


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


def persist_item(item: Base):
    s = properties.open_session()
    s.add(item)
    s.commit()
    logger.info("Added new item to database: %s", item)


def delete_item(item: Base):
    s = properties.open_session()
    s.delete(item)
    s.commit()
    logger.info("Removed entry from database: %s", item)


def update_person(value_dict: dict):
    s = properties.open_session()
    person: Person = s.query(Person).filter_by(id=value_dict["item_id"]).first()
    person.firstname = value_dict["firstname"]
    person.lastname = value_dict["lastname"]
    person.email = value_dict["email"]
    s.commit()


def update_inventory(value_dict: dict):
    s = properties.open_session()
    item: InventoryItem = s.query(InventoryItem).filter_by(id=value_dict["item_id"]).first()
    item.name = value_dict["name"]
    item.category = value_dict["category"]
    item.info = value_dict["info"]
    item.mot_required = value_dict["mot_required"]
    item.next_mot = value_dict["next_mot"]
    item.available = value_dict["available"]
    s.commit()
