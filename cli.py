import click
from src.__main__ import init
from src.cmd.execute import execute_cmd
from src.cmd.init_db import init_db_cmd
from src.config_manager import wrapper_mysql_info


@click.group()
@click.option('--mysql_host', required=False, default='127.0.0.1', type=str, help='Mysql connect host')
@click.option('--mysql_port', required=False, default=3306, type=int, help='Mysql connect port')
@click.option('--mysql_user', required=False, default='root', type=str, help='Mysql connect user')
@click.option('--mysql_passwd', required=False, default='123456', type=str, help='Mysql connect passwd')
@click.pass_context
def cli(ctx,
        mysql_host, mysql_port, mysql_user, mysql_passwd
        ):
    init()
    ctx.ensure_object(dict)
    ctx.obj['mysql_host'] = mysql_host
    ctx.obj['mysql_port'] = mysql_port
    ctx.obj['mysql_user'] = mysql_user
    ctx.obj['mysql_passwd'] = mysql_passwd


@cli.command(help='初始化数据库')
@click.pass_context
def init_db(
        ctx
):
    mysql_info(ctx)
    init_db_cmd()


@cli.command(help='执行造数')
@click.option('--table', required=True, type=str, help='The table name of the work.')
@click.option('--uniq_key', required=True, type=str, help='A unique index of the data, use commas to separate fields.')
@click.option('--task_name', required=True, type=str, help='Remark the nickname of the mission.')
@click.pass_context
def execute(
        ctx,
        table, uniq_key, task_name
):
    mysql_info(ctx)
    execute_cmd(table, uniq_key, task_name)


def mysql_info(ctx):
    mysql_host = ctx.obj['mysql_host']
    mysql_port = ctx.obj['mysql_port']
    mysql_user = ctx.obj['mysql_user']
    mysql_passwd = ctx.obj['mysql_passwd']
    wrapper_mysql_info(mysql_host, mysql_port, mysql_user, mysql_passwd)


if __name__ == '__main__':
    cli(obj={})
