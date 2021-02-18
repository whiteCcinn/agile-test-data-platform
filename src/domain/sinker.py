from abc import ABCMeta, abstractmethod
from src.domain.context import get_context
from src.log.logger import logger_domain
import datetime
import src.constant.common as app_mysql_constant
from src.entity.Tasks import Tasks
from src.entity.Entries import Entries
from src.util.func import now
from pymysql.err import IntegrityError
import pymysql
from src.log.error import SinkerError, SINKER_ERROR_EXIST_MSG
from src.domain.common import MysqlExt


class ISinker(metaclass=ABCMeta):

    def __init__(self):
        self.task = None

    @abstractmethod
    def sink(self):
        pass


class FileSinker(ISinker):
    def __init__(self, task):
        self.task = task

    def sink(self):
        get_context().get_sinker_mysql().execute(self._sink)

    async def _sink(self, conn, cur):
        await cur.execute("show databases;")
        one = await cur.fetchall()
        print(one)


class MysqlSinker(ISinker, MysqlExt):
    def __init__(self, task):
        self.task = task

    def sink(self):
        get_context().get_sinker_mysql().execute(self._sink)

    async def _sink(self, conn, cur):
        # 查看是否有重复的task
        sql = f'SELECT * FROM {app_mysql_constant.MYSQL_DB}.{Tasks.get_table_name()} WHERE `identify` = \'{self.task.scenario.identify}\''
        logger_domain.debug(f'[ {sql} ]')
        data = await MysqlSinker.fetch_one(cur, sql)
        if data is not None:
            e = SinkerError(f'{SINKER_ERROR_EXIST_MSG} : {self.task}')
            logger_domain.fatal(e)
            raise e

        # 记录信息
        sql = f'INSERT INTO {app_mysql_constant.MYSQL_DB}.{Tasks.get_table_name()} ({Tasks.get_insert_fields_str()}) VALUES ({Tasks.get_s_chart()})'
        insert_args = (
            self.task.scenario.identify,
            self.task.scenario.name,
            self.task.scenario.identify_ref,
            now()
        )
        task: Tasks
        try:
            await cur.execute(sql, insert_args)
            await conn.commit()
            task = Tasks.new_instance(insert_args)
            task.id = cur.lastrowid
        except IntegrityError as e:
            logger_domain.fatal(e)
            raise e

        # 查看对应的数据
        where_condition = ' and '.join(self.task.meta.uniq_key)
        sql = f'SELECT * FROM {self.task.meta.table} WHERE {where_condition}'
        logger_domain.debug(f'[ {sql} ]')
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
        self.task.entries = data

        # 记录数据
        insert_data = []
        for d in data:
            v = []
            for dd in d:
                if isinstance(dd, int):
                    v.append(str(dd))
                elif dd is None:
                    v.append('NULL')
                else:
                    v.append("\"%s\"" % dd)
            insert_data.append('(' + ','.join(v) + ')')

        insert_fields = [f'`{field}`' for field in fields]
        insert_fields = ','.join(insert_fields)
        insert_values = ','.join(insert_data)
        save_insert_sql = f'INSERT INTO {self.task.meta.table} ({insert_fields}) VALUES {insert_values}'
        logger_domain.debug(f'[ {save_insert_sql} ]')
        sql = f'INSERT INTO {app_mysql_constant.MYSQL_DB}.{Entries.get_table_name()} ({Entries.get_insert_fields_str()}) VALUES ({Entries.get_s_chart()})'
        insert_args = (
            task.id,
            save_insert_sql
        )
        try:
            await cur.execute(sql, insert_args)
            await conn.commit()
        except IntegrityError as e:
            logger_domain.fatal(e)
            raise e
