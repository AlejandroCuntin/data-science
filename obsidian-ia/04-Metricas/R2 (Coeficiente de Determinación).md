---
tags:
  - metrica
  - regresion
---

# 🏆 R2 (Coeficiente de Determinación)

> **Proyecto donde lo programé desde cero:** [[03-Regresión Lineal desde Cero]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es la métrica que le pone una **nota del 0% al 100% (de 0 a 1)** a un modelo de [[Regresión Lineal]], comparando el error de nuestra recta contra un "modelo tonto" que siempre predice la media (`np.mean(y)`).

---

## ⚙️ ¿Por qué lo necesitamos si ya tenemos el [[MSE (Error Cuadrático Medio)]]?
Si te digo que mi modelo tiene un `MSE = 2.76`, no sabes de un vistazo si eso es un 5 raspado o un sobresaliente.
En cambio, el **$R^2$** siempre está en una escala universal:
* **$R^2 = 0.00$ (0%):** Tu recta no explica nada (es igual de mala que decir a todos el sueldo medio de la empresa sin mirar sus años de experiencia).
* **$R^2 = 1.00$ (100%):** Tu recta pasa exactamente por encima de todos los puntos sin un solo milímetro de error.

---

## 💻 Fórmula y Código desde Cero en [[03-Regresión Lineal desde Cero]]

$$R^2 = 1 - \frac{\sum (y - \hat{y})^2}{\sum (y - \bar{y})^2}$$

```python
def calcular_r2(y_real, y_pred):
    error_nuestra_recta = np.sum((y_real - y_pred) ** 2)
    variacion_respecto_media = np.sum((y_real - np.mean(y_real)) ** 2)
    return 1 - (error_nuestra_recta / variacion_respecto_media)
```

En nuestro proyecto de los 30 salarios, tanto nuestra clase `LinearRegressionFromScratch` como el `LinearRegression` oficial de [[scikit-learn]] obtuvieron exactamente **`R² = 96.55%`** (el 3.45% restante es simplemente el ruido aleatorio natural que metimos al crear los sueldos).
