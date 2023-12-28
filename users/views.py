from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from users.forms import UserLoginFrom, UserRegisterFrom, UserProfileUpdateFrom, UserProfileForm, UserPasswordChangeForm


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
    model = get_user_model()
    success_url = reverse_lazy('user:login')
    extra_context = {
        'title': 'Регистрация',
        'button': 'Зарегистрироваться',
    }


class UserProfileView(LoginRequiredMixin, DetailView):
    form_class = UserProfileForm
    extra_context = {
        'title': 'Мой профиль',
        'button': 'Редактировать',
    }

    def get_object(self, queryset=None):
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileUpdateFrom
    extra_context = {
        'title': 'Редактирование профиля',
        'button': 'Сохранить',
    }

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {
        'title': 'Смена пароля',
        'button': 'Сохранить',
    }


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'
    extra_context = {
        'title': 'Ваш пароль был успешно изменен!',
        'button': 'Вернуться в профиль',
    }
