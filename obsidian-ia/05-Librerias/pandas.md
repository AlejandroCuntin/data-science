---
tags:
  - libreria
  - codigo
---

# 🐼 pandas

> **Proyectos donde lo usé:** [[01-EDA Vivienda España]] · [[02-Clasificación Iris]] · [[03-Regresión Lineal desde Cero]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Para qué sirve en Data Science?
Es la librería reina para cargar, limpiar, cruzar y analizar **tablas de datos** (`DataFrames` y `Series`) en Python (`import pandas as pd`).

---

## 🛠️ Chuleta de Funciones que ya Dominamos

| Comando | ¿Qué hace? | Detalle clave que aprendimos |
|---|---|---|
| **`pd.read_csv("../data/iris.csv")`** | Carga un fichero CSV como DataFrame. | En Jupyter la ruta parte desde la carpeta del notebook (`notebooks/`), por eso usamos `..` para subir un nivel. |
| **`df.head()` / `df.columns`** | Muestra las 5 primeras filas / los nombres exactos de las columnas. | Python distingue mayúsculas y minúsculas (`'species'` $\neq$ `'Species'`). |
| **`df.drop(columns='species')`** | Devuelve la tabla quitando la columna respuesta (para crear `X`). | Separa las variables predictoras (`X`) de la etiqueta (`y = df['species']`). |
| **`df.to_csv("../data/salarios.csv", index=False)`** | Guarda tu DataFrame como archivo CSV en disco. | `index=False` evita que guarde una columna extra con los números de fila `0, 1, 2...`. |
| **`pd.Series(valores, index=nombres)`** | Crea una columna etiquetada de 1 dimensión. | Lo usamos para emparejar `best_rf.feature_importances_` con `X.columns` en [[Feature Importances]]. |
| **`df.groupby(...)` y `pd.merge(...)`** | Agrupa filas para resumirlas / Cruza dos tablas distintas. | Base de [[01-EDA Vivienda España]] (ver [[DataFrame, Limpieza y Deflactar]]). |
