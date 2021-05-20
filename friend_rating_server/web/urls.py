"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.views import static
from friend_rating_server.web import views
from friend_rating_server.web import api

urlpatterns = [
    url('^$', views.index),
    url("^admin$", views.admin),
    url('^api/reload_config$', api.reload_config),
    url('^api/get_atcoder_data$', api.get_atcoder_data),
    url('^api/get_codeforces_data$', api.get_codeforces_data),
    url('^api/get_codeforces_submit_data$', api.get_codeforces_submit_data),
    url('^api/get_nowcoder_data$', api.get_nowcoder_data),
    url('^api/get_luogu_submit_data$', api.get_luogu_submit_data),
    url('^api/get_all_data$', api.get_all_data),
    url('^api/get_all_data_simple$', api.get_all_data_simple),
    url('^api/get_members$', api.get_members),
    url('^api/delete_member$', api.delete_member),
    url('^api/add_member$', api.add_member),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}),
]
