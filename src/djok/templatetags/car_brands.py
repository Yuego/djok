"""Template tags для отображения иконок автомобильных брендов (PNG).

    {% load car_brands %}
    {% car_brand_icon item.brand %}                 {# 24px высота #}
    {% car_brand_icon item.brand "me-1" %}          {# с CSS-классом #}
    {% car_brand_icon item.brand "me-1" 64 %}       {# 64px высота #}
    {% car_brand_icon_with_name item.brand %}       {# иконка + текст #}
    {{ item.brand|brand_id }}                       {# raw slug или '' #}

Иконки лежат в STATIC/frontend/car-brands/<slug>.png (источник
car-logos-dataset, ~387 брендов).
"""
from django import template
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from djok.car_brands import brand_id as _brand_id

register = template.Library()

DEFAULT_HEIGHT = 24
MAX_HEIGHT = 128


def _clamp_height(height) -> int:
    """Высота иконки в px. Защита от слишком больших значений."""
    try:
        h = int(height) if height else DEFAULT_HEIGHT
    except (TypeError, ValueError):
        h = DEFAULT_HEIGHT
    if h <= 0:
        h = DEFAULT_HEIGHT
    return min(h, MAX_HEIGHT)


@register.simple_tag
def car_brand_icon(brand: str, css_class: str = '', height=DEFAULT_HEIGHT) -> str:
    """PNG-иконка бренда. Если бренда нет в наборе — пустая строка.

    Args:
        brand: текстовое имя (любой регистр/раскладка).
        css_class: дополнительные CSS-классы (например 'me-1').
        height: высота в пикселях, default 24, ограничено сверху MAX_HEIGHT=128.
    """
    bid = _brand_id(brand or '')
    if not bid:
        return ''
    h = _clamp_height(height)
    src = static(f'frontend/car-brands/{bid}.png')
    return format_html(
        '<img src="{}" alt="{}" title="{}" class="{}" '
        'style="height:{}px;width:auto;" loading="lazy">',
        src, brand, brand, css_class, h,
    )


@register.simple_tag
def car_brand_icon_with_name(brand: str, css_class: str = '', height=DEFAULT_HEIGHT) -> str:
    """Иконка бренда + текст рядом. Если бренда нет в наборе — только текст."""
    if not brand:
        return mark_safe('<span class="text-body-secondary">—</span>')
    icon = car_brand_icon(brand, css_class=css_class, height=height)
    if icon:
        return format_html(
            '<span class="d-inline-flex align-items-center gap-1">{}<span>{}</span></span>',
            icon, brand,
        )
    return format_html('<span>{}</span>', brand)


@register.filter
def brand_id(value: str) -> str:
    """Filter: бренд → slug (или ''). Полезен в условиях шаблона."""
    return _brand_id(value or '')
