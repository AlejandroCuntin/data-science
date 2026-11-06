"""Configuración compartida del proyecto.

Una única definición de rutas, parámetros y del catálogo de provincias.
Las provincias se identifican siempre por código INE de 2 dígitos; el nombre
canónico es solo para mostrar.
"""

from __future__ import annotations

import re
from pathlib import Path

#Definimos donde están los ficheros

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"

#Parámetros de nuestro analisis

#Buscamos analizar 90 metros cuadrados
REFERENCE_M2 = 90 

#Rango entre 70 y 100 metros cuadrados
SENSITIVITY_M2 = (70, 100) 

#Desde 2007 hasta 2026
PRICE_START_YEAR = 2007 
PRICE_END_YEAR = 2026
INCOME_START_YEAR = 2015
INCOME_END_YEAR = 2024

#Cuatro trimestres por año 
QUARTERS_PER_YEAR = 4

# Años con menos trimestres publicados: 2026 solo llega a Q2.
PARTIAL_YEAR_QUARTERS = {2026: 2}

#Ficheros de entrada

MITMA_FILES = {
    "total": RAW_DIR / "mitma_35101000_libre.xls",
    "nueva": RAW_DIR / "mitma_35101500_libre_nueva.xls",
    "usada": RAW_DIR / "mitma_35102000_libre_usada.xls",
}

INE_FILES = {
    "ipc": RAW_DIR / "ine_ipc_76144_anual.xlsx",
    "adrh": RAW_DIR / "ine_adrh_53689_provincial.xlsx",
    "ipv": RAW_DIR / "ine_ipv_79563_ccaa.xlsx",
}

#Catálogo de provincias (código INE -> nombre canónico)

PROVINCES = {
    "01": "Araba/Álava",
    "02": "Albacete",
    "03": "Alicante/Alacant",
    "04": "Almería",
    "05": "Ávila",
    "06": "Badajoz",
    "07": "Illes Balears",
    "08": "Barcelona",
    "09": "Burgos",
    "10": "Cáceres",
    "11": "Cádiz",
    "12": "Castellón/Castelló",
    "13": "Ciudad Real",
    "14": "Córdoba",
    "15": "A Coruña",
    "16": "Cuenca",
    "17": "Girona",
    "18": "Granada",
    "19": "Guadalajara",
    "20": "Gipuzkoa",
    "21": "Huelva",
    "22": "Huesca",
    "23": "Jaén",
    "24": "León",
    "25": "Lleida",
    "26": "La Rioja",
    "27": "Lugo",
    "28": "Madrid",
    "29": "Málaga",
    "30": "Murcia",
    "31": "Navarra",
    "32": "Ourense",
    "33": "Asturias",
    "34": "Palencia",
    "35": "Las Palmas",
    "36": "Pontevedra",
    "37": "Salamanca",
    "38": "Santa Cruz de Tenerife",
    "39": "Cantabria",
    "40": "Segovia",
    "41": "Sevilla",
    "42": "Soria",
    "43": "Tarragona",
    "44": "Teruel",
    "45": "Toledo",
    "46": "Valencia/València",
    "47": "Valladolid",
    "48": "Bizkaia",
    "49": "Zamora",
    "50": "Zaragoza",
    "51": "Ceuta",
    "52": "Melilla",
}

PROVINCE_CODES = frozenset(PROVINCES)

# "00" no es un código INE: es la convención propia para la serie de España.
# Las tres fuentes publican su propio Total Nacional, que no equivale a la
# media simple de las provincias, así que se conserva tal cual.
NATIONAL_CODE = "00"

#Etiquetas de MITMA
# Cada fuente nombra las provincias a su manera. Se resuelven contra una tabla
# explícita, nunca por similitud de texto.

MITMA_NAMES = {
    "TOTAL NACIONAL": NATIONAL_CODE,
    "Almería": "04",
    "Cádiz": "11",
    "Córdoba": "14",
    "Granada": "18",
    "Huelva": "21",
    "Jaén": "23",
    "Málaga": "29",
    "Sevilla": "41",
    "Huesca": "22",
    "Teruel": "44",
    "Zaragoza": "50",
    "Asturias (Principado de)": "33",
    "Balears (Illes)": "07",
    "Palmas (Las)": "35",
    "Santa Cruz de Tenerife": "38",
    "Cantabria": "39",
    "Ávila": "05",
    "Burgos": "09",
    "León": "24",
    "Palencia": "34",
    "Salamanca": "37",
    "Segovia": "40",
    "Soria": "42",
    "Valladolid": "47",
    "Zamora": "49",
    "Albacete": "02",
    "Ciudad Real": "13",
    "Cuenca": "16",
    "Guadalajara": "19",
    "Toledo": "45",
    "Barcelona": "08",
    "Girona": "17",
    "Lleida": "25",
    "Tarragona": "43",
    "Alicante/Alacant": "03",
    "Castellón/Castelló": "12",
    "Valencia/València": "46",
    "Badajoz": "06",
    "Cáceres": "10",
    "Coruña (A)": "15",
    "Lugo": "27",
    "Ourense": "32",
    "Pontevedra": "36",
    "Madrid (Comunidad de)": "28",
    "Murcia (Región de)": "30",
    "Navarra (Comunidad Foral de)": "31",
    "Navarra (Com. Foral de)": "31",  # variante en la hoja 2015-2018
    "Araba/Alava": "01",
    "Gipuzkoa": "20",
    "Bizkaia": "48",
    "Rioja (La)": "26",
    "Ceuta": "51",
    "Melilla": "52",
}

# Filas que no son provincias: CCAA pluriprovinciales, agregados y notas.
MITMA_IGNORED = {
    "Andalucía",
    "Aragón",
    "Canarias",
    "Castilla y León",
    "Castilla-La Mancha",
    "Cataluña",
    "Comunidad Valenciana",
    "Extremadura",
    "Galicia",
    "País Vasco",
    "Ceuta y Melilla",
    "n.r: el dato no es representativo o no existen observaciones",
}

SOURCE_NAMES = {"mitma": MITMA_NAMES}
SOURCE_IGNORED = {"mitma": MITMA_IGNORED}

# ADRH: catalogo por posicion, no por nombre. "Balears, Illes", "Cantabria",
# "Rioja, La", "Ceuta" y "Melilla" aparecen dos veces, como CCAA y como
# provincia; un diccionario por nombre perderia la provincia en silencio.
# None = bloque ignorado (CCAA, isla o ciudad autonoma duplicada).
ADRH_BLOCKS = (
    ("Total Nacional", NATIONAL_CODE),
    ("Andalucía", None),
    ("Almería", "04"),
    ("Cádiz", "11"),
    ("Córdoba", "14"),
    ("Granada", "18"),
    ("Huelva", "21"),
    ("Jaén", "23"),
    ("Málaga", "29"),
    ("Sevilla", "41"),
    ("Aragón", None),
    ("Huesca", "22"),
    ("Teruel", "44"),
    ("Zaragoza", "50"),
    ("Asturias, Principado de", None),
    ("Asturias", "33"),
    ("Balears, Illes", None),
    ("Balears, Illes", "07"),
    ("Ibiza y Formentera", None),
    ("Mallorca", None),
    ("Menorca", None),
    ("Canarias", None),
    ("Palmas, Las", "35"),
    ("Fuerteventura", None),
    ("Gran Canaria", None),
    ("Lanzarote", None),
    ("Santa Cruz de Tenerife", "38"),
    ("Gomera, La", None),
    ("Hierro, El", None),
    ("Palma, La", None),
    ("Tenerife", None),
    ("Cantabria", None),
    ("Cantabria", "39"),
    ("Castilla y León", None),
    ("Ávila", "05"),
    ("Burgos", "09"),
    ("León", "24"),
    ("Palencia", "34"),
    ("Salamanca", "37"),
    ("Segovia", "40"),
    ("Soria", "42"),
    ("Valladolid", "47"),
    ("Zamora", "49"),
    ("Castilla - La Mancha", None),
    ("Albacete", "02"),
    ("Ciudad Real", "13"),
    ("Cuenca", "16"),
    ("Guadalajara", "19"),
    ("Toledo", "45"),
    ("Cataluña", None),
    ("Barcelona", "08"),
    ("Girona", "17"),
    ("Lleida", "25"),
    ("Tarragona", "43"),
    ("Comunitat Valenciana", None),
    ("Alicante/Alacant", "03"),
    ("Castellón/Castelló", "12"),
    ("Valencia/València", "46"),
    ("Extremadura", None),
    ("Badajoz", "06"),
    ("Cáceres", "10"),
    ("Galicia", None),
    ("Coruña, A", "15"),
    ("Lugo", "27"),
    ("Ourense", "32"),
    ("Pontevedra", "36"),
    ("Madrid, Comunidad de", None),
    ("Madrid", "28"),
    ("Murcia, Región de", None),
    ("Murcia", "30"),
    ("Navarra, Comunidad Foral de", None),
    ("Navarra", "31"),
    ("País Vasco", None),
    ("Araba/Álava", "01"),
    ("Bizkaia", "48"),
    ("Gipuzkoa", "20"),
    ("Rioja, La", None),
    ("Rioja, La", "26"),
    ("Ceuta", None),
    ("Ceuta", "51"),
    ("Melilla", None),
    ("Melilla", "52"),
)

# ADRH publica 10 anios (2015-2024); los huecos reales se declaran, no se rellenan.
ADRH_YEARS = tuple(range(2015, 2025))

# Huecos conocidos de la fuente, por codigo de territorio.
# Cualquier otro NaN en la renta aborta la limpieza.
ADRH_KNOWN_GAPS = {
    NATIONAL_CODE: set(range(2015, 2021)),
    "31": set(range(2015, 2021)),  # Navarra
    "01": set(range(2015, 2020)),  # Araba/Álava
    "20": {2015},                  # Gipuzkoa, marcado '..' en origen
}

_WHITESPACE = re.compile(r"\s+")
_SPACE_BEFORE_PAREN = re.compile(r"\s+\)")


def normalize_label(label: object) -> str:
    """Normaliza una etiqueta de territorio: espacios, saltos y espacios antes de ')'.

    MITMA trae etiquetas como 'Almería           ' o 'Asturias (Principado de )'.
    """
    text = _WHITESPACE.sub(" ", str(label)).strip()
    return _SPACE_BEFORE_PAREN.sub(")", text)


def resolve_territory(label: object, source: str = "mitma") -> str | None:
    """Devuelve el código del territorio o None si la fila no es una provincia.

    El código puede ser una provincia o NATIONAL_CODE. Lanza ValueError si la
    etiqueta no se reconoce: preferimos fallar a perder un territorio en silencio.
    """
    if source not in SOURCE_NAMES:
        raise ValueError(f"Fuente desconocida: {source!r}. Válidas: {sorted(SOURCE_NAMES)}")

    key = normalize_label(label)
    if key in SOURCE_IGNORED[source]:
        return None
    try:
        return SOURCE_NAMES[source][key]
    except KeyError:
        raise ValueError(
            f"Etiqueta no reconocida en {source}: {key!r}. "
            f"Añádela al catálogo de {source} en src/config.py."
        ) from None


# Salvaguardas del catálogo: si alguien edita la tabla, falla al importar.
ALL_TERRITORY_CODES = PROVINCE_CODES | {NATIONAL_CODE}
EXPECTED_ADRH_CODES = PROVINCE_CODES | {NATIONAL_CODE}

assert len(PROVINCES) == 52, f"Se esperaban 52 provincias, hay {len(PROVINCES)}"
assert set(MITMA_NAMES.values()) == ALL_TERRITORY_CODES, (
    "MITMA no cubre las 52 provincias y el total nacional"
)
assert not set(MITMA_NAMES) & MITMA_IGNORED, "Una etiqueta no puede ser provincia e ignorada a la vez"
assert len(ADRH_BLOCKS) == 82, f"Se esperaban 82 bloques en ADRH, hay {len(ADRH_BLOCKS)}"
assert {code for _, code in ADRH_BLOCKS if code} == EXPECTED_ADRH_CODES, (
    "ADRH no cubre las 52 provincias y el total nacional"
)
