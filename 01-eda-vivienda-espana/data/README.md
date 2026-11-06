# Datos

- `raw/`: descargas originales tal cual llegan de la fuente. **Se versiona**: los ficheros son el registro de qué datos se usaron. Diccionario en [`raw/README.md`](raw/README.md).
- `interim/`: datos limpios pero aún sin métricas finales. No se versiona.
- `processed/`: datasets listos para el análisis. Se versionan si son pequeños.

`interim/` se regenera ejecutando el pipeline de `src/`; `raw/` no se regenera, se descarga y se conserva.

## Productos intermedios

| Fichero | Generado por | Filas | Contenido |
|---|---|---|---|
| `mitma_long.csv` | `python -m src.clean_mitma` | 13.674 | Valor tasado por serie, provincia y trimestre, 1995–2026 |
| `ipc_long.csv` | `python -m src.clean_ine` | 24 | Índice general anual, base 2025 = 100, 2002–2025 |
| `adrh_long.csv` | `python -m src.clean_ine` | 530 | Renta neta media por hogar, 2015–2024, con los huecos declarados |
| `ipv_long.csv` | `python -m src.clean_ine` | 1.560 | IPV trimestral, nacional y 19 CCAA, 2007T1–2026T2 |
