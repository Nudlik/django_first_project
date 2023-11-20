from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Product

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Каталог', 'url_name': 'catalog'},
    {'title': 'Контакты', 'url_name': 'contacts'},
]


def index(request: HttpRequest) -> HttpResponse:

    data = {
        'url': '/',
        'title': 'Главная страница сайта',
        'description': 'Skystore - это интернет-магазин',
        'menu': menu,
    }

    return render(request, 'catalog/index.html', context=data)


def catalog(request: HttpRequest) -> HttpResponse:
    """ Функция представляет собой домашнюю страницу с каталогом продуктов """

    if request.method == 'POST':
        products_ids = request.POST.getlist('product_ids')
        print('Пользователь выбрал продукты с ID:', ', '.join(products_ids))

    products = Product.published.all().order_by('-time_update')

    data = {
        'url': 'catalog/',
        'title': 'Каталог',
        'description': 'Skystore - это отличный вариант хранения ваших вещей '
                       'и примеров товаров, который вы бы хотели продать',
        'menu': menu,
        'products': products
    }

    return render(request, 'catalog/catalog.html', context=data)


def contacts(request: HttpRequest) -> HttpResponse:
    """ Функция представляет собой страницу с контактами для обратной связи """

    if request.method == 'POST':
        form_data = request.POST
        name = form_data.get('name')
        phone = form_data.get('phone')
        message = form_data.get('message')
        print(name, phone, message)

    data = {
        'url': '/contacts/',
        'title': 'Контакты',
        'description': '',
        'menu': menu,
    }

    return render(request, 'catalog/contacts.html', context=data)
