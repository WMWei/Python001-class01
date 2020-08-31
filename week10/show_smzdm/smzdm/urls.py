# from django.contrib import admin
from django.urls import path
from . import views


app_name = 'smzdm'

urlpatterns = [
    # localhost:8000/
    path('', views.home, name='home'),
    path('hot/', views.home, name='hot'),
    # localhost:8000/index/
    # localhost:8000/index/<str:cate>/?pageNo={}&q={}
    path('index/', views.index, name='index'),
    # localhost:8000/p/  # 404
    # localhost:8000/p/<int:pid>/
    path('p/<int:pid>/', views.detail, name='detail'),
    # localhost:8000/p/<int:pid>/comments/?pageNo={}&q={}
    path('p/<int:pid>/comments/', views.comments, name='comments'),

]
