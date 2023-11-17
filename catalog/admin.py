from django.contrib import admin

from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'price', 'category', 'is_published']
    list_filter = ['is_published', 'category']
    search_fields = ['title', 'description']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title']
    search_fields = ['title', 'description']
