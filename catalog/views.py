from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

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


class ProductDetailView(DetailView):
    template_name = 'catalog/product.html'
    pk_url_kwarg = 'product_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, pk=self.kwargs['product_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница с описанием продукта: {self.object.title}'
        context['menu'] = menu
        return context

    def post(self, request, product_id):
        print(f'Пользователь нажал на кнопку купить, товар с id: {self.request.POST.get("button_buy")}')
        return self.get(request)


class CategoryListView(ListView):
    template_name = 'catalog/category.html'
    extra_context = {
        'title': 'Категории',
        'description': 'Таблица всех категорий продуктов на сайте',
        'menu': menu,
    }

    def get_queryset(self):
        return Category.objects.annotate(total_products=Count('products'),
                                         total_price=Sum('products__price')
                                         ).order_by('pk')


class CategoryDetailView(DetailView):
    template_name = 'catalog/list_category.html'
    pk_url_kwarg = 'category_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Category, pk=self.kwargs['category_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.get_object()
        products = Product.objects.filter(category=category).select_related('category')
        paginator = Paginator(products, per_page=3)
        page_id = self.request.GET.get('page')
        page_obj = paginator.get_page(page_id)

        context['title'] = f'Категория: {self.object.title}'
        context['menu'] = menu
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        return context


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
