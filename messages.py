from tinydb import Query

from database import Database


class Messages:
    INFO = {"topic": "str", "content": "str"}
    PRIMARY_KEY = "topic"

    def __init__(self) -> None:
        self.db = Database(
            db_name=f"db/messages",
            primary_key=self.PRIMARY_KEY,
            schema_info=self.INFO,
        )

    def query(self, item):
        q = Query()[self.PRIMARY_KEY] == item

        return q

    