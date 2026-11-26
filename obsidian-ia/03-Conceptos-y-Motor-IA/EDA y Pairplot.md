---
tags:
  - concepto
  - eda
---

# 🔍 EDA y Pairplot

> **Proyectos donde lo usé:** [[01-EDA Vivienda España]] · [[02-Clasificación Iris]] · [[03-Regresión Lineal desde Cero]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es el EDA y qué es un Pairplot?
* **EDA (*Exploratory Data Analysis*):** Es mirar y dibujar los datos antes de entrenar cualquier modelo para entender qué patrones, errores o fronteras tienen.
* **Pairplot (Gráfico por parejas / Matriz de dispersión):** Es un gráfico de [[matplotlib y seaborn]] (`sns.pairplot`) que **cruza todas tus columnas numéricas de 2 en 2** coloreando cada punto según su categoría (`hue="species"`).

---

## ⚙️ Cómo leer los 16 cuadros del Pairplot de [[02-Clasificación Iris]] sin volverse loco

Como una pantalla solo tiene 2 ejes ($X$ e $Y$), no podemos pintar 4 medidas juntas en un solo cuadro. El Pairplot crea una tabla de $4 \times 4 = 16$ cuadros dividida en **3 zonas**:

```text
                 Col 1           Col 2          Col 3           Col 4
              sepal_length    sepal_width    petal_length    petal_width
            +---------------+--------------+---------------+--------------+
Fila 1      | 🏔️ DIAGONAL 1 |   (Espejo)   |   (Espejo)    |   (Espejo)   |
sepal_length|               |              |               |              |
            +---------------+--------------+---------------+--------------+
Fila 2      |   Gráfica A   | 🏔️ DIAGONAL 2|   (Espejo)    |   (Espejo)   |
sepal_width |               |              |               |              |
            +---------------+--------------+---------------+--------------+
Fila 3      |   Gráfica B   |  Gráfica C   | 🏔️ DIAGONAL 3 |   (Espejo)   |
petal_length|               |              |               |              |
            +---------------+--------------+---------------+--------------+
Fila 4      |   Gráfica D   |  Gráfica E   | ⭐ GRÁFICA F  | 🏔️ DIAGONAL 4|
petal_width |               |              |               |              |
            +---------------+--------------+---------------+--------------+
```

1. **Los 6 cuadros de arriba a la derecha (`Espejo`) $\rightarrow$ ¡Se ignoran!** Son exactamente los mismos 6 gráficos de abajo pero con los ejes girados.
2. **Las 4 gráficas de la `🏔️ DIAGONAL` (Montañas de densidad):** Muestra dónde se concentran los valores de cada medida individual:
   * En `sepal_width` las 3 montañas se pisan (mala medida para distinguir flores).
   * En `petal_length` y `petal_width` la montaña de *Setosa* está 100% sola a la izquierda.
3. **Las 6 gráficas de puntos de abajo a la izquierda:** Cada punto es una de las 150 flores.
   * En la **`⭐ GRÁFICA F` (`petal_length` vs `petal_width`)** los puntos suben en diagonal (*cuanto más largo es el pétalo, más ancho es*) y se ve que los **pétalos** separan las 3 especies casi a la perfección (algo que luego confirmó matemáticamente [[Feature Importances]] con un **86.68%** de peso).

---

## 🎲 ¿Qué es el "Ruido" en un gráfico de dispersión?
Como vimos en [[03-Regresión Lineal desde Cero]] (`ruido = np.random.normal(0, 2.0, size=30)`), en la vida real los datos nunca forman una línea recta perfecta hecha con regla: dos trabajadores con la misma experiencia cobran un poquito distinto ($\pm 2.000\text{ €}$). Esa variación aleatoria natural alrededor del patrón se llama **ruido**, y un buen modelo debe **ignorar el ruido** y quedarse solo con la tendencia general (evitando el [[Overfitting vs Underfitting]]).
