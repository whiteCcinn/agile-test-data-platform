from src.domain.db import init_db
from src.log.logger import logger_cmd


def init_db_cmd():
    init_db()
    print('[-] Initialize db and table successfully')
    logger_cmd.info('Initialize db and table successfully')
