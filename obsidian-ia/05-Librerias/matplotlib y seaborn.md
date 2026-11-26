---
tags:
  - libreria
  - codigo
  - eda
---

# 🎨 matplotlib y seaborn

> **Proyectos donde lo usé:** [[01-EDA Vivienda España]] · [[02-Clasificación Iris]] · [[03-Regresión Lineal desde Cero]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Para qué sirven y en qué se diferencian?
* **`matplotlib.pyplot as plt`:** Es el lienzo base de Python para dibujar puntos (`plt.scatter`), líneas (`plt.plot`), poner títulos, hacer zoom (`plt.ylim`) y guardar los archivos PNG en alta resolución (`plt.savefig`).
* **`seaborn as sns`:** Construida encima de `matplotlib`, permite crear gráficos estadísticos complejos (como el [[EDA y Pairplot]]) en una sola línea de código.

---

## 🛠️ Los 4 Gráficos Clave que Hemos Creado

1. **Gráfico de Dispersión (*Scatter Plot*):**
   ```python
   plt.scatter(X, y, color="royalblue", label="Datos reales")
   ```
   Dibuja una nube de puntos $(X, y)$. Usado en la Fase 1 de [[03-Regresión Lineal desde Cero]].
2. **Gráfico de Línea / Recta o Curva de Error (*Line Plot*):**
   ```python
   plt.plot(X, y_pred_final, color="forestgreen", linewidth=2.5)
   ```
   Dibuja la recta aprendida o la caída del error [[MSE (Error Cuadrático Medio)]] época tras época.
3. **Pairplot (Matriz de dispersión por parejas):**
   ```python
   sns.pairplot(iris_df, hue="species", diag_kind="kde", palette="Set2")
   ```
   Cruza las 4 medidas de [[02-Clasificación Iris]] coloreadas por especie (ver [[EDA y Pairplot]]).
4. **Exportación Limpia a `reports/figures/`:**
   ```python
   plt.savefig("../reports/figures/nombre_grafico.png", dpi=150, bbox_inches="tight")
   ```
   `dpi=150` da nitidez para el `README.md` de GitHub y `bbox_inches="tight"` evita que se corten los títulos o leyendas.
