import os
import logging
import yaml

CONF = None


def reload_config():
    global CONF
    dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    with open(os.path.join(dir_name, 'config.yml'), 'r', encoding='utf-8') as config_file:
        CONF = yaml.load(config_file.read(), yaml.FullLoader)


reload_config()


def get_config(path: str, default=None):
    global CONF
    args = path.split('.')
    ret = CONF
    for arg in args:
        if ret is None:
            return default
        try:
            ret = ret[arg]
        except Exception as e:
            logging.exception(e)
            return default
    return ret


if __name__ == '__main__':
    print(get_config("apple.banana.cat.dog", "default"))
    print(get_config("apple.banana.cat.dot", "default"))
