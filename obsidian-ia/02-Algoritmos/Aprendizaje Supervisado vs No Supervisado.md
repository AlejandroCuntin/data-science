---
tags:
  - algoritmo
  - concepto
---

# 🎯 Aprendizaje Supervisado vs No Supervisado

> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
* **Aprendizaje Supervisado:** Entrenas a la máquina dándole **las preguntas (`X`) y también las respuestas correctas (`y`)** para que aprenda la relación.
* **Aprendizaje No Supervisado (Clustering):** Solo tienes los datos (`X`) **sin respuestas (`y`)**, y la máquina agrupa los puntos a ciegas fijándose solo en cuáles están más cerca unos de otros.

---

## 🔬 Mi Ejemplo Real: ¿Por qué el [[EDA y Pairplot]] NO es un K-Means?

Cuando pintamos el Pairplot en [[02-Clasificación Iris]] vimos 3 nubes de puntos de colores. Es fácil confundirlo con **K-Means**, pero hacen cosas totalmente distintas:

| | Gráfico Pairplot (`seaborn`) | Modelos Supervisados (LogReg / RF / SVM) | K-Means (No Supervisado) |
|---|---|---|---|
| **¿Qué es?** | **Un dibujo** para tus ojos | **Clasificación Supervisada** | **Clustering No Supervisado** |
| **¿Usa la columna `species`?** | **Sí**, simplemente lee lo que escribió el botánico y pinta el punto de ese color. No adivina nada. | **Sí**, estudia `species` en las 120 flores de `Train` para adivinarla en las 30 flores de `Test`. | **No**. Se usa cuando **no existe la columna `species`** y le pides que invente $K=3$ grupos por cercanía matemática. |

---

## 🔗 Conceptos Relacionados
* [[Clasificación vs Regresión]]
* [[EDA y Pairplot]]
* [[02-Clasificación Iris]] · [[03-Regresión Lineal desde Cero]]
