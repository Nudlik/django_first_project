from django.core.management import BaseCommand
from django.db import connection

from catalog.models import Category, Product
from catalog.utils import create_product


class Command(BaseCommand):
    help = 'Очищает и добавляет рандомные данные в БД'

    def handle(self, *args, **kwargs):
        for model in (Product, Category):
            model.objects.all().delete()
            table_name = model._meta.db_table

            # сбрасываем счетчик
            with connection.cursor() as cursor:
                query = f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), 1, false);"
                cursor.execute(query)

        categories, products = create_product(10)

        categories = [Category(title=category) for category in categories]
        Category.objects.bulk_create(categories)

        products_ = []
        for product in products:
            cat = Category.objects.get(title=product['category'])
            product['category'] = cat
            products_.append(Product(**product))

        Product.objects.bulk_create(products_)
