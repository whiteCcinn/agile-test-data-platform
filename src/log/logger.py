import logging
import os
from logging import handlers
from pathlib import Path

logger_config = logging.getLogger('config')

logger_system = logging.getLogger('system')

logger_cmd = logging.getLogger('cmd')

logger_constant = logging.getLogger('constant')

logger_domain = logging.getLogger('domain')

logger_log = logging.getLogger('log')

logger_pool = logging.getLogger('pool')

logger_util = logging.getLogger('util')

log_level: int


def set_loggers_level(level):
    logger_config.setLevel(level)
    logger_system.setLevel(level)
    logger_cmd.setLevel(level)
    logger_constant.setLevel(level)
    logger_domain.setLevel(level)
    logger_log.setLevel(level)
    logger_util.setLevel(level)


def customized_logger(name):
    logger = logging.getLogger(name)
    if log_level is not None:
        logger.setLevel(log_level)
    else:
        logger.setLevel(logging.DEBUG)
    return logger


def file_handler(dir_path, filename, mode='a', encoding=None, max_bytes=10 * 1024 * 1024, backup_count=6):
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    file_path = dir_path + filename
    if not os.path.exists(file_path):
        open(file_path, 'a').close()
    return handlers.RotatingFileHandler(file_path, mode=mode, encoding=encoding,
                                        maxBytes=max_bytes, backupCount=backup_count)
