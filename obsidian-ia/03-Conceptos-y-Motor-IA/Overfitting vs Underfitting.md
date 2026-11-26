---
tags:
  - concepto
  - motor-ia
---

# 🎭 Overfitting vs Underfitting

> **Proyectos donde lo vimos:** [[02-Clasificación Iris]] · [[03-Regresión Lineal desde Cero]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué son en 1 frase sencilla?
* **Overfitting (Sobreajuste):** El modelo **memoriza** los datos de entrenamiento (incluido su ruido y casos raros), sacando un 100% en `Train` pero fallando estrepitosamente con datos nuevos en `Test`.
* **Underfitting (Infraajuste):** El modelo es **demasiado simple o está demasiado atado de manos**, por lo que no aprende ni siquiera el patrón básico (falla tanto en `Train` como en `Test`).

---

## ⚙️ Comparativa Visual

| Estado | Qué hace el modelo | Nota en Train | Nota en Test | Ejemplo en nuestros proyectos |
|---|---|---|---|---|
| **Underfitting** | No aprende el patrón | ❌ Baja | ❌ Baja | Poner $C \to 0.0001$ en [[Regresión Logística]] (fuerza todos los pesos a 0) o una recta en el suelo ($w=0, b=0$). |
| **Equilibrio Óptimo** | **Aprende a generalizar** | ✅ Alta | ✅ Alta | [[Random Forest]] o [[Regresión Logística]] con `95.83%` en CV y `100%` en Test. |
| **Overfitting** | Memoriza el ruido | 💯 Perfecta | ❌ Baja | Un [[Árbol de Decisión]] individual sin límite de preguntas que crea una rama para 1 sola flor deforme. |

---

## 🛡️ Las 3 Armas para Evitar el Overfitting
1. **Separar siempre en Train y Test:** [[Train-Test Split y Data Leakage]] y [[RandomizedSearchCV y Validación Cruzada]].
2. **Aplicar Regularización:** [[Regularización (Parámetro C y Penalty)]] en modelos lineales y [[SVM (Support Vector Machine)]].
3. **Limitar la profundidad o usar Ensambles:** Limitar `max_depth` o pasar de 1 árbol a 200 árboles con [[Random Forest]].
