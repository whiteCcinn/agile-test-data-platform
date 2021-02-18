from src.domain.context import close_context


def invoke_cmd(f, *args):
    f(*args)
    invoke_close_context()


def invoke_close_context():
    close_context()
