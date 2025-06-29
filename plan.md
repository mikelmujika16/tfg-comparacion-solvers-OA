# 📘 Proyecto: Comparación de Solvers para la Generación de Arreglos Ortogonales (Orthogonal Arrays)

## 🎯 Objetivo General

Evaluar el rendimiento y escalabilidad de distintas estrategias de modelado y solvers (MILP, Branch-and-Price, Hexaly, CP, heurísticas) en la generación de arreglos ortogonales OA(N, k, s, t), considerando cobertura exacta y criterios de eficiencia computacional.

---

## 📅 Fases del Proyecto

### 🔵 FASE 1: Especificación del problema y diseño experimental

**Duración:** 1–2 semanas  
**Responsables:** TBD  
**Tareas:**
- [ ] Definir parámetros de entrada: \(N, k, s, t\).
- [ ] Seleccionar subconjunto de instancias (valores válidos de \(s, t, k\), con \(\lambda = N/s^t \in \mathbb{Z}\)).
- [ ] Establecer métricas: tiempo, factibilidad, gap, calidad del diseño.
- [ ] Elegir métodos a implementar:
  - [x] MILP (selección de filas, variables por celda)
  - [x] Hexaly
  - [ ] Branch-and-Price (Gurobi + CP)
  - [ ] Metaheurísticas (opcional)
- [ ] Crear tabla de benchmark (ej. `results/oa_metrics.csv`)

---

### 🟢 FASE 2: Implementación de modelos

**Duración:** 3–5 semanas  
**Responsables:** TBD  
**Subtareas:**

#### 🔹 MILP en Pyomo (con Gurobi)
- [ ] Selección de filas (modelo básico)
- [ ] Modelo con variables \(x_{i,j,v}\) y restricciones de cobertura
- [ ] Modelo de generación columna por columna

#### 🔹 Hexaly y OR-tools
- [ ] Traducir modelos MILP a los formatos de modelado de Hexaly y OR-tools
- [ ] Implementar restricciones de cobertura exacta

---

### 🟡 FASE 3: Ejecución experimental

**Duración:** 2–3 semanas  
**Responsables:** TBD  
**Tareas:**
- [ ] Ejecutar cada método sobre el conjunto de instancias
- [ ] Medir:
  - Tiempo total
  - Calidad del diseño (aunque siempre se exige cobertura exacta)
- [ ] Guardar resultados (`results/oa_metrics.csv`)
- [ ] Generar gráficos de comparación (`figures/`)

---

### 🔴 FASE 4: Análisis y documentación

**Duración:** 1–2 semanas  
**Responsables:** TBD  
**Tareas:**
- [ ] Analizar qué métodos escalan mejor con \(s\), \(t\), \(k\)
- [ ] Comparar tiempo de cómputo, factibilidad, facilidad de modelado, estabilidad
- [ ] Redactar memoria (`memoria/memoria.tex`)
- [ ] Conclusiones y recomendaciones por tipo de instancia

---


