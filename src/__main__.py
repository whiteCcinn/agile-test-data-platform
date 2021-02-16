import asyncio
import os
import sys
import traceback

from src import config_manager
from src.log.logger import logger_system, set_loggers_level
from src.constant.common import APP_NAME

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)


async def _init(log_level=None) -> None:
    # logger和config初始化
    config_manager.init_logger(log_level)
    config_manager.init_configs()


def init(log_level=None):
    loop = asyncio.new_event_loop()  # 创建并返回一个新的事件对象
    asyncio.events.set_event_loop(loop)  # 将当前上下文的事件循环设置为loop
    loop.run_until_complete(_init(log_level))  # 运行startup直到这个任务完成
    return loop


def main() -> None:
    loop = init()
    try:
        debug = True
        loop.set_debug(debug)
        logger_system.info(f'{APP_NAME} starts up!')
        add_signal_handlers(loop)
        loop.run_forever()

    finally:
        try:
            _cancel_all_tasks(loop)
            loop.run_until_complete(loop.shutdown_asyncgens())
        finally:
            asyncio.events.set_event_loop(None)
            loop.close()
            logger_system.info(f'{APP_NAME} shuts down!')


def stop_it(signame, loop):
    try:
        logger_system.info(f'got signal {signame}')
        loop.stop()
        logger_system.info('event loop stopped!')
        # sys.exit(0)
    except Exception as e:
        print(e)


def add_signal_handlers(loop):
    if sys.platform == 'win32':
        pass
    else:
        import functools
        import signal
        for signame in {'SIGINT', 'SIGTERM'}:
            loop.add_signal_handler(
                getattr(signal, signame),
                functools.partial(stop_it, signame, loop))


def _cancel_all_tasks(loop):
    logger_system.info("cancel all tasks...")
    to_cancel = asyncio.tasks.all_tasks(loop)
    if not to_cancel:
        return

    for task in to_cancel:
        task.cancel()

    loop.run_until_complete(
        asyncio.tasks.gather(*to_cancel, loop=loop, return_exceptions=True))

    for task in to_cancel:
        if task.cancelled():
            continue
        if task.exception() is not None:
            loop.call_exception_handler({
                'message': 'unhandled exception during asyncio.run() shutdown',
                'exception': task.exception(),
                'task': task,
            })


if __name__ == '__main__':
    # noinspection PyBroadException
    try:
        main()
    except Exception:
        logger_system.error(traceback.format_exc())
        sys.exit()
