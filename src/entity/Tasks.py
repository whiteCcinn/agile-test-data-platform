tbl_name = 'tasks'


class Tasks:
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
            'identify',
            'name',
            'identify_ref',
            'created_time'
        ]

    @staticmethod
    def get_insert_fields_str():
        fields = [f'`{field}`' for field in Tasks.get_insert_fields()]
        return ','.join(fields)

    @staticmethod
    def get_insert_fields_num():
        return len(Tasks.get_insert_fields())

    @staticmethod
    def get_s_chart():
        data = []
        i = Tasks.get_insert_fields_num()
        while i > 0:
            data.append("%s")
            i = i - 1

        return ','.join(data)

    @staticmethod
    def new_instance(data):
        if len(data) != len(Tasks.get_insert_fields()):
            return None
        obj = Tasks()
        for i, field in enumerate(Tasks.get_insert_fields()):
            setattr(obj, field, data[i])

        return obj
