from src.domain.tasker import create_task


def execute(table, uniq_key, scenario_name):
    task = create_task(table, uniq_key, scenario_name)
    print(task)


if __name__ == '__main__':
    execute("my.runoob_tbl", "runoob_id=1", "开发测试")
