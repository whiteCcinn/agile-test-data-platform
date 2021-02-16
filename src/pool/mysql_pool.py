import aiomysql
from src.util.asyncio import run_await


class MysqlPool:
    def __init__(self, min_size=1, max_size=10, host='127.0.0.1', port=3306,
                 user='root', password='', echo=False,
                 loop=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.min_size = min_size
        self.max_size = max_size
        self.echo = echo
        self.loop = loop
        self.pool = run_await(aiomysql.create_pool(
            minsize=self.min_size, maxsize=self.max_size, echo=echo, host=self.host, port=self.port,
            user=self.user, password=self.password,
            loop=self.loop
        ))

    def execute(self, f):
        return run_await(self.internal_execute(f))

    async def internal_execute(self, f):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await f(conn, cur)

    def close(self):
        self.pool.close()
        run_await(self.pool.wait_closed())
