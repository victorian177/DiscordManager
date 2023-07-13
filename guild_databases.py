import os
from pathlib import Path

from tinydb import Query

from database import Database


class GuildDatabases:
    def __init__(self, name) -> None:
        self.filepath = Path("db")
        self.name = name

        if not os.path.exists(self.filepath):
            os.mkdir(self.filepath)

        self.filepath = self.filepath / self.name
        if not os.path.exists(self.filepath):
            os.mkdir(self.filepath)

        if not os.path.exists(self.filepath / "members"):
            self.members = Database(db_name="members", db_filepath=self.filepath)
            self.projects = Database(db_name="projects", db_filepath=self.filepath)
            self.feedback = Database(db_name="feedback", db_filepath=self.filepath)
