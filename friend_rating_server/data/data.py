import logging
from friend_rating_server.util.config import get_config
from friend_rating_server.util.scheduler_cache import SchedulerCache
from friend_rating_server.crawler.atcoder.get_atcoder_contest_data import get_atcoder_contest_data
from friend_rating_server.crawler.codeforces.get_codeforces_contest_data import get_codeforces_contest_data
from friend_rating_server.crawler.codeforces.get_codeforces_submit_data import get_codeforces_submit_data
from friend_rating_server.crawler.nowcoder.get_nowcoder_contest_data import get_nowcoder_contest_data
from friend_rating_server.crawler.luogu.get_luogu_submit_data import get_luogu_submit_data
from friend_rating_server.crawler.vjudge.get_vjudge_submit_data import get_vjudge_submit_data

ATCODER_RATING_CACHE = SchedulerCache(get_atcoder_contest_data)
CODEFORCES_RATING_CACHE = SchedulerCache(get_codeforces_contest_data)
NOWCODER_RATING_CACHE = SchedulerCache(get_nowcoder_contest_data)
CODEFORCES_SUBMIT_CACHE = SchedulerCache(get_codeforces_submit_data)
LUOGU_SUBMIT_CACHE = SchedulerCache(get_luogu_submit_data)
VJUDGE_SUBMIT_CACHE = SchedulerCache(get_vjudge_submit_data)


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
