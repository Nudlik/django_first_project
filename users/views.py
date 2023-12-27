from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserLoginFrom, UserRegisterFrom


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginFrom
    extra_context = {
        'title': 'Авторизация',
        'button': 'Войти',
    }


class UserLogoutView(LogoutView):
    pass


class UserRegisterView(CreateView):
    form_class = UserRegisterFrom
    template_name = 'users/register.html'
    success_url = reverse_lazy('user:login')
    extra_context = {
        'title': 'Регистрация',
        'button': 'Зарегистрироваться',
    }
