import logging
import json
import datetime
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from friend_rating_server.util.rsa_checker import RSAChecker
from friend_rating_server.util.config import get_config, reload_config as reload
from friend_rating_server.data.data import code_start_init


EXPIRE_RSA_CHECKER = RSAChecker()


def expire_checker(request: WSGIRequest, key=None) -> bool:
    global EXPIRE_RSA_CHECKER
    if key is None:
        key = get_config("admin.cookie_key", "admin_token")
    cookie = request.COOKIES.get(key)
    if cookie is None:
        return False
    _, msg = EXPIRE_RSA_CHECKER.decrypt(cookie)
    try:
        year, month, day, hour, minute, second = map(int, msg.split(','))
        date = datetime.datetime(year, month, day, hour, minute, second)
        return datetime.datetime.now() < date
    except Exception as e:
        logging.exception(e)
        return False


def reload_config(request: WSGIRequest):
    if request.method == 'POST' and expire_checker(request):
        reload()
        code_start_init()
        return HttpResponse(json.dumps({
            'status': 'OK',
        }))
    return HttpResponse(json.dumps({
        'status': 'ERROR',
    }))
