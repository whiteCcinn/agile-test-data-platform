from src.pool.mysql_pool import *
from src.util.singleton import SingletonType
from src.log.logger import logger_domain
from asyncio import get_event_loop
from src.config_manager import get_mysql_config

ctx = None


class Context(metaclass=SingletonType):
    def __init__(self, mysql_pool: dict):
        self.mysql_pool_config = mysql_pool
        self.mysql_pool = self.target_mysql_pool = None
        if self.mysql_pool_config.get('source') is not None:
            self.mysql_pool = MysqlPool(**self.mysql_pool_config.get('source'))
        if self.mysql_pool_config.get('target') is not None:
            self.target_mysql_pool = MysqlPool(**self.mysql_pool_config.get('target'))
        global ctx
        ctx = self

    def __repr__(self):
        return f"Context(mysql_pool={self.mysql_pool_config}," \
               f"target_mysql_pool={self.target_mysql_pool})"

    __str__ = __repr__

    def get_sinker_mysql(self):
        return self.target_mysql_pool

    def get_source_mysql(self):
        return self.mysql_pool


def get_context() -> Context:
    global ctx
    if ctx is None:
        loop = get_event_loop()
        mysql_info = get_mysql_config()
        Context(mysql_pool={
            'min_size': 1,
            'max_size': 10,
            'loop': loop,
            'echo': True,
            **mysql_info
        })
        logger_domain.debug(f'Initialize {ctx} successfully')

    return ctx


async def test_example(conn, cur):
    # await cur.execute("SELECT 42;")
    await cur.execute("show databases;")
    # print(cur.description)
    # (r,) = await cur.fetchall()
    one = await cur.fetchall()
    # (r,) = await cur.fetchone
    print(one)
    # assert r == 42


if __name__ == '__main__':
    import asyncio
    from src.util.asyncio import run_await

    loop = asyncio.get_event_loop()
    # Context(mysql_pool={
    #     s'min_size': 1,
    #     'max_size': 10,
    #     'host': '127.0.0.1',
    #     'port': 3306,
    #     'user': 'root',
    #     'password': '123456',
    #     'loop': loop
    # })
    print(get_context().get_sinker_mysql().execute(test_example))
