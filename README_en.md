# 📊 Comparative Study of Commercial Solvers for Orthogonal Array Generation

This repository contains the code, data, and documentation for the **Final Degree Project (TFG)** titled:

> **"Exploring the Efficiency of Commercial Solvers in Orthogonal Array Construction"**

The project aims to **compare different commercial and open-source solvers** (such as Gurobi, CPLEX, Hexaly, OR-Tools, among others) to solve the problem of **generating orthogonal arrays (OAs)** given their parameters \( N, k, s, t \). A common mathematical model will be implemented (preferably in Python) and adapted to each solver in order to evaluate them fairly across multiple dimensions.

## 🚀 Quickstart

Follow these steps to clone the repository, install dependencies, and run the application:

### 1. Clone the repository

```bash
git clone https://github.com/mikelmujika16/tfg-comparacion-solvers-OA.git
cd tfg-comparacion-solvers-OA
```

### 2. Create a virtual environment (optional but recommended)

To install the project's dependencies, it is recommended to create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate        # On Linux/macOS
venv\Scripts\activate           # On Windows
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Licenses for the Solvers

To use commercial solvers like Gurobi, CPLEX, and Hexaly, you will need to have a valid license. Check the documentation for each solver for information on how to obtain and configure licenses.

### 5. Run the application

From the root directory of the project, you can run the main script to generate and compare the orthogonal arrays:

```bash
python src/menu.py
```


## 📁 Repository Structure

```plaintext
tfg-comparacion-solvers-OA/
├── src/           # Python or Julia scripts for each solver
├── data/            # Input instances and raw results
├── figures/          # Exported plots and diagrams (PDF/PNG)
├── results/           # Benchmark results and metrics
│   └── oa_metrics.csv  # CSV file with performance metrics
├── memoria/          # LaTeX project exported from Overleaf
│   └── memtfg.tex    # Main document for the written report
├── plan.md           # Project plan and methodology
└── README.md         # This file
```

## 🧰 Technologies and Tools Used

- **Language:** Python 3.x
- **Mathematical Modeling:** Pyomo, Hexaly Python API, OR-tools Python API
- **Solvers:** Gurobi, CPLEX, Hexaly, OR-Tools, others
- **Visualization:** Matplotlib, Seaborn, Plotly
- **Documentation:** LaTeX (Overleaf), Markdown, GitHub

## ⚙️ Comparison Criteria

- ⏱️ **Performance** (execution time)
- 🧠 **Solution Quality** (orthogonality, coverage, completeness)
- ✍️ **Modeling Ease** (clarity and conciseness of the model)
- 📈 **Scalability** (performance with increasing problem size)
- 💸 **License and Cost**
- 🌐 **Other Factors** (community, documentation, integration, support)

## 📅 Project Timeline

See [plan.md](./plan.md) for project phases and target dates.

## 📜 License

This project is licensed under:

**Creative Commons BY-NC-ND 4.0 International**

> © This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

## ✍️ Author

**Mikel Mugica Arregui**  
Bachelor’s Degree in Computer Engineering  
University of La Laguna  
Supervisor: Juan José Salazar González
