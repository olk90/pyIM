from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DatabaseExport(object):

    def __init__(self, identifier, persons, items, history):
        self.identifier = identifier
        self.persons = persons
        self.items = items
        self.history = history


class Person(Base):
    id = Column(Integer, primary_key=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(100))

    def get_full_name(self):
        return "{} {}".format(self.firstname, self.lastname)


class InventoryItem(Base):

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    available = Column(Boolean, nullable=False)
    lending_date = Column(Date)
    info = Column(String(500))
    category = Column(String(100), nullable=False)
    mot_required = Column(Boolean, nullable=False)
    next_mot = Column(Date)


class AccessRecord(object):

    def __init__(self, file_path, last_access_time):
        self.file_path = file_path
        self.last_access_time = last_access_time


class LendingHistoryRecord(object):

    def __init__(self, lender_id, item_id, lending_date="", return_date=""):
        self.lender_id = lender_id
        self.item_id = item_id
        self.lending_date = lending_date
        self.return_date = return_date
