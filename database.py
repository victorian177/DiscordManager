from collections import OrderedDict
from pathlib import Path

from BetterJSONStorage import BetterJSONStorage
from tinydb import Query, TinyDB, operations

from schema import Schema


class Database:
    def __init__(self, db_name, primary_key, schema_info) -> None:
        self.path = Path(f"{db_name}.db")
        self.primary_key = primary_key
        self.schema = Schema(schema_info, primary_key)

        db = TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage)
        db.close()

    def get_count(self):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            print()
            print(db.all())
            print(f"Count: {len(db)}")
            print()

    def create(self, input_data: dict):
        record = self.schema.check(input_data)
        if record is not None:
            with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
                db.insert(record)

    def delete(self, query):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            data = db.remove(query)

        return data

    def modify(self, query, update_data):
        record = self.schema.check(update_data)
        if record is not None:
            with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
                for key, value in update_data.items():
                    db.update(operations.set(key, value), query)

    def retrieve(self, query):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            data = db.get(query)

        return data


if __name__ == "__main__":
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

    database = Database("test_db", primary_key, info)

    correct_record = {
        "name": "john",
        "nickname": "johnny_0",
        "email": "john@email.com",
        "date_joined": "01/2001",
    }

    incorrect_record = {
        "name": "john",
        "nickname": "johnny_1",
        "email": "john@email.com",
        "date_joined": "01/2001",
        "song": "last last",
    }

    print("Correct")
    database.create(correct_record)
    database.get_count()

    print("Incorrect")
    database.create(incorrect_record)
    database.get_count()

    print("Update")
    database.modify(
        query=Query()["nickname"] == "johnny_0",
        update_data={"name": "peter", "email": "peter@gmail.com"},
    )
    database.get_count()

    print("Retrieve")
    print(database.retrieve(query=Query()["nickname"] == "johnny_0"))

    print("Delete")
    database.delete(Query()["nickname"] == "johnny_0")
    database.get_count()
