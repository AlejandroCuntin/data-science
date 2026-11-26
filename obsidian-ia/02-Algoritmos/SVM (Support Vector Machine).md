---
tags:
  - algoritmo
  - clasificacion
---

# 🚧 SVM (Support Vector Machine)

> **Proyecto donde lo usé:** [[02-Clasificación Iris]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es un algoritmo geométrico que busca trazar **la única frontera divisoria que deje la "carretera" (margen de seguridad) más ancha posible** entre los puntos más cercanos de cada especie.

---

## ⚙️ ¿Cómo funciona por dentro?

```text
      Especie Versicolor (o)          /      /          Especie Virginica (x)
                                     /  |   /
            o     o                 /   |  /                  x      x
               o       (o) <-------/----| /        (x)
                                  /     |/ <-------/
                       Margen    /      /   Margen
                                /      /
                              Frontera SVM
```

* **Vectores de Soporte `(o)` y `(x)`:** Son las flores más difíciles que están justo en el borde entre dos especies. Se llaman así porque son las que "sujetan" o definen por dónde pasa la carretera.
* Es uno de los algoritmos más potentes cuando tienes **datasets pequeños o medianos muy bien medidos** (como las 150 flores de Iris).
* **Requiere [[StandardScaler (Escalado)]]:** Como mide distancias geométricas en el espacio, todas las variables deben estar en la misma escala.

---

## 🎛️ Sus 2 Hiperparámetros Clave en [[02-Clasificación Iris]]

1. **`kernel` (La forma de la frontera):**
   * `'linear'`: Dibuja fronteras completamente **rectas** (fue el ganador en nuestro proyecto).
   * `'rbf'` (*Radial Basis Function*): Permite dibujar fronteras **curvas o circulares** alrededor de los grupos cuando una línea recta no basta.
2. **`C` (Rigidez del margen — ver [[Regularización (Parámetro C y Penalty)]]):**
   * **$C$ pequeño (`0.1`, `1`):** Prioriza una carretera ancha y suave aunque alguna flor rebelde quede en el lado equivocado.
   * **$C$ grande (`10`, `100`):** No tolera fallos en entrenamiento; estrecha la carretera todo lo necesario para acertar las flores de `Train`.
* **Resultado en [[02-Clasificación Iris]]:** Ganó `C=10, kernel='linear'` con **95.83%** en Validación Cruzada y **96.67%** (29/30) en Test (su único fallo lo vimos en la [[Matriz de Confusión]]).
