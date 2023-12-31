import os

from django.template.defaulttags import register

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
    contacts = Contact.objects.filter(pk=1)

    if contacts.exists():
        contact = (
            ('Страна', contacts[0].city),
            ('ИНН', contacts[0].inn),
            ('Адрес', contacts[0].address),
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
