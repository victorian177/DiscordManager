from tinydb import Query

from database import Database


class Lists:
    INFO = {"name": "str", "information": "list"}
    PRIMARY_KEY = "name"

    def __init__(self) -> None:
        self.db = Database(
            db_name=f"db/lists",
            primary_key=self.PRIMARY_KEY,
            schema_info=self.INFO,
        )

    def query(self, item):
        q = Query()[self.PRIMARY_KEY] == item

        return q
