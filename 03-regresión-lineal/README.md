# Regresión Lineal desde Cero · Machine Learning Under the Hood

Construcción de un algoritmo de **Regresión Lineal 100% desde cero usando únicamente Python y NumPy** (*No Scikit-learn allowed* para el entrenamiento). El objetivo es programar y entender qué ocurre "bajo el capó" cuando una máquina aprende a partir de datos: la ecuación de la recta, la función de pérdida (MSE) y la optimización mediante **Descenso del Gradiente**.

---

## Plan de Trabajo (Hoja de ruta en 6 Fases para hacer por mi cuenta)

Sigue estos pasos dentro de `notebooks/01-regresion-lineal.ipynb`:

### Fase 1: Preparar los Datos y Visualizar la Nube de Puntos (EDA) ✅
- [x] Crear las carpetas `data/`, `notebooks/` y `reports/figures/` dentro de `03-regresión-lineal/`.
- [x] Generar o cargar nuestro dataset lineal (por ejemplo: **Años de Experiencia ($x$) vs. Salario ($y$)**) y guardarlo en `data/`.
- [x] Dibujar un gráfico de dispersión (**Scatter Plot**) con `matplotlib` para ver la tendencia lineal de los puntos y guardarlo en `reports/figures/01_scatter_datos.png`.

### Fase 2: Programar la Recta ($\hat{y} = w \cdot x + b$) y el Medidor de Error (MSE) ✅
- [x] Programar la función de predicción de la recta:
  $$\hat{y} = w \cdot x + b$$
- [x] Programar la función de coste / error cuadrático medio (**MSE - Mean Squared Error**):
  $$\text{MSE} = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$
- [x] Probar cuánto error da una recta inicial puesta a ciegas (con $w = 0$ y $b = 0$, dando un error inicial $\text{MSE} = 1750.74$).

### Fase 3: Programar el Motor de Aprendizaje (Descenso del Gradiente)
- [ ] Calcular las derivadas (gradientes $dw$ y $db$), que indican hacia dónde debemos girar ($w$) y subir/bajar ($b$) la recta para reducir el error:
  $$dw = -\frac{2}{N} \sum_{i=1}^{N} x_i \cdot (y_i - \hat{y}_i)$$
  $$db = -\frac{2}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)$$
- [ ] Actualizar $w$ y $b$ paso a paso en un bucle de entrenamiento (`epochs`) usando una tasa de aprendizaje (`learning_rate`, $\alpha$):
  $$w = w - \alpha \cdot dw$$
  $$b = b - \alpha \cdot db$$

### Fase 4: Visualizar cómo Aprende la Máquina
- [ ] **Gráfico 1 (Curva de Aprendizaje):** Graficar cómo cae el error **MSE** época tras época hasta estabilizarse cerca de cero (`reports/figures/02_curva_error_mse.png`).
- [ ] **Gráfico 2 (Ajuste de la Recta):** Pintar los puntos reales junto con la recta final aprendida por nuestro algoritmo (`reports/figures/03_recta_ajustada.png`).

### Fase 5: Crear nuestra propia Clase `LinearRegressionFromScratch`
- [ ] Empaquetar todo nuestro código matemático dentro de una clase limpia de Python con la misma estructura profesional que usa `scikit-learn`:
  * `modelo.fit(X, y)` $\rightarrow$ Entrena la recta con Descenso del Gradiente.
  * `modelo.predict(X)` $\rightarrow$ Predice valores nuevos con los $w$ y $b$ aprendidos.

### Fase 6: Prueba de Fuego (Tu Modelo desde Cero vs. Scikit-learn Oficial)
- [ ] Programar desde cero la métrica de evaluación **$R^2$ (Coeficiente de Determinación)**, que mide de 0 a 1 (0% a 100%) qué tan bien explica nuestra recta los datos.
- [ ] Entrenar el `LinearRegression()` oficial de `scikit-learn` con los mismos datos **solo para comparar** y rellenar la tabla final de resultados demostrando que nuestro algoritmo llega a la misma solución matemática.

---

## 1. ¿Cómo funciona una Regresión Lineal "bajo el capó"?

Cuando entrenamos un modelo en Machine Learning (desde una simple regresión hasta una red neuronal gigante de Deep Learning), siempre ocurren **3 pasos en bucle**:

### 1.1. La Predicción: La ecuación de la recta
Queremos encontrar la línea recta que mejor pase por en medio de nuestros puntos:
$$\hat{y} = w \cdot x + b$$
* **$x$:** El dato de entrada (ej. años de experiencia).
* **$\hat{y}$:** La predicción que hace nuestra recta (ej. salario estimado).
* **$w$ (Weight / Peso o Pendiente):** Cuánto se inclina la recta (cuánto sube el salario por cada año extra de experiencia).
* **$b$ (Bias / Sesgo o Intercepto):** La altura donde empieza la recta cuando $x = 0$ (el salario base con 0 años de experiencia).

### 1.2. El Castigo: La Función de Error (MSE)
Al principio la máquina no sabe cuánto valen $w$ y $b$, así que empieza en $0$. Para saber qué tan mala es su recta, mide la distancia vertical entre cada punto real ($y$) y la recta ($\hat{y}$), la eleva al cuadrado (para que los errores negativos no se anulen con los positivos y para castigar más los fallos grandes) y calcula el promedio (**MSE**).

### 1.3. El Aprendizaje: Descenso del Gradiente (*Gradient Descent*)
Imagina que estás en una montaña a oscuras y quieres bajar al valle más profundo (donde el error MSE es mínimo):
* **El Gradiente (la derivada):** Te dice hacia qué lado está cuesta abajo.
* **El Learning Rate ($\alpha$):** Es el tamaño de tu zancada. Si das pasos diminutos tardarás miles de épocas en llegar; si das saltos gigantes te pasarás de largo y el error explotará.

---

## 2. Análisis Exploratorio de los Datos

> *(Pendiente de insertar gráfico tras la Fase 1: `![Scatter Datos](reports/figures/01_scatter_datos.png)`)*

---

## 3. Evolución del Aprendizaje (Curva de Error y Recta Final)

> *(Pendiente de insertar gráficos tras la Fase 4:*
> *`![Curva MSE](reports/figures/02_curva_error_mse.png)`*
> *`![Recta Ajustada](reports/figures/03_recta_ajustada.png)`)*

---

## 4. Resultados: Modelo desde Cero vs. Scikit-learn

> *(Rellenar tras completar la Fase 6)*

| Implementación | Pendiente ($w$) | Sesgo / Intercepto ($b$) | Error Final (MSE) | Nota $R^2$ (Test) |
|---|---|---|---|---|
| **Nuestra Regresión (100% NumPy)** | *pendiente* | *pendiente* | *pendiente* | *pendiente* |
| **Scikit-learn (`LinearRegression`)** | *pendiente* | *pendiente* | *pendiente* | *pendiente* |

---

## 5. Estructura del proyecto

```text
03-regresión-lineal/
├── data/                                   # Dataset lineal utilizado
├── notebooks/
│   └── 01-regresion-lineal.ipynb           # Implementación paso a paso desde cero
├── reports/
│   └── figures/                            # Gráficos de dispersión, curva MSE y recta final
└── README.md
```

---

## 6. Requisitos e Instalación

```bash
# 1. Activar entorno virtual (desde la raíz del repositorio)
.venv\Scripts\activate

# 2. Instalar librerías necesarias
pip install numpy pandas matplotlib jupyter scikit-learn

# 3. Abrir el notebook
jupyter notebook notebooks/01-regresion-lineal.ipynb
```
