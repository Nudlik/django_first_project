# Generated by Django 4.2.7 on 2023-12-27 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True, verbose_name='URL')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Содержание')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('photo', models.ImageField(blank=True, default=None, null=True, upload_to='photos/blog/%Y/%m/%d/', verbose_name='Фото')),
                ('view_count', models.IntegerField(default=0, verbose_name='Количество просмотров')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ['time_create'],
            },
        ),
    ]
