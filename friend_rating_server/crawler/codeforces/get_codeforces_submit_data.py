import logging
import json
import requests
from friend_rating_server.crawler.codeforces.thread_pool_executor import CODEFORCES_THREAD_EXECUTOR


def get_codeforces_status(handle: str) -> dict:
    try:
        task = CODEFORCES_THREAD_EXECUTOR.submit(requests.get,
                                                 f"https://codeforces.com/api/user.status?handle={handle}")
        response = json.loads(task.result().text)
        return response
    except Exception as e:
        logging.exception(e)
        return {
            "status": "unknown error",
        }


def get_codeforces_submit_data(handle: str) -> dict:
    try:
        response = get_codeforces_status(handle)
        ac_problem_set = set()
        accept_count = 0
        submit_count = len(response["result"])
        distribution = dict()
        for submit in response["result"]:
            problem = json.dumps(sorted(list(submit["problem"].items())))
            problem_rating = submit["problem"].get("rating")
            if submit["verdict"] == "OK" and problem not in ac_problem_set:
                ac_problem_set.add(problem)
                if problem_rating is not None:
                    distribution[problem_rating] = distribution.get(problem_rating, 0) + 1
                accept_count += 1
        return {
            "status": "OK",
            "handle": handle,
            "accept_count": accept_count,
            "submit_count": submit_count,
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
    print(get_codeforces_submit_data('ConanYu'))
