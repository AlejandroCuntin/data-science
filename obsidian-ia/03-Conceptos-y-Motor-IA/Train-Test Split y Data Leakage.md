---
tags:
  - concepto
  - preprocesamiento
---

# 🔐 Train-Test Split y Data Leakage

> **Proyecto donde lo usé:** [[02-Clasificación Iris]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Qué es en 1 frase sencilla?
Es dividir nuestras filas en dos grupos antes de empezar (**80% `Train` para estudiar** y **20% `Test` guardado bajo llave para el examen final**) para comprobar que el modelo realmente aprendió a predecir datos nuevos y no solo memorizó las respuestas ([[Overfitting vs Underfitting]]).

---

## ⚙️ Cómo lo hicimos en [[02-Clasificación Iris]]

De nuestras **150 flores**:
```python
X = iris_df.drop(columns='species')  # Las 4 medidas (sépalos y pétalos)
y = iris_df['species']               # La respuesta (especie de la flor)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```
* **`X_train, y_train` (120 flores - 80%):** Con lo que entrenamos y hacemos [[RandomizedSearchCV y Validación Cruzada]].
* **`X_test, y_test` (30 flores - 20%):** Flores que ningún modelo ve hasta la última celda del notebook (cuando calculamos [[Accuracy]], [[F1-Score (Precisión y Recall)]] y [[Matriz de Confusión]]).
* **`random_state=42`:** Semilla fija para que el sorteo aleatorio reparta siempre las mismas 120 y 30 flores cada vez que ejecutamos el notebook.

---

## 🚨 ¿Qué es el *Data Leakage* (Fuga de Datos) y cómo se evita?
Es cuando, sin darte cuenta, **le chivas información del examen (`Test`) al modelo durante el entrenamiento**.
* *Ejemplo típico de error:* Calcular la media del [[StandardScaler (Escalado)]] con las 150 flores juntas antes de separar.
* *Cómo se hace bien:*
  1. Primero divides con `train_test_split`.
  2. Ajustas el escalador **solo con Train**: `scaler.fit_transform(X_train)`.
  3. Transformas Test usando la regla de Train: `scaler.transform(X_test)`.
