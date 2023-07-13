from pathlib import Path

from tinydb import TinyDB, operations


class Database:

    """A database class that provides an interface for creating, modifying,
    retrieving, and deleting records.

    Args:
        db_name: The name of the database.
        db_filepath: The path to the database file.
    """

    def __init__(self, db_name, db_filepath: Path) -> None:
        self.name = db_name
        self._filepath = db_filepath

        path = self._filepath / f"{self.name}.json"
        self.db = TinyDB(path)

    def create(self, data):
        """Creates record(s) in the database.

        Args:
            data: A record or list of records to be created in database.
        """
        if isinstance(data, dict):
            self.db.insert(data)

        elif isinstance(data, list):
            self.db.insert_multiple(data)

    def modify(self, query, modify_info):
        """Modifies a record in the database. Is inactive for Read-Only Databases

        Args:
            query: The query to use to find the record to modify.
            modify_info: A dictionary specifying key(s) and the new value(s).
        """
        for k, v in modify_info.items():
            self.db.update(operations.set(k, v), query)

    def retrieve(self, query=None, retrieve_info: list = [], unique: bool = True):
        """Retrieves a record from the database.

        Args:
            query: The query to use to find the record(s) to retrieve.
            retriever_info: A list specifying which data is to be returned.
            unique: A bool specifying whether only one record or all records with query is to be retrieved.

        Returns:
            A dictionary or list of dictionaries of the record(s) to be retrieved.
        """
        if query is not None:
            if unique:
                retrieve_data = [self.db.get(query)]
            else:
                retrieve_data = self.db.search(query)
        else:
            retrieve_data = self.db.all()

        if retrieve_info:
            retrieve_data = [
                {k: v for k, v in record.items() if k in retrieve_info}
                for record in retrieve_data
            ]

        return retrieve_data

    def delete(self, query, unique=True):
        """Deletes a record from the database.

        Args:
            query: The query to use to find the record to delete.
            unique: A bool specifying whether only one record or all records with query is to be deleted.
        """
        self.db.remove(query)

    def info(self):
        print(f"Name: {self.name}\nNumber of documents: {len(self.db)}")
        print(self.db.all())



