from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=150,
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput,
        min_length=8,
    )