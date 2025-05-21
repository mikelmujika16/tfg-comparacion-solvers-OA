# 📊 Comparative Study of Commercial Solvers for Orthogonal Array Generation

This repository contains the code, data, and documentation for the **Final Degree Project (TFG)** titled:

> **"Exploring the Efficiency of Commercial Solvers in Orthogonal Array Construction"**

The project aims to **compare different commercial and open-source solvers** (such as Gurobi, CPLEX, Hexaly, OR-Tools, among others) to solve the problem of **generating orthogonal arrays (OAs)** given their parameters \( N, k, s, t \). A common mathematical model will be implemented (preferably in Python) and adapted to each solver in order to evaluate them fairly across multiple dimensions.

## 📁 Repository Structure

```plaintext
tfg-comparacion-solvers-OA/
├── src/           # Python or Julia scripts for each solver
├── data/            # Input instances and raw results
├── figuras/          # Exported plots and diagrams (PDF/PNG)
├── tablas/           # LaTeX or CSV tables for the written report
├── memoria/          # LaTeX project exported from Overleaf
│   └── memtfg.tex    # Main document for the written report
├── plan.md           # Project plan and methodology
└── README.md         # This file
```

## 🧰 Technologies and Tools Used

- **Language:** Python 3.x
- **Mathematical Modeling:** PuLP, Pyomo, JuMP (depending on solver)
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
