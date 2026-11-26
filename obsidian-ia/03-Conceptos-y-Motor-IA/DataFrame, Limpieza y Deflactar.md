---
tags:
  - concepto
  - eda
  - preprocesamiento
---

# 🧹 DataFrame, Limpieza y Deflactar

> **Proyecto donde lo usé:** [[01-EDA Vivienda España]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 Conceptos Fundamentales de Manipulación de Datos

### 1. DataSet vs DataFrame
* **DataSet:** El conjunto de datos en bruto (por ejemplo, el fichero `iris.csv`, `salarios.csv` o las tablas descargadas del INE y MITMA).
* **DataFrame:** La tabla inteligente cargada en la memoria de Python mediante [[pandas]] (`pd.read_csv(...)`) con filas y columnas listas para filtrar, limpiar y operar.

---

### 2. Las 3 Operaciones Esenciales de [[pandas]] en Data Science

1. **`groupby()` (Agrupar y resumir):**
   Agrupa muchas filas que comparten una categoría (por ejemplo, los 4 trimestres de un mismo año y provincia) para calcular su media (`.mean()`), suma (`.sum()`) o conteo.
2. **`merge()` (Cruzar fuentes distintas):**
   Une dos tablas diferentes que comparten una columna común (como un `JOIN` de SQL). En [[01-EDA Vivienda España]] cruzamos la tabla de precios de vivienda (`MITMA`) con la tabla de renta de los hogares (`INE`) por provincia y año.
3. **Operaciones entre columnas (Ingeniería de variables / *Feature Engineering*):**
   Crear una métrica nueva operando columnas existentes:
   $$\text{Años de renta para comprar 90 m}^2 = \frac{\text{Precio m}^2 \times 90}{\text{Renta neta anual}}$$

---

### 3. Expresiones Regulares (Regex) y Limpieza
Patrones de búsqueda de texto que permiten limpiar nombres sucios de provincias, extraer códigos postales o eliminar símbolos extraños (`n.r`, puntos de miles, espacios) antes de convertir una columna a número.

---

### 4. ¿Qué significa Deflactar?
En series temporales de dinero (como precios de vivienda de 2007 a 2025), **1.000 € de 2007 no compran lo mismo que 1.000 € de 2025** por culpa de la inflación.
* **Precio Nominal:** El precio tal cual se pagó en aquel año (sin corregir inflación).
* **Precio Real (Deflactado):** El precio corregido dividiéndolo por el índice de inflación (**IPC**), para expresar todos los años en euros equivalentes de hoy y poder comparar épocas distintas sin engaños.
