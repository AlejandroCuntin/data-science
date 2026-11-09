"""Exporta el panel a un JSON pequeño para la calculadora web.

Lee `data/processed/panel_provincia_anual.csv` y escribe
`web/data/panel.json` con la ventana 2015-2024, las 52 provincias y el total
nacional. No transforma los datos: solo selecciona columnas, redondea y cambia
los NaN a `null` para que el navegador los distinga de un cero.

Uso:
    python -m src.build_web_data
"""

from __future__ import annotations

import json
import math
import unicodedata
from pathlib import Path

import pandas as pd

from src.config import (
    INCOME_END_YEAR,
    INCOME_START_YEAR,
    NATIONAL_CODE,
    PROCESSED_DIR,
    PROVINCES,
    REFERENCE_M2,
    SENSITIVITY_M2,
)

PANEL_PATH = PROCESSED_DIR / "panel_provincia_anual.csv"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "web" / "data" / "panel.json"

KIND_LABELS = {"total": "Total", "nueva": "Nueva", "usada": "Usada"}
KIND_ORDER = {"total": 0, "nueva": 1, "usada": 2}


def sort_key(name: str) -> str:
    """Ordena en español sin que las tildes caigan al final del alfabeto."""
    normalized = unicodedata.normalize("NFKD", name)
    return normalized.encode("ascii", "ignore").decode("ascii").lower()


def number(value: object) -> float | None:
    """Convierte un valor de pandas en un número JSON o en `null`."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    if pd.isna(value):
        return None
    return round(float(value), 2)


def main() -> None:
    panel = pd.read_csv(PANEL_PATH, dtype={"province_code": str})
    panel = panel[
        panel["year"].between(INCOME_START_YEAR, INCOME_END_YEAR)
        & panel["province_code"].isin({*PROVINCES, NATIONAL_CODE})
        & panel["kind"].isin(KIND_LABELS)
    ].copy()

    expected = (len(PROVINCES) + 1) * (INCOME_END_YEAR - INCOME_START_YEAR + 1) * len(KIND_LABELS)
    if len(panel) != expected:
        raise ValueError(f"Se esperaban {expected} filas, hay {len(panel)}")

    panel["kind_order"] = panel["kind"].map(KIND_ORDER)
    panel = panel.sort_values(["province_code", "year", "kind_order"])

    provinces = [
        {"code": NATIONAL_CODE, "name": "España"},
        *[
            {"code": code, "name": name}
            for code, name in sorted(PROVINCES.items(), key=lambda item: sort_key(item[1]))
        ],
    ]

    records = [
        {
            "province_code": row.province_code,
            "year": int(row.year),
            "kind": row.kind,
            "price_eur_m2": number(row.price_nominal_eur_m2),
            "income_eur": number(row.net_income_household_eur),
        }
        for row in panel.itertuples(index=False)
    ]

    payload = {
        "meta": {
            "source": "data/processed/panel_provincia_anual.csv",
            "start_year": INCOME_START_YEAR,
            "end_year": INCOME_END_YEAR,
            "reference_m2": REFERENCE_M2,
            "sensitivity_m2": list(SENSITIVITY_M2),
            "national_code": NATIONAL_CODE,
            "kind_labels": KIND_LABELS,
        },
        "provinces": provinces,
        "records": records,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    missing_price = sum(record["price_eur_m2"] is None for record in records)
    missing_income = sum(record["income_eur"] is None for record in records)
    size_kb = OUTPUT_PATH.stat().st_size / 1024
    print(f"Escrito {OUTPUT_PATH.relative_to(Path.cwd())} | {size_kb:.1f} KB")
    print(f"Provincias: {len(provinces)} | registros: {len(records)}")
    print(f"Sin precio: {missing_price} | sin renta: {missing_income}")


if __name__ == "__main__":
    main()
