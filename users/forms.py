from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class WidgetsMixin:

    class Meta:
        widgets = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widgets = self.Meta.widgets
        if widgets:
            for field_name, widget in widgets.items():
                self.fields[field_name].widget = widget


class UserLoginFrom(WidgetsMixin, AuthenticationForm):

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш логин'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ваш пароль'}),
        }

