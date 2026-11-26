---
tags:
  - libreria
  - codigo
---

# 🧱 Programación Orientada a Objetos en ML (fit y predict)

> **Proyecto donde construí mi propia clase:** [[03-Regresión Lineal desde Cero]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es la arquitectura estándar con la que están construidos todos los modelos de [[scikit-learn]]: empaquetar las fórmulas matemáticas dentro de un molde (`class`) que guarda lo aprendido en su memoria interna (`self`) y se maneja con dos botones: **`.fit()` (entrenar)** y **`.predict()` (adivinar)**.

---

## ⚙️ Los 3 Bloques de Nuestro `LinearRegressionFromScratch`

```text
+----------------------------------------------------------------------+
|                class LinearRegressionFromScratch                     |
|                                                                      |
|  1. __init__(self)     -->  "Encender la máquina" (w=0, b=0)         |
|  2. fit(self, X, y)    -->  "Entrenar" (Bucle Descenso del Gradiente)|
|  3. predict(self, X)   -->  "Predecir" (Devuelve self.w * X + self.b)|
+----------------------------------------------------------------------+
```

### ¿Qué significa `self.` (y por qué va con punto `.` y no con coma `,`)?
**`self`** es la "mochila" interna del modelo:
* En `__init__`: Metemos en la mochila `self.epochs = 3000`, `self.w = 0.0` y `self.b = 0.0`.
* En `fit(self, X, y)`: El bucle `for _ in range(self.epochs):` entrena la recta y actualiza `self.w` (`3.2736`) y `self.b` (`22.8689`) dentro de la mochila.
* En `predict(self, X)`: Ya no hace falta pasarle `w` ni `b` a mano, porque simplemente los saca de su mochila (`return self.w * X + self.b`).

---

## 💻 Cómo se usa una vez creada (igual en todos los algoritmos)
```python
mi_modelo = LinearRegressionFromScratch(learning_rate=0.01, epochs=3000)
mi_modelo.fit(X, y)                                     # 1. Aprende de los datos
predicciones = mi_modelo.predict(np.array([5.0, 12.0])) # 2. Predice casos nuevos
```
