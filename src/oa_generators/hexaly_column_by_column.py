import numpy as np
from itertools import combinations, product
import time
import hexaly.optimizer


def select_next_column_hexaly(fixed, s, t, λ, forbidden=None, time_limit=10, verbose=False):
    """
    Construye una nueva columna que extiende una matriz OA parcial 'fixed',
    fijando además un orden lexicográfico en la propia columna.
    """
    N, p_minus_1 = fixed.shape
    if forbidden is None:
        forbidden = []

    # Pre-cálculo de las "clases" para ortogonalidad
    subsets = list(combinations(range(p_minus_1), t - 1))
    classes = {}
    for U in subsets:
        block = fixed[:, U]
        for v_fixed in product(range(s), repeat=t - 1):
            rows = np.where((block == v_fixed).all(axis=1))[0]
            classes[(U, v_fixed)] = rows

    with hexaly.optimizer.HexalyOptimizer() as optimizer:
        model = optimizer.model

        # 1) Variables enteras: nueva columna
        new_col_vars = [model.int(0, s - 1) for _ in range(N)]
        new_col      = model.array(new_col_vars)

        # 2) Balance global: cada símbolo v aparece N/s veces
        for v in range(s):
            model.constraint(
                model.sum(new_col[i] == v for i in range(N))
                == N // s
            )

        # 3) Simetría lexicográfica en la nueva columna:
        #    first[v] = índice de la PRIMERA aparición de v en new_col
        first = [model.int(0, N-1) for _ in range(s)]
        for v in range(s):
            for i in range(N):
                eq_v = model.eq(new_col[i], v)
                # Si new_col[i]==v ⇒ first[v] ≤ i
                # Si new_col[i]!=v ⇒ first[v] ≤ i+N (no lo restringe)
                model.constraint(
                    first[v] <= i + (1 - eq_v) * N
                )
        # Impongo first[0] < first[1] < ... < first[s-1]
        for v in range(s - 1):
            model.constraint(
                first[v] <= first[v+1] - 1
            )

        # 4) Ortogonalidad: para cada clase (u_idx,v_fixed), contamos v_new
        for rows in classes.values():
            for v_new in range(s):
                model.constraint(
                    model.sum(new_col[i] == v_new for i in rows)
                    == λ
                )

        # 5) Evitar columnas previamente probadas
        for fcol in forbidden:
            # sum_i [new_col[i] == fcol[i]] ≤ N-1
            model.constraint(
                model.sum(new_col[i] == int(fcol[i]) for i in range(N))
                <= N - 1
            )

        # 6) Objetivos lexicográficos: minimizar new_col[0], luego new_col[1], …
        #    de modo que la solución sea la mínima en orden lex.
        #for i in range(N):
            #model.minimize(new_col[i])
        model.minimize(model.create_constant(0))
        model.close()

        # 7) Parámetros y resolución
        optimizer.param.time_limit = time_limit
        optimizer.param.verbosity  = 1 if verbose else 0
        optimizer.solve()

        # 8) Lectura de la solución
        status = optimizer.solution.status
        if status in (hexaly.optimizer.HxSolutionStatus.FEASIBLE,
                      hexaly.optimizer.HxSolutionStatus.OPTIMAL):
            return np.array([v.value for v in new_col_vars], dtype=int)
        else:
            return None

def backtrack_build_hexaly(fixed, N, k, s, t, λ, time_limit=10):
    """
    Construye recursivamente un OA por método de generación columna a columna.
    """
    p = fixed.shape[1]
    if p == k:
        return fixed

    print(f"Intentando extender... columnas actuales: {p}/{k}")
    forbidden = []

    while True:
        new_col = select_next_column_hexaly(fixed, s, t, λ, forbidden, time_limit)
        if new_col is None:
            return None
        candidate = np.hstack((fixed, new_col.reshape(-1, 1)))
        result = backtrack_build_hexaly(candidate, N, k, s, t, λ, time_limit)
        if result is not None:
            return result
        print("Backtracking: columna fallida", list(map(int, new_col)))
        forbidden.append(new_col)


def generate_oa_hexaly_column_by_column(N, k, s, t, time_limit=1000):
    """
    Punto de entrada principal para generar un OA con Hexaly y backtracking.
    """
    λ = N // (s ** t)
    if N != λ * (s ** t):
        raise ValueError("Parámetros incoherentes: N ≠ λ·s^t")

    base = np.array(list(product(range(s), repeat=t)))
    fixed = np.repeat(base, λ, axis=0)

    start = time.time()
    OA = backtrack_build_hexaly(fixed, N, k, s, t, λ, time_limit)
    runtime = time.time() - start

    if OA is None:
        raise RuntimeError("No se encontró OA factible.")
    return OA, round(runtime, 4)


