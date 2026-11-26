---
tags:
  - metrica
  - clasificacion
---

# 🎯 Accuracy

> **Proyecto donde lo usé:** [[02-Clasificación Iris]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es la métrica más básica de **clasificación**: mide simplemente el **porcentaje total de aciertos** sobre el total de casos evaluados.

---

## ⚙️ Fórmula y Ejemplo Real en [[02-Clasificación Iris]]

$$\text{Accuracy} = \frac{\text{Número de aciertos}}{\text{Total de flores del examen}}$$

En nuestras **30 flores de `X_test`**:
* [[Regresión Logística]], [[Árbol de Decisión]] y [[Random Forest]] acertaron las **30 de 30 flores** $\rightarrow$ $\frac{30}{30} = \mathbf{1.0000}$ (**100% de Accuracy**).
* [[SVM (Support Vector Machine)]] acertó **29 de 30 flores** (falló solo 1 flor frontera) $\rightarrow$ $\frac{29}{30} = \mathbf{0.9667}$ (**96.67% de Accuracy**).

---

## ⚠️ ¿Cuándo NO basta solo con el Accuracy? (La trampa de las clases desbalanceadas)
En Iris teníamos 50 flores de cada especie (dataset balanceado), por eso el `Accuracy` funciona genial.
Pero imagina un dataset con **98 flores *Setosa* y solo 2 *Virginica***:
* Un modelo vago que dijera siempre *"todas son Setosa"* sacaría un **98% de Accuracy**, a pesar de haber fallado el 100% de las *Virginica*.
* Para que nunca nos engañen con eso, acompañamos siempre el `Accuracy` con el [[F1-Score (Precisión y Recall)]] y la [[Matriz de Confusión]].
