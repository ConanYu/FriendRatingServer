import logging
from friend_rating_server.util.config import get_config
from friend_rating_server.util.scheduler_cache import SchedulerCache
from friend_rating_server.crawler.atcoder.get_user_rating import get_competition_history as get_atcoder_rating
from friend_rating_server.crawler.codeforces.get_user_rating import get_user_rating as get_codeforces_rating
from friend_rating_server.crawler.nowcoder.get_user_rating import get_user_rating_history as get_nowcoder_rating

ATCODER_RATING_CACHE = SchedulerCache(get_atcoder_rating)
CODEFORCES_RATING_CACHE = SchedulerCache(get_codeforces_rating)
NOWCODER_RATING_CACHE = SchedulerCache(get_nowcoder_rating)


def code_start_init():
    members = get_config("members")
    if members is not None:
        for member in members:
            atcoder_name = member.get("atcoder")
            codeforces_name = member.get("codeforces")
            nowcoder_name = member.get("nowcoder")
            if atcoder_name is not None:
                ATCODER_RATING_CACHE.get(atcoder_name)
            if codeforces_name is not None:
                CODEFORCES_RATING_CACHE.get(codeforces_name)
            if nowcoder_name is not None:
                NOWCODER_RATING_CACHE.get(nowcoder_name)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    code_start_init()
    print(ATCODER_RATING_CACHE.get("ConanYu"))
    print(ATCODER_RATING_CACHE.get("tourist"))
    print(ATCODER_RATING_CACHE.get("ConanYu"))
    print(CODEFORCES_RATING_CACHE.get("ConanYu"))
    print(CODEFORCES_RATING_CACHE.get("ConanYu"))
    print(NOWCODER_RATING_CACHE.get("6693394"))
