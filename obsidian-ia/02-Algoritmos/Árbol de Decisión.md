---
tags:
  - algoritmo
  - clasificacion
---

# 🌳 Árbol de Decisión

> **Proyecto donde lo usé:** [[02-Clasificación Iris]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es un algoritmo que aprende a clasificar datos haciendo una **cadena de preguntas de `Sí / No` basadas en cortes numéricos (umbrales)**, igual que un diagrama de flujo.

---

## ⚙️ Esquema Visual con Nuestras Flores de [[02-Clasificación Iris]]

```text
               [ ¿El largo del pétalo mide menos de 2.45 cm? ]
                       /                             \
                     SÍ                               NO
                    /                                   \
         ¡Es una SETOSA!               [ ¿El ancho del pétalo mide menos de 1.75 cm? ]
          (100% seguro)                        /                             \
                                             SÍ                               NO
                                            /                                   \
                                 ¡Es una VERSICOLOR!                 ¡Es una VIRGINICA!
```

Matemáticamente, en cada nudo busca el corte que deje los grupos lo más "puros" posible (reduciendo la impureza de **Gini** o la **Entropía**).

---

## 🔬 ¿Para qué sirve meterlo si ya existe [[Random Forest]]?

1. **Para hacer un "casting" de algoritmos:** Comparamos cómo piensa 1 árbol de preguntas frente a fórmulas de probabilidad ([[Regresión Logística]]) o fronteras geométricas ([[SVM (Support Vector Machine)]]).
2. **Como línea base (*baseline*) para demostrar que [[Random Forest]] merece la pena:**
   * Un solo árbol tiene un gran defecto: **alta varianza** (tiende al [[Overfitting vs Underfitting]], memorizando ramas para flores raras).
   * En [[02-Clasificación Iris]], **1 solo Árbol de Decisión** sacó **95.00%** en validación cruzada (114/120 aciertos), mientras que el **Random Forest de 200 árboles** subió a **95.83%** (115/120 aciertos).

---

## 🎛️ Sus Hiperparámetros Clave
* **`max_depth` (Profundidad máxima):** Límite de pisos de preguntas hacia abajo. Si es `None`, crece sin límite hasta que cada hoja es pura (riesgo de memorizar ruido).
* **`min_samples_split`:** Mínimo de flores que debe haber en un grupo para permitirle dividirlo en otra pregunta más.
* *(Nota: A los árboles **NO** les hace falta [[StandardScaler (Escalado)]], porque el orden de mayor o menor no cambia al escalar).*
