import sys
from sqlalchemy.orm import Session

from PySide6.QtSql import QSqlDatabase
from sqlalchemy import create_engine as ce

from logic.model import create_tables, Person

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
