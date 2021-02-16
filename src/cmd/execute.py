from src.domain.tasker import create_task
from src.log.logger import logger_cmd


def execute_cmd(table, uniq_key, scenario_name):
    task = create_task(table, uniq_key, scenario_name)
    logger_cmd.info(f'Created {task}')
    task.sinker.sink()


if __name__ == '__main__':
    execute_cmd("my.runoob_tbl", "runoob_id=1", "开发测试")
