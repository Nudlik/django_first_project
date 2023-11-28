from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from catalog import views

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='home'),
    path('catalog/', views.ProductListView.as_view(), name='catalog'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('catalog/<int:product_id>/', views.ProductDetailView.as_view(), name='product'),
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('category/<int:category_id>/', views.CategoryDetailView.as_view(), name='category_by_id'),
    path('add_product/', views.add_product, name='add_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
