"""Limpieza de los ficheros del INE: IPC, renta de los hogares e IPV.

Cada serie tiene una forma distinta en origen y produce su propio CSV:

    ipc_long.csv    year, ipc_index                      (base 2025 = 100)
    adrh_long.csv   province_code, year, net_income_household_eur
    ipv_long.csv    level, territory_code, territory_name, year, quarter, ipv_index

No une ni deflacta: eso es trabajo de build_panel.py.
"""

from __future__ import annotations

import math
import re
import warnings
from numbers import Real
from pathlib import Path

import pandas as pd

from src.config import (
    ADRH_BLOCKS,
    ADRH_KNOWN_GAPS,
    ADRH_YEARS,
    INE_FILES,
    INTERIM_DIR,
    NATIONAL_CODE,
    normalize_label,
)

IPC_OUTPUT = INTERIM_DIR / "ipc_long.csv"
ADRH_OUTPUT = INTERIM_DIR / "adrh_long.csv"
IPV_OUTPUT = INTERIM_DIR / "ipv_long.csv"

IPC_TOTAL_LABEL = "Índice general"
ADRH_INDICATOR_PREFIX = "Renta neta"
IPV_PERIOD_PATTERN = re.compile(r"^(\d{4})T([1-4])$")
IPV_CCAA_PATTERN = re.compile(r"^(\d{2})\s+(.+)$")

# Los .xlsx del INE no declaran estilo por defecto y openpyxl avisa en cada
# hoja. No afecta a los datos.
warnings.filterwarnings("ignore", message="Workbook contains no default style")


def to_number(value: object, where: str) -> float:
    """Convierte una celda numérica a float. Vacíos y 'n.r' se vuelven NaN."""
    if pd.isna(value):
        return math.nan
    if isinstance(value, Real) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        text = value.strip()
        if text in {"", ".."} or text.lower().startswith("n.r"):
            return math.nan
    raise ValueError(f"{where}: valor no reconocido {value!r}")


def as_year(value: object) -> int | None:
    """Año de una celda de cabecera, que el INE publica como texto o como número."""
    if isinstance(value, Real) and not isinstance(value, bool):
        return int(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def parse_ipc(path: Path) -> pd.DataFrame:
    """Serie anual del índice general, base 2025 = 100."""
    grid = pd.read_excel(path, sheet_name=0, header=None, engine="openpyxl").to_numpy()

    value_row = next(
        (r for r in range(len(grid)) if normalize_label(grid[r, 0]) == IPC_TOTAL_LABEL),
        None,
    )
    if value_row is None:
        raise ValueError(f"No se encontró la fila {IPC_TOTAL_LABEL!r}")

    # El año se lee de la fila superior. Las columnas de variación repiten los
    # años, así que el bloque termina cuando el año deja de decrecer.
    years: list[int] = []
    columns: list[int] = []
    for c in range(1, grid.shape[1]):
        year = as_year(grid[value_row - 1, c])
        if year is None:
            break
        if years and year >= years[-1]:
            break
        years.append(year)
        columns.append(c)

    values = [to_number(grid[value_row, c], f"IPC columna {c}") for c in columns]
    df = pd.DataFrame({"year": years, "ipc_index": values})
    return df.sort_values("year").reset_index(drop=True)


def parse_adrh(path: Path) -> pd.DataFrame:
    """Renta neta media por hogar, por provincia y año."""
    grid = pd.read_excel(path, sheet_name=0, header=None, engine="openpyxl").to_numpy()
    labels = [normalize_label(value) for value in grid[:, 0]]

    starts = [
        r
        for r in range(len(labels) - 1)
        if labels[r] and labels[r + 1].startswith(ADRH_INDICATOR_PREFIX)
    ]
    if len(starts) != len(ADRH_BLOCKS):
        raise ValueError(
            f"ADRH: {len(starts)} bloques, se esperaban {len(ADRH_BLOCKS)} "
            "(¿ha cambiado la estructura del fichero?)"
        )

    expected_years = {str(year) for year in ADRH_YEARS}
    rows: list[dict[str, object]] = []

    for start, (expected_label, code) in zip(starts, ADRH_BLOCKS):
        label = labels[start]
        if label != normalize_label(expected_label):
            raise ValueError(
                f"ADRH: en la fila {start} se esperaba {expected_label!r}, hay {label!r}"
            )
        if code is None:
            continue

        for r in range(start + 2, len(grid)):
            row_label = labels[r]
            if row_label in expected_years:
                rows.append(
                    {
                        "province_code": code,
                        "year": int(row_label),
                        "net_income_household_eur": to_number(
                            grid[r, 1], f"ADRH {label} {row_label}"
                        ),
                    }
                )
            elif not row_label:
                continue
            else:
                break

    df = pd.DataFrame(rows)
    return df.sort_values(["province_code", "year"]).reset_index(drop=True)


def parse_ipv(path: Path) -> pd.DataFrame:
    """Índice de precios de vivienda por trimestre, nacional y por CCAA."""
    grid = pd.read_excel(path, sheet_name=0, header=None, engine="openpyxl").to_numpy()

    header_row = max(
        range(min(15, len(grid))),
        key=lambda r: sum(
            1 for v in grid[r] if isinstance(v, str) and IPV_PERIOD_PATTERN.match(v.strip())
        ),
    )
    periods = {}
    for c, value in enumerate(grid[header_row]):
        if isinstance(value, str):
            match = IPV_PERIOD_PATTERN.match(value.strip())
            if match:
                periods[c] = (int(match.group(1)), int(match.group(2)))
    if not periods:
        raise ValueError("IPV: no se encontró la cabecera de trimestres")

    rows: list[dict[str, object]] = []
    for r in range(len(grid) - 1):
        label = normalize_label(grid[r, 0])
        if not label or normalize_label(grid[r + 1, 0]) != "General":
            continue

        if label == "Nacional":
            level, code, name = "national", NATIONAL_CODE, "Nacional"
        else:
            match = IPV_CCAA_PATTERN.match(label)
            if not match:
                raise ValueError(f"IPV: etiqueta de territorio no reconocida {label!r}")
            level, code, name = "ccaa", match.group(1), match.group(2)

        for c, (year, quarter) in periods.items():
            rows.append(
                {
                    "level": level,
                    "territory_code": code,
                    "territory_name": name,
                    "year": year,
                    "quarter": quarter,
                    "ipv_index": to_number(grid[r + 1, c], f"IPV {name} {year}T{quarter}"),
                }
            )

    df = pd.DataFrame(rows)
    return df.sort_values(
        ["level", "territory_code", "year", "quarter"], ascending=[False, True, True, True]
    ).reset_index(drop=True)


def validate_ipc(df: pd.DataFrame) -> None:
    expected_years = list(range(2002, 2026))
    if df["year"].tolist() != expected_years:
        raise ValueError(f"IPC: años inesperados {df['year'].min()}-{df['year'].max()}")
    base = df.loc[df["year"] == 2025, "ipc_index"]
    if base.empty or base.iloc[0] != 100:
        raise ValueError(f"IPC: la base 2025 debería valer 100, vale {base.tolist()}")
    if df["ipc_index"].isna().any() or (df["ipc_index"] <= 0).any():
        raise ValueError("IPC: hay índices vacíos o no positivos")


def validate_adrh(df: pd.DataFrame) -> None:
    counts = df.groupby("province_code")["year"].nunique()
    if len(counts) != 53 or (counts != len(ADRH_YEARS)).any():
        raise ValueError(f"ADRH: se esperaban 53 territorios con {len(ADRH_YEARS)} años")

    missing = df["net_income_household_eur"].isna()
    for _, row in df[missing].iterrows():
        allowed = ADRH_KNOWN_GAPS.get(row["province_code"], set())
        if row["year"] not in allowed:
            raise ValueError(
                f"ADRH: hueco no declarado en {row['province_code']} {row['year']}"
            )


def validate_ipv(df: pd.DataFrame) -> None:
    expected_codes = {NATIONAL_CODE} | {f"{i:02d}" for i in range(1, 20)}
    if set(df["territory_code"]) != expected_codes:
        raise ValueError(f"IPV: territorios inesperados {sorted(set(df['territory_code']))}")

    periods = df[["year", "quarter"]].drop_duplicates()
    duplicated = int(df.duplicated(["territory_code", "year", "quarter"]).sum())
    if duplicated:
        raise ValueError(f"IPV: {duplicated} claves duplicadas")

    counts = df.groupby("territory_code")["year"].count()
    if (counts != len(periods)).any():
        raise ValueError(f"IPV: algún territorio no tiene los {len(periods)} trimestres")
    if periods["year"].min() != 2007 or periods["year"].max() != 2026:
        raise ValueError(f"IPV: rango inesperado {periods['year'].min()}-{periods['year'].max()}")
    if df["ipv_index"].isna().any() or (df["ipv_index"] <= 0).any():
        raise ValueError("IPV: hay índices vacíos o no positivos")


def main() -> None:
    for path in INE_FILES.values():
        if not path.exists():
            raise FileNotFoundError(f"No existe {path}")

    builders = (
        ("IPC", parse_ipc, IPC_OUTPUT, validate_ipc),
        ("ADRH", parse_adrh, ADRH_OUTPUT, validate_adrh),
        ("IPV", parse_ipv, IPV_OUTPUT, validate_ipv),
    )

    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    for name, parse, output, validate in builders:
        df = parse(INE_FILES[name.lower()])
        validate(df)
        df.to_csv(output, index=False)
        print(f"{name:5s} {len(df):5d} filas -> {output.name}")


if __name__ == "__main__":
    main()
