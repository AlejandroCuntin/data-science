"""Limpieza de los ficheros de valor tasado de MITMA.

Convierte los informes .xls en una tabla larga con una fila por provincia,
año y trimestre:

    kind, province_code, year, quarter, price_eur_m2

`kind` distingue vivienda libre total, de hasta 5 años y de más de 5 años.
No agrega ni deflacta: eso es trabajo de build_panel.py.
"""

from __future__ import annotations

import math #Sirve para representar valores ausentes (que no existen)
import re #Sirve para buscar patrones de texto como detectar el año y los trimestres en Excel
from numbers import Real #Sirve para identificar numeros, aqui comprobamos si una celta contiene un número
from pathlib import Path  #Sirve para localizar los Excels y guardar el CSV

#Pandas es una de las bibliotecas más importantes de Data Science.Permite trabajar con datos estructurados, 
#como si fueran tablas de Excel, pero desde Python
import pandas as pd #trabajamos con las tablas de datos

#Importamos apartir de nuestar configuracion base 
from src.config import (
    ALL_TERRITORY_CODES,
    INTERIM_DIR,
    MITMA_FILES,
    PARTIAL_YEAR_QUARTERS,
    QUARTERS_PER_YEAR,
    resolve_territory,
)

#Guardamos la ruta donde queremos guardar el archivo final en una constante
#INTERIM_DIR es la ruta hasta el directorio data/interim

OUTPUT_PATH = INTERIM_DIR / "mitma_long.csv"

#Definimos tambien la constante columns con las variables que guardaremos, es una lista
#Cada elemento de la lista corresponde a la cabecera de una de las columnas
COLUMNS = ["kind", "province_code", "year", "quarter", "price_eur_m2"]

# Pistas para localizar los elementos del Excel
# "re.compile()" prepara un patrón de búsqueda para poder reutilizarlo
LABEL_ANCHOR = "TOTAL NACIONAL" #Buscamos el texto TOTAL NACIONAL
YEAR_PATTERN = re.compile(r"Año\s+(\d{4})") #Buscamos la palabra año + un numero de 4 digitos
QUARTER_PATTERN = re.compile(r"^([1-4])º$") #Buscamos textos como 1, 2, 3, 4


#Aqui estableceremos limites para detectar posibles errores: lo aplicaremos en "validate()"

# Rango de plausibilidad: detecta textos o variaciones coladas como precio
MIN_PRICE = 300.0
MAX_PRICE = 10_000.0

#Margen de tolerancia en el contraste
CROSS_CHECK_TOLERANCE = 10.0

#Maximo 1 % de casos fuera del rango esperado
CROSS_CHECK_MAX_SHARE = 0.01


#Buscamos donde están los años, los trimestres, y las provinicias en el Excel

def find_header(grid: list[list[object]]) -> tuple[int, int, dict[int, tuple[int, int]]]:
    """Localiza la columna de territorios y el mapa columna -> (año, trimestre).

    `grid` es la hoja en crudo, como lista de filas.
    Es el contenido de una hoja de Excel representado como listas de python
    """

    #Creamos dos variables vacias
    label_col = None
    first_data_row = None

    #Recorremos una lista obteniendo simultaneamente la posicion del elemento y el propio elemento gracias a "enumerate(grid)"
    # "r" es el número de la fila y "row" es el contenido de esa fila
    for r, row in enumerate(grid):

        #Ahora al entrar en el segundo bucle, recorre las celdas de esa fila
        for c, value in enumerate(row):

            #Comprobamos esta condición: Si el valor de esa celda es texto y despues de eliminar espacios sobrantes, es
            #Igual a "TOTAL NACIONAL", entonces hemos encontrado la columna de territorios
            if isinstance(value, str) and value.strip() == LABEL_ANCHOR:

                #Entonces asignamos a first_data_row el numero de la fila y a label_col el numero de la celda
                label_col, first_data_row = c, r

                #Usamos break para cortar el codigo, porque ya hemos encontrado lo que necesitamos
                break
        
        if label_col is not None:
            break
    if label_col is None:
        raise ValueError(f"No se encontró la fila {LABEL_ANCHOR!r}")

    # 2. Fila de años. Se busca de abajo arriba para quedarse con la más
    # cercana a los datos si algún título contuviera un año.
    year_row = None
    for r in range(first_data_row - 1, -1, -1):
        if any(isinstance(v, str) and YEAR_PATTERN.search(v) for v in grid[r]):
            year_row = r
            break
    if year_row is None:
        raise ValueError("No se encontró la fila de años ('Año 2023', ...)")

    # 3. Fila de trimestres: la primera entre los años y los datos
    quarter_row = None
    for r in range(year_row + 1, first_data_row):
        if any(isinstance(v, str) and QUARTER_PATTERN.match(v.strip()) for v in grid[r]):
            quarter_row = r
            break
    if quarter_row is None:
        raise ValueError("No se encontró la fila de trimestres ('1º', '2º', ...)")

    # 4. Mapa columna -> (año, trimestre). La fila de años viene combinada en
    # el Excel: el año se arrastra a la derecha hasta que aparece otro.
    # Las columnas de variación no casan con el patrón de trimestre, así que
    # se descartan solas.
    col_map: dict[int, tuple[int, int]] = {}
    current_year = None
    for c, value in enumerate(grid[year_row]):
        if isinstance(value, str):
            match = YEAR_PATTERN.search(value)
            if match:
                current_year = int(match.group(1))
        if current_year is None:
            continue
        q_value = grid[quarter_row][c]
        if not isinstance(q_value, str):
            continue
        q_match = QUARTER_PATTERN.match(q_value.strip())
        if q_match:
            col_map[c] = (current_year, int(q_match.group(1)))

    # 5. Salvaguardas de estructura
    if not col_map:
        raise ValueError("La hoja no tiene ninguna columna de trimestre")
    if len(col_map) != len(set(col_map.values())):
        raise ValueError("Hay más de una columna para el mismo año y trimestre")
    for year in {y for y, _ in col_map.values()}:
        quarters = sorted(q for y, q in col_map.values() if y == year)
        if quarters != list(range(1, len(quarters) + 1)):
            raise ValueError(f"Trimestres no consecutivos en {year}: {quarters}")

    #Devolvemos 
    return label_col, first_data_row, col_map


#Convierte los precios del Excel en números para que python pueda utilizarlo

def to_price(value: object) -> float:
    """Convierte una celda de precio a float. Vacíos y 'n.r' se vuelven NaN."""
    if pd.isna(value):
        return math.nan
    if isinstance(value, Real) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        text = value.strip()
        if text == "" or text.lower().startswith("n.r"):
            return math.nan
    raise ValueError(f"Valor de precio no reconocido: {value!r}")


#Extraen informacion de las hojas y de los distintos archivos Excel
#Tanto parse_sheet como parse_workbook()

def parse_sheet(
    grid: list[list[object]],
    kind: str,
    sheet: str,
) -> list[dict[str, object]]:
    """Convierte una hoja en filas (provincia, año, trimestre, precio)."""
    label_col, first_data_row, col_map = find_header(grid)

    rows: list[dict[str, object]] = []
    for r in range(first_data_row, len(grid)):
        label = grid[r][label_col]
        if not isinstance(label, str) or not label.strip():
            continue

        code = resolve_territory(label, "mitma")
        if code is None:
            continue

        for c, (year, quarter) in col_map.items():
            try:
                price = to_price(grid[r][c])
            except ValueError as exc:
                raise ValueError(f"{kind} / {sheet}: fila {r}, columna {c}: {exc}") from None

            # Se emite la fila aunque el precio sea NaN, para poder distinguir
            # "no publicado" (n.r) de "observación perdida por el parser".

            #Aqui creamos cuantas columnas tendrá nuestro dataset
            rows.append(
                {
                    #Tipo de vivienda (total, nueva, usada)
                    "kind": kind,

                    #Código INE de provincia (Por ejemplo Madrid = 28)
                    "province_code": code,

                    #Año de la observación
                    "year": year,

                    #Trimestre
                    "quarter": quarter,

                    #Precio tasado por metro cuadrado
                    "price_eur_m2": price,
                }
            )

    #Una fila podria significar:
    #El precio tasado por metro cuadrado de vivienda libre total en Madrid durante el pruimer trimestre de 2023 fue de 3000 euros

    return rows


def parse_workbook(kind: str, path: Path) -> pd.DataFrame:
    """Recorre todas las hojas de un libro y devuelve la tabla larga."""
    rows: list[dict[str, object]] = []
    workbook = pd.ExcelFile(path, engine="xlrd")

    for sheet in workbook.sheet_names:
        grid = workbook.parse(sheet_name=sheet, header=None).values.tolist()
        rows.extend(parse_sheet(grid, kind, sheet))

    return pd.DataFrame(rows, columns=COLUMNS)



#Comprueba que los datos no tengan errores importantes
def validate(df: pd.DataFrame) -> None:
    """Puertas de calidad. Lanza ValueError si algo no cuadra."""
    if df.empty:
        raise ValueError("La tabla está vacía")

    # 1. Las 52 provincias y el total nacional en cada kind
    expected = set(ALL_TERRITORY_CODES)
    for kind, group in df.groupby("kind"):
        codes = set(group["province_code"])
        if codes != expected:
            raise ValueError(
                f"{kind}: faltan {sorted(expected - codes)}, "
                f"sobran {sorted(codes - expected)}"
            )

    # 2. Sin claves duplicadas
    duplicated = int(df.duplicated(["kind", "province_code", "year", "quarter"]).sum())
    if duplicated:
        raise ValueError(f"{duplicated} claves duplicadas (kind, provincia, año, trimestre)")

    # 3. Trimestres por año: 4, salvo los años parciales declarados
    counts = df.groupby(["kind", "year"])["quarter"].nunique()
    for (kind, year), n in counts.items():
        expected_quarters = PARTIAL_YEAR_QUARTERS.get(year, QUARTERS_PER_YEAR)
        if n != expected_quarters:
            raise ValueError(
                f"{kind} {year}: {n} trimestres, se esperaban {expected_quarters}"
            )

    # 4. Precios en rango plausible
    prices = df["price_eur_m2"].dropna()
    outliers = prices[(prices < MIN_PRICE) | (prices > MAX_PRICE)]
    if not outliers.empty:
        raise ValueError(
            f"{len(outliers)} precios fuera de [{MIN_PRICE}, {MAX_PRICE}] €/m² "
            f"(mín {outliers.min():.1f}, máx {outliers.max():.1f})"
        )

    # 5. Cruce total vs nueva/usada: la media ponderada tiene que quedar entre
    # sus dos componentes. Un desplazamiento de columnas daría miles de
    # violaciones, no seis.
    wide = df.pivot_table(
        index=["province_code", "year", "quarter"],
        columns="kind",
        values="price_eur_m2",
    )
    if not {"total", "nueva", "usada"}.issubset(wide.columns):
        raise ValueError(f"Faltan series en el cruce: {list(wide.columns)}")

    wide = wide.dropna(subset=["total", "nueva", "usada"])
    if not wide.empty:
        low = wide[["nueva", "usada"]].min(axis=1)
        high = wide[["nueva", "usada"]].max(axis=1)
        outside = (wide["total"] < low - CROSS_CHECK_TOLERANCE) | (
            wide["total"] > high + CROSS_CHECK_TOLERANCE
        )
        if outside.mean() > CROSS_CHECK_MAX_SHARE:
            raise ValueError(
                f"{outside.sum()} de {len(wide)} tripletas ({outside.mean():.1%}) "
                "tienen el total fuera de nueva/usada: ¿columnas desalineadas?"
            )


#Guardamos los datos en un CSV final

def main() -> None:
    frames = []
    for kind, path in MITMA_FILES.items():
        if not path.exists():
            raise FileNotFoundError(f"No existe {path}")
        print(f"Leyendo {kind:5s} {path.name}")
        frames.append(parse_workbook(kind, path))

    df = pd.concat(frames, ignore_index=True)
    # La fuente publica un decimal: redondear elimina el ruido binario
    # (1156.6000000000001) sin perder información.
    df["price_eur_m2"] = df["price_eur_m2"].round(1)

    validate(df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nEscrito {OUTPUT_PATH}")
    print(f"Filas: {len(df)}")
    for kind, group in df.groupby("kind"):
        print(
            f"  {kind:6s} {len(group):5d} filas · "
            f"{group['province_code'].nunique()} territorios · "
            f"{group['price_eur_m2'].isna().sum()} nulos · "
            f"{group['year'].min()}-{group['year'].max()}"
        )


if __name__ == "__main__":
    main()
