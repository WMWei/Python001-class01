from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from .form import LoginForm


@login_required
def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_info = form.cleaned_data
            is_user = authenticate(
                username=login_info['username'],
                password=login_info['password'],
            )
            if is_user:
                login(request, is_user)
                messages.success(request, '登录成功')
                return redirect(f'{reverse("myapp:home")}')
            else:
                messages.error(request, '用户名或者密码错误')
                return render(
                    request,
                    'login.html',
                    locals(),
                )
    # 如果是get请求，返回登录的表单页面
    if request.method == 'GET':
        form = LoginForm()
        return render(
            request,
            'login.html',
            locals(),
        )