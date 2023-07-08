from collections import OrderedDict
from pathlib import Path

from BetterJSONStorage import BetterJSONStorage
from tinydb import Query, TinyDB, operations


class Database:
    def __init__(
        self, db_name, primary_key, schema: OrderedDict, checklist: list = []
    ) -> None:
        self.path = Path(f"db/{db_name}.db")
        self.primary_key = primary_key
        self.schema = schema
        self.checklist = checklist

        db = TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage)
        db.close()

    def get_count(self):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            count = len(db)

        return count

    def create(self, record: dict):
        data = OrderedDict()
        for k, v in self.schema.items():
            data[k] = [] if v == "list" else None

        record_keys_set = set(record.keys())
        schema_keys_set = set(self.schema.keys())

        is_primary = self.primary_key in record_keys_set
        is_subset = (
            record_keys_set.issubset(schema_keys_set) and len(record_keys_set) > 0
        )

        if is_primary and is_subset:
            for k, v in record.items():
                if self.schema[k] == "list":
                    data[k].append(v)
                else:
                    data[k] = v
            with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
                db.insert(data)
            print(f"Inserted: {data}")
        else:
            print(f"Primary key: {is_primary}")
            print(f"Subset: {is_subset}")

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

    def checker(self, query=None, all=False):
        data = None
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            if all:
                data = db.all()
            else:
                data = db.get(query)

        for datum in data:
            ...


if __name__ == "__main__":
    schema = {
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
    database = Database("test_db", primary_key=primary_key, schema=schema)

    for i in range(5):
        database.create(
            record={
                "name": "john",
                "nickname": f"johnny_{i}",
                "email": "john@email.com",
                "date_joined": "01/2001",
            }
        )

    print(f"Created {database.get_count()} records.")

    User = Query()

    del_query = User.nickname == "johnny_4"
    print(f"Deleted: {database.delete(del_query)}")
    print(f"Count is now {database.get_count()}.")

    mod_query = User.nickname == "johnny_0"
    update_info = ("date_joined", "99/9999")
    print(f"Modified: {database.modify(mod_query, update_info)}")

    ret_query = User.nickname == "johnny_0"
    print(f"Retrieved: {database.retrieve(ret_query)}")
