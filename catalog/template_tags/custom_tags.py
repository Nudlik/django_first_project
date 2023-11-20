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
        contact = {
            'city': contacts[0].city,
            'inn': contacts[0].inn,
            'address': contacts[0].address,
        }
    else:
        contact = None

    return {'contacts': contact}
