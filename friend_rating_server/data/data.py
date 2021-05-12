from typing import List
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
        source_level = logging.getLogger().level
        logging.getLogger().setLevel(logging.INFO)
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
        logging.getLogger().setLevel(source_level)


code_start_init()


def get_reduce_data(s: List[str], source: List[dict]) -> List[dict]:
    ret = []
    for ele in source:
        ret_ele = dict()
        for item in s:
            value = ele.get(item)
            if value is not None:
                ret_ele[item] = value
        ret.append(ret_ele)
    return ret


def get_member() -> list:
    members = get_config("members").copy()
    logging.info(members)
    index = 0
    if members is not None:
        for member in members:
            member["index"] = index
            index += 1
            member["atcoder_name"] = member.get("atcoder", "")
            member["atcoder_profile_url"] = f"https://atcoder.jp/users/{member['atcoder_name']}"
            member["codeforces_name"] = member.get("codeforces", "")
            member["codeforces_profile_url"] = f"https://codeforces.com/profile/{member['codeforces_name']}"
            if member["atcoder_name"] is not None:
                atcoder_rating = ATCODER_RATING_CACHE.get(member["atcoder_name"])
                if atcoder_rating["status"] == "OK":
                    member["atcoder_data"] = atcoder_rating
                    if len(atcoder_rating["data"]):
                        member["atcoder_rating"] = atcoder_rating["data"][-1]["rating"]
            if member["codeforces_name"] is not None:
                codeforces_rating = CODEFORCES_RATING_CACHE.get(member["codeforces_name"])
                if codeforces_rating["status"] == "OK":
                    member["codeforces_data"] = codeforces_rating
                    if len(codeforces_rating["data"]):
                        member["codeforces_rating"] = codeforces_rating["data"][-1]["rating"]
    return get_reduce_data([
        "name",
        "grade",
        "index",
        "atcoder_name",
        "atcoder_profile_url",
        "codeforces_name",
        "codeforces_profile_url",
        "atcoder_data",
        "atcoder_rating",
        "codeforces_data",
        "codeforces_rating",
    ], members)


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
