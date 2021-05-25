import logging
import json
import datetime
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from friend_rating_server.util.rsa_checker import RSAChecker
from friend_rating_server.util.config import get_config, set_config, reload_config as reload
from friend_rating_server.data.data import \
    ATCODER_RATING_CACHE, \
    CODEFORCES_RATING_CACHE, \
    NOWCODER_RATING_CACHE, \
    CODEFORCES_SUBMIT_CACHE, \
    LUOGU_SUBMIT_CACHE, \
    VJUDGE_SUBMIT_CACHE
from friend_rating_server.data.data import get_member as get_members_from_config

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


def get_luogu_submit_data(request: WSGIRequest):
    handle = request.GET.get('handle', '')
    result = LUOGU_SUBMIT_CACHE.get(handle)
    return HttpResponse(json.dumps(result))


def get_vjudge_sumbit_data(request: WSGIRequest):
    handle = request.GET.get('handle', '')
    result = VJUDGE_SUBMIT_CACHE.get(handle)
    return HttpResponse(json.dumps(result))


def get_all_data_source(request: WSGIRequest) -> dict:
    codeforces = request.GET.get('codeforces', '')
    atcoder = request.GET.get('atcoder', '')
    nowcoder = request.GET.get('nowcoder', '')
    luogu = request.GET.get('luogu', '')
    vjudge = request.GET.get('vjudge', '')
    return {
        "codeforces_contest": CODEFORCES_RATING_CACHE.get(codeforces),
        "atcoder_contest": ATCODER_RATING_CACHE.get(atcoder),
        "nowcoder_contest": NOWCODER_RATING_CACHE.get(nowcoder),
        "codeforces_submit": CODEFORCES_SUBMIT_CACHE.get(codeforces),
        "luogu_submit": LUOGU_SUBMIT_CACHE.get(luogu),
        "vjudge_submit": VJUDGE_SUBMIT_CACHE.get(vjudge),
    }


def get_all_data(request: WSGIRequest):
    return HttpResponse(json.dumps(get_all_data_source(request)))


def get_members(request: WSGIRequest):
    return HttpResponse(json.dumps(get_members_from_config()))


@csrf_exempt
def delete_member(request: WSGIRequest):
    if request.method == 'POST':
        if not expire_checker(request):
            return HttpResponseBadRequest()
        conf = get_config('')
        index = request.POST.get("index")
        name = request.POST.get("name")
        logging.info(index, name)
        print(index, name)
        try:
            if conf['members'][int(index)]['name'] != name:
                raise KeyError()
        except (KeyError, TypeError):
            return HttpResponseBadRequest()
        members: list = conf['members']
        new_members = []
        for key, value in enumerate(members):
            if key != int(index):
                new_members.append(value)
        conf['members'] = new_members
        set_config(conf)
        return HttpResponse(json.dumps({
            'status': 'OK',
            'message': f'key {index} name {name} have been remove',
        }))
    return HttpResponseNotAllowed(('POST',))


def dict_push_item(dic: dict, key, value=None):
    if value is not None and value != '':
        dic[key] = value


@csrf_exempt
def add_member(request: WSGIRequest):
    if request.method == 'POST':
        if not expire_checker(request):
            return HttpResponseBadRequest()
        conf = get_config('')
        name = request.POST.get("name")
        grade = request.POST.get("grade")
        codeforces = request.POST.get("codeforces")
        atcoder = request.POST.get("atcoder")
        nowcoder = request.POST.get("nowcoder")
        luogu = request.POST.get("luogu")
        vjudge = request.POST.get("vjudge")
        if name is None or name == '':
            return HttpResponseBadRequest()
        res = {
            'name': name,
        }
        dict_push_item(res, 'grade', grade)
        dict_push_item(res, 'codeforces', codeforces)
        dict_push_item(res, 'atcoder', atcoder)
        dict_push_item(res, 'nowcoder', nowcoder)
        dict_push_item(res, 'luogu', luogu)
        dict_push_item(res, 'vjudge', vjudge)
        conf["members"].append(res)
        set_config(conf)
        return HttpResponse(json.dumps({
            'status': 'OK',
            'message': f'member {res} have been insert',
        }))
    return HttpResponseNotAllowed(('POST',))


def get_all_data_simple(request: WSGIRequest):
    data = get_all_data_source(request)
    for value in data.values():
        try:
            del value["data"]
        except Exception as e:
            logging.exception(e)
    return HttpResponse(json.dumps(data))
