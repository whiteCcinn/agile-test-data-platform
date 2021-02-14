import logging
from src.log.error import MetaInitError, TaskError
from src.util.func import md5
from src.constant.domain import FILE_SINK_TYPE, MYSQL_SINK_TYPE
from src.domain.sinker import MysqlSinker, FileSinker


class Task:
    def __init__(self, meta=None, scenario=None, entries=[], sink_type=MYSQL_SINK_TYPE):
        self.meta = meta
        self.scenario = scenario
        self.entries = entries
        self.sink_type = sink_type
        if self.sink_type == MYSQL_SINK_TYPE:
            self.sinker = MysqlSinker(self)
        elif self.sink_type == FILE_SINK_TYPE:
            self.sinker = FileSinker(self)
        else:
            raise TaskError(f'task init failed: f{self}')

    def __repr__(self):
        return f"Task(meta={self.meta}," \
               f"scenario={self.scenario}," \
               f"sink_type={self.sink_type}," \
               f"entries={self.entries})"

    __str__ = __repr__


class Meta:
    def __init__(self, table, uniq_key):
        self.table = table
        if isinstance(uniq_key, str):
            self.uniq_key = uniq_key.split(',')
        elif isinstance(uniq_key, list):
            self.uniq_key = uniq_key
        else:
            logging.error(f'Meta uniq_key is unSupport {uniq_key}')
            raise MetaInitError

    def __repr__(self):
        return f"Meta(table={self.table}," \
               f"uniq_key={self.uniq_key})"


class Scenario:
    def __init__(self, name):
        self.name = name
        self.identify = md5(name)

    def __repr__(self):
        return f"Scenario(name={self.name}," \
               f"identify={self.identify})"


class Entry:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"Entry(data={self.data})"


def create_task(table, uniq_key, scenario_name, sink_type=MYSQL_SINK_TYPE):
    # 1. 确包task_name不存在
    meta = Meta(table, uniq_key)
    scenario = Scenario(scenario_name)

    task = Task(meta=meta, scenario=scenario, sink_type=sink_type)
    return task


if __name__ == '__main__':
    task = create_task("my.runoob_tbl", "runoob_id=1", "开发测试")
    print(task)
    task.sinker.sink()
