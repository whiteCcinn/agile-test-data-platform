import logging
import logging.config
import os
import sys
import traceback
from src.constant.common import get_runtime_env

import yaml
import src

CFG_SYSTEM_DIR = 'system'

cfg_maps = {}

loaded_cfgs = {}

_cfg_base_path = ""


# 获取配置当前的目录
def get_cfg_base_path():
    global _cfg_base_path
    if _cfg_base_path == "":
        proj_root = src.__path__[0].strip("src")
        _cfg_base_path = os.path.join(proj_root, "config")
    return _cfg_base_path


# 日志系统主函数
def init_logger() -> None:
    try:
        cfg_logger = _get_cfg_path('logger')
        with open(cfg_logger, 'r', encoding='UTF-8') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        logging.info('Initialize logger successfully')
    except Exception:
        logging.error(traceback.format_exc())
        sys.exit()


# 配置系统主函数
def init_configs() -> None:
    global cfg_maps
    runtime_env = get_runtime_env()
    if runtime_env is None:
        runtime_env = _do_find("base", "env")
    cfg_maps = {
        "base": runtime_env
    }
    logging.info(f'Initialize [{runtime_env}] config successfully')


def find(cfg_name, key, default=None):
    target_cfg = cfg_maps.get(cfg_name, cfg_name)
    ret = _do_find(target_cfg, key)
    if ret is not None:
        return ret
    else:
        return default


# 根据配置文件获取其中某个key对应的value
# noinspection PyBroadException
def _do_find(cfg_name, key):
    try:
        global loaded_cfgs
        if cfg_name not in loaded_cfgs:
            cfg_path = _get_cfg_path(cfg_name)
            with open(cfg_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f.read())
                loaded_cfgs[cfg_name] = config
                return config.get(key, None)
        else:
            return loaded_cfgs[cfg_name].get(key, None)

    except FileNotFoundError:
        return None
    except IOError:
        return None
    except Exception:
        logging.error(traceback.format_exc())
        return None


def _get_cfg_path(cfg_name):
    """
    get config path
    :param cfg_name:
    :return:
    """
    cfg_file = cfg_name + '.yaml'
    cfg_path = os.path.join(get_cfg_base_path(), cfg_file)
    cfg_system_path = os.path.join(get_cfg_base_path(), CFG_SYSTEM_DIR, cfg_file)
    if os.path.exists(cfg_path):
        return cfg_path
    else:
        return cfg_system_path


if __name__ == '__main__':
    env = find('base', 'env')
    print(f'find env in base.yaml, result: {env}')
    whatever = find('base', 'whatever')
    print(f'find whatever in base.yaml, result: {whatever}')
    print(find('base', 'upload_service'))
    init_logger()
    init_configs()
    print(find('base', 'comment'))
