import logging
import json
import datetime
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from friend_rating_server.util.rsa_checker import RSAChecker
from friend_rating_server.util.config import get_config, reload_config as reload
from friend_rating_server.data.data \
    import ATCODER_RATING_CACHE, CODEFORCES_RATING_CACHE, NOWCODER_RATING_CACHE, CODEFORCES_SUBMIT_CACHE

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
        return HttpResponse(json.dumps({
            'status': 'OK',
        }))
    return HttpResponse(json.dumps({
        'status': 'ERROR',
    }))


def get_atcoder_data(request: WSGIRequest):
    handle = request.GET.get('handle', '')
    result = ATCODER_RATING_CACHE.get(handle)
    return HttpResponse(json.dumps(result))


def get_codeforces_data(request: WSGIRequest):
    handle = request.GET.get('handle', '')
    result = CODEFORCES_RATING_CACHE.get(handle)
    return HttpResponse(json.dumps(result))


def get_nowcoder_data(request: WSGIRequest):
    handle = request.GET.get('handle', '')
    result = NOWCODER_RATING_CACHE.get(handle)
    return HttpResponse(json.dumps(result))


def get_codeforces_submit_data(request: WSGIRequest):
    handle = request.GET.get('handle', '')
    result = CODEFORCES_SUBMIT_CACHE.get(handle)
    return HttpResponse(json.dumps(result))


def get_all_data_source(request: WSGIRequest) -> dict:
    codeforces = request.GET.get('codeforces', '')
    atcoder = request.GET.get('atcoder', '')
    nowcoder = request.GET.get('nowcoder', '')
    return {
        "codeforces_contest": CODEFORCES_RATING_CACHE.get(codeforces),
        "atcoder_contest": ATCODER_RATING_CACHE.get(atcoder),
        "nowcoder_contest": NOWCODER_RATING_CACHE.get(nowcoder),
        "codeforces_submit": CODEFORCES_SUBMIT_CACHE.get(codeforces),
    }


def get_all_data(request: WSGIRequest):
    return HttpResponse(json.dumps(get_all_data_source(request)))


def get_all_data_simple(request: WSGIRequest):
    data = get_all_data_source(request)
    for value in data.values():
        try:
            del value["data"]
        except Exception as e:
            logging.exception(e)
    return HttpResponse(json.dumps(data))
