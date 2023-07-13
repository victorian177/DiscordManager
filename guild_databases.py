import os
from pathlib import Path
from typing import Dict

from tinydb import Query

from database import Database


class GuildDatabases:
    DB_FILENAMES = [
        "members",
        "projects",
        "member_projects",
        "feedback",
        "project_drafts",
    ]

    def __init__(self, name, pending_members: list = []) -> None:
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
            self.dbs[filename] = Database(
                db_name=filename,
                db_filepath=self.filepath,
            )

    def op_package(self, db_name, op_name, data):
        retrieve_data = None

        if op_name == "create":
            self.dbs[db_name].create(data)
        elif op_name == "modify":
            self.dbs[db_name].modify(
                query=data["query"],
                modify_info=data["modify_info"],
            )
        elif op_name == "retrieve":
            retrieve_data = self.dbs[db_name].retrieve(
                query=data["query"],
                retrieve_info=data["retrieve_info"],
                unique=data["unique"],
            )
        elif op_name == "delete":
            self.dbs[db_name].delete(
                query=data["query"],
                unique=data["unique"],
            )

        return retrieve_data
