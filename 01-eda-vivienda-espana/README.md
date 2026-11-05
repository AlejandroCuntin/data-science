# EDA · Vivienda en España

¿Cuánto esfuerzo real cuesta comprar una vivienda en España, cómo ha cambiado desde 2007 y qué provincias están en una situación más crítica?

## Métrica principal

**Años de renta neta del hogar necesarios para comprar una vivienda de 90 m².**

Métricas de apoyo:

- Precio real (€/m² deflactado por IPC) por provincia, 2007–2026.
- Ratio precio/renta y su evolución.
- Divergencia territorial: brecha entre la provincia más y menos asequible.
- Escenario hipotecario: cuota mensual sobre renta mensual neta (análisis de sensibilidad).

## Fuentes

| Uso | Fuente | Nivel | Enlace |
|---|---|---|---|
| Precio €/m² (principal) | MITMA · Valor tasado de la vivienda | Provincia y municipios >25.000 hab. | [transportes.gob.es](https://www.transportes.gob.es/el-ministerio/informacion-estadistica/vivienda-y-actuaciones-urbanas/estadisticas/valor-tasado-de-la-vivienda) |
| Renta de los hogares | INE · Atlas de Distribución de Renta de los Hogares (2015–2024) | Municipio y sección censal | [ine.es](https://www.ine.es/experimental/atlas/experimental_atlas.htm) |
| Índice de precios | INE · IPV base 2015 | Nacional y CCAA | [INE tabla 25171](https://www.ine.es/jaxiT3/Tabla.htm?t=25171) |
| Deflactor | INE · IPC | Nacional | [ine.es](https://www.ine.es) |
| Población | INE · Padrón / Cifras de población | Municipio | [ine.es](https://www.ine.es) |
| Contrastación | Registradores · Anuario Estadístico | Provincia | [registradores.org](https://www.registradores.org) |

## Decisiones metodológicas

- **Precios**: se usa el valor tasado de MITMA como fuente principal porque el IPV del INE no desciende a nivel provincial.
- **Valor tasado ≠ precio de transacción**: es una limitación declarada; se contrasta con Registradores.
- **Renta provincial**: se agrega desde los municipios del ADRH ponderando por población.
- **Euros reales**: el análisis principal se hace deflactado por IPC; el nominal queda como anexo.
- **Vivienda de referencia**: 90 m², con sensibilidad a 70 y 100 m².

## Estructura

```
01-eda-vivienda-espana/
├── data/
│   ├── raw/          # descargas originales (no versionado)
│   ├── interim/      # limpieza intermedia (no versionado)
│   └── processed/    # datasets finales
├── src/              # descarga, limpieza y construcción de métricas
├── notebooks/        # análisis narrativo
└── reports/figures/  # visualizaciones finales
```

## Estado

- [x] Estructura del proyecto
- [ ] Sprint 0 · Ingesta y diccionario de datos
- [ ] Sprint 1 · Panorama nacional y mapa provincial
- [ ] Sprint 2 · Affordability y evolución
- [ ] Sprint 3 · Conclusiones y README final
