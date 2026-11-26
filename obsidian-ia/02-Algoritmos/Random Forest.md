---
tags:
  - algoritmo
  - clasificacion
  - ensamble
---

# 🌲 Random Forest

> **Proyecto donde lo usé:** [[02-Clasificación Iris]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es un algoritmo de ensamble (*Bagging*) que entrena **cientos de [[Árbol de Decisión|Árboles de Decisión]] distintos** (dándole a cada árbol flores y medidas elegidas al azar) y decide la predicción final por **mayoría de votos**.

---

## ⚙️ ¿Cómo funciona a nivel técnico (sus 3 secretos)?

Si entrenaras 200 árboles con las mismas 120 flores y las mismas 4 medidas, los 200 árboles saldrían clones idénticos y se equivocarían en lo mismo. Para que sean distintos entre sí, Random Forest aplica:

1. **Bootstrapping (Muestreo de filas con reemplazo):**
   Cada árbol se entrena con una selección aleatoria de las 120 flores (ve ~63.2% de flores únicas).
2. **Random Subspace (Subconjunto aleatorio de columnas en cada corte):**
   En cada pregunta, el árbol no puede elegir entre las 4 medidas de la flor; se le obliga a elegir solo entre $\sqrt{4} = 2$ medidas al azar. Así ningún árbol se copia de otro.
3. **Agregación por Votación Democrática:**
   Cuando entra una flor del Test, los 200 árboles votan. Al promediar árboles descorrelacionados, **la varianza (los errores individuales) se reduce** sin aumentar el sesgo.

---

## 🎛️ Sus Hiperparámetros Clave y Resultados en [[02-Clasificación Iris]]

* **`n_estimators` (Número de árboles):** Probamos `[100, 200, 300]` y ganó **`200`**.
  * *¿Más árboles es siempre mejor?* No produce [[Overfitting vs Underfitting]], pero a partir de 100-200 árboles llega a una asíntota (ya no mejora la precisión y solo gasta más memoria y tiempo de CPU).
* **`max_depth` (Profundidad máxima de cada árbol):** Limita cuántas preguntas encadenadas puede hacer cada árbol individual.
* **Bonus estrella:** Guarda dentro `best_rf.feature_importances_` (ver [[Feature Importances]]), con el que descubrimos que los pétalos tienen el **86.68%** del peso de la decisión.
