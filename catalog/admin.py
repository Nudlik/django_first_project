from django import forms
from django.contrib import admin

from catalog.forms import VersionForm, ProductValidateMixin
from .models import Product, Category, Contact, Version


class VersionInline(admin.StackedInline):
    model = Version
    form = VersionForm
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = type('ProductAdminForm', (forms.ModelForm, ProductValidateMixin), {})
    list_display = ['title', 'price', 'category', 'is_published']
    list_filter = ['is_published', 'category']
    search_fields = ['title', 'description']
    list_display_links = ['title']
    ordering = ['-time_update']
    inlines = [
        VersionInline,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title', 'description']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['city', 'inn', 'address']
    search_fields = ['city']


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product', 'version_number', 'title', 'is_active']
    search_fields = ['title', 'product__title']
