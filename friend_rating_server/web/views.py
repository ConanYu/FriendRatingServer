import logging
import json
import datetime
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from friend_rating_server.data.data import get_member, code_start_init
from friend_rating_server.util.config import get_config
from friend_rating_server.web.form.login_form import LoginForm
from friend_rating_server.web.api import EXPIRE_RSA_CHECKER, expire_checker


def index(request: WSGIRequest):
    members = get_member()
    members_json = json.dumps(members)
    return render(request, 'index.html', locals())


def admin_post(request: WSGIRequest):
    form = LoginForm(request.POST)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        print(type(get_config('admin.password', 0)))
        if password == get_config('admin.password', 0):
            expire_time = datetime.datetime.now() + datetime.timedelta(hours=1)
            time_msg = (f'{expire_time.year},{expire_time.month},{expire_time.day},'
                       f'{expire_time.hour},{expire_time.minute},{expire_time.second}')
            cookie = EXPIRE_RSA_CHECKER.encrypt(time_msg)
            user = True
            response = render(request, 'admin.html', locals())
            response.set_cookie(get_config("admin.cookie_key", "admin_token"), cookie)
            logging.debug(user)
            return response
    message = "密码错误"
    user = False
    return render(request, 'admin.html', locals())


def admin(request: WSGIRequest):
    if request.method == 'POST':
        return admin_post(request)
    form = LoginForm()
    user = expire_checker(request)
    members = []
    if user:
        members = get_config("members")
    return render(request, 'admin.html', locals())
