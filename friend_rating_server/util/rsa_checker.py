from typing import Tuple, Union
import rsa
import logging
from friend_rating_server.util.scheduler_cache import SchedulerCache
from friend_rating_server.util.config import get_config


def new_key(name):
    logging.info(f'object {name} get new key')
    return rsa.newkeys(1024)


class RSAChecker(object):
    def encrypt(self, msg: str) -> str:
        public_key, private_key = RSAChecker.key_cache.get(self.__str__())
        logging.info(public_key, private_key)
        result = rsa.encrypt(msg.encode(), public_key)
        return '|'.join([str(e) for e in result])

    def decrypt(self, msg: str) -> Tuple[Union[None, Exception], str]:
        try:
            _, private_key = RSAChecker.key_cache.get(self.__str__())
            result = rsa.decrypt(bytes([int(e) for e in msg.split('|')]), private_key)
            ret = result.decode()
            return None, ret
        except Exception as e:
            return e, ''

    key_cache = SchedulerCache(new_key, get_config("rsa.expire", 43200))
