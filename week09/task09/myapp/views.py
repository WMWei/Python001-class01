from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


from .form import LoginForm


@login_required(login_url='login/')
def home(request):
    return render(request, 'home.html')


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_info = form.cleaned_data
            user = authenticate(
                username=login_info['username'],
                password=login_info['password'],
            )
            if user:
                login(request, user)
                messages.success(request, '登录成功')
                return redirect(f'{reverse("myapp:home")}', username=login_info['username'])
            else:
                messages.error(request, '用户名或者密码错误')
                return redirect(f'{reverse("myapp:login")}')
    # 如果是get请求，返回登录的表单页面
    else:
        form = LoginForm()
        return render(
            request,
            'login.html',
            locals(),
        )


# def register(request):
#     pass
#     return render(request,'register.html')

# def logout(request):
#     pass
#     return redirect('/index/')