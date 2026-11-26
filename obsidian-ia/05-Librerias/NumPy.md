---
tags:
  - libreria
  - codigo
---

# 🔢 NumPy

> **Proyectos donde lo usé:** [[02-Clasificación Iris]] · [[03-Regresión Lineal desde Cero]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Para qué sirve en IA?
Es el motor de cálculo numérico y vectorial de Python (`import numpy as np`). Permite operar listas enteras de números de un solo golpe (`w * X + b`) sin tener que escribir bucles `for` elemento por elemento.

---

## 🛠️ Funciones de NumPy que ya hemos usado en nuestros proyectos

| Función | ¿Qué hace? | ¿Dónde la usamos? |
|---|---|---|
| **`np.linspace(1, 10, 30)`** | Genera 30 números repartidos a igual distancia entre `1` y `10`. | Crear los años de experiencia `X` en [[03-Regresión Lineal desde Cero]]. |
| **`np.logspace(-4, 4, 10)`** | Genera 10 números en escala logarítmica desde $10^{-4}$ (`0.0001`) hasta $10^4$ (`10.000`). | Probar el parámetro `C` de [[Regularización (Parámetro C y Penalty)]] en [[02-Clasificación Iris]]. |
| **`np.random.seed(42)`** | Fija la semilla aleatoria para que los números al azar salgan siempre iguales. | Reproducibilidad en [[03-Regresión Lineal desde Cero]]. |
| **`np.random.normal(0, 2.0, size=30)`** | Genera 30 variaciones aleatorias centradas en `0` (campana de Gauss). | Simular el **ruido** realista de los sueldos ($\pm 2.000\text{ €}$). |
| **`np.mean(...)`** | Calcula el promedio de un vector de números. | Calcular el [[MSE (Error Cuadrático Medio)]] y las derivadas del [[Descenso del Gradiente]]. |
| **`np.sum(...)`** | Suma todos los elementos de un vector. | Calcular la nota [[R2 (Coeficiente de Determinación)]]. |
| **`X.reshape(-1, 1)`** | Convierte una lista plana 1D de 30 números en una columna 2D de $30 \times 1$. | Formato obligatorio que exige [[scikit-learn]] para hacer `.fit(X_2d, y)`. |
