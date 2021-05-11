from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from friend_rating_server.data.data import get_member
from friend_rating_server.util.config import reload_config as reload


def index(request: WSGIRequest):
    members = get_member()
    return render(request, 'index.html', locals())


def reload_config(request: WSGIRequest):
    reload()
    return render(request, 'redirect.html', locals())
