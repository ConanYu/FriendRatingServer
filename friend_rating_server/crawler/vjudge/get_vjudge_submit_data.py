import json
import logging
from friend_rating_server.util.new_session import new_session
from friend_rating_server.crawler.vjudge.login import login
from friend_rating_server.crawler.vjudge.thread_pool_executor import VJUDGE_THREAD_EXECUTOR
from friend_rating_server.util.config import get_config


def get_vjudge_submit_data(handle: str):
    session = new_session()
    if not login(session, get_config("vjudge.username"), get_config("vjudge.password")):
        raise ValueError(f"login failed with username {get_config('vjudge.username')} and password {get_config('vjudge.password')}")
    accept_count = 0
    submit_count = 0
    oj_distribution = dict()
    problem_set = set()
    try:
        max_id = ""
        while True:
            task = VJUDGE_THREAD_EXECUTOR.submit(session.get, "https://vjudge.net/user/submissions", params={
                "username": handle,
                "pageSize": 500,
                "maxId": max_id,
            })
            rsp = json.loads(task.result().text)
            if len(rsp["data"]) == 0:
                break
            max_id = rsp["data"][-1][0] - 1
            for data in rsp["data"]:
                pb = data[2] + data[3]
                if pb not in problem_set and data[4] == 'AC':
                    accept_count += 1
                    oj_distribution[data[2]] = oj_distribution.get(data[2], 0) + 1
                    problem_set.add(pb)
            submit_count += len(rsp["data"])
    except Exception as e:
        logging.exception(e)
    finally:
        return {
            "status": "OK",
            "handle": handle,
            "accept_count": accept_count,
            "submit_count": submit_count,
            "profile_url": f"https://vjudge.net/user/{handle}",
            "data": {
                "oj_distribution": oj_distribution,
            },
        }


if __name__ == '__main__':
    print(get_vjudge_submit_data('ConanYu'))
