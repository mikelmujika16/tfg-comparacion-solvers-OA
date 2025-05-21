# 📊 Comparación de Solvers Comerciales para la Generación de Matrices Ortogonales

> 🌐 This README is also available in [English](README_en.md).

Este repositorio contiene el código, datos y documentación del **Trabajo de Fin de Grado (TFG)** titulado:

> **"Explorando la Eficiencia de Solvers Comerciales en la Construcción de Matrices Ortogonales"**

El objetivo del proyecto es **comparar diferentes solvers comerciales y libres** (como Gurobi, CPLEX, Hexaly, OR-Tools, entre otros) para resolver el problema de **generación de matrices ortogonales (Orthogonal Arrays, OA)** dadas combinaciones de parámetros \( N, k, s, t \), empleando un modelo matemático común y evaluando diversos criterios técnicos y prácticos.

## 📁 Estructura del repositorio

```plaintext
tfg-comparacion-solvers-OA/
├── src/           # Scripts Python o Julia para cada solver
├── data/            # Instancias de entrada y resultados crudos
├── figuras/          # Gráficas exportadas (PDF/PNG) para la memoria
├── tablas/           # Tablas en LaTeX o CSV para incluir en la memoria
├── memoria/          # Proyecto LaTeX exportado desde Overleaf
│   └── memtfg.tex    # Documento principal de la memoria
├── plan.md           # Planificación del proyecto, fases y metodología
└── README.md         # Este archivo
```

## 🧰 Tecnologías y herramientas utilizadas

- **Lenguaje:** Python 3.x
- **Modelado matemático:** PuLP, Pyomo, JuMP (según solver)
- **Solvers:** Gurobi, CPLEX, Hexaly, OR-Tools, otros
- **Visualización:** Matplotlib, Seaborn, Plotly
- **Documentación:** LaTeX (Overleaf), Markdown, GitHub

## ⚙️ Criterios de comparación entre solvers

- ⏱️ **Performance** (tiempo de resolución)
- 🧠 **Calidad de la solución** (ortonormalidad, cobertura)
- ✍️ **Facilidad de modelado**
- 📈 **Escalabilidad** (instancias grandes)
- 💸 **Licencia y coste**
- 🌐 **Otros**: comunidad, documentación, integración, soporte

## 📅 Cronograma de trabajo

Consulta [plan.md](./plan.md) para ver las fases y fechas previstas del proyecto.

## 📜 Licencia

Este proyecto está bajo una licencia:

**Creative Commons BY-NC-ND 4.0 Internacional**

> © Esta obra está bajo una licencia de Creative Commons Reconocimiento-NoComercial-SinObraDerivada 4.0 Internacional.

## ✍️ Autor

**Mikel Mugica Arregui**  
Grado en Ingeniería Informática  
Universidad de La Laguna  
Tutor: Juan José Salazar González
