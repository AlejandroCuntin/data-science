---
tags:
  - concepto
  - motor-ia
---

# ⏱️ Learning Rate y Épocas

> **Proyecto donde lo usé:** [[03-Regresión Lineal desde Cero]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué son en 1 frase sencilla?
En el [[Descenso del Gradiente]], el **Learning Rate ($\alpha$, Tasa de Aprendizaje)** es el **tamaño de la zancada** que da el modelo en cada intento, y las **Épocas (`epochs`)** son el **número total de pasos/vueltas** que da al dataset durante el entrenamiento.

---

## ⚙️ ¿Qué pasa si eliges mal el Learning Rate?

```text
1. Learning Rate MUY PEQUEÑO (0.000001):
   Pasos de hormiga -> Tarda millones de épocas en bajar la montaña del error.

2. Learning Rate MUY GRANDE (1.0):
   Saltos gigantes -> Se pasa de largo el valle, rebota de pared a pared y el error explota a infinito.

3. Learning Rate ÓPTIMO (0.01 en nuestro proyecto):
   Pasos suaves y firmes -> Baja en tobogán hasta el fondo del valle.
```

---

## 📉 El Electrocardiograma del Modelo: La Curva de Aprendizaje (*Loss Curve*)

En la Fase 4 de [[03-Regresión Lineal desde Cero]] guardamos el error [[MSE (Error Cuadrático Medio)]] de cada una de las `3000` épocas en `historial_mse` y lo dibujamos:
* **Época 0:** `MSE = 1750.74`
* **Época 500:** `MSE = 4.88`
* **Época 1500 a 3000:** `MSE = 2.76` (la curva se queda totalmente plana).
* **Regla de oro:** Cuando ves que la curva del error cae en picado y luego se aplana como un tobogán horizontal, sabes al 100% que el `learning_rate` fue bueno y que el modelo ya terminó de aprender.
