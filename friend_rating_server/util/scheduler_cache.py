import logging
import threading
from copy import deepcopy
from apscheduler.schedulers.blocking import BlockingScheduler
from readerwriterlock import rwlock
from friend_rating_server.util.config import get_config


class SchedulerCache(object):
    def __init__(self, func, expire=7200):
        self.scheduler = BlockingScheduler()
        self.data = dict()
        self.func = func
        self.lock = rwlock.RWLockFairD()
        self.scheduler.add_job(self.__gao, 'interval', seconds=expire)
        threading.Thread(target=self.scheduler.start).start()
        SchedulerCache.objects.append(self)

    def get(self, key):
        update = False
        with self.lock.gen_rlock():
            value = self.data.get(key)
        if value is None:
            logging.info(f'start loading key {key}')
            value = self.func(key)
            logging.info(f'end loading key {key}')
            update = True
        if update:
            with self.lock.gen_wlock():
                if len(self.data) > get_config('scheduler_cache.max_size', 100000):
                    self.data.clear()
                self.data[key] = value
        logging.debug(self.data)
        return deepcopy(value)

    def __gao(self):
        logging.info("__gao start")
        data = dict()
        for key in self.data.keys():
            data[key] = self.func(key)
            logging.info(data[key])
        with self.lock.gen_wlock():
            self.data = data

    @staticmethod
    def shutdown_all():
        for obj in SchedulerCache.objects:
            obj.scheduler.shutdown()

    objects = []
