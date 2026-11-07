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

## Estructura

```
01-eda-vivienda-espana/
├── data/
│   ├── raw/          # descargas originales (versionado)
│   ├── interim/      # limpieza intermedia (no versionado)
│   └── processed/    # datasets finales
├── src/              # descarga, limpieza y construcción de métricas
├── notebooks/        # análisis narrativo
└── reports/figures/  # visualizaciones finales
```

## Estado

- [x] Estructura del proyecto
- [x] Descarga de fuentes (MITMA, IPC, ADRH, IPV)
- [x] Auditoría y diccionario de datos → `data/raw/README.md`
- [x] Limpieza de MITMA e INE → 4 CSV en `data/interim/`
- [x] Panel provincia-año y métricas → `data/processed/`
- [ ] Sprint 1 · Panorama nacional y mapa provincial
- [ ] Sprint 2 · Affordability y evolución
- [ ] Sprint 3 · Conclusiones y README final
