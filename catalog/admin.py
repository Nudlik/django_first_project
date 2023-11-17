from django.contrib import admin

from .models import Product, Category, Contact


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'price', 'category', 'is_published']
    list_filter = ['is_published', 'category']
    search_fields = ['title', 'description']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title']
    search_fields = ['title', 'description']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['pk', 'city', 'inn', 'address']
    search_fields = ['city']
