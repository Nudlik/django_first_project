from django.template.defaulttags import register


@register.filter
def get_item(iterable: dict, key):
    if isinstance(iterable, dict):
        return iterable.get(key)
    elif isinstance(iterable, list):
        return iterable[int(key)]


@register.filter
def list_breaks(string: str):
    lst = string.replace('[\'', '').replace('\']', '').split('\', \'')
    return lst
