"""Справочник идентификаторов автомобильных брендов.

Используется для маппинга текстового brand из tech_docs.* (часто разный регистр,
с пробелами/дефисами/тире) в slug — имя PNG-файла в
hpt_su/static/frontend/car-brands/<slug>.png

Источник иконок: car-logos-dataset (~387 брендов, kebab-case lowercase).
"""
from __future__ import annotations

import re
import unicodedata

__all__ = ['BRAND_IDS', 'normalize_brand', 'brand_id']


# Список идентификаторов = имена PNG в frontend/car-brands/.
# Сгенерирован из car-logos-dataset/logos/thumb/.
BRAND_IDS: frozenset[str] = frozenset({
    "9ff", "abadal", "abarth", "abbott-detroit", "abt", "ac",
    "acura", "aiways", "aixam", "alfa-romeo", "alpina", "alpine",
    "alta", "alvis", "amc", "apollo", "arash", "arcfox",
    "ariel", "aro", "arrinera", "arrival", "artega", "ascari",
    "askam", "aspark", "aston-martin", "atalanta", "auburn", "audi",
    "audi-sport", "austin", "autobacs", "autobianchi", "axon", "bac",
    "baic-motor", "baojun", "beiben", "bentley", "berkeley", "berliet",
    "bertone", "bestune", "bharatbenz", "bitter", "bizzarrini", "bmw-m",
    "bmw", "borgward", "bowler", "brabus", "brammo", "brilliance",
    "bristol", "brooke", "bufori", "bugatti", "buick", "byd",
    "byton", "cadillac", "camc", "canoo", "caparo", "carlsson",
    "caterham", "changan", "changfeng", "chery", "chevrolet-corvette", "chevrolet",
    "chrysler", "cisitalia", "citroen", "cizeta", "cole", "corre-la-licorne",
    "cupra", "dacia", "daewoo", "daf", "daihatsu", "daimler",
    "dartz", "datsun", "david-brown", "dayun", "delage", "desoto",
    "de-tomaso", "detroit-electric", "devel-sixteen", "diatto", "dina", "dkw",
    "dmc", "dodge", "dodge-viper", "dongfeng", "donkervoort", "drako",
    "ds", "duesenberg", "eagle", "edag", "edsel", "eicher",
    "elemental", "elfin", "elva", "englon", "erf", "eterniti",
    "exeed", "facel-vega", "faraday-future", "faw-jiefang", "faw", "ferrari",
    "fiat", "fioravanti", "fisker", "foden", "force-motors", "ford-mustang",
    "ford", "foton", "fpv", "franklin", "freightliner", "fso",
    "gac-group", "gardner-douglas", "gaz", "geely", "general-motors", "genesis",
    "geometry", "geo", "gilbern", "gillet", "ginetta", "gmc",
    "golden-dragon", "gonow", "great-wall", "grinnall", "gumpert", "hafei",
    "haima", "haval", "hawtai", "hennessey", "higer", "hillman",
    "hindustan-motors", "hino", "hiphi", "hispano-suiza", "holden", "hommell",
    "honda", "hongqi", "hongyan", "horch", "hsv", "hudson",
    "hummer", "hupmobile", "hyundai", "ic-bus", "ih", "ikco",
    "infiniti", "innocenti", "intermeccanica", "international", "irizar", "isdera",
    "iso", "isuzu", "iveco", "jac", "jaguar", "jawa",
    "jba-motors", "jeep", "jensen", "jetour", "jetta", "jmc",
    "kaiser", "kamaz", "karlmann-king", "karma", "keating", "kenworth",
    "kia", "king-long", "koenigsegg", "ktm", "lada", "lagonda",
    "lamborghini", "lancia", "land-rover", "landwind", "laraki", "leapmotor",
    "levc", "lexus", "leyland", "li-auto", "lifan", "ligier",
    "lincoln", "lister", "lloyd", "lobini", "lordstown", "lotus",
    "lucid", "luxgen", "lynk-and-co", "mack", "mahindra", "man",
    "mansory", "marcos", "marlin", "maserati", "mastretta", "maxus",
    "maybach", "mazda", "maz", "mazzanti", "mclaren", "melkus",
    "mercedes-amg", "mercedes-benz", "mercury", "merkur", "mev", "mg",
    "microcar", "mini", "mitsubishi", "mitsuoka", "mk", "morgan",
    "morris", "mosler", "navistar", "nevs", "nikola", "nio",
    "nissan-gt-r", "nissan-nismo", "nissan", "noble", "oldsmobile", "oltcit",
    "omoda", "opel", "osca", "paccar", "packard", "pagani",
    "panhard", "panoz", "pegaso", "perodua", "peterbilt", "peugeot",
    "pgo", "pierce-arrow", "pininfarina", "plymouth", "polestar", "pontiac",
    "porsche", "praga", "premier", "prodrive", "proton", "qoros",
    "radical", "rambler", "ram", "ranz", "renault", "renault-samsung",
    "rezvani", "riley", "rimac", "rinspeed", "rivian", "roewe",
    "rolls-royce", "ronart", "rossion", "rover", "ruf", "saab",
    "saic-motor", "saipa", "saleen", "saturn", "scania", "scion",
    "seat", "setra", "sev", "shacman", "simca", "singer",
    "singulato", "sinotruk", "sisu", "skoda", "smart", "soueast",
    "spania-gta", "spirra", "spyker", "ssangyong", "ssc", "sterling",
    "studebaker", "stutz", "subaru", "suffolk", "suzuki", "talbot",
    "tata", "tatra", "tauro", "techart", "tesla", "toyota-alphard",
    "toyota-century", "toyota-crown", "toyota", "tramontana", "trion", "triumph",
    "troller", "tucker", "tvr", "uaz", "ud", "ultima",
    "vandenbrink", "vauxhall", "vector", "vencer", "venturi", "venucia",
    "vinfast", "vlf", "volkswagen", "volvo", "wanderer", "wartburg",
    "weltmeister", "western-star", "westfield", "wey", "wiesmann", "willys-overland",
    "w-motors", "workhorse", "wuling", "xpeng", "yulon", "yutong",
    "zarooq-motors", "zastava", "zaz", "zeekr", "zenos", "zenvo",
    "zhongtong", "zinoro", "zotye",
})

# Алиасы: написания, которые normalize_brand не сводит к slug-у в BRAND_IDS.
# Большинство теперь сводится напрямую (в наборе есть mercedes-benz, land-rover и т.п.),
# поэтому здесь только редкие сокращения и кириллица.
_ALIASES: dict[str, str] = {
    'vw': 'volkswagen',
    'volkswagen-ag': 'volkswagen',
    'mercedes': 'mercedes-benz',
    'merсedes-benz': 'mercedes-benz',
    'mercedesbenz': 'mercedes-benz',
    'rolls-royce-motor-cars': 'rolls-royce',
    'rolls': 'rolls-royce',
    'rollsroyce': 'rolls-royce',
    'aston': 'aston-martin',
    'astonmartin': 'aston-martin',
    'astonmartinlagonda': 'aston-martin',
    'land': 'land-rover',
    'landrover': 'land-rover',
    'range-rover': 'land-rover',  # range-rover в наборе нет, фолбек на land-rover
    'rangerover': 'land-rover',
    'range': 'land-rover',
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
    """Возвращает slug PNG-иконки бренда, либо ''."""
    s = normalize_brand(value)
    if not s:
        return ''
    if s in BRAND_IDS:
        return s
    alias = _ALIASES.get(s)
    if alias and alias in BRAND_IDS:
        return alias
    return ''
