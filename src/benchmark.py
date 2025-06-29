import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
df = pd.read_csv('../results/oa_metrics.csv', parse_dates=['timestamp'])


# Filtros deseados
metodos_filtrados = [
    'gurobi_row_selection', 'gurobi_column_by_column'
]

oas_filtrados = [
    (128, 6, 4, 3),
    (256, 5, 4, 3),
    (512, 5, 8, 2),
    (512, 5, 8, 3)
]

# Aplicar filtros
df = df[df['method'].isin(metodos_filtrados)]
df = df[df.apply(lambda r: (r.N, r.k, r.s, r.t) in oas_filtrados, axis=1)]

# Etiqueta para OA
df['instance'] = df.apply(lambda r: f"OA({r.N},{r.k},{r.s},{r.t})", axis=1)

# Gráfico
plt.figure(figsize=(12, 6))
sns.barplot(
    data=df,
    x='instance',
    y='runtime_sec',
    hue='method',
    ci='sd',
    capsize=.2
)
plt.yscale('log')  # útil si hay valores muy grandes
plt.xlabel("Instancia (OA)")
plt.ylabel("Tiempo de cómputo (s)")
plt.title("Comparación de escalabilidad de selección de filas vs columna por columna con Gurobi")
plt.legend(title="Método")
plt.tight_layout()
plt.savefig('../figures/RS_vs_CbyC.png')
plt.show()
