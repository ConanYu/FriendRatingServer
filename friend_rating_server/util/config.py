import os
import yaml
from copy import deepcopy
from readerwriterlock.rwlock import RWLockFairD

CONF = None
LOCK = RWLockFairD()
CONF_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config.yml')


def reload_config():
    global CONF, CONF_PATH, LOCK
    with open(CONF_PATH, 'r', encoding='utf-8') as config_file:
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
            if arg == '':
                continue
            if ret is None:
                return default
            try:
                ret = ret[arg]
            except:
                return default
        return deepcopy(ret)


def set_config(config):
    global CONF, CONF_PATH, LOCK
    with LOCK.gen_wlock():
        string = yaml.dump(config, default_flow_style=False, encoding='utf-8', allow_unicode=True).decode('utf-8')
        with open(CONF_PATH, 'w', encoding='utf-8') as config_file:
            config_file.write(string)
        CONF = config
    reload_config()


if __name__ == '__main__':
    conf = get_config('')
    conf["admin"] = ''
    print(conf)
    print(get_config(''))
