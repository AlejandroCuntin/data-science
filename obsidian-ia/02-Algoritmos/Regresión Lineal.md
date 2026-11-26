---
tags:
  - algoritmo
  - regresion
---

# 📏 Regresión Lineal

> **Proyecto donde lo programé desde cero:** [[03-Regresión Lineal desde Cero]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es el algoritmo que busca trazar **la mejor línea recta posible** por en medio de una nube de puntos para predecir un número continuo ($\hat{y}$) a partir de un dato de entrada ($x$).

---

## ⚙️ La Fórmula de la Recta Pieza por Pieza

$$\hat{y} = w \cdot x + b$$

* **$x$ (Variable de entrada / Feature):** El dato que conocemos (ej. `Años de experiencia`).
* **$\hat{y}$ (Predicción):** El número que estima nuestra recta (ej. `Salario estimado en miles de €`).
* **$w$ (Weight / Peso o Pendiente):** Cuánto se inclina la recta hacia arriba o hacia abajo (cuánto sube el salario por cada 1 año extra de experiencia).
* **$b$ (Bias / Sesgo o Intercepto):** La altura inicial donde arranca la recta cuando $x = 0$ (el sueldo base de alguien con 0 años de experiencia).

---

## 🔬 Ejemplo Real en [[03-Regresión Lineal desde Cero]]

En nuestra empresa de 30 trabajadores:
* Empezamos con una recta tirada en el suelo: **$w = 0.0$** y **$b = 0.0$** (con un [[MSE (Error Cuadrático Medio)]] enorme de `1750.74`).
* Tras 3.000 pasos de [[Descenso del Gradiente]], nuestro algoritmo descubrió la recta ganadora:
  $$\text{Salario} = \mathbf{3.2736} \cdot \text{Años} + \mathbf{22.8689}$$
* Con esa recta ya entrenada, al llamar a `.predict([5.0, 12.0])` supimos al instante que alguien con 5 años debe cobrar **39.24 mil €** y alguien con 12 años **62.15 mil €**, logrando un [[R2 (Coeficiente de Determinación)]] del **96.55%**.

---

## 🔗 Conceptos Relacionados
* [[Descenso del Gradiente]] · [[Learning Rate y Épocas]]
* [[MSE (Error Cuadrático Medio)]] · [[R2 (Coeficiente de Determinación)]]
* [[Programación Orientada a Objetos en ML (fit y predict)]]
