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
        is_subset = input_keys_set.issubset(schema_keys_set)

        if is_primary and is_subset:
            for k, v in record.items():
                if self.info[k] == "int":
                    if v.isdigit():
                        record[k] = v
                elif self.info[k] == "date":
                    if "/" in v:
                        record[k] = v
                elif self.info[k] == "list":
                    record[k].append(v)
                else:
                    record[k] = v

            return record
        return
