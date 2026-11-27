# Data Science Portfolio

Proyectos de análisis de datos, de la pregunta al hallazgo. Cada carpeta contiene un proyecto independiente, con su propio README, datos procesados, código y conclusiones.

## Proyectos

| # | Proyecto | Pregunta | Stack | Estado |
|---|----------|----------|-------|--------|
| 01 | [EDA Vivienda España](01-eda-vivienda-espana/) | ¿Cuánto esfuerzo cuesta comprar vivienda en España y dónde duele más? | Python · pandas · geopandas · JS | Completado |
| 02 | [Clasificación Iris](02-iris-clasificación/) | ¿Cómo clasificar especies de flores comparando Regresión Logística, Árbol de Decisión, Random Forest y SVM? | Python · pandas · scikit-learn · seaborn | Completado |
| 03 | [Regresión Lineal desde Cero](03-regresión-lineal/) | ¿Cómo aprende una máquina bajo el capó programando una Regresión Lineal y el Descenso del Gradiente 100% desde cero con NumPy? | Python · NumPy · matplotlib | Completado |
| 04 | [Supervivencia del Titanic](04-titanic-supervivencia/) | ¿Qué factores determinaron sobrevivir al Titanic limpiando datos reales con nulos y aplicando Feature Engineering? | Python · pandas · scikit-learn · seaborn | En progreso |

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

Alejandro Cuntin Bariteau
