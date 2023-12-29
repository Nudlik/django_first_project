from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    avatar = models.ImageField(**NULLABLE, upload_to='photos/users/avatars/%Y/%m/%d', verbose_name='Аватар')
    phone = models.CharField(**NULLABLE, max_length=35, verbose_name='Телефон')
    country = models.CharField(**NULLABLE, max_length=150, verbose_name='Страна')
    email = models.EmailField(max_length=50, unique=True, verbose_name='Электронная почта')
    email_verify = models.BooleanField(default=False)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        **NULLABLE,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
