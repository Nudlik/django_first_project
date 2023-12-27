from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    avatar = models.ImageField(**NULLABLE, upload_to='photos/users/avatars/%Y/%m/%d', verbose_name='Аватар')
    phone = models.CharField(**NULLABLE, max_length=35, verbose_name='Телефон')
    country = models.CharField(**NULLABLE, max_length=150, verbose_name='Страна')
