from src.domain.show_data import select_table_show
from src.log.logger import logger_cmd


def show_data_cmd(fields, name, id, offset, limit, order_by, group_by, having):
    select_table_show(fields, name, id, offset, limit, order_by, group_by, having)
    logger_cmd.info('Select successfully')
