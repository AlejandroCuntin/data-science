# AGENTS.md

Proyecto `01-eda-vivienda-espana`. Este archivo es específico de este proyecto:
cada carpeta del portfolio (`02`, `03`, ...) tendrá el suyo.

- Objetivo y metodología: `README.md`.
- Datos, fuentes y diccionario: `data/raw/README.md`.
- Portada del portfolio: `../README.md`.
- Dependencias: `../requirements.txt`.

## Entorno

- Python 3.13. Dependencias en `../requirements.txt`.
- `xlrd` es imprescindible para los `.xls` de MITMA (está instalado, pero aún no
  figura en `../requirements.txt`); `openpyxl` para los `.xlsx` del INE.

## Reglas de datos (no negociables)

- `data/raw/` es inmutable y está versionado: se lee, nunca se escribe ni se
  reformatea. Si un fichero está mal, se descarga de nuevo y se sustituye.
- Toda transformación va a `data/interim/` o `data/processed/`.
- Las provincias se identifican por código INE de 2 dígitos, nunca por nombre:
  MITMA, ADRH e IPV usan grafías distintas para la misma provincia.
- 2026 es parcial (solo Q1–Q2): excluir de medias anuales y variaciones
  interanuales, y marcarlo en las gráficas.
- No interpolar los huecos de renta (Navarra 2015–2020, Álava 2015–2019,
  Total Nacional 2015–2020, Gipuzkoa 2015). Se declaran, no se rellenan.
- El valor tasado no es precio de transacción: no presentarlo como tal.
- La cartografía vive en `data/raw/cartografia/`. El código INE de cada polígono
  sale de `nationalcode` y se valida contra `PROVINCES` antes de simplificar:
  el IGN sirve 53 unidades, una más que provincias.

## Convenciones

- Los notebooks solo leen de `data/processed/`; la limpieza y las métricas viven
  en `src/`.
- Código e identificadores en inglés; documentación y narrativa en español.
- Un notebook = una pregunta. Nada de celdas de limpieza suelta.
- Los notebooks se numeran (`00_auditoria`, `01_precios`, ...) y se ejecutan de
  arriba a abajo sin errores antes de commitear.

## Git

- `main` siempre presentable. Ramas cortas por fase (`01/limpieza`), fusionadas al
  terminar y borradas después.
- No reescribir historia ni hacer `force push`.
- `data/raw/` se versiona a propósito: los ficheros originales son parte del
  proyecto. `data/interim/` no se versiona.
