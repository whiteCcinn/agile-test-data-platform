import click
from src.__main__ import init
from src.cmd.execute import execute as execute_cmd


@click.group()
def cli():
    init()


@cli.command(help='执行造数')
@click.option('--table', required=True, type=str, help='The table name of the work.')
@click.option('--uniq_key', required=True, type=str, help='A unique index of the data, use commas to separate fields.')
@click.option('--task_name', required=True, type=str, help='Remark the nickname of the mission.')
def execute(table, uniq_key, task_name):
    execute_cmd(table, uniq_key, task_name)


if __name__ == '__main__':
    cli()
