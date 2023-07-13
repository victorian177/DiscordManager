import os
from pathlib import Path
from typing import Dict

from tinydb import Query

from database import Database


class GuildDatabases:
    DB_FILENAMES = ["members", "projects", "member_projects", "feedback"]

    def __init__(self, name, pending_members: list = None) -> None:
        self.filepath = Path("db")
        self.name = name
        self.pending_members = pending_members

        if not os.path.exists(self.filepath):
            os.mkdir(self.filepath)

        self.filepath = self.filepath / self.name
        if not os.path.exists(self.filepath):
            os.mkdir(self.filepath)

        self.dbs: Dict[str, Database] = {}

        for filename in self.DB_FILENAMES:
            file = f"{filename}.db"
            if not os.path.exists(self.filepath / file):
                self.dbs[filename] = Database(
                    db_name=filename,
                    db_filepath=self.filepath,
                )

    def op_package(self, db_name, op_name, data):
        retrieve_data = None

        if op_name == "create":
            self.dbs[db_name].create(*data)
        elif op_name == "modify":
            self.dbs[db_name].modify(*data)
        elif op_name == "retrieve":
            retrieve_data = self.dbs[db_name].retrieve(*data)
        elif op_name == "delete":
            self.dbs[db_name].delete(*data)

        return retrieve_data
