from django.core.management import BaseCommand, call_command
from django.db import connection

from blog.models import Post
from catalog.models import Category, Product
from users.models import User


class Command(BaseCommand):
    help = 'Очищает и добавляет данные с фикстуры в БД'

    def handle(self, *args, **kwargs):
        models = (
            Product,
            Category,
            Post,
            User,
        )
        for model in models:
            model.objects.all().delete()
            table_name = model._meta.db_table

            # сбрасываем счетчик
            with connection.cursor() as cursor:
                query = f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), 1, false);"
                cursor.execute(query)

        call_command('loaddata', 'catalog/fixtures/catalog_data.json')
        call_command('loaddata', 'blog/fixtures/blog_data.json')
        call_command('loaddata', 'users/fixtures/users_data.json')
