# 📘 Plan de Proyecto TFG: Comparación de Solvers para OA

## 🎯 Objetivo del Proyecto

Comparar distintos **solvers comerciales y libres** para resolver el problema de **generación de matrices ortogonales (Orthogonal Arrays, OA)** dados sus parámetros \( N, k, s, t \).

Se utilizará un **modelo matemático común**, implementado **preferiblemente en Python**, que será adaptado a cada solver para realizar una comparación justa y rigurosa.

## 🧰 Solvers considerados

- [x] Gurobi
- [x] CPLEX
- [x] Hexaly
- [x] OR-Tools
- [ ] Otros (a evaluar): Z3, MiniZinc, Chuffed...

## ⚙️ Criterios de comparación

| Criterio                 | Descripción |
|--------------------------|-------------|
| 🕒 **Performance**        | Tiempo de cómputo para resolver instancias variadas. |
| ✅ **Calidad de solución** | Grado de ortonormalidad, cobertura y completitud de las matrices generadas. |
| ✍️ **Facilidad de modelado** | Claridad, concisión y legibilidad del modelo en el lenguaje del solver. |
| 📈 **Escalabilidad**       | Comportamiento al aumentar los parámetros \( N, k, s, t \). |
| 💸 **Precio y licencia**   | Coste de uso, disponibilidad de licencias académicas. |
| 🌍 **Otros factores**      | Soporte técnico, comunidad activa, documentación, facilidad de integración, etc. |

## 🧪 Metodología

1. Definir modelo matemático base.
2. Adaptarlo a cada solver (Python preferred).
3. Ejecutar sobre varias instancias OA con diferentes parámetros.
4. Registrar tiempos, soluciones y logs.
5. Analizar resultados con gráficos y tablas.
6. Redactar memoria con interpretación crítica.

## 📦 Organización del repositorio

```
tfg-comparacion-solvers-OA/
├── codigo/       → Implementaciones por solver
├── datos/        → Instancias, resultados crudos
├── figuras/      → Gráficas exportadas
├── tablas/       → Comparativas en LaTeX/CSV
├── memoria/      → Proyecto LaTeX exportado desde Overleaf
├── plan.md       → Este documento
└── README.md     → Descripción general del proyecto
```

## 📅 Fases y entregas estimadas

| Fase                             | Fecha objetivo   | Estado |
|----------------------------------|------------------|--------|
| Búsqueda de solvers y documentación | 1 junio 2025     | ☐      |
| Diseño del modelo matemático OA     | 5 junio 2025     | ☐      |
| Implementación en Gurobi y CPLEX    | 10 junio 2025    | ☐      |
| Implementación en Hexaly y OR-Tools | 15 junio 2025    | ☐      |
| Experimentación y benchmarking      | 20 junio 2025    | ☐      |
| Generación de gráficos/tablas       | 25 junio 2025    | ☐      |
| Redacción final de la memoria       | 30 junio 2025    | ☐      |

## 📝 Notas

- Todo código preferentemente en Python para facilitar comparación.
- Las gráficas se generarán con Matplotlib o Plotly.
- La exportación de resultados para LaTeX será automática desde scripts.
