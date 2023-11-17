from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.utils import format_to_row
from .models import Product, Contact

menu = [
    {'title': 'Каталог', 'url_name': 'home'},
    {'title': 'Контакты', 'url_name': 'contacts'},
]


def index(request: HttpRequest) -> HttpResponse:
    """ Функция представляет собой домашнюю страницу с каталогом продуктов """

    if request.method == 'POST':
        products_ids = request.POST.getlist('product_ids')
        print('Пользователь выбрал продукты с ID:', ', '.join(products_ids))

    products = Product.published.all().order_by('-time_update')
    formatted_products = format_to_row(products, 4)

    data = {
        'url': '/',
        'title': 'Каталог',
        'description': 'Skystore - это отличный вариант хранения ваших вещей '
                       'и примеров товаров, который вы бы хотели продать',
        'menu': menu,
        'products': formatted_products
    }

    return render(request, 'catalog/index.html', context=data)


def contacts(request: HttpRequest) -> HttpResponse:
    """ Функция представляет собой страницу с контактами для обратной связи """

    if request.method == 'POST':
        form_data = request.POST
        name = form_data.get('name')
        phone = form_data.get('phone')
        message = form_data.get('message')
        print(name, phone, message)

    contacts_ = get_object_or_404(Contact, pk=1)

    data = {
        'url': '/contacts/',
        'title': 'Контакты',
        'description': '',
        'menu': menu,
        'contacts': contacts_,
    }

    return render(request, 'catalog/contacts.html', context=data)
