---
tags:
  - concepto
  - motor-ia
---

# 🎰 RandomizedSearchCV y Validación Cruzada

> **Proyecto donde lo usé:** [[02-Clasificación Iris]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es un "robot probador" que entrena automáticamente decenas de modelos con **distintas combinaciones de hiperparámetros** evaluándolos en **5 exámenes internos (`cv=5`)** y te entrega directamente el modelo ganador (`best_estimator_`).

---

## ⚙️ ¿Cómo funciona por dentro y cuántos modelos entrena?

En [[02-Clasificación Iris]] queríamos encontrar las mejores "ruedas de ajuste" (hiperparámetros) para [[Regresión Logística]], [[Árbol de Decisión]], [[Random Forest]] y [[SVM (Support Vector Machine)]]:

```python
grid_search_rf = RandomizedSearchCV(rf, param_grid_rf, cv=5, n_jobs=-1, random_state=42)
grid_search_rf.fit(X_train_scaled, y_train)
```

1. **Sorteo de combinaciones (`n_iter=10` por defecto):** Elige al azar 10 combinaciones de tu diccionario `param_grid`.
2. **Validación Cruzada (`cv=5` / 5-Fold Cross-Validation):**
   Divide tus **120 flores de `X_train`** en 5 bloques de 24 flores. Entrena con 4 bloques (96 flores) y hace un examen con el bloque restante (24 flores), repitiendo esto 5 veces cambiando el bloque de examen.
   $$\text{Total de modelos entrenados} = 10 \text{ combinaciones} \times 5 \text{ particiones} = \mathbf{50 \text{ entrenamientos}}$$
3. **`n_jobs=-1`:** Usa todos los núcleos del procesador en paralelo para terminar mucho más rápido.

---

## 🏆 Los 3 Resultados que le Pedimos al Terminar

* **`grid_search.best_params_`:** Nos dice qué combinación de ajustes ganó (ej. `{'n_estimators': 200, 'max_depth': 20}`).
* **`grid_search.best_score_`:** La nota media en los 5 exámenes de validación cruzada sobre `Train`:
  * En nuestras 120 flores de `Train`, [[Regresión Logística]], [[Random Forest]] y [[SVM (Support Vector Machine)]] acertaron **115 de 120 flores** ($\frac{115}{120} = \mathbf{95.83\%}$), mientras que el [[Árbol de Decisión]] acertó **114 de 120** ($\frac{114}{120} = \mathbf{95.00\%}$).
* **`grid_search.best_estimator_`:** El modelo ganador ya entrenado y listo para hacer `.predict(X_test_scaled)`.
