from django.shortcuts import render
from friend_rating_server.data.data import get_member


def index(request):
    text = "hello world"
    members = get_member()
    return render(request, 'index.html', locals())
