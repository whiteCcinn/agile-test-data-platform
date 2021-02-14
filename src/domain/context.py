from src.pool.mysql_pool import *
from src.util.singleton import SingletonType
import asyncio

ctx = None


class Context(metaclass=SingletonType):
    def __init__(self, mysql_pool: dict):
        self.mysql_pool = MysqlPool(**mysql_pool)
        global ctx
        ctx = self


def get_context() -> Context:
    global ctx
    if ctx is None:
        loop = asyncio.get_event_loop()
        Context(mysql_pool={
            'min_size': 1,
            'max_size': 10,
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'loop': loop
        })

    return ctx


async def test_example(cur):
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
    print(get_context().mysql_pool.execute(test_example))
