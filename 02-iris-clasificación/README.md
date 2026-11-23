# Clasificación de Flores Iris · Machine Learning

Proyecto introductorio de clasificación multiclase donde predecimos la especie de una flor a partir de sus medidas anatómicas, comparando dos algoritmos clave (**Regresión Logística** y **Random Forest**) y optimizando sus hiperparámetros.

---

## El problema y los datos

A partir del dataset clásico de **Iris** (150 flores en total), queremos predecir la **especie** (`setosa`, `versicolor` o `virginica`) basándonos en 4 medidas numéricas continuas:

* `sepal_length`: Longitud del sépalo (cm)
* `sepal_width`: Ancho del sépalo (cm)
* `petal_length`: Longitud del pétalo (cm)
* `petal_width`: Ancho del pétalo (cm)

---

## Metodología paso a paso

### 1. Separación de datos (`train_test_split`)
Para evaluar el modelo con honestidad y asegurarnos de que no memoriza las flores, dividimos el dataset:
* **Train (80% - 120 flores):** Con lo que los algoritmos aprenden los patrones.
* **Test (20% - 30 flores):** Flores guardadas bajo llave para comprobar al final la precisión real.

### 2. Escalado de variables (`StandardScaler`)
Transformamos las columnas numéricas para que tengan **media 0 y desviación estándar 1**. Esto evita que variables con números más grandes dominen el cálculo de distancias o gradientes (especialmente importante para modelos lineales como la Regresión Logística). Se ajusta solo en *Train* para evitar fuga de datos (*Data Leakage*).

### 3. Modelos y Búsqueda de Hiperparámetros (`RandomizedSearchCV`)
En lugar de elegir los ajustes de los modelos a ojo, usamos **`RandomizedSearchCV`** con validación cruzada (`cv=5`), que prueba múltiples combinaciones al azar y se queda automáticamente con la ganadora:

* **Regresión Logística:**
  * Calcula la probabilidad (de 0 a 1) de pertenecer a cada una de las 3 especies.
  * Se optimiza el parámetro **`C`** (fuerza de regularización inversa) y **`penalty`** para evitar el sobreajuste (*overfitting*).

* **Random Forest:**
  * En lugar de confiar en un solo árbol de decisión (que suele memorizar y cometer errores), crea un conjunto de árboles entrenados con muestras y medidas aleatorias.
  * Cada árbol vota por una especie y el modelo predice la más votada.
  * Se optimiza **`n_estimators`** (número de árboles en el bosque) y **`max_depth`** (profundidad máxima de preguntas para evitar reglas demasiado específicas).

---

## Estructura del proyecto

```text
02-iris-clasificación/
├── data/
│   └── iris.csv            # Dataset original
├── notebooks/
│   └── 01-iris.ipynb       # Flujo completo de modelado y experimentación
└── README.md
```

---

## Aprendizajes clave

1. **Rutas en Jupyter:** El directorio de ejecución del notebook es su propia carpeta (`notebooks/`), por lo que los datos se leen desde `../data/iris.csv`.
2. **Escalado:** Vital para la Regresión Logística; prescindible para modelos basados en árboles como Random Forest, pero compatible con ambos.
3. **Regularización ($C$):** $C$ pequeño penaliza mucho (evita memorizar pero puede causar infraajuste); $C$ grande da libertad total al modelo.
4. **Fuerza del ensamble (Random Forest):** Al combinar múltiples árboles no correlacionados, los errores individuales se cancelan, consiguiendo un modelo mucho más estable y generalizable.
