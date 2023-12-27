from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class WidgetsMixin:

    class Meta:
        widgets = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widgets = self.Meta.widgets
        if widgets:
            for field_name, widget in widgets.items():
                self.fields[field_name].widget = widget


class LabelsMixin:

    class Meta:
        labels = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = self.Meta.labels
        if labels:
            for field_name, label in labels.items():
                self.fields[field_name].label = label


class UserLoginFrom(WidgetsMixin, LabelsMixin, AuthenticationForm):

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'username', 'username1']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш логин'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ваш пароль'}),
        }
        labels = {
            'username': 'Логин / E-mail',
        }


class UserRegisterFrom(WidgetsMixin, UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш логин'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ваш пароль'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
        }
        labels = {
            'username': 'Логин',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким E-mail уже существует')
        return email

