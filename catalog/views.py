from django.shortcuts import render

from catalog.utils import create_product, format_to_row

url_list = {}


def append_url_list(url, title, description):
    url_list[url] = [title, description]

    def wrapper(func):
        def inner(request, *args, **kwargs):
            return func(request, *args, **kwargs)

        return inner

    return wrapper


# Create your views here.
@append_url_list(url='/',
                 title='Каталог',
                 description='Skystore - это отличный вариант хранения ваших вещей '
                             'и примеров товаров, который вы бы хотели продать',
                 )
def index(request):
    """ Функция представляет собой домашнюю страницу с каталогом продуктов """

    if request.method == 'POST':
        products_ids = request.POST.getlist('product_ids')
        print('Пользователь выбрал продукты с ID:', ', '.join(products_ids))

    random_products = create_product()
    formatted_products = format_to_row(random_products, 4)
    return render(request, 'catalog/index.html', {'lst': url_list, 'products': formatted_products})


@append_url_list(url='/contacts/',
                 title='Контакты',
                 description='',
                 )
def contacts(request):
    """ Функция представляет собой страницу с контактами для обратной связи """

    if request.method == 'POST':
        form_data = request.POST
        name = form_data.get('name')
        phone = form_data.get('phone')
        message = form_data.get('message')
        print(name, phone, message)

    return render(request, 'catalog/contacts.html', {'lst': url_list})
