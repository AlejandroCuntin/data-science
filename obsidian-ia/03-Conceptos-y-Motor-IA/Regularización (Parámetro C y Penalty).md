---
tags:
  - concepto
  - motor-ia
---

# ⚖️ Regularización (Parámetro C y Penalty)

> **Proyecto donde lo usé:** [[02-Clasificación Iris]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es un "castigo matemático" que le ponemos a los modelos (como [[Regresión Logística]] o [[SVM (Support Vector Machine)]]) para prohibirles poner pesos ($w$) gigantescos y evitar que memoricen los datos ([[Overfitting vs Underfitting]]).

---

## ⚠️ ¡Cuidado! La Inversión del Parámetro `C` en [[scikit-learn]]

En `scikit-learn`, el parámetro **`C` funciona al revés** de lo que parece por su nombre, porque es el **inverso** de la fuerza de penalización ($C = \frac{1}{\lambda}$):

* **📉 `C` muy PEQUEÑO (ej. `0.0001` o `0.1`):**
  * **Penalización MÁXIMA** (modelo muy atado de manos).
  * En [[Regresión Logística]]: Si te pasas de pequeño, obliga a que todos los pesos sean casi $0$, causando **Underfitting** (no aprende nada).
  * En [[SVM (Support Vector Machine)]]: Prioriza una "carretera" (margen) muy ancha y suave aunque alguna flor quede en el lado equivocado.
* **📈 `C` muy GRANDE (ej. `100` o `10.000`):**
  * **Penalización MÍNIMA o NULA** (libertad total para el modelo).
  * El modelo se vuelve súper estricto intentando no fallar ni un solo dato de `Train`, con riesgo de **Overfitting**.

*(Por eso usamos [[RandomizedSearchCV y Validación Cruzada]] con `np.logspace(-4, 4, 10)` en [[02-Clasificación Iris]] para probar desde $0.0001$ hasta $10.000$ y encontrar el punto medio perfecto: **`C = 21.54`** en Regresión Logística y **`C = 10`** en SVM).*

---

## 🧬 Tipos de Penalización (`penalty`)
* **L2 (Ridge):** Castiga la suma de los pesos al cuadrado ($\sum w_i^2$). Reduce todos los pesos suavemente sin hacerlos cero. Ideal cuando todas las medidas aportan información.
* **L1 (Lasso):** Castiga el valor absoluto ($\sum |w_i|$). Fuerza a que las columnas inútiles pasen a valer **exactamente 0** (actúa como selector de variables).
* **ElasticNet:** Combina L1 y L2.
