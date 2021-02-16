import datetime


class MysqlExt:
    @staticmethod
    async def fetch_all(cur, sql):
        await cur.execute(sql)
        fields = MysqlExt.get_fields(cur)
        rets = await cur.fetchall()
        data = []
        for ret in rets:
            internal_data = []
            for r in ret:
                if isinstance(r, datetime.date):
                    r = r.isoformat()
                internal_data.append(r)
            data.append(internal_data)
        result = [dict(zip(fields, ret)) for ret in data]
        result = tuple(result)
        return result

    @staticmethod
    async def fetch_one(cur, sql):
        await cur.execute(sql)
        fields = MysqlExt.get_fields(cur)
        rets = await cur.fetchone()
        data = []
        if rets is None:
            return None
        for value in rets:
            if isinstance(value, datetime.date):
                value = value.isoformat()
            data.append(value)
        result = dict(zip(fields, data))
        return result

    @staticmethod
    def get_fields(cur):
        fields = [desc[0] for desc in cur.description]
        return fields
