from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from catalog import views

urlpatterns = [
    path('', views.index, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('contacts/', views.contacts, name='contacts'),
    path('catalog/<int:product_id>/', views.show_product, name='product'),
    path('category/', views.show_category, name='category'),
    path('category/<int:category_id>/', views.category_by_id, name='category_by_id'),
    path('add_product/', views.add_product, name='add_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
