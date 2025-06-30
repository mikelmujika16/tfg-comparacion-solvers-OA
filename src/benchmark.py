import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
df = pd.read_csv('../results/oa_metrics.csv', parse_dates=['timestamp'])


# Filtros deseados

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
plt.title("Comparación general de tiempos de cómputo para OAs")
plt.legend(title="Método")
plt.tight_layout()
plt.savefig('../figures/GlobalComparison.png')
plt.show()
