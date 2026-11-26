---
tags:
  - proyecto
  - regresion
  - supervisado
---

# 📈 03 · Regresión Lineal desde Cero

> **Carpeta en el repositorio:** `03-regresión-lineal/`
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 Objetivo del Proyecto (*No Scikit-learn Allowed*)
Entender cómo aprende realmente una máquina "bajo el capó" programando una [[Regresión Lineal]] **100% desde cero usando solo Python y [[NumPy]]**: la ecuación de la recta, el medidor de error, el motor de aprendizaje con derivadas y nuestra propia clase orientada a objetos.

---

## 🔄 Las 6 Fases que Programamos

1. **Fase 1 · Datos con Regla Secreta + Ruido:**
   * Creamos 30 empleados relacionando **Años de Experiencia ($X$)** con **Salario en miles de € ($y$)** mediante la regla oculta $y = 3.5 \cdot X + 22.0 + \text{ruido}$ (+3.500 €/año sobre una base de 22.000 €).
2. **Fase 2 · La Recta y el Termómetro de Error:**
   * Programamos $\hat{y} = w \cdot X + b$ y el [[MSE (Error Cuadrático Medio)]]. Empezando a ciegas en el suelo ($w=0, b=0$), el error inicial era gigante (`MSE = 1750.74`).
3. **Fase 3 · El Motor de Aprendizaje:**
   * Programamos el [[Descenso del Gradiente]] con [[Learning Rate y Épocas]] (`learning_rate = 0.01`, `epochs = 3000`). La recta subió sola hasta descubrir $w = 3.2736$ y $b = 22.8689$, bajando el error a **`2.762`**.
4. **Fase 4 · Electrocardiograma del Modelo:**
   * Dibujamos la Curva de Aprendizaje (viendo cómo cae el MSE y se aplana) y la recta verde atravesando el centro de los 30 empleados.
5. **Fase 5 · Nuestro Propio Scikit-learn:**
   * Empaquetamos el algoritmo en `class LinearRegressionFromScratch` usando [[Programación Orientada a Objetos en ML (fit y predict)]].
6. **Fase 6 · Prueba de Fuego contra [[scikit-learn]]:**
   * Programamos la nota [[R2 (Coeficiente de Determinación)]] y comparamos nuestro motor contra `LinearRegression()` oficial:

| Implementación | Pendiente ($w$) | Base / Intercepto ($b$) | Error Final (MSE) | Nota $R^2$ |
|---|---|---|---|---|
| **Nuestra Regresión (100% NumPy)** | `3.2736` | `22.8689` | `2.7620` | `96.55%` |
| **Scikit-learn Oficial** | `3.2735` | `22.8692` | `2.7620` | `96.55%` |

---

## 🔗 Conexiones en el Grafo
* **Tipo de problema:** [[Clasificación vs Regresión]] · [[Aprendizaje Supervisado vs No Supervisado]]
* **Modelo y Motor:** [[Regresión Lineal]] · [[Descenso del Gradiente]] · [[Learning Rate y Épocas]]
* **Métricas:** [[MSE (Error Cuadrático Medio)]] · [[R2 (Coeficiente de Determinación)]]
* **Librerías y Código:** [[Programación Orientada a Objetos en ML (fit y predict)]] · [[NumPy]] · [[pandas]] · [[matplotlib y seaborn]] · [[scikit-learn]]
