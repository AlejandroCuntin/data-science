---
tags:
  - libreria
  - codigo
---

# 🤖 scikit-learn

> **Proyectos donde lo usé:** [[02-Clasificación Iris]] · [[03-Regresión Lineal desde Cero]]
> **Volver al centro:** [[00-Mapa-Mental-IA]]

---

## 💡 ¿Para qué sirve en Machine Learning?
Es la librería estándar de Machine Learning clásico en Python (`sklearn`). Reúne en un mismo diseño ([[Programación Orientada a Objetos en ML (fit y predict)]]) todos los algoritmos, preprocesadores, buscadores de hiperparámetros y métricas.

---

## 🗂️ Mapa de Módulos de `sklearn` que ya Hemos Usado

### 1. División y Búsqueda (`sklearn.model_selection`)
* `train_test_split` $\rightarrow$ [[Train-Test Split y Data Leakage]]
* `RandomizedSearchCV` $\rightarrow$ [[RandomizedSearchCV y Validación Cruzada]]

### 2. Preprocesamiento (`sklearn.preprocessing`)
* `StandardScaler` $\rightarrow$ [[StandardScaler (Escalado)]]

### 3. Modelos de Clasificación y Regresión
* `sklearn.linear_model` $\rightarrow$ [[Regresión Logística]] (`LogisticRegression`) y [[Regresión Lineal]] (`LinearRegression`)
* `sklearn.tree` $\rightarrow$ [[Árbol de Decisión]] (`DecisionTreeClassifier`)
* `sklearn.ensemble` $\rightarrow$ [[Random Forest]] (`RandomForestClassifier`)
* `sklearn.svm` $\rightarrow$ [[SVM (Support Vector Machine)]] (`SVC`)

### 4. Métricas de Evaluación (`sklearn.metrics`)
* `accuracy_score` $\rightarrow$ [[Accuracy]]
* `f1_score` $\rightarrow$ [[F1-Score (Precisión y Recall)]]
* `ConfusionMatrixDisplay` $\rightarrow$ [[Matriz de Confusión]]
