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

Páginas y endpoints de descarga:

- MITMA: <https://www.transportes.gob.es/el-ministerio/informacion-estadistica/vivienda-y-actuaciones-urbanas/estadisticas/valor-tasado-de-la-vivienda>
  - `https://apps.fomento.gob.es/BoletinOnline2/sedal/35101000.XLS`
  - `https://apps.fomento.gob.es/BoletinOnline2/sedal/35101500.XLS`
  - `https://apps.fomento.gob.es/BoletinOnline2/sedal/35102000.XLS`
- INE (CSV equivalente, para reproducir):
  - `https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/76144.csv`
  - `https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/53689.csv`
  - `https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/79563.csv`

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
  Excluir las islas y las filas duplicadas de CCAA uniprovinciales.
- **IPV**: solo contiene el índice `General`.

## Incidencias conocidas

| Incidencia | Detalle |
|---|---|
| 2026 parcial | MITMA con Q1–Q2; IPV hasta 2026T2. Excluir de medias anuales y YoY. |
| `n.r` en MITMA | Total: 17 celdas · Nueva: 162 · Usada: 3. Teruel, Huesca, Ceuta, Melilla, Ávila. |
| Huecos ADRH | Navarra 2015–2020, Álava 2015–2019, Total Nacional 2015–2020. Son de la fuente. |
| Sin IPC 2026 | La media anual de 2026 no existe hasta enero de 2027. |
| Nombres distintos | `Coruña (A)` ≠ `Coruña, A`; `Rioja (La)` ≠ `Rioja, La`; `Madrid (Comunidad de)` ≠ `Madrid, Comunidad de`; `Comunidad Valenciana` ≠ `Comunitat Valenciana`. Mapear por código INE. |
| Agregado Ceuta y Melilla | Existe en MITMA, no en ADRH. No usar como provincia. |

## Reglas de uso

1. `raw/` es inmutable: se lee, no se escribe.
2. Toda transformación va a `data/interim/` o `data/processed/`.
3. Nunca identificar provincias por nombre: usar código INE de 2 dígitos.
4. Cualquier fichero nuevo se añade a la tabla de fuentes de este documento.
