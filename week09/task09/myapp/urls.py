from django.urls import path

from . import views


app_name = 'myapp'

urlpatterns = [
    # localhost:8000/
    path('', views.home, name='home'),
    # localhost:8000/login
    path('login/', views.login_view, name='login')
]