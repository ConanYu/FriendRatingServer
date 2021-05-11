from typing import Union
import logging
import json
import requests


def get_user_rating_history(handle: Union[str, int]) -> dict:
    logging.info(f'crawling nowcoder handle: {handle}')
    url = f'https://ac.nowcoder.com/acm/contest/rating-history?uid={handle}'
    request = requests.get(url)
    obj = json.loads(request.text)
    obj["status"] = "OK"
    return obj


if __name__ == '__main__':
    print(get_user_rating_history(6693394))
