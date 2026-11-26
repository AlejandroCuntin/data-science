---
tags:
  - proyecto
  - clasificacion
  - supervisado
---

# 🌸 02 · Clasificación Iris

> **Carpeta en el repositorio:** `02-iris-clasificación/`
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 Objetivo del Proyecto
Predecir a qué especie (`setosa`, `versicolor` o `virginica`) pertenece una flor a partir de **4 medidas en cm** (`sepal_length`, `sepal_width`, `petal_length`, `petal_width`), haciendo competir a **4 algoritmos de clasificación** optimizados automáticamente.

---

## 🔄 Flujo Completo que Seguimos

1. **Exploración Visual (EDA):**
   * Pintamos un [[EDA y Pairplot]] ($4 \times 4$ gráficas) y descubrimos visualmente que *Setosa* está 100% aislada gracias al tamaño de su pétalo, mientras que *Versicolor* y *Virginica* se rozan en una pequeña frontera.
2. **División de Datos (80% Train / 20% Test):**
   * Aplicamos [[Train-Test Split y Data Leakage]]: 120 flores para entrenar y 30 flores guardadas bajo llave para el examen final.
3. **Escalado de Variables:**
   * Aplicamos [[StandardScaler (Escalado)]] (`media = 0, desviación = 1`) ajustando solo en `Train` para que modelos como [[Regresión Logística]] y [[SVM (Support Vector Machine)]] trabajen en la misma escala.
4. **Competición de 4 Modelos con [[RandomizedSearchCV y Validación Cruzada]] (`cv=5`):**

| Modelo | CV Accuracy (Train) | Accuracy (Test) | F1-Score (Test) | Mejor Hiperparámetro |
|---|---|---|---|---|
| [[Regresión Logística]] | `95.83%` (115/120) | `100.0%` | `1.0000` | `C=21.54` |
| [[Árbol de Decisión]] | `95.00%` (114/120) | `100.0%` | `1.0000` | `max_depth=None, min_samples_split=2` |
| [[Random Forest]] | `95.83%` (115/120) | `100.0%` | `1.0000` | `n_estimators=200, max_depth=20` |
| [[SVM (Support Vector Machine)]] | `95.83%` (115/120) | `96.67%` (29/30) | `0.9659` | `C=10, kernel='linear'` |

5. **Explicabilidad Final:**
   * Con la [[Matriz de Confusión]] cazamos la única flor frontera que falló el SVM (*Versicolor* confundida con *Virginica*).
   * Con [[Feature Importances]] demostramos que los 200 árboles del Random Forest toman el **86.68%** de su decisión mirando solo el **pétalo** (`petal_length` 45.80% + `petal_width` 40.88%).

---

## 🔗 Conexiones en el Grafo
* **Tipo de problema:** [[Clasificación vs Regresión]] · [[Aprendizaje Supervisado vs No Supervisado]]
* **Modelos:** [[Regresión Logística]] · [[Árbol de Decisión]] · [[Random Forest]] · [[SVM (Support Vector Machine)]]
* **Conceptos:** [[Overfitting vs Underfitting]] · [[Regularización (Parámetro C y Penalty)]] · [[RandomizedSearchCV y Validación Cruzada]]
* **Métricas:** [[Accuracy]] · [[F1-Score (Precisión y Recall)]] · [[Matriz de Confusión]] · [[Feature Importances]]
* **Librerías:** [[pandas]] · [[NumPy]] · [[scikit-learn]] · [[matplotlib y seaborn]]
