import random

from django.core.cache import cache
from django.db import transaction
from django.db.models import QuerySet, Model
from django.http import Http404
from django.shortcuts import _get_queryset

from catalog.forms import ProductVersionFormSet
from config import settings


def create_product(size: int = 10) -> tuple:
    """ Функция для создания продуктов. """

    category = ['Одежда', 'Электроника', 'Аксессуары', 'Инструменты', 'Спорт', 'Игры', 'Книги']

    products = {
        'Одежда': ['Джинсы', 'Юбка', 'Носки', 'Обувь', 'Шапка', 'Брюки', 'Шорты', 'Пальто', 'Свитер', 'Платье',
                   'Футболка', 'Блузка', 'Куртка'],
        'Электроника': ['Смарт-часы', 'Смартфон', 'Ноутбук', 'Наушники', 'Планшет',
                        'Плазменная панель', 'Клавиатура', 'Мышка'],
        'Аксессуары': ['Очки', 'Шарф', 'Ремень', 'Зонт', 'Сумка', 'Подставка', 'Подставка для ноутбука', 'Коврик'],
        'Инструменты': ['Ножницы', 'Отвертка', 'Шуруп', 'Ножовка', 'Молоток', 'Электродрель', 'Паяльник', 'Клещи',
                        'Шуруповерт', 'Киянка', 'Пила', 'Нож', 'Гаечный ключ', 'Мерный ленточный нож'],
        'Спорт': ['Мяч', 'Ворота', 'Теннисная ракетка', 'Баскетбольное кольцо', 'Футбольные бутсы', 'Бейсбольная бита'],
        'Игры': ['Монополия', 'Шахматы', 'Карточные игры', 'Дженга', 'Мафия', 'Крокодил', 'Машина времени'],
        'Книги': ['1984', 'Убить пересмешника', 'Война и мир', 'Гарри Поттер и философский камень',
                  'Преступление и наказание', 'Мастер и Маргарита', 'Три товарища', 'Алиса в Стране чудес',
                  'Властелин колец: Братство кольца', 'Дюна'],
    }
    lst_price = [10.99, 19.99, 25.99, 14.99, 9.99, 29.99, 12.99, 22.99, 17.99, 27.99, 32.99, 16.99, 21.99, 24.99, 18.99,
                 11.99, 15.99, 20.99, 26.99, 13.99, 23.99, 28.99, 30.99, 31.99, 34.99, 37.99, 39.99, 33.99, 36.99,
                 35.99]
    lst_description = ['Эксклюзивный продукт высокого качества',
                       'Инновационное решение для повседневного использования', 'Непревзойденное мастерство и дизайн',
                       'Элегантный и стильный аксессуар для вашего образа',
                       'Идеальное сочетание комфорта и функциональности', 'Ультра-прочный материал для долговечности',
                       'Неподвластный времени и износу', 'Превосходное качество звука для истинных ценителей музыки',
                       'Высокая степень надежности и безопасности',
                       'Профессиональное оборудование для опытных пользователей',
                       'Экологически чистый и устойчивый к продолжительному использованию',
                       'Интеллектуальные функции для повышения эффективности', 'Эксклюзивный дизайн, созданный для вас',
                       'Роскошный внешний вид и впечатляющие характеристики',
                       'Премиальные материалы и отличная отделка',
                       'Интуитивно понятный интерфейс для простого использования',
                       'Продукт, соответствующий самым высоким стандартам качества', 'Уникальный и неповторимый стиль',
                       'Оригинальное решение для повседневного комфорта',
                       'Максимальная производительность и скорость работы',
                       'Эксклюзивное предложение для истинных ценителей',
                       'Многофункциональный и удобный в использовании', 'Превосходное качество сборки и отделки',
                       'Высокая степень прочности и устойчивости', 'Современный дизайн и передовые технологии',
                       'Изысканный и роскошный аксессуар для вашего стиля', 'Производительность на высшем уровне',
                       'Надежное решение для повседневного использования', 'Уникальные функции и возможности',
                       'Элегантное решение для вашего пространства', 'Инновационные технологии и стильный дизайн']

    res_products = []
    res_categories = set()
    for id_ in range(size):
        dict_product = {}
        category_title = random.choice(category)
        res_categories.add(category_title)

        product_title = random.choice(products[category_title]),
        product_price = random.choice(lst_price),
        product_description = random.sample(lst_description, random.randint(2, 5))

        dict_product['title'] = product_title[0]
        dict_product['price'] = product_price[0]
        dict_product['description'] = ';'.join(product_description)
        dict_product['category'] = category_title
        res_products.append(dict_product)

    return res_categories, res_products


class MenuMixin:
    page_title: str = None
    page_description: str = None

    def get_mixin_context(self, context: dict, **kwargs) -> dict:
        context.update(kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.page_title is not None:
            context['title'] = self.page_title

        if self.page_description is not None:
            context['description'] = self.page_description

        return context


class VersionMixin:

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            formset = ProductVersionFormSet(self.request.POST, instance=self.object)
        else:
            formset = ProductVersionFormSet(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        with transaction.atomic():
            if form.is_valid():
                self.object = form.save()  # Product
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()  # Version
                else:
                    return self.form_invalid(form)

        return super().form_valid(form)


def cache_for_queryset(key: str, queryset: QuerySet, time: int = settings.CACHE_TIMEOUT) -> QuerySet:
    """ Кеширует queryset запрос к базе данных """

    if not settings.CACHES_ENABLED:
        return queryset
    queryset_cache = cache.get(key)
    if queryset_cache is not None:
        return queryset_cache
    cache.set(key, queryset, time)
    return queryset


def cache_for_object(klass, *args, **kwargs) -> QuerySet | Model | Http404:
    """ Кеширует object запрос к базе данных или возвращает 404 """

    queryset = _get_queryset(klass)
    if not hasattr(queryset, "get"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        queryset = queryset.get(*args, **kwargs)
        pk = queryset.pk
        return cache_for_queryset(f"{klass.__name__}_{pk}", queryset)
    except queryset.model.DoesNotExist:
        raise Http404(
            "No %s matches the given query." % queryset.model._meta.object_name
        )
