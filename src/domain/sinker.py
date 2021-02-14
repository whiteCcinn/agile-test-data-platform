from abc import ABCMeta, abstractmethod
from src.domain.context import get_context
import datetime
import json


class ISinker(metaclass=ABCMeta):
    @abstractmethod
    def sink(self):
        pass


class FileSinker(ISinker):
    def __init__(self, task):
        self.task = task

    def sink(self):
        get_context().mysql_pool.execute(self._sink)

    async def _sink(self, cur):
        await cur.execute("show databases;")
        one = await cur.fetchall()
        print(one)


class MysqlSinker(ISinker):
    def __init__(self, task):
        self.task = task

    def sink(self):
        get_context().mysql_pool.execute(self._sink)

    async def _sink(self, cur):
        where_condition = ' and '.join(self.task.meta.uniq_key)
        sql = f'select * from {self.task.meta.table} where {where_condition}'
        print(sql)
        await cur.execute(sql)
        fields = [desc[0] for desc in cur.description]
        rets = await cur.fetchall()
        data = []
        for ret in rets:
            internal_data = []
            for r in ret:
                if isinstance(r, datetime.date):
                    r = r.isoformat()
                internal_data.append(r)
            data.append(internal_data)
        # data = tuple(data)
        insert_data = []
        print(data)
        for d in data:
            v = []
            for dd in d:
                if isinstance(dd, int):
                    v.append(str(dd))
                else:
                    v.append("\"%s\"" % dd)
            insert_data.append('(' + ','.join(v) + ')')

        insert_fields = [f'`{field}`' for field in fields]
        insert_fields = ','.join(insert_fields)
        insert_values = ','.join(insert_data)
        insert_sql = f'INSERT INTO {self.task.meta.table} ({insert_fields}) VALUES {insert_values}'
        print(insert_sql)
        #
        # result = [dict(zip(fields, ret)) for ret in data]
        # result = tuple(result)
        # print(result)
