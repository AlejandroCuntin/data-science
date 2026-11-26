---
tags:
  - metrica
  - regresion
---

# 🌡️ MSE (Error Cuadrático Medio)

> **Proyecto donde lo programé desde cero:** [[03-Regresión Lineal desde Cero]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es el **"termómetro de error"** de la [[Regresión Lineal]]: mide con un solo número qué tan lejos está nuestra línea recta de los puntos reales, elevando las distancias al cuadrado y haciendo la media.

---

## ⚙️ Fórmula y los 3 Pasos que Programamos en [[NumPy]]

$$\text{MSE} = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$

```python
def calcular_mse(y_real, y_pred):
    errores = y_real - y_pred
    return np.mean(errores ** 2)
```

1. **Resta la realidad menos la predicción (`y_real - y_pred`):** Calcula la distancia vertical desde cada punto azul hasta la línea recta.
2. **Lo eleva al cuadrado (`** 2`):**
   * *¿Por qué al cuadrado?* Primero, para que un fallo de `+5` y otro de `-5` no se anulen dando `0` de error. Segundo, porque al elevar al cuadrado **castigas muchísimo más los errores grandes** ($10^2 = 100$, mientras que $2^2 = 4$).
3. **Hace la media de todos los empleados (`np.mean`):**
   * **MSE gigante (`1750.74` al empezar con $w=0, b=0$):** La recta está en el suelo, lejísimos de los puntos.
   * **MSE pequeñito (`2.7620` tras el [[Descenso del Gradiente]]):** La recta pasa justo por el centro de los 30 puntos.

---

## 🔗 Relación con [[R2 (Coeficiente de Determinación)]]
Como el valor del MSE depende de las unidades (miles de € al cuadrado), para saber qué nota del 0% al 100% representa ese `2.7620`, lo complementamos con la nota [[R2 (Coeficiente de Determinación)]].
