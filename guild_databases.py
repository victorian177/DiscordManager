import os
from pathlib import Path

from tinydb import Query

from database import Database


class GuildDatabases:
    DB_FILENAMES = ["members", "projects", "member_projects", "feedback"]

    def __init__(self, name) -> None:
        self.filepath = Path("db")
        self.name = name

        if not os.path.exists(self.filepath):
            os.mkdir(self.filepath)

        self.filepath = self.filepath / self.name
        if not os.path.exists(self.filepath):
            os.mkdir(self.filepath)

        self.dbs = {}

        for filename in self.DB_FILENAMES:
            file = f"{filename}.db"
            if not os.path.exists(self.filepath / file):
                self.dbs[filename] = Database(
                    db_name=filename,
                    db_filepath=self.filepath,
                )

if __name__ == "__main__":
    gdb = GuildDatabases("Test Server")