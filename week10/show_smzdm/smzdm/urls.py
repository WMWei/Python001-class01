# from django.contrib import admin
from django.urls import path
from . import views


app_name = 'smzdm'

urlpatterns = [
    # localhost:8000/?cate=<str>
    # new or hot
    path('', views.home, name='home'),
    # localhost:8000/index/?pageNo={}&q={}
    path('index/', views.index, name='index'),
    # localhost:8000/index/<str:cate>/?pageNo={}&q={}
    path('index/<str:cate>/', views.index, name='category'),
    # localhost:8000/p/<int:pid>/
    path('p/<int:pid>/', views.detail, name='detail'),
    # localhost:8000/p/<int:pid>/comments/?pageNo={}&q={}
    path('p/<int:pid>/comments/', views.comments, name='comments'),
    # localhost:8000/p/<int:pid>/sentiment/
    path('p/<int:pid>/sentiment/', views.sentiment, name='sentiment'),
    # localhost:8000/p/<int:pid>/analysis/
    path('p/<int:pid>/analysis/', views.analysis, name='analysis'),
]
