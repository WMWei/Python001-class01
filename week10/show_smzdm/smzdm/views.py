from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

# 主页
@require_http_methods(['GET'])
def home(request):
    return render(
        request,
        'home.html',
    )


def index(request):
    return render(
        request,
        '404.html',
    )


def detail(request, pid):
    pass


def comments(request, pid):
    pass