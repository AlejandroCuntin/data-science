---
tags:
  - algoritmo
  - clasificacion
---

# 🎯 Regresión Logística

> **Proyecto donde lo usé:** [[02-Clasificación Iris]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Aunque se llame "regresión", es un **algoritmo de clasificación** que utiliza una fórmula matemática (la función sigmoide / softmax) para calcular la **probabilidad entre 0 y 1 (0% a 100%)** de que un dato pertenezca a cada categoría, eligiendo la categoría con mayor porcentaje.

---

## ⚙️ ¿Cómo funciona por dentro?

Cuando entra una flor nueva en [[02-Clasificación Iris]], la Regresión Logística no dice de golpe *"es Setosa"*. Calcula 3 probabilidades que suman el 100%:
* *Setosa:* `0.95` (**95%**) $\rightarrow$ **¡Ganadora!**
* *Versicolor:* `0.04` (**4%**)
* *Virginica:* `0.01` (**1%**)

En código de [[scikit-learn]]:
* `modelo.predict(X_test)` $\rightarrow$ Te devuelve directamente la etiqueta ganadora (`"setosa"`).
* `modelo.predict_proba(X_test)` $\rightarrow$ Te enseña los 3 porcentajes `[0.95, 0.04, 0.01]`.

---

## 🎛️ Hiperparámetros y Requisitos Clave

1. **Necesita [[StandardScaler (Escalado)]] obligatoriamente:** Como multiplica cada medida por un peso ($w$) y aplica penalización, si una columna tuviera números de 10.000 y otra de 1, se distorsionaría el aprendizaje.
2. **`max_iter=1000`:** Número máximo de pasos que le damos al optimizador matemático para que converja sin quedarse a medias.
3. **`C` y `penalty`:** Controlan la fuerza de [[Regularización (Parámetro C y Penalty)]] para evitar el [[Overfitting vs Underfitting]].
   * En [[02-Clasificación Iris]], con [[RandomizedSearchCV y Validación Cruzada]] ganó **`C = 21.54`**, logrando un **95.83%** en validación cruzada y un **100%** de [[Accuracy]] en Test.
