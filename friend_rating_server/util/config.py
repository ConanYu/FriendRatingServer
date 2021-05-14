import os
import logging
import yaml
from readerwriterlock.rwlock import RWLockFairD

CONF = None
LOCK = RWLockFairD()


def reload_config():
    global CONF
    dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    with open(os.path.join(dir_name, 'config.yml'), 'r', encoding='utf-8') as config_file:
        conf = yaml.load(config_file.read(), yaml.FullLoader)
    with LOCK.gen_wlock():
        CONF = conf


reload_config()


def get_config(path: str, default=None):
    global CONF
    args = path.split('.')
    with LOCK.gen_rlock():
        ret = CONF
        for arg in args:
            if ret is None:
                return default
            try:
                ret = ret[arg]
            except:
                return default
        return ret


if __name__ == '__main__':
    print(get_config("apple.banana.cat.dog", "default"))
    print(get_config("apple.banana.cat.dot", "default"))
