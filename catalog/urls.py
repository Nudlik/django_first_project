from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='home'),
    path('catalog/', views.ProductListView.as_view(), name='catalog'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('catalog/<int:product_id>/', views.ProductDetailView.as_view(), name='product'),
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('category/<int:category_id>/', views.CategoryDetailView.as_view(), name='category_by_id'),
    path('add_product/', views.ProductCreateView.as_view(), name='add_product'),
]
