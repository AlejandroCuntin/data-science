# Datos

- `raw/`: descargas originales tal cual llegan de la fuente. **Se versiona**: los ficheros son el registro de qué datos se usaron. Diccionario en [`raw/README.md`](raw/README.md).
- `interim/`: datos limpios pero aún sin métricas finales. No se versiona.
- `processed/`: datasets listos para el análisis. Se versionan si son pequeños.

`interim/` se regenera ejecutando el pipeline de `src/`; `raw/` no se regenera, se descarga y se conserva.
