from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AddProductForm
from .models import Product, Category

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Каталог', 'url_name': 'catalog'},
    {'title': 'Категории', 'url_name': 'category'},
    {'title': 'Добавить продукт', 'url_name': 'add_product'},
    {'title': 'Контакты', 'url_name': 'contacts'},
]


def index(request: HttpRequest) -> HttpResponse:
    """ Функция представляет собой домашнюю страницу с главной страницей """

    data = {
        'url': '/',
        'title': 'Главная страница сайта',
        'description': 'Skystore - это интернет-магазин',
        'menu': menu,
    }

    return render(request, 'catalog/index.html', context=data)


def catalog(request: HttpRequest) -> HttpResponse:
    """ Функция представляет собой домашнюю страницу с каталогом продуктов """

    products = Product.published.all().order_by('-time_update')
    paginator = Paginator(products, per_page=6)
    page_id = request.GET.get('page')
    page = paginator.get_page(page_id)

    data = {
        'url': 'catalog/',
        'title': 'Каталог',
        'description': 'Skystore - это отличный вариант хранения ваших вещей '
                       'и примеров товаров, который вы бы хотели продать',
        'menu': menu,
        'products': page,
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


def show_product(request: HttpRequest, product_id: int) -> HttpResponse:
    """ Функция представляет собой страницу с конкретным продуктом """

    if request.method == 'POST':
        if request.POST.get('button_buy'):
            product = Product.objects.get(pk=product_id)
            print(f'Пользователь нажал на кнопку купить: {product}')

    only_product = get_object_or_404(Product, pk=product_id)

    data = {
        'title': f'Страница с описанием продукта: {only_product.title}',
        'menu': menu,
        'product': only_product,
    }

    return render(request, 'catalog/product.html', context=data)


def show_category(request: HttpRequest) -> HttpResponse:
    """ Функция представляет собой страницу с категорией продуктов """

    category = Category.objects.all().order_by('pk')

    data = {
        'title': 'Категории',
        'menu': menu,
        'category': category,
    }

    return render(request, 'catalog/category.html', context=data)


def category_by_id(request: HttpRequest, category_id: int) -> HttpResponse:
    """ Функция представляет собой страницу с категорией продуктов """

    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)

    data = {
        'title': f'Категория: {category.title}',
        'menu': menu,
        'products': products,
    }

    return render(request, 'catalog/list_category.html', context=data)


def add_product(request: HttpRequest) -> HttpResponse:
    """ Функция представляет собой страницу добавления продукта """

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Product.objects.create(**form.cleaned_data)
                return redirect('catalog')
            except Exception as e:
                print(e)
                form.add_error(None, f'Ошибка добавления продукта: {e}')
    else:
        form = AddProductForm()

    data = {
        'title': 'Добавить продукт',
        'menu': menu,
        'form': form,
    }

    return render(request, 'catalog/add_product.html', context=data)
