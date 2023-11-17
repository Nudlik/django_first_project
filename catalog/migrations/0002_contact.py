# Generated by Django 4.2.7 on 2023-11-17 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50, verbose_name='Город')),
                ('inn', models.CharField(max_length=50, unique=True, verbose_name='ИНН')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Контакт',
                'verbose_name_plural': 'Контакты',
                'ordering': ['city'],
            },
        ),
    ]
