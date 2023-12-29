from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView

from .forms import AddProductForm
from .models import Product, Category, Contact
from .utils import MenuMixin, VersionMixin


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
        return Category.objects.annotate(total_products=Count('products'),
                                         total_price=Sum('products__price')
                                         ).order_by('pk')


class CategoryDetailView(MenuMixin, DetailView):

    def get_object(self, queryset=None):
        return get_object_or_404(Category, pk=self.kwargs['pk'])

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


class ProductListView(MenuMixin, ListView):
    paginate_by = 6
    page_title = 'Каталог'
    page_description = ('Skystore - это отличный вариант хранения ваших вещей '
                        'и примеров товаров, который вы бы хотели продать')

    def get_queryset(self):
        return Product.objects.filter(version__is_active=True).order_by('-time_update').select_related('category')


class ProductDetailView(MenuMixin, DetailView):

    def get_object(self, queryset=None):
        return get_object_or_404(Product, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=f'Страница с описанием продукта: {self.object.title}')

    def post(self, request, pk):
        print(f'Пользователь нажал на кнопку купить, товар с id: {self.request.POST.get("button_buy")}')
        return self.get(request)


class ProductCreateView(MenuMixin, LoginRequiredMixin, VersionMixin, CreateView):
    model = Product
    form_class = AddProductForm
    success_url = reverse_lazy('catalog:list_product')
    page_title = 'Добавить продукт'
    page_description = 'Здесь можно добавить новый продукт, чтобы он появился на сайте'


class ProductUpdateView(MenuMixin, VersionMixin, UpdateView):
    model = Product
    form_class = AddProductForm
    page_title = 'Страница для редактирования продукта'
    page_description = 'Здесь можно редактировать информацию о продукте'

    def get_queryset(self):
        return Product.objects.filter(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('catalog:view_product', kwargs={'pk': self.object.pk})


class ProductDeleteView(MenuMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:list_product')
    page_title = 'Страница для удаление статьи'
