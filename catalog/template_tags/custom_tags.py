import os

from django.template.defaulttags import register
from django.utils.safestring import mark_safe

from catalog.models import Contact


@register.filter
def get_item(iterable: dict, key):
    if isinstance(iterable, dict):
        return iterable.get(key)
    elif isinstance(iterable, list):
        return iterable[int(key)]


@register.filter
def list_breaks(string: str):
    return string.split(';')


@register.inclusion_tag('catalog/includes/contact_info.html')
def contact_info():
    contacts = Contact.objects.filter(pk=1).first()
    if contacts:
        contact = (
            ('Страна', contacts.city),
            ('ИНН', contacts.inn),
            ('Адрес', contacts.address),
        )
    else:
        contact = None

    return {'contacts': contact}


@register.inclusion_tag('catalog/includes/button_navigation.html', name='btn_nav')
def button_navigation(paginator, page_obj):
    return {'paginator': paginator, 'page_obj': page_obj}


@register.filter
def file_exists(path):
    return os.path.exists(path)


@register.filter
def get_name_or_email(user, default='Неизвестно'):
    if user:
        return user.username or user.email or default
    return default
