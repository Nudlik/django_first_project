from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView

from .forms import AddProductForm
from .models import Product, Category

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Каталог', 'url_name': 'catalog'},
    {'title': 'Категории', 'url_name': 'category'},
    {'title': 'Добавить продукт', 'url_name': 'add_product'},
    {'title': 'Контакты', 'url_name': 'contacts'},
]


class IndexTemplateView(TemplateView):
    template_name = 'catalog/index.html'
    extra_context = {
        'title': 'Главная страница',
        'description': 'Skystore - это интернет-магазин',
        'menu': menu
    }


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    paginate_by = 6
    extra_context = {
        'title': 'Каталог',
        'description': 'Skystore - это отличный вариант хранения ваших вещей '
                       'и примеров товаров, который вы бы хотели продать',
        'menu': menu,
    }

    def get_queryset(self):
        return Product.published.all().order_by('-time_update').select_related('category')


class ContactsView(View):
    data = {
        'title': 'Контакты',
        'description': 'Мы всегда рады обратной связи',
        'menu': menu,
    }

    def get(self, request):
        return render(request, 'catalog/contacts.html', context=self.data)

    def post(self, request):
        form_data = request.POST
        [print(i, form_data.get(i)) for i in ('name', 'phone', 'message')]
        return render(request, 'catalog/contacts.html', context=self.data)


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

    category = Category.objects.annotate(total_products=Count('products'),
                                         total_price=Sum('products__price')
                                         ).order_by('pk')

    data = {
        'title': 'Категории',
        'description': 'Таблица всех категорий продуктов на сайте',
        'menu': menu,
        'category': category,
    }

    return render(request, 'catalog/category.html', context=data)


def category_by_id(request: HttpRequest, category_id: int) -> HttpResponse:
    """ Функция представляет собой страницу с категорией продуктов """

    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category).select_related('category')

    paginator = Paginator(products, per_page=3)
    page_id = request.GET.get('page')
    page = paginator.get_page(page_id)

    data = {
        'title': f'Категория: {category.title}',
        'menu': menu,
        'products': page,
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
        'description': 'Здесь можно добавить новый продукт, чтобы он появился на сайте',
        'menu': menu,
        'form': form,
    }

    return render(request, 'catalog/add_product.html', context=data)
