from typing import List
import logging
from friend_rating_server.util.config import get_config
from friend_rating_server.util.scheduler_cache import SchedulerCache
from friend_rating_server.crawler.atcoder.get_atcoder_contest_data import get_atcoder_contest_data as get_atcoder_rating
from friend_rating_server.crawler.codeforces.get_codeforces_contest_data import get_codeforces_contest_data as get_codeforces_rating
from friend_rating_server.crawler.nowcoder.get_user_rating import get_user_rating_history as get_nowcoder_rating

ATCODER_RATING_CACHE = SchedulerCache(get_atcoder_rating)
CODEFORCES_RATING_CACHE = SchedulerCache(get_codeforces_rating)
NOWCODER_RATING_CACHE = SchedulerCache(get_nowcoder_rating)


def get_member() -> list:
    members = get_config("members").copy()
    for index, member in enumerate(members):
        member["index"] = index
    logging.info(members)
    return members


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    print(ATCODER_RATING_CACHE.get("ConanYu"))
    print(ATCODER_RATING_CACHE.get("tourist"))
    print(ATCODER_RATING_CACHE.get("ConanYu"))
    print(CODEFORCES_RATING_CACHE.get("ConanYu"))
    print(CODEFORCES_RATING_CACHE.get("ConanYu"))
    print(NOWCODER_RATING_CACHE.get("6693394"))
    try:
        while True:
            pass
    except KeyboardInterrupt:
        SchedulerCache.shutdown_all()
