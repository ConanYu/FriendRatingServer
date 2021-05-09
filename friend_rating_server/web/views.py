from django.shortcuts import render


def index(request):
    text = "hello world"
    title = "TITLE"
    return render(request, 'index.html', locals())
