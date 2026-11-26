---
tags:
  - algoritmo
  - concepto
---

# ⚖️ Clasificación vs Regresión

> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es la división principal de los problemas de [[Aprendizaje Supervisado vs No Supervisado]] según **qué tipo de respuesta (`y`) queremos adivinar**: una **etiqueta/categoría** (Clasificación) o un **número continuo** (Regresión).

---

## ⚙️ Tabla Comparativa Directa

| Característica | 🌸 Clasificación | 📈 Regresión |
|---|---|---|
| **¿Qué predice (`y`)?** | **Una categoría o clase** (texto o grupo cerrado) | **Un número continuo** (dinero, temperatura, metros) |
| **Pregunta típica** | *"¿Qué especie de flor es?"* / *"¿Es spam o no?"* | *"¿Cuánto salario cobrará?"* / *"¿Cuánto vale este piso?"* |
| **Proyecto donde lo usé** | [[02-Clasificación Iris]] (`setosa`, `versicolor`, `virginica`) | [[03-Regresión Lineal desde Cero]] (`salario en miles de €`) |
| **Algoritmos típicos** | [[Regresión Logística]], [[Árbol de Decisión]], [[Random Forest]], [[SVM (Support Vector Machine)]] | [[Regresión Lineal]], Random Forest Regressor, SVR |
| **Métricas para poner nota** | [[Accuracy]], [[F1-Score (Precisión y Recall)]], [[Matriz de Confusión]] | [[MSE (Error Cuadrático Medio)]], [[R2 (Coeficiente de Determinación)]] |

---

## ⚠️ Trampa clásica de nombre: ¡La Regresión Logística es de CLASIFICACIÓN!
Aunque se llame [[Regresión Logística]], **sirve para CLASIFICAR** (porque calcula la probabilidad de 0% a 100% de pertenecer a cada categoría y elige la categoría con mayor porcentaje).
