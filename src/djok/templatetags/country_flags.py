"""
Template tags для отображения флагов и названий стран.

Использование:
    {% load country_flags %}
    {% country_flag entity.country_code %}                            {# флаг 16px #}
    {% country_flag entity.country_code "icon-lg" %}                  {# с CSS-классом #}
    {% country_flag_with_name entity.country_code %}                  {# флаг + русское имя #}
    {{ entity.country_code|country_name }}                            {# только имя #}

Спрайт ожидается по пути: STATIC/frontend/icons/flags.svg
ID-шники флагов — lowercase ISO 3166-1 alpha-2 (#ru, #cn, #de, ...).
"""
from django import template
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from djok.countries import country_name as _country_name

register = template.Library()


@register.simple_tag
def country_flag(country_code: str, css_class: str = 'icon', title: str = '') -> str:
    """Рендерит флаг страны как SVG `<use>` из спрайта.

    Если country_code пуст — возвращает прочерк.
    Если title не передан — используется русское имя страны (для tooltip).

    Спрайт грузится лениво в base.html (см. блок про flags.svg). До инжекта
    SVG-элементы пустые (прозрачные). Поэтому ссылка на symbol — внутренняя
    (`#ru`), без URL.
    """
    if not country_code:
        return mark_safe('<span class="text-body-secondary">—</span>')

    code = country_code.lower().strip()
    label = title or _country_name(country_code)

    return format_html(
        '<svg class="{}" role="img" aria-label="{}" title="{}">'
        '<use xlink:href="#{}"></use>'
        '</svg>',
        css_class, label, label, code,
    )


@register.simple_tag
def country_flag_with_name(country_code: str, css_class: str = 'icon') -> str:
    """Флаг + русское имя страны рядом."""
    if not country_code:
        return mark_safe('<span class="text-body-secondary">—</span>')

    flag = country_flag(country_code, css_class=css_class)
    name = _country_name(country_code)
    return format_html('<span class="d-inline-flex align-items-center gap-1">{}<span>{}</span></span>', flag, name)


@register.filter
def country_name(country_code: str) -> str:
    """Filter: ISO-код → русское название (или сам код для неизвестных)."""
    return _country_name(country_code or '')
