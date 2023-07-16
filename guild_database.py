from sql_database import Database


class GuildDatabase:
    def __init__(self, name) -> None:
        self.db = Database(name)

    def op_package(self, table_name, op_name, data):
        if op_name == "insert":
            self.db.insert_row(table_name=table_name, values=data["values"])

        elif op_name == "update":
            self.db.update_row(
                table_name=table_name,
                values=data["values"],
                where=data["where"],
            )

        elif op_name == "select":
            return self.db.select_rows(
                table_name=table_name,
                columns=data["columns"],
                where=data["where"],
            )

        elif op_name == "delete":
            self.db.delete_row(table_name=table_name, where=data["where"])

        return
    
    def close(self):
        self.db.close()


if __name__ == "__main__":
    test_guild = GuildDatabase("TestGuild")
    print(
        test_guild.op_package(
            "Members",
            "select",
            {"columns": "username", "where": "university_department='CSC'"},
        )
    )
    print(
        test_guild.op_package(
            "Members",
            "select",
            {"columns": "username, name", "where": "username='nicki'"},
        )
    )
