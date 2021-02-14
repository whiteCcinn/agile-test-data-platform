import asyncio


def create_new_future():
    loop = asyncio.get_running_loop()
    return loop.create_future()


def run_await(co):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(co)
