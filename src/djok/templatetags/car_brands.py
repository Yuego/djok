"""
Template tags для отображения иконок автомобильных брендов из SVG-спрайта.

    {% load car_brands %}
    {% car_brand_icon item.brand %}                           {# моно-иконка 16px #}
    {% car_brand_icon item.brand "icon-lg" %}                 {# большая #}
    {% car_brand_icon_with_name item.brand %}                 {# иконка + текст #}
    {{ item.brand|brand_id }}                                 {# raw id или '' #}

Спрайт: STATIC/frontend/icons/car-brands.svg, id-шники в kebab-case.
Если бренд не найден в наборе — иконка не рендерится (только текст там, где это уместно).
"""
from django import template
from django.templatetags.static import static
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

from djok.car_brands import brand_id as _brand_id

register = template.Library()


@register.simple_tag
def car_brand_icon(brand: str, css_class: str = 'icon') -> str:
    """SVG-иконка бренда. Если бренда нет в спрайте — пустая строка."""
    bid = _brand_id(brand or '')
    if not bid:
        return ''
    sprite_url = static('frontend/icons/car-brands.svg')
    return format_html(
        '<svg class="{}" role="img" aria-label="{}" title="{}">'
        '<use xlink:href="{}#{}"></use>'
        '</svg>',
        css_class, brand, brand, sprite_url, bid,
    )


@register.simple_tag
def car_brand_icon_with_name(brand: str, css_class: str = 'icon') -> str:
    """Иконка бренда + текст рядом. Если бренда в спрайте нет — только текст."""
    if not brand:
        return mark_safe('<span class="text-body-secondary">—</span>')
    icon = car_brand_icon(brand, css_class=css_class)
    if icon:
        return format_html(
            '<span class="d-inline-flex align-items-center gap-1">{}<span>{}</span></span>',
            icon, brand,
        )
    return format_html('<span>{}</span>', brand)


@register.filter
def brand_id(value: str) -> str:
    """Filter: бренд → kebab-case id (или ''). Полезен в условиях шаблона."""
    return _brand_id(value or '')
