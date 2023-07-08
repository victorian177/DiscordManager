from collections import OrderedDict


class Schema:
    def __init__(self, info, primary_key) -> None:
        self.info = info
        self.primary_key = primary_key

    def check(self, input_data: dict):
        record = OrderedDict()
        for k, v in self.info.items():
            record[k] = [] if v == "list" else None

        input_keys_set = set(input_data.keys())
        schema_keys_set = set(self.info.keys())

        is_primary = self.primary_key in input_keys_set
        is_subset = input_keys_set.issubset(schema_keys_set) and len(input_keys_set) > 0

        for k, v in record.items():
            if self.info[k] == "int":
                ...
            elif self.info[k] == "str":
                ...
            elif self.info[k] == "date":
                ...
            elif self.info[k] == "list":
                ...
