from django.contrib.auth.views import LoginView, LogoutView

from users.forms import UserLoginFrom


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginFrom
    extra_context = {
        'title': 'Авторизация',
        'button': 'Войти',
    }


class UserLogoutView(LogoutView):
    pass
