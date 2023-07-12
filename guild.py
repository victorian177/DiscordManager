from pathlib import Path


class Guild:
    def __init__(self, name) -> None:
        self._name = name
        self.members = None
        self.projects = None
