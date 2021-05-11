import requests
import json


def get_user_rating(handle: str) -> dict:
    try:
        rsp = requests.get(f"https://codeforces.com/api/user.rating?handle={handle}")
        result = json.loads(rsp.text)
        for contest in result["result"]:
            contest["rating"] = contest["newRating"]
            contest["timestamp"] = contest["ratingUpdateTimeSeconds"]
            contest["url"] = "https://codeforces.com/contest/" + str(contest["contestId"])
            contest["name"] = contest["contestName"]
        result["data"] = result["result"]
        return result
    except Exception as e:
        return {
            "status": "unknown error",
            "data": [],
            "exception": e,
        }


if __name__ == '__main__':
    print(get_user_rating("ConanYu"))
