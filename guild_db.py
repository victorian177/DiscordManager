from sql_database import Database


class GuildDB:
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


if __name__ == "__main__":
    test_guild = GuildDB("TestGuild")
    userdata = [
        (
            "johnny",
            "John Bee",
            "johnny",
            "john@email.com",
            "Frontend",
            "CSC",
            "17/01",
            "A",
        ),
        (
            "jane",
            "Jane Smith",
            "jane123",
            "jane@email.com",
            "Backend",
            "CSC",
            "18/02",
            "B",
        ),
        (
            "peter",
            "Peter Lee",
            "peterl",
            "peter@email.com",
            "Fullstack",
            "CSE",
            "21/03",
            "A+",
        ),
        (
            "sara",
            "Sara Johnson",
            "sara.j",
            "sara@email.com",
            "Data Science",
            "ECE",
            "12/04",
            "A",
        ),
        (
            "mike",
            "Mike Brown",
            "mikeb",
            "mike@email.com",
            "Mobile Development",
            "CSC",
            "23/05",
            "B+",
        ),
        (
            "emma",
            "Emma Davis",
            "emmad",
            "emma@email.com",
            "UI/UX Design",
            "CSC",
            "14/06",
            "A-",
        ),
    ]

    for user in userdata:
        data = {"values": user}
        print(data["values"])
        test_guild.op_package("Members", "insert", data)
