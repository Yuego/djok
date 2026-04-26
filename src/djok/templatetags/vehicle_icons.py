"""
Template tags для иконок автомобильной специфики (hpt.svg специфичный спрайт).

    {% load vehicle_icons %}
    {% category_icon cat %}                        {# по объекту TsCategory #}
    {% category_icon "M1" %}                       {# по short_name #}
    {{ "M1G"|category_icon_id }}                   {# raw id для use #}
    {% spec_icon "vin" %}                          {# spec-vin из hpt.svg #}
    {% part_icon "engine" %}                       {# part-engine из hpt.svg #}
    {% doc_type_icon "otts" %}                     {# otts из hpt.svg #}

Спрайт: STATIC/frontend/icons/hpt.svg.
"""
from django import template
from django.templatetags.static import static
from django.utils.html import format_html

register = template.Library()


# ─── Категории ТС: short_name → доступный id в спрайте ─────────────────
# В спрайте: category-l1, l3, m1-m3, n1-n3, o1-o4.
# Отсутствуют L2, L4-L7 (мопеды/мотоциклы) — fallback на ближайший.
_CATEGORY_MAP = {
    'L1': 'category-l1',
    'L2': 'category-l1',
    'L3': 'category-l3',
    'L4': 'category-l3',
    'L5': 'category-l3',
    'L6': 'category-l3',
    'L7': 'category-l3',
    'M1': 'category-m1',
    'M1G': 'category-m1',
    'M2': 'category-m2',
    'M2C': 'category-m2',
    'M2G': 'category-m2',
    'M3': 'category-m3',
    'N1': 'category-n1',
    'N1G': 'category-n1',
    'N2': 'category-n2',
    'N2G': 'category-n2',
    'N3': 'category-n3',
    'N3G': 'category-n3',
    'O1': 'category-o1',
    'O2': 'category-o2',
    'O3': 'category-o3',
    'O4': 'category-o4',
}


def _category_id(value) -> str:
    """value — TsCategory или строка short_name."""
    if value is None:
        return ''
    short = getattr(value, 'short_name', value)
    if not short:
        return ''
    return _CATEGORY_MAP.get(str(short).upper(), '')


def _hpt_svg(symbol_id: str, css_class: str = 'icon', label: str = '') -> str:
    sprite_url = static('frontend/icons/hpt.svg')
    return format_html(
        '<svg class="{}" role="img" aria-label="{}" title="{}">'
        '<use xlink:href="{}#{}"></use>'
        '</svg>',
        css_class, label or symbol_id, label or symbol_id, sprite_url, symbol_id,
    )


@register.simple_tag
def category_icon(value, css_class: str = 'icon') -> str:
    """SVG-иконка категории ТС. Принимает TsCategory или short_name."""
    sid = _category_id(value)
    if not sid:
        return ''
    label = getattr(value, 'name', None) or getattr(value, 'short_name', None) or str(value)
    return _hpt_svg(sid, css_class=css_class, label=label)


@register.filter
def category_icon_id(value) -> str:
    """Filter: TsCategory/short_name → id в спрайте."""
    return _category_id(value)


@register.simple_tag
def spec_icon(name: str, css_class: str = 'icon', label: str = '') -> str:
    """SVG-иконка спецификации (spec-co2, spec-power, spec-vin, и т.д.)."""
    if not name:
        return ''
    sid = name if name.startswith('spec-') else f'spec-{name}'
    return _hpt_svg(sid, css_class=css_class, label=label or sid)


@register.simple_tag
def part_icon(name: str, css_class: str = 'icon', label: str = '') -> str:
    """SVG-иконка узла ТС (part-engine, part-brakes, part-wheel, и т.д.)."""
    if not name:
        return ''
    sid = name if name.startswith('part-') else f'part-{name}'
    return _hpt_svg(sid, css_class=css_class, label=label or sid)


@register.simple_tag
def doc_type_icon(name: str, css_class: str = 'icon', label: str = '') -> str:
    """SVG-иконка типа документа (otts, sbkts, otsh, sut, zoets, certificate, declaration, ...)."""
    if not name:
        return ''
    return _hpt_svg(name.lower(), css_class=css_class, label=label or name)
