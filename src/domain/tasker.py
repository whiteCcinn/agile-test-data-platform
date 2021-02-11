import logging
import traceback
from src.log.Error import MetaInitError
from src.util.func import md5


class Task:
    def __init__(self, meta=None, scenario=None, entries=[]):
        self.meta = meta
        self.scenario = scenario
        self.entries = entries

    def __repr__(self):
        return f"Task(meta={self.meta}," \
               f"scenario={self.scenario}," \
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


def create_task(table, uniq_key, scenario_name):
    # 1. 确包task_name不存在
    meta = Meta(table, uniq_key)
    scenario = Scenario(scenario_name)

    task = Task(meta, scenario)
    return task
