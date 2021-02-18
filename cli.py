import click
from src.__main__ import init
from src.cmd.execute import execute_cmd
from src.cmd.init_db import init_db_cmd
from src.cmd.show_data import show_data_cmd
import src.cmd
from src.config_manager import wrapper_mysql_info
import logging

common_options = [
    click.option('--log_level', required=False, default=logging.ERROR, type=int, help='log-level', show_default=True),
]

source_mysql_options = [
    click.option('--source_mysql_host', required=False, default='127.0.0.1', type=str,
                 help='Mysql[source] connect host', show_default=True),
    click.option('--source_mysql_port', required=False, default=3306, type=int, help='Mysql[source] connect port',
                 show_default=True),
    click.option('--source_mysql_user', required=False, default='root', type=str, help='Mysql[source] connect user',
                 show_default=True),
    click.option('--source_mysql_passwd', required=False, default='123456', type=str,
                 help='Mysql[source] connect passwd', show_default=True),
]

target_mysql_options = [
    click.option('--target_mysql_host', required=False, default='127.0.0.1', type=str,
                 help='Mysql[target] connect host', show_default=True),
    click.option('--target_mysql_port', required=False, default=3306, type=int, help='Mysql[target] connect port',
                 show_default=True),
    click.option('--target_mysql_user', required=False, default='root', type=str, help='Mysql[target] connect user',
                 show_default=True),
    click.option('--target_mysql_passwd', required=False, default='123456', type=str,
                 help='Mysql[target] connect passwd', show_default=True)
]


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


@click.group()
def cli():
    pass


@cli.command(help='初始化数据库')
@add_options(common_options)
@add_options(target_mysql_options)
def init_db(**kwargs):
    pre(kwargs)
    src.cmd.invoke_cmd(init_db_cmd)


@cli.command(help='执行造数')
@add_options(common_options)
@add_options(source_mysql_options)
@add_options(target_mysql_options)
@click.option('--table', required=True, type=str, help='The table name of the work.', show_default=True)
@click.option('--uniq_key', required=True, type=str, help='A unique index of the data, use commas to separate fields.',
              show_default=True)
@click.option('--task_name', required=True, type=str, help='Remark the nickname of the mission.', show_default=True)
def execute(
        table, uniq_key, task_name,
        **kwargs
):
    pre(kwargs)
    src.cmd.invoke_cmd(execute_cmd, table, uniq_key, task_name)


@cli.command(help='终端展示表')
@add_options(common_options)
@add_options(target_mysql_options)
@click.option('--fields', default='*', required=False, type=str, help='Task\'s fields,table alias in [task,entry]',
              show_default=True)
@click.option('--name', required=False, type=str, help='Task\'s.name', show_default=True)
@click.option('--id', required=False, type=int, help='Task\'s.id', show_default=True)
@click.option('--offset', required=False, type=str, help='offset stat', show_default=True)
@click.option('--limit', required=False, type=str, help='limit stat', show_default=True)
@click.option('--order_by', required=False, type=str, help='order_by stat', show_default=True)
@click.option('--group_by', required=False, type=str, help='group_by stat', show_default=True)
@click.option('--having', required=False, type=str, help='having stat', show_default=True)
def show_data(
        fields, name, id,
        offset, limit,
        order_by,
        group_by,
        having,
        **kwargs
):
    pre(kwargs)
    src.cmd.invoke_cmd(show_data_cmd, fields, name, id, offset, limit, order_by, group_by, having)


def pre(ctx: dict):
    init(ctx.get('log_level'))
    mysql_info(ctx)


def mysql_info(ctx: dict):
    source_mysql_host = ctx.get('source_mysql_host')
    source_mysql_port = ctx.get('source_mysql_port')
    source_mysql_user = ctx.get('source_mysql_user')
    source_mysql_passwd = ctx.get('source_mysql_passwd')

    target_mysql_host = ctx.get('target_mysql_host')
    target_mysql_port = ctx.get('target_mysql_port')
    target_mysql_user = ctx.get('target_mysql_user')
    target_mysql_passwd = ctx.get('target_mysql_passwd')
    wrapper_mysql_info(
        source_mysql_host, source_mysql_port, source_mysql_user, source_mysql_passwd,
        target_mysql_host, target_mysql_port, target_mysql_user, target_mysql_passwd,
    )


if __name__ == '__main__':
    cli()
