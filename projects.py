from tinydb import Query

from database import Database


class Projects:
    INFO = {
        "name": "str",
        "description": "str",
        "project_lead": "str",
        "teams": "list",
        "members": "list",
        "project_management": "str",
    }
    PRIMARY_KEY = "name"

    def __init__(self, name) -> None:
        path = f"db/{name}"
        self.db = Database(
            db_name=f"{path}/projects",
            primary_key=self.PRIMARY_KEY,
            schema_info=self.INFO,
        )

    def query(self, item):
        q = Query()[self.PRIMARY_KEY] == item

        return q
