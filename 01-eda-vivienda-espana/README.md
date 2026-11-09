# EDA · Vivienda en España

¿Cuánto esfuerzo real cuesta comprar una vivienda en España, cómo ha cambiado desde 2007 y qué provincias están en una situación más crítica?

## Métrica principal

**Años de renta neta del hogar necesarios para comprar una vivienda de 90 m².**

Métricas de apoyo:

- Precio real (€/m² deflactado por IPC) por provincia, 2007–2025 (+2026 parcial).
- Ratio precio/renta y su evolución.
- Divergencia territorial: brecha entre la provincia más y menos asequible.
- Escenario hipotecario: cuota mensual sobre renta mensual neta (análisis de sensibilidad).

## Alcance temporal por serie

| Serie | Ventana | Fuente | Nota |
|---|---|---|---|
| Precio €/m² (nominal y real) | 2007–2025 (+2026 parcial) | MITMA | Anual = media de 4 trimestres |
| Nueva vs. usada | 2010–2025 | MITMA | 355 huecos `n.r` en nueva y 3 en usada |
| Renta neta del hogar | 2015–2024 | ADRH | Sin Navarra 2015–2020, Álava 2015–2019, Gipuzkoa 2015 ni Total Nacional 2015–2020 |
| Años de renta (métrica principal) | 2015–2024 | MITMA + ADRH | Intersección de ambas series |
| Contraste de tendencia | 2007T1–2026T2 | IPV | Solo nacional y CCAA |

## Fuentes

| Uso | Fuente | Nivel | Enlace |
|---|---|---|---|
| Precio €/m² (principal) | MITMA · Valor tasado de la vivienda | Nacional, CCAA y provincia | [transportes.gob.es](https://www.transportes.gob.es/el-ministerio/informacion-estadistica/vivienda-y-actuaciones-urbanas/estadisticas/valor-tasado-de-la-vivienda) |
| Renta de los hogares | INE · ADRH tabla 53689 (2015–2024) | Nacional, CCAA y provincia | [INE tabla 53689](https://www.ine.es/jaxiT3/Tabla.htm?t=53689) |
| Contraste de precios | INE · IPV base 2025, tabla 79563 | Nacional y CCAA | [INE tabla 79563](https://www.ine.es/jaxiT3/Tabla.htm?t=79563) |
| Deflactor | INE · IPC base 2025, tabla 76144 | Nacional | [INE tabla 76144](https://www.ine.es/jaxiT3/Tabla.htm?t=76144) |
| Contrastación | Registradores · Anuario Estadístico *(pendiente)* | Provincia | [registradores.org](https://www.registradores.org) |

Diccionario de datos y detalle de cada fichero: [`data/raw/README.md`](data/raw/README.md).

## Decisiones metodológicas

- **Precios**: valor tasado de MITMA como fuente principal; el IPV del INE no baja a provincia.
- **Valor tasado ≠ precio de transacción**: limitación declarada; se contrasta con Registradores.
- **Renta provincial**: se toma directamente de la tabla provincial 53689 del INE (no se agregan municipios).
- **Euros reales**: deflactado por IPC base 2025. El ratio precio/renta es invariante al deflactor, así que se calcula en nominal.
- **Vivienda de referencia**: 90 m², con sensibilidad a 70 y 100 m².
- **Ventanas temporales distintas**: precios 2007–2026, asequibilidad 2015–2024. No se extrapola renta.
- **2026 parcial**: solo Q1–Q2; se excluye de medias anuales y variaciones interanuales.

## Conclusiones

El desarrollo está en [`notebooks/02_asequibilidad.ipynb`](notebooks/02_asequibilidad.ipynb)
(bloques 4 y 5). En corto:

- **La provincia mediana mejora, pero desde el peor año de la serie.** El
  esfuerzo pasa de 3,73 a 3,09 años entre 2015 y 2024 (−17,2 %); en el tramo
  2021–2024 baja un −8,8 %. España, con serie desde 2021, pasa de 4,40 a 4,24
  (−3,6 %).
- **España no es la provincia mediana.** En 2024, la mediana provincial son
  3,24 años y 117.426 € por 90 m²; el total nacional, 4,24 años y 172.226 €.
  Solo 8 provincias superan el coste nacional.
- **El problema está concentrado.** Cinco provincias pasan de cinco años:
  Málaga (6,08), Baleares (5,97), Madrid (5,62), Gipuzkoa (5,43) y Barcelona
  (5,20). Cuarenta y una no llegan a cuatro y veintidós no llegan a tres.
- **La brecha la explica el precio, no la renta.** De las 49 provincias con
  serie completa, 45 mejoran y 4 empeoran. Málaga es la sexta en coste pero la
  primera en esfuerzo; Madrid, la primera en coste y la tercera en esfuerzo.
- **2025 queda abierto.** El precio acelera un +11,2 % sin la renta del ADRH,
  así que no se puede saber si la mejora de 2024 fue un respiro o una pausa.

Los límites se mantienen: valor tasado —no precio de compraventa—, coste bruto
sin impuestos ni intereses, huecos de renta declarados y no interpolados, y 2026
parcial fuera de las medias.

## Estructura

```
01-eda-vivienda-espana/
├── data/
│   ├── raw/          # descargas originales (versionado)
│   ├── interim/      # limpieza intermedia (no versionado)
│   └── processed/    # datasets finales
├── src/              # descarga, limpieza y construcción de métricas
├── notebooks/        # análisis narrativo
├── web/              # calculadora estática (HTML, CSS y JS sin framework)
├── tests/            # comprobaciones de la calculadora
└── reports/figures/  # visualizaciones finales
```

## Calculadora web

`web/` contiene una página estática, sin framework ni servidor de aplicaciones,
con dos modos sobre los mismos datos:

- **Años de renta**: la métrica principal, con superficie de 70, 90 o 100 m².
- **Cuota hipotecaria**: simulación a tipo fijo con entrada, interés y plazo
  editables (20 %, 3 % y 25 años por defecto).

Cubre 2015–2024, las 52 provincias y el total nacional, con vivienda total,
nueva y usada. Los huecos de renta y precio se declaran en la propia página; no
se interpolan. El precio sigue siendo valor tasado, no precio de compraventa.
Precio y renta van en euros nominales: al deflactar ambos, el cociente no cambia.

El JSON que consume la página se regenera desde el panel con:

```bash
python -m src.build_web_data
```

El JSON resultante, `web/data/panel.json`, se versiona para que la página
funcione sin un paso de build en el navegador.

Para abrirla hace falta un servidor local, porque el navegador bloquea `fetch`
sobre `file://`:

```bash
python -m http.server 8000
```

Y entrar en <http://localhost:8000/web/>. El estado se puede enlazar por URL con
`provincia`, `anio`, `tipo`, `m2`, `modo=hipoteca`, `entrada`, `interes`,
`plazo`, `precio` y `renta`; los valores por defecto se omiten. Ejemplo:
<http://localhost:8000/web/?provincia=28&anio=2024&modo=hipoteca>.

Comprobaciones de las funciones de cálculo y del export (requiere Node 18 o
superior):

```bash
node tests/test_calculator.js
```

## Estado

- [x] Estructura del proyecto
- [x] Descarga de fuentes (MITMA, IPC, ADRH, IPV)
- [x] Auditoría y diccionario de datos → `data/raw/README.md`
- [x] Limpieza de MITMA e INE → 4 CSV en `data/interim/`
- [x] Panel provincia-año y métricas → `data/processed/`
- [x] Auditoría del panel → `notebooks/00_auditoria.ipynb`
- [x] Sprint 1 · Panorama nacional y mapa provincial → `notebooks/01_precios.ipynb`
- [x] Sprint 2 · Affordability y evolución → `notebooks/02_asequibilidad.ipynb`
      - De las 49 provincias con serie completa, 45 mejoran y 4 empeoran; la
        brecha la explica el precio, no la renta. En 2024, la mediana provincial
        de 90 m² es 117.426 €; Madrid, 291.596 €.
- [x] Sprint 3 · Conclusiones y README final
      - Las cinco respuestas y los límites cierran la narrativa en
        `notebooks/02_asequibilidad.ipynb` (bloques 4 y 5); el resumen queda en
        la sección [Conclusiones](#conclusiones).
- [x] Calculadora interactiva de esfuerzo → `web/`
      - Dos modos: años de renta y cuota hipotecaria con entrada, interés y
        plazo editables.
      - Panel 2015–2024 para 52 provincias y total nacional, con aviso de los
        huecos de renta y precio y de que el precio es valor tasado.
      - Export reproducible con `python -m src.build_web_data` y pruebas con
        `node tests/test_calculator.js`.
