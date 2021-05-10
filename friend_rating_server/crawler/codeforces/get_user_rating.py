import logging
import requests
import json
import datetime
from friend_rating_server.util.loading_cache import SchedulerCache


def get_user_rating(handle: str) -> dict:
    try:
        rsp = requests.get(f"https://codeforces.com/api/user.rating?handle={handle}")
        result = json.loads(rsp.text)
        for item in result["result"]:
            item['time'] = datetime.datetime.fromtimestamp(item['ratingUpdateTimeSeconds'])
        return result
    except Exception as e:
        return {
            "status": "unknown error",
            "exception": e,
        }


USER_RATING_CACHE = SchedulerCache(get_user_rating)


if __name__ == '__main__':
    logging.getLogger().setLevel(20)
    print(USER_RATING_CACHE.get('ConanYu'))
    print(USER_RATING_CACHE.get('ConanYu'))
    print(USER_RATING_CACHE.get('tourist'))
    print(USER_RATING_CACHE.get('ConanYu'))
    while True:
        pass
