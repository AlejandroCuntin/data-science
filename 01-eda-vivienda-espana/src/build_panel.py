"""Panel provincia-año: precios reales, renta y asequibilidad.

Une los tres CSV de data/interim/ que entran en el panel y escribe una fila por
territorio, año y tipo de vivienda. No grafica ni filtra el análisis: eso es el
notebook.
"""

from __future__ import annotations

import pandas as pd

from src.config import (
    ADRH_YEARS,
    ALL_TERRITORY_CODES,
    INTERIM_DIR,
    PARTIAL_YEAR_QUARTERS,
    PRICE_START_YEAR,
    PROCESSED_DIR,
    QUARTERS_PER_YEAR,
    REFERENCE_M2,
    SENSITIVITY_M2,
)

OUTPUT_PATH = PROCESSED_DIR / "panel_provincia_anual.csv"

COLUMNS = [
    "province_code", "year", "kind",
    "price_nominal_eur_m2", "price_real_eur_m2",
    "net_income_household_eur",
    "years_70m2", "years_90m2", "years_100m2",
    "quarters_used",
]


def annual_prices(mitma: pd.DataFrame) -> pd.DataFrame:
    """Media anual por territorio y tipo, descartando los años parciales."""
    # 2026 solo tiene dos trimestres: su media no es comparable con las demás.
    full = mitma[~mitma["year"].isin(PARTIAL_YEAR_QUARTERS)]

    annual = full.groupby(["kind", "province_code", "year"], as_index=False).agg(
        price_nominal_eur_m2=("price_eur_m2", "mean"),
        # Cuántos trimestres sostienen la media anual.
        quarters_used=("price_eur_m2", "count"),
    )
    # Se redondea antes de deflactar para que en 2025 nominal y real coincidan.
    annual["price_nominal_eur_m2"] = annual["price_nominal_eur_m2"].round(2)
    return annual


def deflate(df: pd.DataFrame, ipc: pd.DataFrame) -> pd.DataFrame:
    """Pasa los precios a euros de 2025 (IPC 2025 = 100)."""
    df = df.merge(
        ipc,
        on="year",
        how="left",
        # Un año puede repetirse en los precios, pero en el IPC solo una vez.
        validate="many_to_one",
    )
    df["price_real_eur_m2"] = df["price_nominal_eur_m2"] * 100 / df["ipc_index"]
    return df.drop(columns="ipc_index")


def add_affordability(df: pd.DataFrame, income: pd.DataFrame) -> pd.DataFrame:
    """Añade la renta del hogar y los años de renta por tamaño de vivienda."""
    # La renta cambia por provincia y año: unir solo por año mezclaría Madrid
    # con Barcelona.
    df = df.merge(
        income,
        on=["province_code", "year"],
        how="left",
        validate="many_to_one",
    )

    # En nominal a propósito: el IPC va en el numerador y el denominador.
    for m2 in sorted({REFERENCE_M2, *SENSITIVITY_M2}):
        df[f"years_{m2}m2"] = df["price_nominal_eur_m2"] * m2 / df["net_income_household_eur"]

    return df


def validate(df: pd.DataFrame) -> None:
    """Comprueba cobertura, deflactor y coherencia de la métrica."""
    if df.empty:
        raise ValueError("El panel está vacío")

    expected = set(ALL_TERRITORY_CODES)
    for kind, group in df.groupby("kind"):
        codes = set(group["province_code"])
        if codes != expected:
            raise ValueError(
                f"{kind}: faltan {sorted(expected - codes)}, sobran {sorted(codes - expected)}"
            )

    duplicated = int(df.duplicated(["kind", "province_code", "year"]).sum())
    if duplicated:
        raise ValueError(f"{duplicated} claves duplicadas (kind, provincia, año)")

    if not df["quarters_used"].between(0, QUARTERS_PER_YEAR).all():
        raise ValueError("Hay medias anuales con más trimestres que un año")

    # Deflactar a 2025 sube los precios anteriores: si baja, el IPC está cruzado.
    old = df.dropna(subset=["price_real_eur_m2"])
    old = old[old["year"] < 2025]
    if not (old["price_real_eur_m2"] > old["price_nominal_eur_m2"]).all():
        raise ValueError("Precio real <= nominal antes de 2025: revisa el IPC")

    priced = df.dropna(subset=["years_70m2", "years_90m2", "years_100m2"])
    if not (
        (priced["years_70m2"] <= priced["years_90m2"])
        & (priced["years_90m2"] <= priced["years_100m2"])
    ).all():
        raise ValueError("No se cumple years_70 <= years_90 <= years_100")

    if not priced["years_90m2"].between(0, 30, inclusive="neither").all():
        raise ValueError(
            "Años de renta fuera de rango "
            f"({priced['years_90m2'].min():.1f}-{priced['years_90m2'].max():.1f})"
        )

    with_income = set(df.loc[df["net_income_household_eur"].notna(), "year"])
    if with_income != set(ADRH_YEARS):
        raise ValueError(f"La renta no cubre exactamente {min(ADRH_YEARS)}-{max(ADRH_YEARS)}")


def main() -> None:
    # Sin dtype, pandas convierte "04" en 4 y el merge deja de casar.
    mitma = pd.read_csv(INTERIM_DIR / "mitma_long.csv", dtype={"province_code": str})
    ipc = pd.read_csv(INTERIM_DIR / "ipc_long.csv")
    income = pd.read_csv(INTERIM_DIR / "adrh_long.csv", dtype={"province_code": str})

    panel = annual_prices(mitma)
    panel = deflate(panel, ipc)
    panel = add_affordability(panel, income)
    panel = panel[panel["year"] >= PRICE_START_YEAR]

    validate(panel)

    panel = panel.sort_values(["province_code", "year", "kind"]).reset_index(drop=True)
    panel["price_real_eur_m2"] = panel["price_real_eur_m2"].round(2)
    for m2 in sorted({REFERENCE_M2, *SENSITIVITY_M2}):
        panel[f"years_{m2}m2"] = panel[f"years_{m2}m2"].round(2)

    panel = panel[COLUMNS]
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(OUTPUT_PATH, index=False)

    print(f"Escrito {OUTPUT_PATH}")
    print(f"Filas: {len(panel)}")
    for kind, group in panel.groupby("kind"):
        print(
            f"  {kind:6s} {len(group):4d} filas · "
            f"{group['province_code'].nunique()} territorios · "
            f"{group['year'].min()}-{group['year'].max()} · "
            f"{group['years_90m2'].notna().sum()} con renta"
        )


if __name__ == "__main__":
    main()
