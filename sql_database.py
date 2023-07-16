import json
import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_name):
        self.db_file = Path(f"db/{db_name}.sqlite")
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

        # Load the config file
        with open("config.json") as f:
            self.config = json.load(f)

        # Create all of the tables
        for table_name, schema in self.config.items():
            self._create_table(table_name, schema)

    def _create_table(self, table_name, columns):
        sql = "CREATE TABLE IF NOT EXISTS {table_name} ({columns})".format(
            table_name=table_name, columns=", ".join(columns)
        )
        # print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_row(self, table_name, values):
        sql = "INSERT OR IGNORE INTO {table_name} VALUES ({values})".format(
            table_name=table_name, values=", ".join(["?" for v in values])
        )
        self.cursor.execute(sql, values)
        self.conn.commit()

    def select_rows(self, table_name, columns=None, where=None):
        sql = "SELECT {columns} FROM {table_name}".format(
            columns=columns or "*", table_name=table_name
        )
        if where:
            sql += " WHERE {where}".format(where=where)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def update_row(self, table_name, values, where):
        sql = "UPDATE {table_name} SET {values} WHERE {where}".format(
            table_name=table_name,
            values=", ".join([f"{k}={v}" for k, v in values.items()]),
            where=where,
        )
        self.cursor.execute(sql, values)
        self.conn.commit()

    def delete_row(self, table_name, where):
        sql = "DELETE FROM {table_name} WHERE {where}".format(
            table_name=table_name, where=where
        )
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    db = Database("test")
    db.insert_row("Member", ("johnny", "John Bee", "john@email.com"))
    db.insert_row("Member", ("julie", "Juliet Han", "juliet@email.com"))
    db.insert_row("Member", ("paulo", "Paul Tea", "paul@email.com"))
    db.insert_row("Member", ("bella", "Isabella Fun", "isabella@email.com"))

    print(db.select_rows("Member"))

    db.update_row("Member", {"name": "'Paul Cae'"}, "username='paulo'")
    db.delete_row("Member", "username='bella'")

    print(db.select_rows("Member"))
