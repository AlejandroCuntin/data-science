---
tags:
  - metrica
  - clasificacion
  - explicabilidad
---

# 📊 Feature Importances

> **Proyecto donde lo usé:** [[02-Clasificación Iris]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es una propiedad de los modelos basados en árboles (como [[Árbol de Decisión]] y [[Random Forest]]) que suma `1.00` (**100%**) y te dice **qué porcentaje de importancia tuvo cada columna** para tomar las decisiones.

---

## 🔬 Cómo cerró el círculo en [[02-Clasificación Iris]]

En el Paso 1 del proyecto, al mirar el [[EDA y Pairplot]] con nuestros ojos, dijimos: *"Parece que los pétalos separan genial a las flores y los sépalos las mezclan"*.
En el Paso 5, le preguntamos a los 200 árboles de nuestro [[Random Forest]] (`best_rf.feature_importances_`) a qué medidas les hicieron caso realmente:

| Medida de la flor | Importancia en el Random Forest |
|---|---|
| **`petal_length` (Largo del pétalo)** | **45.80%** (`0.4580`) |
| **`petal_width` (Ancho del pétalo)** | **40.88%** (`0.4088`) |
| `sepal_length` (Largo del sépalo) | **10.20%** (`0.1020`) |
| `sepal_width` (Ancho del sépalo) | **3.12%** (`0.0312`) |

**Conclusión matemática:** Las dos medidas del **pétalo concentran el 86.68% de toda la decisión**, confirmando al 100% nuestra intuición visual del EDA.

---

## 💻 Código en Python
```python
importancias = pd.Series(best_rf.feature_importances_, index=X.columns).sort_values()
importancias.plot(kind="barh", color="teal")
```
*(Recuerda: se accede con punto `best_rf.feature_importances_`, porque es un atributo guardado dentro del modelo entrenado).*
