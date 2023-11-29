from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .forms import AddProductForm
from .models import Product, Category, Contact
from .utils import MenuMixin


class IndexTemplateView(MenuMixin, TemplateView):
    template_name = 'catalog/index.html'
    page_title = 'Главная страница'
    page_description = 'Skystore - это интернет-магазин'


class ProductListView(MenuMixin, ListView):
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    paginate_by = 6
    page_title = 'Каталог'
    page_description = ('Skystore - это отличный вариант хранения ваших вещей '
                        'и примеров товаров, который вы бы хотели продать')

    def get_queryset(self):
        return Product.published.all().order_by('-time_update').select_related('category')


class ContactsView(MenuMixin, ListView):
    model = Contact
    template_name = 'catalog/contacts.html'
    page_title = 'Контакты'
    page_description = 'Мы всегда рады обратной связи'

    def post(self, request):
        form_data = request.POST
        [print(i, form_data.get(i)) for i in ('name', 'phone', 'message')]
        return self.get(request)


class ProductDetailView(MenuMixin, DetailView):
    template_name = 'catalog/product.html'
    pk_url_kwarg = 'product_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, pk=self.kwargs['product_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,
                                      title=f'Страница с описанием продукта: {self.object.title}',
                                      )

    def post(self, request, product_id):
        print(f'Пользователь нажал на кнопку купить, товар с id: {self.request.POST.get("button_buy")}')
        return self.get(request)


class CategoryListView(MenuMixin, ListView):
    template_name = 'catalog/category.html'
    page_title = 'Категории'
    page_description = 'Таблица всех категорий продуктов на сайте'

    def get_queryset(self):
        return Category.objects.annotate(total_products=Count('products'),
                                         total_price=Sum('products__price')
                                         ).order_by('pk')


class CategoryDetailView(MenuMixin, DetailView):
    template_name = 'catalog/list_category.html'
    pk_url_kwarg = 'category_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Category, pk=self.kwargs['category_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.get_object()
        products = Product.objects.filter(category=category).select_related('category')
        paginator = Paginator(products, per_page=3)
        page_num = self.request.GET.get('page')
        page_obj = paginator.get_page(page_num)

        return self.get_mixin_context(context,
                                      title=f'Категория: {self.object.title}',
                                      paginator=paginator,
                                      page_obj=page_obj
                                      )


class ProductCreateView(MenuMixin, CreateView):
    form_class = AddProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:catalog')
    page_title = 'Добавить продукт'
    page_description = 'Здесь можно добавить новый продукт, чтобы он появился на сайте'
