from database import Database
from tinydb import Query


class Members:
    INFO = {
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
    PRIMARY_KEY = "nickname"

    def __init__(self, name) -> None:
        path = f"db/{name}"
        self.db = Database(
            db_name=f"{path}/members",
            primary_key=self.PRIMARY_KEY,
            schema_info=self.INFO,
        )

    def query(self, key):
        q = Query()[self.PRIMARY_KEY] == key

        return q
