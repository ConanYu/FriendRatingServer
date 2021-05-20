import re
import json
import urllib
import logging
import requests


def get_luogu_userid(handle: str) -> int:
    rsp = requests.get("https://www.luogu.com.cn/api/user/search", headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36",
    }, params={
        "keyword": handle,
    })
    return json.loads(rsp.text)["users"][0]["uid"]


def get_luogu_submit_msg(user_id: int) -> dict:
    rsp = requests.get(f"https://www.luogu.com.cn/user/{user_id}", headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36",
    })
    f, t = re.search(r'decodeURIComponent\(.*\"\)', rsp.text).span()
    msg = rsp.text[f + len('decodeURIComponent("'): t - len('")')]
    return json.loads(urllib.parse.unquote(msg))


def get_luogu_submit_data(handle: str) -> dict:
    try:
        user_id = get_luogu_userid(handle)
        msg = get_luogu_submit_msg(user_id)
        accept_count = msg["currentData"]["user"]["passedProblemCount"]
        submit_count = msg["currentData"]["user"]["submittedProblemCount"]
        distribution = dict()
        accept_problem_set = set()
        for accept_problem in msg["currentData"]["passedProblems"]:
            if accept_problem["pid"] not in accept_problem_set:
                accept_problem_set.add(accept_problem["pid"])
                diff = accept_problem["difficulty"] * 100 + 100
                distribution[diff] = distribution.get(diff, 0) + 1
        return {
            "status": "OK",
            "handle": handle,
            "accept_count": accept_count,
            "submit_count": submit_count,
            "profile_url": f"https://www.luogu.com.cn/user/{user_id}",
            "data": {
                "distribution": distribution,
            },
        }
    except Exception as e:
        logging.exception(e)
        return {
            "status": "unknown error",
        }


if __name__ == '__main__':
    print(get_luogu_submit_data("Fee_clе6418"))
