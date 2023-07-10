import os

from members import Members
from projects import Projects


class Guild:
    def __init__(self, name) -> None:
        path = f"db/{name}"
        Guild.create_folder(path)

        self.members = Members(name)
        self.projects = Projects(name)

    @staticmethod
    def create_folder(folder_path):
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
