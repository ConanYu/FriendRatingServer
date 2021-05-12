import logging
import json
import requests


def get_user_rating(handle: str) -> dict:
    logging.info(f'crawling codeforces handle: {handle}')
    try:
        rsp = requests.get(f"https://codeforces.com/api/user.rating?handle={handle}")
        result = json.loads(rsp.text)
        result["data"] = []
        for contest in result["result"]:
            cur = dict()
            cur["rating"] = contest["newRating"]
            cur["timestamp"] = contest["ratingUpdateTimeSeconds"]
            cur["url"] = "https://codeforces.com/contest/" + str(contest["contestId"])
            cur["name"] = contest["contestName"]
            result["data"].append(cur)
        del result["result"]
        return result
    except Exception as e:
        logging.exception(e)
        return {
            "status": "unknown error",
            "data": [],
            "exception": e,
        }


if __name__ == '__main__':
    print(get_user_rating("ConanYu"))
