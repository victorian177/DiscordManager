from database import Database
from tinydb import Query


class Templates:
    INFO = {"type": "str", "link": "str"}
    PRIMARY_KEY = "topic"

    def __init__(self) -> None:
        self.db = Database(
            db_name=f"db/templates",
            primary_key=self.PRIMARY_KEY,
            schema_info=self.INFO,
        )

    def query(self, item):
        q = Query()[self.PRIMARY_KEY] == item

        return q

    