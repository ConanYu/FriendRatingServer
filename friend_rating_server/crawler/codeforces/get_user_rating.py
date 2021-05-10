import requests
import json
import datetime


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


if __name__ == '__main__':
    print(get_user_rating("ConanYu"))
