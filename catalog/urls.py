from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='home'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),

    path('category/', views.CategoryListView.as_view(), name='list_category'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='view_category'),

    path('catalog/', views.ProductListView.as_view(), name='list_product'),
    path('create-product/', views.ProductCreateView.as_view(), name='create_product'),
    path('catalog/<int:pk>/', views.ProductDetailView.as_view(), name='view_product'),
    path('catalog/<int:pk>/update/', views.ProductUpdateView.as_view(), name='update_product'),
    path('catalog/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete_product'),
]

