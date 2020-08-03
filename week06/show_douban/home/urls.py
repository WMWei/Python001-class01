from django.urls import path

from . import views


app_name = 'home'

urlpatterns = [
    # localhost:8000/
    path('', views.home, name='home'),
]