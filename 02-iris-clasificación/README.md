# Clasificación de Flores Iris · Machine Learning

Proyecto introductorio de clasificación multiclase donde predecimos la especie de una flor a partir de sus medidas anatómicas, comparando dos algoritmos clave (**Regresión Logística** y **Random Forest**) y optimizando sus hiperparámetros.

---

## ✅ Lo que ya tenemos hecho

### El problema y los datos

A partir del dataset clásico de **Iris** (150 flores en total), queremos predecir la **especie** (`setosa`, `versicolor` o `virginica`) basándonos en 4 medidas numéricas continuas:

* `sepal_length`: Longitud del sépalo (cm)
* `sepal_width`: Ancho del sépalo (cm)
* `petal_length`: Longitud del pétalo (cm)
* `petal_width`: Ancho del pétalo (cm)

---

### Metodología paso a paso (Ya implementada en el Notebook)

#### 1. Separación de datos (`train_test_split`)
Para evaluar el modelo con honestidad y asegurarnos de que no memoriza las flores, dividimos el dataset:
* **Train (80% - 120 flores):** Con lo que los algoritmos aprenden los patrones.
* **Test (20% - 30 flores):** Flores guardadas bajo llave para comprobar al final la precisión real.

#### 2. Escalado de variables (`StandardScaler`)
Transformamos las columnas numéricas para que tengan **media 0 y desviación estándar 1**. Esto evita que variables con números más grandes dominen el cálculo de distancias o gradientes (especialmente importante para modelos lineales como la Regresión Logística). Se ajusta solo en *Train* para evitar fuga de datos (*Data Leakage*).

#### 3. Modelos y Búsqueda de Hiperparámetros (`RandomizedSearchCV`)
En lugar de elegir los ajustes de los modelos a ojo, usamos **`RandomizedSearchCV`** con validación cruzada (`cv=5`), que prueba múltiples combinaciones al azar y se queda automáticamente con la ganadora:

* **Regresión Logística (`best_log_reg`):**
  * Calcula la probabilidad (de 0 a 1) de pertenecer a cada una de las 3 especies.
  * Se optimiza el parámetro **`C`** (fuerza de regularización inversa) y **`penalty`** para evitar el sobreajuste (*overfitting*).
  * **Resultado actual en Test:** `1.0000` (100% de precisión).

* **Random Forest (`best_rf`):**
  * En lugar de confiar en un solo árbol de decisión (que suele memorizar y cometer errores), crea un conjunto de árboles entrenados con muestras y medidas aleatorias.
  * Cada árbol vota por una especie y el modelo predice la más votada.
  * Se optimiza **`n_estimators`** (número de árboles en el bosque) y **`max_depth`** (profundidad máxima de preguntas para evitar reglas demasiado específicas).
  * **Resultado actual en Test:** `1.0000` (100% de precisión).

---

### Estructura actual del proyecto

```text
02-iris-clasificación/
├── data/
│   └── iris.csv            # Dataset original
├── notebooks/
│   └── 01-iris.ipynb       # Flujo completo de modelado y experimentación
└── README.md
```

---

### Aprendizajes clave hasta ahora

1. **Rutas en Jupyter:** El directorio de ejecución del notebook es su propia carpeta (`notebooks/`), por lo que los datos se leen desde `../data/iris.csv`.
2. **Escalado:** Vital para la Regresión Logística; prescindible para modelos basados en árboles como Random Forest, pero compatible con ambos.
3. **Regularización ($C$):** $C$ pequeño penaliza mucho (evita memorizar pero puede causar infraajuste); $C$ grande da libertad total al modelo.
4. **Fuerza del ensamble (Random Forest):** Al combinar múltiples árboles no correlacionados, los errores individuales se cancelan, consiguiendo un modelo mucho más estable y generalizable.

---
---

## 📋 Plan de Mejora (Lo que falta por hacer por mi cuenta)

Checklist paso a paso basado en las recomendaciones de NotebookLM para completar el notebook [`notebooks/01-iris.ipynb`](notebooks/01-iris.ipynb) y dejar el README final listo para reclutadores:

### Paso 1: Análisis Exploratorio Visual (EDA - Pairplot) ✅
- [x] Importar `seaborn as sns` y `matplotlib.pyplot as plt`.
- [x] Crear el gráfico de dispersión cruzado (**Pairplot**) coloreado por especie:
  ```python
  sns.pairplot(iris_df, hue='species', diag_kind='hist')
  ```
- [x] Anotar cómo **`setosa`** queda totalmente aislada mientras que **`versicolor`** y **`virginica`** se solapan ligeramente.
- [x] Crear la carpeta `reports/figures/` y guardar la imagen (`plt.savefig("../reports/figures/01_pairplot_iris.png")`).

### Paso 2: Corregir aviso en Regresión Logística y ver hiperparámetros ganadores ✅
- [x] En la celda de `LogisticRegression`, cambiar `'penalty': ['none', 'l2']` por `'penalty': ['l2']` (o `None` sin comillas) para evitar los warnings.
- [x] Ver qué combinación ganó ejecutando `grid_search_log_reg.best_params_` y `grid_search_rf.best_params_`.
- [x] Ver la nota media de validación cruzada en entrenamiento con `grid_search_log_reg.best_score_` y `grid_search_rf.best_score_`.

### Paso 3: Añadir los algoritmos que sugiere el vídeo (Árbol de Decisión simple y SVM)
- [ ] **Árbol de Decisión individual (`DecisionTreeClassifier`):**
  * Importar `from sklearn.tree import DecisionTreeClassifier`.
  * Entrenarlo con `RandomizedSearchCV` probando `'max_depth': [None, 2, 3, 5, 10]`.
  * *Objetivo:* Usarlo como línea base para comparar un solo árbol contra el **Random Forest**.
- [ ] **Support Vector Machine (`SVC`):**
  * Importar `from sklearn.svm import SVC`.
  * Entrenarlo con `RandomizedSearchCV` probando `'C': [0.1, 1, 10, 100]` y `'kernel': ['linear', 'rbf']`.

### Paso 4: Calcular F1-Score y completar la Tabla Comparativa
- [ ] Importar `from sklearn.metrics import f1_score`.
- [ ] Calcular `f1_score(y_test, y_pred, average='macro')` para cada modelo y rellenar esta tabla:

| Modelo | CV Accuracy (Train) | Accuracy (Test) | F1-Score | Mejor Hiperparámetro |
|---|---|---|---|---|
| **Regresión Logística** | `95.83%` | `100.0%` | *pendiente* | `C=21.54` |
| **Árbol de Decisión** | *pendiente* | *pendiente* | *pendiente* | `max_depth=...` |
| **Random Forest** | `95.83%` | `100.0%` | *pendiente* | `n_estimators=200, max_depth=20` |
| **SVM (SVC)** | *pendiente* | *pendiente* | *pendiente* | `C=..., kernel=...` |

### Paso 5: Matriz de Confusión e Importancia de Variables
- [ ] Importar `from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay`.
- [ ] Dibujar la matriz de confusión para comprobar dónde se confunden los modelos (en la frontera entre *Versicolor* y *Virginica*).
- [ ] Ver qué variables pesan más en Random Forest con `best_rf.feature_importances_`.

### Paso 6: Sección de Requisitos e Instalación (Ya lista para el README)
```bash
# 1. Activar entorno virtual
.venv\Scripts\activate

# 2. Instalar librerías necesarias
pip install pandas numpy scikit-learn matplotlib seaborn jupyter

# 3. Iniciar el notebook
jupyter notebook notebooks/01-iris.ipynb
```
