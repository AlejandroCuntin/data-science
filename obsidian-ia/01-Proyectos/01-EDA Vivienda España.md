---
tags:
  - proyecto
  - eda
---

# 🏠 01 · EDA Vivienda España

> **Carpeta en el repositorio:** `01-eda-vivienda-espana/`
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 Pregunta Principal del Proyecto
**¿Cuánto esfuerzo real cuesta comprar una vivienda de 90 m² en España (medido en años de renta neta del hogar), cómo ha cambiado desde 2007 y qué provincias están en una situación más crítica?**

---

## 🧠 Conceptos Clave Aplicados

1. **Manipulación y Cruce de Fuentes Oficiales (MITMA + INE):**
   * Uso de [[DataFrame, Limpieza y Deflactar]] con [[pandas]] para cruzar precios de tasación (`MITMA`) con renta neta por hogar (`INE ADRH`) e inflación (`IPC`).
2. **Operaciones Esenciales de Data Science:**
   * **`groupby()`:** Resumir observaciones (por ejemplo, pasar de datos trimestrales a la media anual de cada provincia).
   * **`merge()`:** Combinar tablas de distintas fuentes usando claves comunes (código de provincia + año).
   * **Creación de métricas nuevas entre columnas:**
     $$\text{Años de renta} = \frac{\text{Precio m}^2 \times 90}{\text{Renta neta anual del hogar}}$$
3. **Economía Aplicada a Datos (Deflactar):**
   * Convertir precios nominales a **euros reales** descontando el efecto de la inflación (IPC) para poder comparar 2007 con 2025 de forma justa.

---

## 🔗 Conexiones en el Grafo
* **Conceptos:** [[DataFrame, Limpieza y Deflactar]] · [[EDA y Pairplot]]
* **Librerías:** [[pandas]] · [[NumPy]] · [[matplotlib y seaborn]]
