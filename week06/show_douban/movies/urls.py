# from django.contrib import admin
from django.urls import path
from . import views


app_name = 'movies'

urlpatterns = [
    # localhost:8000/movies/
    # localhost:8000/index/?start={start}&pagesize={count}
    path('', views.index, name='index'),
    # localhost:8000/movies/{mk}/
    path('<int:mk>/', views.detail, name='detail'),
    # localhost:8000/movies/{mk}/comments/?start={}&pagesize={}&q={}
    path('<int:mk>/comments/', views.comments, name='comments')
]