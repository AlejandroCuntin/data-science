---
tags:
  - concepto
  - motor-ia
---

# 🧭 Descenso del Gradiente

> **Proyecto donde lo programé desde cero:** [[03-Regresión Lineal desde Cero]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es el **motor de aprendizaje universal de la Inteligencia Artificial**: un algoritmo que ajusta los pesos ($w$ y $b$) paso a paso usando las **derivadas como brújula** para bajar por la montaña del error hasta llegar al valle donde el fallo ([[MSE (Error Cuadrático Medio)]]) es mínimo.

---

## ⚙️ Las 2 Brújulas (Derivadas `dw` y `db`)

Cuando nuestra [[Regresión Lineal]] empieza tirada en el suelo ($w=0, b=0$), calcula dos derivadas en cada vuelta:

1. **`db` (Brújula de la altura base `b`):**
   $$db = -\frac{2}{N} \sum (y - \hat{y}) \quad \longrightarrow \quad \texttt{db = -2 * np.mean(y - y\_pred)}$$
   Mira cuánto nos falta de altura media para llegar a los puntos reales.
2. **`dw` (Brújula de la inclinación `w`):**
   $$dw = -\frac{2}{N} \sum x \cdot (y - \hat{y}) \quad \longrightarrow \quad \texttt{dw = -2 * np.mean(X * (y - y\_pred))}$$
   Multiplica el error por los años `X` para saber hacia dónde hay que girar la pendiente de la recta.

Luego actualiza ambos valores dando un pasito controlado por el [[Learning Rate y Épocas]]:
```python
w = w - learning_rate * dw
b = b - learning_rate * db
```

---

## 🔬 Ejemplo Real en [[03-Regresión Lineal desde Cero]]: ¿Por qué varió `0.0001` respecto a [[scikit-learn]]?

* Nuestro Descenso del Gradiente (con `epochs=3000` y `learning_rate=0.01`) bajó el error desde `1750.74` hasta **`2.7620`**, encontrando **`w = 3.2736`** y **`b = 22.8689`**.
* `LinearRegression()` de `scikit-learn` dio **`w = 3.2735`** y **`b = 22.8692`**.
* **¿Por qué esa diferencia de una diezmilésima (`0.0001`)?**
  Porque para tablas pequeñas `scikit-learn` despeja una fórmula matricial de golpe (*Mínimos Cuadrados Ordinarios / OLS*), mientras que el Descenso del Gradiente se acerca caminando paso a paso.
* **¿Por qué entonces se usa Descenso del Gradiente en IA?**
  Porque con millones de datos o en Redes Neuronales de Deep Learning, la fórmula directa de `scikit-learn` explota la memoria RAM del ordenador y es imposible de calcular; allí **toda la IA moderna aprende con Descenso del Gradiente**.
