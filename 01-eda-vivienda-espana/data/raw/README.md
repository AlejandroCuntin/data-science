# Datos raw

Descargas originales, sin transformar. No se editan a mano.

**Fecha de descarga**: 2026-11-06
**Última revisión**: 2026-11-06

## Fuentes

| Fichero | Fuente | Tabla / código | Nivel | Cobertura | Unidad |
|---|---|---|---|---|---|
| `mitma_35101000_libre.xls` | MITMA · Valor tasado | 35101000 | Nacional, CCAA, provincia | 1995–2026 | €/m² |
| `mitma_35101500_libre_nueva.xls` | MITMA · Valor tasado | 35101500 | Nacional, CCAA, provincia | 2010–2026 | €/m² |
| `mitma_35102000_libre_usada.xls` | MITMA · Valor tasado | 35102000 | Nacional, CCAA, provincia | 2010–2026 | €/m² |
| `ine_ipc_76144_anual.xlsx` | INE · IPC base 2025 | 76144 | Nacional | 2002–2025 | índice (2025 = 100) |
| `ine_adrh_53689_provincial.xlsx` | INE · ADRH | 53689 | Nacional, CCAA, provincia, isla | 2015–2024 | €/hogar/año |
| `ine_ipv_79563_ccaa.xlsx` | INE · IPV base 2025 | 79563 | Nacional, CCAA | 2007T1–2026T2 | índice (2025 = 100) |
| `cartografia/provincias_ign.geojson` | IGN · Unidades administrativas (BDLJE) | `nationallevelname=Provincia` | Provincia | 53 unidades (52 provincias + 1 residual) | polígonos, EPSG:4326 |

Páginas y endpoints de descarga:

- MITMA: <https://www.transportes.gob.es/el-ministerio/informacion-estadistica/vivienda-y-actuaciones-urbanas/estadisticas/valor-tasado-de-la-vivienda>
  - `https://apps.fomento.gob.es/BoletinOnline2/sedal/35101000.XLS`
  - `https://apps.fomento.gob.es/BoletinOnline2/sedal/35101500.XLS`
  - `https://apps.fomento.gob.es/BoletinOnline2/sedal/35102000.XLS`
- INE (CSV equivalente, para reproducir):
  - `https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/76144.csv`
  - `https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/53689.csv`
  - `https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/79563.csv`
- IGN · API OGC-Features de unidades administrativas (ver *Cartografía provincial*):
  - `https://api-features.ign.es/collections/administrativeunit/items?nationallevelname=Provincia&limit=10&offset=0&f=json`

## Qué mide cada cosa

- **Valor tasado**: valoración media de la vivienda libre, no precio de transacción.
- **Vivienda libre total** = media ponderada por número de tasaciones de nueva y usada.
- **ADRH · renta neta media por hogar**: renta neta anual del hogar, en euros corrientes.
- **IPC**: deflactor a euros constantes de 2025 (2025 = 100).
- **IPV**: contraste externo de la tendencia; solo `General`.

## Estructura de los ficheros MITMA

- Cada pestaña cubre un bloque de 4 años (5 en nueva/usada).
- Columnas = años × 4 trimestres + 2 columnas finales de **variación porcentual**.
  Esas dos últimas **no son €/m²** y hay que descartarlas.
- 2026 solo tiene Q1 y Q2 publicados.
- La columna de territorios mezcla cuatro niveles: total nacional, 17 CCAA,
  provincias y el agregado `Ceuta y Melilla`. Las 52 provincias se obtienen con
  43 filas explícitas + 7 CCAA uniprovinciales + Ceuta + Melilla.
- Última fila de la columna de territorios es una nota (`n.r: ...`), no un territorio.
- Las celdas `n.r` son texto: convertir a nulo.

## Estructura de los ficheros INE

- Formato "informe": cabecera en las primeras filas, territorios en columnas
  y años/trimestres en filas, o al revés según la tabla. No usar `header=0`.
- **ADRH**: 82 bloques = 1 nacional + 19 CCAA/ciudades + 52 provincias + 10 islas.
  Excluir las islas y las filas duplicadas de CCAA uniprovinciales. Los bloques
  se resuelven **por posición**: `Balears, Illes`, `Cantabria`, `Rioja, La`,
  `Ceuta` y `Melilla` aparecen dos veces con el mismo nombre (CCAA y provincia).
- **IPV**: solo contiene el índice `General`, para Nacional y 19 CCAA; no hay
  provincias.
- **Código `00`**: convención propia para la serie de España (Total
  Nacional/Nacional). No es un código INE y no debe mezclarse con provincias.

## Incidencias conocidas

| Incidencia | Detalle |
|---|---|
| 2026 parcial | MITMA con Q1–Q2; IPV hasta 2026T2. Excluir de medias anuales y YoY. |
| `n.r` y vacíos en MITMA | Total: 89 celdas (17 `n.r` + 72 vacías), 1995–2013 · Nueva: 355, 2010–2026 · Usada: 3 (Ceuta y Melilla, 2013). Se conservan como fila con valor nulo. |
| Huecos ADRH | Navarra 2015–2020, Álava 2015–2019, Total Nacional 2015–2020 y Gipuzkoa 2015 (marcado `..`). Son de la fuente. |
| Sin IPC 2026 | La media anual de 2026 no existe hasta enero de 2027. |
| Nombres distintos | `Coruña (A)` ≠ `Coruña, A`; `Rioja (La)` ≠ `Rioja, La`; `Madrid (Comunidad de)` ≠ `Madrid, Comunidad de`; `Comunidad Valenciana` ≠ `Comunitat Valenciana`. Mapear por código INE. |
| Agregado Ceuta y Melilla | Existe en MITMA, no en ADRH. No usar como provincia. |
| Cartografía: descarga única corrupta | `limit=100` devuelve 187 MB con un corchete perdido. Descargar por tandas con `offset`. |

## Cartografía provincial

`cartografia/provincias_ign.geojson` son los límites provinciales del IGN (BDLJE),
en WGS84, para pintar los mapas del análisis. Se lee, no se edita: la versión
simplificada que consumen los notebooks se genera con `src/prepare_map.py`.

- **Descarga**: 2026-11-08 · <https://api-features.ign.es/collections/administrativeunit/items>
- **Licencia**: CC-BY 4.0 · atribución al Instituto Geográfico Nacional (IGN/CNIG).
- **Tamaño**: 38.643.018 bytes · SHA-256 `CACDD9B345B54A677503710825A400B4CCC379D489D10ECD314BF812489C359F`.
- **Contenido**: 53 elementos con `nationallevelname = "Provincia"`, EPSG:4326,
  1.193.428 vértices. No es exactamente lo que devuelve el servicio, ver abajo.

Cómo se generó, porque el fichero no es una descarga literal:

1. La petición única (`limit=100`, 187 MB) llega **corrupta**: falta un corchete
   a la altura de Málaga y fallan `json` y `pyogrio` (GDAL) en el mismo carácter.
2. Se descargó en 6 tandas de 10 con `offset=0,10,20,30,40,50`, todas completas
   (`numberReturned` = `len(features)`).
3. Se unieron en un único `FeatureCollection` **sin tocar ninguna coordenada**,
   solo eliminando la sangría de 4 espacios con la que el servicio formatea
   (de 187 a 39 MB).

Campos y uso:

- `nationalcode` es la clave: sus caracteres 5 y 6 son el código INE de la
  provincia (`34160100000` → `01` Álava). `nameunit` es solo para mostrar.
- `codnut3` viene nulo en todas y no se usa.
- La unidad `54 | Territorios no asociados a ninguna provincia` es un residuo
  del IGN de 7 km² (islotes y zonas sin asignar). No es una provincia y se
  descarta al cruzar con el panel, que es lo que da las 52.

Validación en la descarga: 53/53 geometrías válidas y no vacías, extensión
−18,16 a 4,33 de longitud y 27,64 a 43,79 de latitud (entra Canarias y El
Hierro), superficie total 506.079 km² frente a ~505.990 oficiales.

## Reglas de uso

1. `raw/` es inmutable: se lee, no se escribe.
2. Toda transformación va a `data/interim/` o `data/processed/`.
3. Nunca identificar provincias por nombre: usar código INE de 2 dígitos.
4. Cualquier fichero nuevo se añade a la tabla de fuentes de este documento.
