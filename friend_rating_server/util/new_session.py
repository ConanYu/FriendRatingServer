import requests
from friend_rating_server.util.config import get_config


def new_session() -> requests.Session:
    session = requests.Session()
    session.proxies = get_config('proxies', dict())
    return session
