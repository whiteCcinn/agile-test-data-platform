import os

import aiofiles

import src
from src.domain.context import get_context
from src.constant.common import INIT_DB_FILE


def init_db():
    get_context().mysql_pool.execute(_init_db_worker)


async def _init_db_worker(conn, cur):
    async with aiofiles.open(get_sql_file_path(), mode='r') as f:
        contents = await f.read()
        await cur.execute(contents)
        await conn.commit()


def get_sql_file_path():
    proj_root = src.__path__[0].strip("src")
    return os.path.join(proj_root, INIT_DB_FILE)
