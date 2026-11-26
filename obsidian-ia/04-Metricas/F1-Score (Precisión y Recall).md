---
tags:
  - metrica
  - clasificacion
---

# ⚖️ F1-Score (Precisión y Recall)

> **Proyecto donde lo usé:** [[02-Clasificación Iris]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es la nota de **clasificación** que equilibra dos exigencias especie por especie: que el modelo **no dé falsas alarmas (*Precisión*)** y que **no se le escape ningún caso real sin detectar (*Recall / Exhaustividad*)**.

---

## ⚙️ Las 2 Piezas que Une el F1-Score

Imagina que evaluamos qué tal detecta la especie **Virginica**:

1. **Precisión (*Precision* — "No dar falsas alarmas"):**
   De todas las veces que el modelo gritó *"¡Es una Virginica!"*, ¿cuántas eran *Virginica* de verdad?
2. **Recall (*Exhaustividad* — "Que no se escape ninguna"):**
   De todas las *Virginica* reales que había en el jardín, ¿cuántas logró cazar el modelo sin confundirlas con otra especie?
3. **F1-Score:** Es la media armónica de las dos. Si una de las dos falla, el `F1-Score` cae inmediatamente.

---

## 🔬 Código y Ejemplo en [[02-Clasificación Iris]]

```python
from sklearn.metrics import f1_score
f1 = f1_score(y_test, y_pred, average="macro")
```
* **¿Qué hace `average="macro"`?** Calcula el `F1-Score` de *Setosa*, el de *Versicolor* y el de *Virginica* por separado y hace la media dándole exactamente la misma importancia a las 3 especies.
* En [[02-Clasificación Iris]], [[Random Forest]] y [[Regresión Logística]] sacaron **`1.0000`** (ni una falsa alarma ni una flor escapada), mientras que [[SVM (Support Vector Machine)]] sacó **`0.9659`** por la única flor *Versicolor* que confundió con *Virginica* en la [[Matriz de Confusión]].
