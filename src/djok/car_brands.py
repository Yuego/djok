"""
Справочник идентификаторов автомобильных брендов в SVG-спрайте car-brands.svg.

Используется для маппинга текстового brand из tech_docs.* (часто разный регистр,
с пробелами/дефисами/тире) в id-шник спрайта (lowercase, kebab-case).
"""
from __future__ import annotations

import re
import unicodedata

__all__ = ['BRAND_IDS', 'normalize_brand', 'brand_id']


# Список идентификаторов в спрайте hpt_su/static/frontend/icons/car-brands.svg
# (имена SVG-файлов в docs/icons/car-brands).
BRAND_IDS: frozenset[str] = frozenset({
    'acura', 'alfa-romeo', 'alpine', 'aston-martin', 'audi',
    'bentley', 'bmw', 'bugatti', 'buick', 'byd',
    'cadillac', 'changan', 'chery', 'chevrolet', 'chrysler', 'citroen', 'cupra',
    'dacia', 'daihatsu', 'dodge', 'dongfeng', 'ds',
    'faw', 'ferrari', 'fiat', 'ford',
    'gac', 'gaz', 'geely', 'genesis', 'gmc',
    'haval', 'hino', 'honda', 'hyundai',
    'infiniti', 'isuzu',
    'jaguar', 'jeep',
    'kamaz', 'kia', 'koenigsegg',
    'lada', 'lamborghini', 'lancia', 'land-rover', 'lexus', 'li-auto',
    'lincoln', 'lotus', 'lucid',
    'mahindra', 'maserati', 'maybach', 'mazda', 'mclaren',
    'mercedes', 'mg', 'mini', 'mitsubishi',
    'nio', 'nissan',
    'opel',
    'pagani', 'perodua', 'peugeot', 'polestar', 'porsche', 'proton',
    'range-rover', 'renault', 'rimac', 'rivian', 'rolls-royce',
    'saab', 'seat', 'skoda', 'smart', 'ssangyong', 'subaru', 'suzuki',
    'tata', 'tesla', 'toyota',
    'uaz',
    'vinfast', 'volkswagen', 'volvo',
    'xpeng', 'zeekr',
})

# Алиасы для распространённых вариантов написания, которые не сводятся
# простой нормализацией (lowercase + замена пробелов/тире → дефис).
_ALIASES: dict[str, str] = {
    'vw': 'volkswagen',
    'volkswagen-ag': 'volkswagen',
    'mercedes-benz': 'mercedes',
    'merсedes-benz': 'mercedes',
    'mercedes-amg': 'mercedes',
    'rolls-royce-motor-cars': 'rolls-royce',
    'rolls': 'rolls-royce',
    'aston': 'aston-martin',
    'land': 'land-rover',
    'range': 'range-rover',
    'alfa': 'alfa-romeo',
    'alfaromeo': 'alfa-romeo',
    'romeo': 'alfa-romeo',
    'lada-vaz': 'lada',
    'vaz': 'lada',
    'ваз': 'lada',
    'лада': 'lada',
    'газ': 'gaz',
    'уаз': 'uaz',
    'камаз': 'kamaz',
    'tesla-motors': 'tesla',
    'mini-cooper': 'mini',
    'mercedesbenz': 'mercedes',
    'astonmartin': 'aston-martin',
    'astonmartinlagonda': 'aston-martin',
    'rangerover': 'range-rover',
    'landrover': 'land-rover',
    'rollsroyce': 'rolls-royce',
    'liauto': 'li-auto',
    'li': 'li-auto',
}


_ws_re = re.compile(r'[\s_/]+')
_dash_collapse_re = re.compile(r'-+')


def normalize_brand(value: str) -> str:
    """Приводит текстовое имя бренда к kebab-case: 'Mercedes-Benz' → 'mercedes-benz'."""
    if not value:
        return ''
    s = value.strip().lower()
    # NFKC: «не‑разрывный» дефис, фигурные тире → обычный
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('—', '-').replace('–', '-')
    # пробелы/подчёркивания/слэши → дефис
    s = _ws_re.sub('-', s)
    # схлопываем повторные дефисы
    s = _dash_collapse_re.sub('-', s).strip('-')
    return s


def brand_id(value: str) -> str:
    """Возвращает id в спрайте car-brands для текстового бренда либо ''.

    Бренды, отсутствующие в наборе SVG, дают пустую строку — шаблон
    в этом случае ничего не рендерит.
    """
    if not value:
        return ''
    norm = normalize_brand(value)
    if not norm:
        return ''
    if norm in BRAND_IDS:
        return norm
    # alias-таблица
    alias = _ALIASES.get(norm)
    if alias and alias in BRAND_IDS:
        return alias
    # частичный fallback: первое слово (на случай 'Toyota Motor Corp')
    head = norm.split('-', 1)[0]
    if head in BRAND_IDS:
        return head
    return ''
