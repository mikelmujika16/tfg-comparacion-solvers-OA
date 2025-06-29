from pyomo.environ import *
from itertools import product, combinations
import numpy as np
import time
import hexaly.optimizer

def generate_oa_row_selection_hexaly(N, k, s, t, verbose=True):
    """
    Genera un Orthogonal Array usando Pyomo + Gurobi.
    Devuelve (OA_matrix, runtime_en_segundos) o (None, None) si no hay solución.
    """
    λ = N // (s ** t)
    if N != s ** t * λ:
        if verbose:
            print("Parámetros inconsistentes: N debe ser igual a s^t * λ.")
        return None, None
    
    with hexaly.optimizer.HexalyOptimizer() as optimizer:

        model = optimizer.model

        ALL_ROWS = list(product(range(s), repeat=k))
        ROW_IDX = range(len(ALL_ROWS))
        COL_COMBOS = list(combinations(range(k), t))
        TUPLES = list(product(range(s), repeat=t))
        
        rows = [model.bool() for _ in ROW_IDX]

        model.constraint(model.sum(rows[i] for i in ROW_IDX) == N)
        
        for column_combo in COL_COMBOS:
            for s_tuple in TUPLES:
                matching_rows = [
                    i for i, row in enumerate(ALL_ROWS)
                    if tuple(row[column] for column in column_combo) == s_tuple
                ]
                model.constraint(model.sum(rows[i] for i in matching_rows) == λ)

        # Rompimiento de simetría: fijar la primera fila (0,0,...,0)
        model.constraint(rows[0] == 1)
               

        # Factibilidad: sin objetivo real
        model.minimize(0)
        model.close()

        start = time.time()
        optimizer.solve()
        end = time.time()
        runtime = end - start

        if optimizer.solution.status in [hexaly.optimizer.HxSolutionStatus.FEASIBLE, hexaly.optimizer.HxSolutionStatus.OPTIMAL]:
            selected = [i for i in ROW_IDX if rows[i].value > 0.5]
            oa_matrix = np.array([ALL_ROWS[i] for i in selected], dtype=int)
            if verbose:
                print("OA found:")
                print(oa_matrix)
            

        return oa_matrix, runtime



