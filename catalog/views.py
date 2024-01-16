from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView

from config import settings
from .forms import AddProductForm
from .models import Product, Category, Contact
from .utils import MenuMixin, VersionMixin, cache_for_queryset


class IndexTemplateView(MenuMixin, TemplateView):
    template_name = 'catalog/index.html'
    page_title = 'Главная страница'
    page_description = 'Skystore - это интернет-магазин'


class ContactsView(MenuMixin, ListView):
    model = Contact
    page_title = 'Контакты'
    page_description = 'Мы всегда рады обратной связи'

    def post(self, request):
        form_data = request.POST
        [print(i, form_data.get(i)) for i in ('name', 'phone', 'message')]
        return self.get(request)


class CategoryListView(MenuMixin, ListView):
    page_title = 'Категории'
    page_description = 'Таблица всех категорий продуктов на сайте'

    def get_queryset(self):
        queryset = cache_for_queryset(
            key=settings.CACHE_CATEGORY_LIST,
            queryset=Category.objects.annotate(
                total_products=Count('products'),
                total_price=Sum('products__price')
            ).order_by('pk')
        )
        return queryset


class CategoryDetailView(MenuMixin, DetailView):

    def get_object(self, queryset=None):
        return get_object_or_404(Category, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.get_object()
        products = cache_for_queryset(
            key=settings.CACHE_CATEGORY_PRODUCTS,
            queryset=Product.objects.filter(category=category).select_related('category')
        )
        paginator = Paginator(products, per_page=3)
        page_num = self.request.GET.get('page')
        page_obj = paginator.get_page(page_num)

        return self.get_mixin_context(context,
                                      title=f'Категория: {self.object.title}',
                                      paginator=paginator,
                                      page_obj=page_obj
                                      )


class ProductListView(MenuMixin, ListView):
    paginate_by = 6
    page_title = 'Каталог'
    page_description = ('Skystore - это отличный вариант хранения ваших вещей '
                        'и примеров товаров, который вы бы хотели продать')

    def get_queryset(self):
        queryset = cache_for_queryset(
            key=settings.CACHE_PRODUCT_LIST,
            queryset=Product.objects.filter(version__is_active=True).order_by('-time_update').select_related('category')
        )
        return queryset


class ProductDetailView(MenuMixin, DetailView):

    def get_object(self, queryset=None):
        return get_object_or_404(Product, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=f'Страница с описанием продукта: {self.object.title}')

    def post(self, request, pk):
        print(f'Пользователь нажал на кнопку купить, товар с id: {self.request.POST.get("button_buy")}')
        return self.get(request)


class ProductCreateView(LoginRequiredMixin, MenuMixin, VersionMixin, CreateView):
    model = Product
    form_class = AddProductForm
    page_title = 'Добавить продукт'
    page_description = 'Здесь можно добавить новый продукт, чтобы он появился на сайте'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        cache.delete(settings.CACHE_PRODUCT_LIST)
        return reverse('catalog:list_product')


class ProductUpdateView(UserPassesTestMixin, MenuMixin, VersionMixin, UpdateView):
    model = Product
    form_class = AddProductForm
    page_title = 'Страница для редактирования продукта'
    page_description = 'Здесь можно редактировать информацию о продукте'

    def get_queryset(self):
        return Product.objects.filter(pk=self.kwargs['pk'])

    def get_success_url(self):
        cache.delete(settings.CACHE_PRODUCT_LIST)
        return reverse('catalog:view_product', kwargs={'pk': self.object.pk})

    def test_func(self):
        check_perms = bool(
            self.get_object().owner == self.request.user
            or self.request.user.is_superuser
            or self.request.user.has_perms(['catalog.change_product'])
        )
        return check_perms

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user != self.get_object().owner:
            fields = [i for i in form.fields]
            for field in fields:
                if not self.request.user.has_perm(f'catalog.set_{field}'):
                    del form.fields[field]
        return form


class ProductDeleteView(UserPassesTestMixin, MenuMixin, DeleteView):
    model = Product
    page_title = 'Страница для удаление статьи'

    def test_func(self):
        check_perms = bool(
            self.get_object().owner == self.request.user
            or self.request.user.is_superuser
            or self.request.user.has_perms(['catalog.delete_product'])
        )
        return check_perms

    def get_success_url(self):
        cache.delete(settings.CACHE_PRODUCT_LIST)
        return reverse('catalog:list_product')
