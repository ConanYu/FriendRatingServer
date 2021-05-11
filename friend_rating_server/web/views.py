import json
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from friend_rating_server.data.data import get_member, code_start_init
from friend_rating_server.util.config import reload_config as reload


def index(request: WSGIRequest):
    members = get_member()
    members_json = json.dumps(members)
    return render(request, 'index.html', locals())


def reload_config(request: WSGIRequest):
    reload()
    code_start_init()
    return render(request, 'redirect.html', locals())
