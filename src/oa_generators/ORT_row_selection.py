from ortools.sat.python import cp_model
from itertools import product, combinations
from math import gcd
import time
import numpy as np

def generate_row_ORT(N, k, s, t, max_time=60, max_retries=5, debug=False):
    def compute_lambda(N, s, t):
        base = s ** t
        return N // base if N % base == 0 else None

    λ = compute_lambda(N, s, t)
    if λ is None:
        print("[ERROR] N no divisible por s^t. λ no entero.")
        return None

    t_tuples = list(product(range(s), repeat=t))
    col_combos = list(combinations(range(k), t))

    start = time.time()

    for attempt in range(max_retries):
        if debug:
            print(f"[TRY] Intento {attempt + 1}/{max_retries}")
        model = cp_model.CpModel()
        X = [[model.NewIntVar(0, s - 1, f"x_{i}_{j}") for j in range(k)] for i in range(N)]

        # Fijar las primeras s^t filas con cada t-tupla en las primeras t columnas
        if len(t_tuples) <= N:
            for idx, tup in enumerate(t_tuples):
                for rep in range(λ):
                    row = idx * λ + rep
                    if row < N:
                        for j in range(t):
                            model.Add(X[row][j] == tup[j])

        # Simetría adicional: primera fila todo ceros
        for j in range(k):
            model.Add(X[0][j] == 0)

        for cols in col_combos:
            coeffs = [s**p for p in reversed(range(t))]
            tuple_codes = []
            for i in range(N):
                code = model.NewIntVar(0, s**t - 1, f"code_{i}_{cols}")
                model.Add(code == sum(X[i][cols[j]] * coeffs[j] for j in range(t)))
                tuple_codes.append(code)

            for val in range(s**t):
                indicators = []
                for i in range(N):
                    b = model.NewBoolVar(f"b_{i}_{val}_{cols}")
                    model.Add(tuple_codes[i] == val).OnlyEnforceIf(b)
                    model.Add(tuple_codes[i] != val).OnlyEnforceIf(b.Not())
                    indicators.append(b)
                model.Add(sum(indicators) == λ)

        # Configurar solver
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 600
        solver.parameters.random_seed = attempt  # Cambia la búsqueda
        solver.parameters.num_search_workers = 8  # Usa multithreading

        status = solver.Solve(model)
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            if debug:
                print(f"[SUCCESS] Solución encontrada.")
            runtime = time.time() - start
            oa_matrix = np.array([[solver.Value(X[i][j]) for j in range(k)] for i in range(N)])
            print(f"[SUCCESS] Solución encontrada en {runtime:.2f} s.")
            return oa_matrix, runtime

    print("[FAIL] No se encontró solución tras múltiples intentos.")
    return None, None
