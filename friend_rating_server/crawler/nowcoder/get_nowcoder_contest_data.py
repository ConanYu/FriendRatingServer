from typing import Union
import logging
import json
import requests


def get_nowcoder_contest_data(handle: Union[str, int]) -> dict:
    logging.info(f'crawling nowcoder handle: {handle}')
    url = f'https://ac.nowcoder.com/acm/contest/rating-history?uid={handle}'
    try:
        request = requests.get(url)
        obj = json.loads(request.text)
        obj["status"] = obj["msg"]
        del obj["msg"]
        del obj["code"]
        obj["handle"] = str(handle)
        obj["length"] = len(obj["data"])
        obj["profile_url"] = f"https://ac.nowcoder.com/acm/home/{handle}"
        if len(obj["data"]):
            obj["rating"] = int(obj["data"][-1]["rating"])
        for value in obj["data"]:
            value["timestamp"] = value["time"] // 1000
            value["rating"] = int(value["rating"])
            value["name"] = value["contestName"]
            value["url"] = f"https://ac.nowcoder.com/acm/contest/{value['contestId']}"
            try:
                del value["contestId"]
                del value["rank"]
                del value["contestName"]
                del value["changeValue"]
                del value["colorLevel"]
                del value["time"]
            except Exception as e:
                logging.exception(e)
    except Exception as e:
        logging.exception(e)
        return {
            "status": "unknown error",
        }
    return obj


if __name__ == '__main__':
    print(get_nowcoder_contest_data(6693394))
