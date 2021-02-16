from src.domain.context import get_context
from src.entity.Tasks import Tasks
from src.entity.Entries import Entries
import src.constant.common as app_mysql_constant
from src.domain.common import MysqlExt
from src.log.logger import logger_domain
from prettytable import PrettyTable
import prettytable


def select_table_show(fields, name, id, offset, limit, order_by, group_by, having):
    SelectTableShow(
        fields=fields,
        name=name,
        id=id,
        offset=offset,
        limit=limit,
        order_by=order_by,
        group_by=group_by,
        having=having
    ).execute()


class SelectTableShow(MysqlExt):
    default_fields = 'task.*,entry.task_id,entry.sql'

    def __init__(self,
                 fields='*',
                 id=None,
                 name=None,
                 offset=None,
                 limit=None,
                 order_by=None,
                 group_by=None,
                 having=None
                 ):
        if fields == '*':
            self.fields = SelectTableShow.default_fields
        else:
            self.fields = fields
        self.id = id
        self.name = name
        self.limit = limit
        self.offset = offset
        self.order_by = order_by
        self.group_by = group_by
        self.having = having

    async def _worker(self, conn, cur):

        where = []
        if self.id is not None:
            where.append(f'`id` = {self.id}')
        if self.name is not None:
            where.append(f'`name` LIKE %{self.name}%')
        where = ' AND '.join(where)

        sql = f'select {self.fields} from {app_mysql_constant.MYSQL_DB}.{Tasks.get_table_name()} as task ' \
              f'inner join {app_mysql_constant.MYSQL_DB}.{Entries.get_table_name()} as entry on task.id = entry.task_id '
        if len(where) > 0:
            sql += f'WHERE {where} '
        if self.order_by is not None:
            sql += f'ORDER BY {self.order_by} '
        if self.limit is not None:
            sql += f'LIMIT {self.limit} '
        if self.offset is not None:
            sql += f'OFFSET {self.offset} '
        if self.group_by is not None:
            sql += f'GROUP BY {self.group_by} '
        if self.having is not None:
            sql += f'HAVING {self.having}'

        logger_domain.debug(f'[ {sql} ]')

        result = await SelectTableShow.fetch_all(cur, sql)
        tables = PrettyTable()
        tables.set_style(prettytable.DEFAULT)
        tables.field_names = SelectTableShow.get_fields(cur)
        tables.padding_width = 5
        tables.align['path'] = 'l'

        for item in result:
            row = []
            for k, v in item.items():
                row.append(v)

            tables.add_row(row)

        print(tables.get_string())

    def execute(self):
        get_context().mysql_pool.execute(self._worker)
