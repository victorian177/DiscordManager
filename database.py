from collections import OrderedDict
from pathlib import Path

from BetterJSONStorage import BetterJSONStorage
from tinydb import Query, TinyDB, operations


class Database:
    def __init__(self, db_name) -> None:
        self.path = Path(f"db/{db_name}.db")
        self.primary_key = primary_key

        db = TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage)
        db.close()

    def get_count(self):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            count = len(db)

        return count

    def create(self, record: dict):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            db.insert(record)

    def delete(self, query):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            data = db.remove(query)

        return data

    def modify(self, query, update_info):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            data = db.update(operations.set(update_info[0], update_info[1]), query)

        return data

    def retrieve(self, query):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            data = db.get(query)

        return data


if __name__ == "__main__":
    from schema import Schema

    info = {
        "name": "str",
        "nickname": "str",
        "specialisation": "str",
        "email": "email",
        "date_joined": "date",
        "cohort": "str",
        "teams": "list",
        "personal_projects": "list",
        "projects_done": "list",
        "projects_undertaking": "list",
    }
    primary_key = "nickname"

    schema = Schema(info, primary_key)
    database = Database("test_db")

    correct_record = {
        "name": "john",
        "nickname": "johnny_0",
        "email": "john@email.com",
        "date_joined": "01/2001",
    }

    incorrect_record = {
        "name": "john",
        "nickname": "johnny_0",
        "email": "john@email.com",
        "date_joined": "01/2001",
        "song": "last last",
    }

    result = schema.check(correct_record) is not None
    print(f"A result was gotten? {result}")

    

    result = schema.check(incorrect_record) is not None
    print(f"A result was gotten? {result}")
