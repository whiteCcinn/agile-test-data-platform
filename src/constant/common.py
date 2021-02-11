import os

APP_NAME = "agile-test-data-platform"

RUNTIME_ENV = "ATDP_ENV"

runtime_enum = ["dev", "prod"]


def get_runtime_env():
    runtime_env = os.environ.get(RUNTIME_ENV)
    if runtime_env is not None:
        if runtime_env not in runtime_enum:
            return None

    return runtime_env


if __name__ == '__main__':
    print(os.environ.get(RUNTIME_ENV))
    os.environ[RUNTIME_ENV] = "prod"
    print(os.environ.get(RUNTIME_ENV))
