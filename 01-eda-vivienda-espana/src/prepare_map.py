"""Cartografía provincial lista para los mapas.

Lee el GeoJSON del IGN de data/raw/cartografia/ (53 unidades, una de ellas
residual) y escribe un GeoJSON simplificado con las 52 provincias indexado por
código INE. El notebook pinta el mapa a partir de esta salida, nunca del raw.
"""

from __future__ import annotations

import json

import geopandas as gpd
from shapely import make_valid, set_precision
from shapely.geometry import mapping

from src.config import PROCESSED_DIR, PROVINCE_CODES, RAW_DIR

INPUT_PATH = RAW_DIR / "cartografia" / "provincias_ign.geojson"
OUTPUT_PATH = PROCESSED_DIR / "provincias.geojson"

# El servicio devuelve 53 unidades: 52 provincias y una residual de 7 km².
RESIDUAL_CODE = "54"

# En grados (~500 m). A tamaño de pantalla no se distingue y el fichero baja de
# decenas de MB a unos cientos de KB.
SIMPLIFY_TOLERANCE = 0.005

# Rejilla de 0,0001° (~11 m), por debajo del detalle que queda tras simplificar.
# Se aplica con set_precision y no redondeando floats al escribir: redondear a
# mano deja anillos degenerados que solo se ven al releer el fichero.
COORD_GRID = 0.0001

# La simplificación puede mover un poco el borde; más de un 1 % de superficie
# sería un error de la tolerancia, no un redondeo.
MAX_AREA_LOSS = 0.01


def vertex_count(geometry) -> int:
    """Vértices del anillo exterior y de los interiores."""
    polygons = geometry.geoms if geometry.geom_type == "MultiPolygon" else [geometry]
    return sum(
        len(polygon.exterior.coords) + sum(len(ring.coords) for ring in polygon.interiors)
        for polygon in polygons
    )


def total_area(geometries) -> float:
    """Superficie en km², medida en una proyección de área igual."""
    projected = gpd.GeoSeries(geometries, crs="EPSG:4326").to_crs("EPSG:3035")
    return float(projected.area.sum() / 1e6)


def load_provinces() -> gpd.GeoDataFrame:
    """Lee el raw y deja una fila por provincia con su código INE."""
    provinces = gpd.read_file(INPUT_PATH, engine="pyogrio")

    if provinces.crs is None or provinces.crs.to_epsg() != 4326:
        raise ValueError(f"Se esperaba EPSG:4326, llega {provinces.crs}")

    # El código INE son los caracteres 5 y 6 de nationalcode:
    # 34160100000 -> "01". No se usa el nombre, que cambia de grafía.
    provinces["province_code"] = provinces["nationalcode"].astype(str).str[4:6]

    residual = provinces[provinces["province_code"] == RESIDUAL_CODE]
    provinces = provinces[provinces["province_code"] != RESIDUAL_CODE].copy()

    codes = set(provinces["province_code"])
    if codes != PROVINCE_CODES:
        raise ValueError(
            "La cartografía no cubre el catálogo: "
            f"faltan {sorted(PROVINCE_CODES - codes)}, sobran {sorted(codes - PROVINCE_CODES)}"
        )
    if provinces["province_code"].duplicated().any():
        duplicated = provinces.loc[
            provinces["province_code"].duplicated(keep=False), "province_code"
        ]
        raise ValueError(f"Códigos repetidos en la cartografía: {sorted(set(duplicated))}")

    if provinces.geometry.is_empty.any() or provinces.geometry.isna().any():
        raise ValueError("Hay provincias sin geometría")
    if not provinces.geometry.is_valid.all():
        invalid = provinces.loc[~provinces.geometry.is_valid, "province_code"]
        raise ValueError(f"Geometrías inválidas en origen: {sorted(invalid)}")

    # Solo informa: la unidad residual existe y se descarta a propósito.
    if len(residual) != 1:
        raise ValueError(f"Se esperaba 1 unidad residual, hay {len(residual)}")

    return provinces


def simplify(provinces: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Simplifica la geometría, fija la rejilla y comprueba el daño."""
    before = total_area(provinces.geometry)

    def one(geometry):
        # preserve_topology evita que un polígono se parta en dos o se cierre
        # sobre sí mismo.
        simplified = geometry.simplify(SIMPLIFY_TOLERANCE, preserve_topology=True)
        # set_precision unifica los vértices en una rejilla: es lo que hace que
        # el fichero pese la mitad sin inventar geometrías.
        simplified = set_precision(simplified, COORD_GRID)
        return simplified if simplified.is_valid else make_valid(simplified)

    provinces = provinces.copy()
    provinces["geometry"] = provinces.geometry.apply(one)

    if not provinces.geometry.is_valid.all():
        invalid = provinces.loc[~provinces.geometry.is_valid, "province_code"]
        raise ValueError(f"Siguen inválidas tras simplificar: {sorted(invalid)}")

    after = total_area(provinces.geometry)
    loss = 1 - after / before
    if loss > MAX_AREA_LOSS:
        raise ValueError(
            f"La simplificación quita un {loss:.1%} de superficie "
            f"(tolerancia {SIMPLIFY_TOLERANCE}°): demasiado"
        )

    return provinces


def write_geojson(provinces: gpd.GeoDataFrame) -> None:
    """Escribe un FeatureCollection compacto, ordenado por código."""
    provinces = provinces.sort_values("province_code")

    features = []
    for code, name, geometry in zip(
        provinces["province_code"], provinces["nameunit"], provinces.geometry
    ):
        features.append(
            {
                "type": "Feature",
                # nameunit es la grafía del IGN, solo para leer el fichero a
                # ojo: la clave del cruce con el panel es province_code.
                "properties": {"province_code": code, "source_name": name},
                "geometry": {
                    "type": geometry.geom_type,
                    "coordinates": mapping(geometry)["coordinates"],
                },
            }
        )

    document = {"type": "FeatureCollection", "features": features}

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(document, file, ensure_ascii=False, separators=(",", ":"))


def validate_output() -> None:
    """Relee el fichero escrito: si no casa con el catálogo, no sirve."""
    provinces = gpd.read_file(OUTPUT_PATH, engine="pyogrio")

    if len(provinces) != len(PROVINCE_CODES):
        raise ValueError(f"El mapa tiene {len(provinces)} provincias, no 52")

    codes = set(provinces["province_code"])
    if codes != PROVINCE_CODES:
        raise ValueError(f"El mapa no cubre el catálogo: {sorted(PROVINCE_CODES ^ codes)}")

    if not provinces.geometry.is_valid.all() or provinces.geometry.is_empty.any():
        raise ValueError("El mapa escrito tiene geometrías inválidas o vacías")

    if set(provinces.geometry.geom_type) - {"Polygon", "MultiPolygon"}:
        raise ValueError(
            f"Geometrías que no son polígonos: {sorted(set(provinces.geometry.geom_type))}"
        )

    bounds = provinces.total_bounds
    # Sin Canarias el mapa saldría recortado y no se notaría.
    if bounds[0] > -12 or bounds[1] > 28:
        raise ValueError(f"El mapa pierde Canarias: límites {bounds.round(2)}")


def main() -> None:
    provinces = load_provinces()
    vertices_before = sum(vertex_count(geometry) for geometry in provinces.geometry)

    simplified = simplify(provinces)
    vertices_after = sum(vertex_count(geometry) for geometry in simplified.geometry)

    write_geojson(simplified)
    validate_output()

    size_kb = OUTPUT_PATH.stat().st_size / 1024
    print(f"Entrada: {INPUT_PATH.name} · {len(provinces)} provincias")
    print(f"Escrito {OUTPUT_PATH} · {size_kb:.0f} KB")
    print(
        f"Vértices: {vertices_before:,} → {vertices_after:,} "
        f"({vertices_after / vertices_before:.1%})"
    )
    print(
        f"Superficie: {total_area(simplified.geometry):,.0f} km² "
        f"(tolerancia {SIMPLIFY_TOLERANCE}°, rejilla {COORD_GRID}°)"
    )


if __name__ == "__main__":
    main()
