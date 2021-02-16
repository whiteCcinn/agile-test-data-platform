tbl_name = 'entries'


class Entries:
    id: int = None
    identify: str = None
    name: str = None
    identify_ref: str = None
    created_time: int = None

    @staticmethod
    def get_table_name():
        global tbl_name
        return tbl_name

    @staticmethod
    def get_insert_fields():
        return [
            'task_id',
            'sql',
        ]

    @staticmethod
    def get_insert_fields_str():
        fields = [f'`{field}`' for field in Entries.get_insert_fields()]
        return ','.join(fields)

    @staticmethod
    def get_insert_fields_num():
        return len(Entries.get_insert_fields())

    @staticmethod
    def get_s_chart():
        data = []
        i = Entries.get_insert_fields_num()
        while i > 0:
            data.append("%s")
            i = i - 1

        return ','.join(data)

    @staticmethod
    def new_instance(data):
        if len(data) != len(Entries.get_insert_fields()):
            return None
        obj = Entries()
        for i, field in Entries.get_insert_fields():
            setattr(obj, field, data[i])

        return obj
