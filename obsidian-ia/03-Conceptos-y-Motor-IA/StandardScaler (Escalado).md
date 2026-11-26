---
tags:
  - concepto
  - preprocesamiento
---

# ⚖️ StandardScaler (Escalado)

> **Proyecto donde lo usé:** [[02-Clasificación Iris]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es un preprocesador que transforma todas las columnas numéricas para que estén en **la misma escala comparable (con Media = 0 y Desviación Estándar = 1)**, evitando que una variable con números grandes domine a otra con números pequeños.

---

## ⚙️ ¿Qué problema resuelve y cuál es su fórmula?

Imagina que predices con dos columnas: **Edad** (de `18` a `80`) y **Sueldo** (de `15.000` a `90.000`).
Si no escalas, un algoritmo matemático pensará que el sueldo es miles de veces más importante que la edad solo porque sus números son gigantes.

`StandardScaler` resta a cada valor la media de su columna ($\mu$) y lo divide por su desviación estándar ($\sigma$):
$$z = \frac{x - \mu}{\sigma}$$
Así todos los valores quedan centrados alrededor del `0` (normalmente entre `-2.5` y `+2.5`).

---

## 🤖 ¿Qué algoritmos lo necesitan y cuáles NO?

| Algoritmo | ¿Necesita `StandardScaler`? | ¿Por qué? |
|---|---|---|
| [[Regresión Logística]] | ✅ **SÍ (Obligatorio)** | Usa gradientes y [[Regularización (Parámetro C y Penalty)]] sobre los pesos $w$. |
| [[SVM (Support Vector Machine)]] | ✅ **SÍ (Obligatorio)** | Calcula distancias geométricas para trazar la carretera de máximo margen. |
| [[Regresión Lineal]] (con Gradiente) | ✅ **SÍ (Muy recomendable)** | Si una variable es gigante, el [[Descenso del Gradiente]] rebota si no bajas mucho el [[Learning Rate y Épocas]]. |
| [[Árbol de Decisión]] | ❌ **NO le hace falta** | Corta con preguntas de orden (`¿valor < umbral?`), y el orden no cambia al escalar. |
| [[Random Forest]] | ❌ **NO le hace falta** | Está compuesto por árboles de decisión (aunque funciona igual de bien si le pasas datos escalados). |

---

## 💻 Código Correcto (Sin [[Train-Test Split y Data Leakage|Data Leakage]])
```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Aprende media/desviación de Train y escala
X_test_scaled = scaler.transform(X_test)        # Solo aplica la transformación a Test
```
