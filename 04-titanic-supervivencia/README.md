# Predicción de Supervivencia del Titanic · Machine Learning con Datos Reales

Proyecto de **clasificación binaria** (`1 = Sobrevive`, `0 = No sobrevive`) sobre el registro histórico de **891 pasajeros del Titanic (1912)**. El foco principal de este cuarto proyecto es enfrentarse por primera vez a un **dataset sucio del mundo real**: limpiar valores nulos (*Missing Data*), transformar texto a números (*Encoding*) y crear nuevas características con sentido lógico (*Feature Engineering*).

---

## 🎯 ¿Qué vamos a aprender aquí que NO tenían los proyectos anteriores?

En el **Proyecto 02 (Iris)** y el **Proyecto 03 (Regresión Lineal)** las tablas venían "de laboratorio": todas las columnas predictoras ya eran números limpios y no faltaba ni un solo dato.
En el mundo real las tablas nunca vienen así. Si intentas meter el CSV del Titanic directamente en un algoritmo de Machine Learning, **Python dará error inmediatamente** por 3 problemas nuevos que aprenderemos a resolver:

### 1. Gestión de Datos Faltantes (*Missing Data / `NaN`*)
En 1912 el registro del barco quedó incompleto:
* A **177 pasajeros** les falta la edad (`Age`).
* Al **77% de los pasajeros (687 filas)** les falta el número de camarote (`Cabin`).
* A **2 pasajeros** les falta el puerto de embarque (`Embarked`).
* **Qué aprenderemos:** Cuándo conviene **eliminar** una columna entera porque tiene demasiados huecos (`Cabin`) y cuándo conviene **imputar (rellenar)** los huecos con inteligencia (por ejemplo, rellenar las edades vacías con la mediana de edad según su clase de billete, sin borrar a esos 177 pasajeros).

### 2. Transformar Texto a Números (*Categorical Encoding*)
Los algoritmos matemáticos ($\hat{y} = w \cdot x + b$) no saben multiplicar palabras como `"female"`, `"male"` o puertos como `"Southampton (S)"`.
* **Qué aprenderemos:** Cómo convertir columnas de texto (*variables categóricas*) en columnas numéricas (`0` y `1`) mediante **Mapeo Binario** y **One-Hot Encoding (`pd.get_dummies`)**.

### 3. Ingeniería de Variables (*Feature Engineering*)
En lugar de limitarnos a las columnas que vienen en el archivo original, fabricaremos **columnas nuevas** combinando pistas:
* En el CSV vienen `SibSp` (nº de hermanos/cónyuge a bordo) y `Parch` (nº de padres/hijos a bordo).
* **Qué aprenderemos:** A combinarlas para crear **`FamilySize` (Tamaño de la familia)** y **`ViajaSolo` (`1` o `0`)**, descubriendo cómo viajar solo o en familias demasiado numerosas cambiaba drásticamente las opciones de llegar a un bote salvavidas.

---

## 📋 Plan de Trabajo (Hoja de ruta en 6 Fases para hacer por mi cuenta)

Sigue estos pasos dentro de `notebooks/01-titanic.ipynb`:

### Fase 1: Cargar el Dataset y Hacer la "Autopsia de Datos Sucios"
- [ ] Cargar el dataset de los **891 pasajeros** (`data/titanic.csv`) y ver las primeras filas.
- [ ] Inspeccionar los tipos de datos (`df.info()`) para identificar qué columnas son texto (`object`) y cuáles son números.
- [ ] Contar cuántos datos vacíos (`NaN`) tiene cada columna con `df.isnull().sum()`.

### Fase 2: Análisis Exploratorio Socioeconómico (EDA Visual)
- [ ] **Gráfico 1 (*"Mujeres y niños primero"*):** Comparar el porcentaje de supervivencia por **Sexo (`Sex`)** y por **Clase del billete (`Pclass`: 1ª, 2ª y 3ª)**, y guardarlo en `reports/figures/01_supervivencia_sexo_clase.png`.
- [ ] **Gráfico 2 (Distribución de Edades):** Ver cómo influyó la edad (`Age`) en sobrevivir y guardarlo en `reports/figures/02_distribucion_edad.png`.

### Fase 3: Limpieza de Datos Faltantes (*Missing Data*)
- [ ] **Eliminar columnas de ruido o con exceso de nulos:** Quitar `Cabin` (77% vacío), `PassengerId`, `Name` y `Ticket`.
- [ ] **Imputar la Edad (`Age`):** Rellenar los 177 huecos de edad usando la mediana de edad de cada clase (`Pclass`), ya que los pasajeros de 1ª clase eran de media más mayores que los de 3ª.
- [ ] **Imputar el Puerto (`Embarked`):** Rellenar los 2 huecos vacíos con el puerto más frecuente (la moda: `"S"`).
- [ ] Verificar con `df.isnull().sum()` que la tabla queda con **0 nulos**.

### Fase 4: Ingeniería de Variables (*Feature Engineering*) y *Encoding*
- [ ] Crear la variable **`FamilySize`** (`SibSp + Parch + 1`, sumando al propio pasajero).
- [ ] Crear la variable **`ViajaSolo`** (`1` si `FamilySize == 1`, `0` si viaja acompañado).
- [ ] Convertir el texto a números (*Encoding*):
  * `Sex`: `"female" -> 1`, `"male" -> 0`.
  * `Embarked`: Convertir los puertos `"C"`, `"Q"`, `"S"` en columnas numéricas con `pd.get_dummies()`.

### Fase 5: Entrenamiento y Competición de Modelos
- [ ] Separar `X` (variables predictoras) e `y` (`Survived`: `0` o `1`) y dividir en **80% Train / 20% Test** (`train_test_split`).
- [ ] Aplicar `StandardScaler` para escalar las variables numéricas (`Age`, `Fare`, `FamilySize`).
- [ ] Entrenar y optimizar con `RandomizedSearchCV` (`cv=5`):
  * **Regresión Logística**
  * **Random Forest**

### Fase 6: Evaluación Final, Matriz de Confusión y `Feature Importances`
- [ ] Calcular `Accuracy` y `F1-Score` en el conjunto de Test y rellenar la tabla comparativa de este `README.md`.
- [ ] Dibujar la **Matriz de Confusión** y el gráfico de **Importancia de Variables (`feature_importances_`)** (`reports/figures/03_matriz_e_importancia.png`) para responder con datos: *¿Qué pesó más en el hundimiento del Titanic: el sexo, el dinero/clase del billete, la edad o la familia?*

---

## 1. Diccionario de Columnas del Dataset Original

| Columna | Significado | Tipo Original | Problema a Resolver |
|---|---|---|---|
| **`Survived`** | **Variable objetivo (`y`):** `1` = Sobrevivió, `0` = Falleció | Número (`0/1`) | Ninguno (es lo que queremos predecir) |
| **`Pclass`** | Clase del billete (`1` = 1ª Clase, `2` = 2ª Clase, `3` = 3ª Clase) | Número (`1, 2, 3`) | Ninguno |
| **`Sex`** | Sexo del pasajero (`"male"` o `"female"`) | Texto | Hay que convertirlo a número (`0` y `1`) |
| **`Age`** | Edad en años | Número decimal | **Faltan 177 valores (`NaN`)** $\rightarrow$ Imputar |
| **`SibSp`** | Nº de hermanos o esposo/a a bordo | Número entero | Combinar en **`FamilySize`** |
| **`Parch`** | Nº de padres o hijos a bordo | Número entero | Combinar en **`FamilySize`** |
| **`Fare`** | Precio pagado por el billete (en libras de 1912) | Número decimal | Escalar con `StandardScaler` |
| **`Cabin`** | Número de camarote | Texto | **Falta el 77% (687 nulos)** $\rightarrow$ Eliminar |
| **`Embarked`** | Puerto de embarque (`C` = Cherburgo, `Q` = Queenstown, `S` = Southampton) | Texto | **Faltan 2 valores** + Convertir a número |

---

## 2. Análisis Exploratorio Socioeconómico (EDA)

> *(Pendiente de insertar gráficos tras la Fase 2:*
> *`![Supervivencia por Sexo y Clase](reports/figures/01_supervivencia_sexo_clase.png)`*
> *`![Distribución de Edad](reports/figures/02_distribucion_edad.png)`)*

---

## 3. Resultados y Evaluación Final

> *(Rellenar tras completar las Fases 5 y 6)*

| Modelo | CV Accuracy (Train) | Accuracy (Test) | F1-Score (Test) | Mejores Hiperparámetros |
|---|---|---|---|---|
| **Regresión Logística** | *pendiente* | *pendiente* | *pendiente* | *pendiente* |
| **Random Forest** | *pendiente* | *pendiente* | *pendiente* | *pendiente* |

### Matriz de Confusión e Importancia de Variables

> *(Pendiente de insertar gráfico tras la Fase 6: `![Matriz e Importancia](reports/figures/03_matriz_e_importancia.png)`)*

---

## 4. Estructura del proyecto

```text
04-titanic-supervivencia/
├── data/
│   └── titanic.csv                           # Registro histórico de 891 pasajeros
├── notebooks/
│   └── 01-titanic.ipynb                      # Limpieza, Feature Engineering y modelado
├── reports/
│   └── figures/                              # Gráficos de EDA, Matriz e Importancia
└── README.md
```

---

## 5. Requisitos e Instalación

```bash
# 1. Activar entorno virtual (desde la raíz del repositorio)
.venv\Scripts\activate

# 2. Instalar librerías necesarias
pip install pandas numpy scikit-learn matplotlib seaborn jupyter

# 3. Abrir el notebook
jupyter notebook notebooks/01-titanic.ipynb
```
