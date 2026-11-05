# Data Science Portfolio

Proyectos de análisis de datos, de la pregunta al hallazgo. Cada carpeta contiene un proyecto independiente, con su propio README, datos procesados, código y conclusiones.

## Proyectos

| # | Proyecto | Pregunta | Stack | Estado |
|---|----------|----------|-------|--------|
| 01 | [EDA Vivienda España](01-eda-vivienda-espana/) | ¿Cuánto esfuerzo cuesta comprar vivienda en España y dónde duele más? | Python · pandas · geopandas | En curso |

## Convenciones

- Un proyecto por carpeta, numerado: `NN-nombre-corto`.
- Los datos crudos (`data/raw`) y los intermedios (`data/interim`) no se versionan; se regeneran con `src/download.py`.
- Los datasets finales pequeños y las figuras sí se versionan.
- Cada proyecto incluye un README con pregunta, fuentes, metodología, hallazgos y limitaciones.

## Entorno

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Autor

Alejandro Cuntín
