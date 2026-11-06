"""Limpieza de los ficheros de valor tasado de MITMA.

Convierte los informes .xls en una tabla larga con una fila por provincia,
año y trimestre:

    kind, province_code, year, quarter, price_eur_m2

`kind` distingue vivienda libre total, de hasta 5 años y de más de 5 años.
No agrega ni deflacta: eso es trabajo de build_panel.py.
"""

from __future__ import annotations

import math
import re
from numbers import Real
from pathlib import Path

import pandas as pd

from src.config import (
    INTERIM_DIR,
    MITMA_FILES,
    PARTIAL_YEAR_QUARTERS,
    PROVINCE_CODES,
    QUARTERS_PER_YEAR,
    resolve_province,
)

OUTPUT_PATH = INTERIM_DIR / "mitma_long.csv"

COLUMNS = ["kind", "province_code", "year", "quarter", "price_eur_m2"]

# Anclas para localizar la estructura dentro de cada hoja
LABEL_ANCHOR = "TOTAL NACIONAL"
YEAR_PATTERN = re.compile(r"Año\s+(\d{4})")
QUARTER_PATTERN = re.compile(r"^([1-4])º$")

# Rango de plausibilidad: detecta textos o variaciones coladas como precio
MIN_PRICE = 300.0
MAX_PRICE = 10_000.0

# El total debería caer entre nueva y usada. En la práctica hay 6 tripletas
# (de 3.066) que se desvían hasta 10 €/m² por cómo redondea la fuente.
CROSS_CHECK_TOLERANCE = 10.0
CROSS_CHECK_MAX_SHARE = 0.01


def find_header(grid: list[list[object]]) -> tuple[int, int, dict[int, tuple[int, int]]]:
    """Localiza la columna de territorios y el mapa columna -> (año, trimestre).

    `grid` es la hoja en crudo, como lista de filas.
    """

    # 1. Columna de territorios: la que contiene el ancla
    label_col = None
    first_data_row = None
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if isinstance(value, str) and value.strip() == LABEL_ANCHOR:
                label_col, first_data_row = c, r
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

    return label_col, first_data_row, col_map


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

        code = resolve_province(label, "mitma")
        if code is None:
            continue

        for c, (year, quarter) in col_map.items():
            try:
                price = to_price(grid[r][c])
            except ValueError as exc:
                raise ValueError(f"{kind} / {sheet}: fila {r}, columna {c}: {exc}") from None

            # Se emite la fila aunque el precio sea NaN, para poder distinguir
            # "no publicado" (n.r) de "observación perdida por el parser".
            rows.append(
                {
                    "kind": kind,
                    "province_code": code,
                    "year": year,
                    "quarter": quarter,
                    "price_eur_m2": price,
                }
            )

    return rows


def parse_workbook(kind: str, path: Path) -> pd.DataFrame:
    """Recorre todas las hojas de un libro y devuelve la tabla larga."""
    rows: list[dict[str, object]] = []
    workbook = pd.ExcelFile(path, engine="xlrd")

    for sheet in workbook.sheet_names:
        grid = workbook.parse(sheet_name=sheet, header=None).values.tolist()
        rows.extend(parse_sheet(grid, kind, sheet))

    return pd.DataFrame(rows, columns=COLUMNS)


def validate(df: pd.DataFrame) -> None:
    """Puertas de calidad. Lanza ValueError si algo no cuadra."""
    if df.empty:
        raise ValueError("La tabla está vacía")

    # 1. Las 52 provincias en cada kind
    expected = set(PROVINCE_CODES)
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
            f"{group['province_code'].nunique()} provincias · "
            f"{group['price_eur_m2'].isna().sum()} nulos · "
            f"{group['year'].min()}-{group['year'].max()}"
        )


if __name__ == "__main__":
    main()
