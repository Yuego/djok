from django import template

register = template.Library()


@register.filter
def pluralize_ru(value, forms):
    """
    Русский pluralize с тремя формами: "1,2-4,5+".
    Usage: {{ count|pluralize_ru:"лист,листа,листов" }}
    """
    try:
        n = abs(int(value))
    except (TypeError, ValueError):
        return ''
    parts = forms.split(',')
    if len(parts) != 3:
        return ''
    one, few, many = parts
    if n % 100 in (11, 12, 13, 14):
        return many
    rem = n % 10
    if rem == 1:
        return one
    if rem in (2, 3, 4):
        return few
    return many
