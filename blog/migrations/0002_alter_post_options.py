# Generated by Django 4.2.7 on 2023-12-22 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['time_create'], 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
    ]