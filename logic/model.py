
class DataContainer(object):

    def __init__(self, identifier, persons, items, history):
        self.identifier = identifier
        self.persons = persons
        self.items = items
        self.history = history


class Person(object):

    def __init__(self, firstname="", lastname="", email=""):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

    def get_full_name(self):
        return "{} {}".format(self.firstname, self.lastname)


class InventoryItem(object):

    def __init__(self, name="", available=False, lending_date="", info="", category="", mot_required=True, next_mot=""):
        self.name = name
        self.available = available
        self.lending_date = lending_date
        self.info = info
        self.category = category
        self.mot_required = mot_required
        self.next_mot = next_mot


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
