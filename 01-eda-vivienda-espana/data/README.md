# Datos

- `raw/`: descargas originales tal cual llegan de la fuente. No se versiona.
- `interim/`: datos limpios pero aún sin métricas finales. No se versiona.
- `processed/`: datasets listos para el análisis. Se versionan si son pequeños.

Los directorios `raw/` e `interim/` se recrean ejecutando `src/download.py`.
