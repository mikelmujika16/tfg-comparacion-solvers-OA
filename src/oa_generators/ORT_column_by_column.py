import numpy as np
import time
from ortools.sat.python import cp_model
from itertools import combinations, product


def select_next_column_cp(fixed, s, t, λ, forbidden=None, timeout=30):
    model = cp_model.CpModel()
    N = fixed.shape[0]
    p = fixed.shape[1]
    col = [model.NewIntVar(0, s - 1, f"col_{i}") for i in range(N)]

    # One-hot encoding
    b = {}
    for i in range(N):
        for v in range(s):
            b[i, v] = model.NewBoolVar(f"b_{i}_{v}")
            model.Add(col[i] == v).OnlyEnforceIf(b[i, v])
            model.Add(col[i] != v).OnlyEnforceIf(b[i, v].Not())

    # Balance exacto
    for v in range(s):
        model.Add(sum(b[i, v] for i in range(N)) == N // s)

    # Ortogonalidad: cada combinación (t-1 fijas + nueva columna) aparece λ veces
    for idxs in combinations(range(p), t - 1):
        for prefix in product(range(s), repeat=t - 1):
            rows = [i for i in range(N) if tuple(fixed[i, list(idxs)]) == prefix]
            if not rows:
                continue
            for v in range(s):
                model.Add(sum(b[i, v] for i in rows) == λ)

    # Simmetry breaking
    model.Add(col[0] == 0)

    for i in range(s):
        model.Add(col[i] == i)

    # Forbidden columns
    if forbidden:
        for fcol in forbidden:
            model.AddBoolOr([b[i, fcol[i]].Not() for i in range(N)])

    # Heurística de decisión: fija primero las variables más restringidas con el menor valor posible
    model.AddDecisionStrategy(col,
                              cp_model.CHOOSE_FIRST,
                              cp_model.SELECT_MIN_VALUE)

    # Solver
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = timeout
    solver.parameters.num_search_workers = 8  # Ajustar según CPU

    status = solver.Solve(model)
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        return np.array([solver.Value(c) for c in col])
    return None


def backtrack_build(fixed, N, k, s, t, λ):
    p = fixed.shape[1]
    if p == k:
        return fixed
    print(f"Extendiendo con columnas... ({p} -> {k})")
    forbidden = []
    while True:
        newcol = select_next_column_cp(fixed, s, t, λ, forbidden)
        if newcol is None:
            return None
        candidate = np.hstack((fixed, newcol.reshape(-1, 1)))
        result = backtrack_build(candidate, N, k, s, t, λ)
        if result is not None:
            return result
        forbidden.append(newcol)
        print(f"Columna fallida (añadida a forb): {newcol}")


def generate_oa_with_backtracking_ORT(N, k, s, t):
    λ = N // (s ** t)
    if N != λ * (s ** t):
        raise ValueError("N debe ser múltiplo de s^t (N = λ·s^t)")

    base = np.array(list(product(range(s), repeat=t)))
    fixed = np.repeat(base, λ, axis=0)

    start = time.time()
    OA = backtrack_build(fixed, N, k, s, t, λ)
    runtime = round(time.time() - start, 4)

    if OA is None:
        raise RuntimeError("No se encontró OA factible.")
    return OA, runtime


