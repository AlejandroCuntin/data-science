---
tags:
  - metrica
  - clasificacion
---

# 🔲 Matriz de Confusión

> **Proyecto donde lo usé:** [[02-Clasificación Iris]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Mientras el [[Accuracy]] te dice **cuántas** flores falló un modelo, la **Matriz de Confusión** es una tabla de $3 \times 3$ que te muestra exactamente **qué especie real confundió con cuál**.

---

## ⚙️ Cómo se lee una Matriz de Confusión

* **Filas (Eje vertical `True label`):** La especie **REAL** de la flor.
* **Columnas (Eje horizontal `Predicted label`):** La especie que **PREDICE** el modelo.
* **La Diagonal Principal (`\`)**: Son los **ACIERTOS** (cuando la realidad coincide con lo que dijo el modelo).
* **Cualquier número fuera de la diagonal:** Son las **CONFUSIONES / ERRORES**.

```text
           Matriz del SVM en nuestras 30 flores de Test (29/30 aciertos)
                       Predicción del Modelo
                   setosa   versicolor   virginica
Realidad  setosa   [ 10 ]       0            0       <-- 10 de 10 Setosa acertadas
       versicolor    0        [ 8 ]         (1)      <-- ¡Cazada! 1 Versicolor confundida con Virginica
        virginica    0          0         [ 11 ]     <-- 11 de 11 Virginica acertadas
```

---

## 🔬 Qué nos demostró en [[02-Clasificación Iris]]
Al pintar `ConfusionMatrixDisplay.from_estimator(...)` comparando [[Random Forest]] (`30/30` en la diagonal) frente a [[SVM (Support Vector Machine)]] (`29/30`), confirmamos lo que habíamos visto en el [[EDA y Pairplot]]:
* *Setosa* nunca falla (`10/10`).
* El único fallo de todo el examen ocurrió en la frontera donde *Versicolor* y *Virginica* se rozan.
