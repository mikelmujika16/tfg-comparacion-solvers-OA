# 📊 Comparación de Solvers Comerciales para la Generación de Matrices Ortogonales

> 🌐 This README is also available in [English](README_en.md).

Este repositorio contiene el código, datos y documentación del **Trabajo de Fin de Grado (TFG)** titulado:

> **"Explorando la Eficiencia de Solvers Comerciales en la Construcción de Arreglos Ortogonales"**

El objetivo del proyecto es **comparar diferentes estrategias de modelado y distintos solvers comerciales y libres** (como Gurobi, CPLEX, Hexaly, OR-Tools, entre otros) para resolver el problema de **generación de arreglos ortogonales (Orthogonal Arrays, OA)** dadas combinaciones de parámetros \( N, k, s, t \), empleando un modelo matemático común y evaluando diversos criterios técnicos y prácticos.

## 🚀 Quickstart

Sigue estos pasos para clonar el repositorio, instalar las dependencias y ejecutar la aplicación:

### 1. Clonar el repositorio

```bash
git clone https://github.com/mikelmujika16/tfg-comparacion-solvers-OA.git
cd tfg-comparacion-solvers-OA
```

### 2. Crear un entorno virtual (opcional pero recomendado)

Para instalar las dependencias del proyecto, es recomendable crear un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate        # En Linux/macOS
venv\Scripts\activate           # En Windows
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Licencias de los Solvers

Para utilizar los solvers comerciales como Gurobi, CPLEX y Hexaly, necesitarás tener una licencia válida. Consulta la documentación de cada solver para obtener información sobre cómo obtener y configurar las licencias.

### 5. Ejecutar la aplicación

Desde el directorio raíz del proyecto, puedes ejecutar el script principal para generar y comparar los arreglos ortogonales:

```bash
python src/menu.py
```

## 📁 Estructura del repositorio

```plaintext
tfg-comparacion-solvers-OA/
├── src/           # Scripts Python o Julia para cada solver
├── data/            # Resultados de los OA creados
├── figures/          # Gráficas exportadas (PDF/PNG) para la memoria
├── results/           # Tablas CSV de las comparativas
├── memoria/          # Proyecto LaTeX exportado desde Overleaf
├── plan.md           # Planificación del proyecto, fases y metodología
└── README.md         # Este archivo
```

## 🧰 Tecnologías y herramientas utilizadas

- **Lenguaje:** Python 3.x
- **Modelado matemático:** Pyomo, Hexaly Python API, OR-tools Python API
- **Solvers:** Gurobi, CPLEX, Hexaly, OR-Tools, otros
- **Visualización:** Matplotlib, Seaborn, Plotly
- **Documentación:** LaTeX (Overleaf), Markdown, GitHub

## ⚙️ Criterios de comparación entre solvers

- ⏱️ **Performance** (tiempo de resolución)
- 🧠 **Calidad de la solución** (ortonormalidad, cobertura)
- ✍️ **Facilidad de modelado**
- 📈 **Escalabilidad** (como escalan los solvers)
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
