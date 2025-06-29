from pyomo.environ import *
from itertools import product, combinations
import numpy as np
import time

def generate_oa_row_selection(N, k, s, t, verbose=True, solver='gurobi'):
    """
    Genera un Orthogonal Array usando Pyomo + Gurobi.
    Devuelve (OA_matrix, runtime_en_segundos) o (None, None) si no hay solución.
    """
    λ = N // (s ** t)
    if N != s ** t * λ:
        if verbose:
            print("Parámetros inconsistentes: N debe ser igual a s^t * λ.")
        return None, None

    # Generate all possible rows: s^k total
    ALL_ROWS = list(product(range(s), repeat=k))

    ROW_IDX = range(len(ALL_ROWS))

    # All t-subsets of columns
    COL_COMBOS = list(combinations(range(k), t))
    TUPLES = list(product(range(s), repeat=t))  # all t-tuples of symbols

    model = ConcreteModel()

    # Row decision variables
    model.x = Var(ROW_IDX, domain=Binary)

    # Constraint: for each t-combo of columns and each value tuple, λ appearances
    def orthogonality_rule(model, *args):
        cj = args[:t]
        vj = args[t:]

        matching_rows = [
            i for i, row in enumerate(ALL_ROWS)
            if tuple(row[j] for j in cj) == vj
        ]
        # Assert valid model (this should never trigger in full universe)
        if not matching_rows:
            raise ValueError(f"No rows match tuple {vj} in columns {cj} — model likely broken")
        
        return sum(model.x[i] for i in matching_rows) == λ

    model.orthogonality = Constraint(
        [(*cj, *vj) for cj in COL_COMBOS for vj in TUPLES],
        rule=orthogonality_rule
    )

    # Fix one row to break symmetry (e.g., first row always selected)
    model.fix_first = Constraint(expr=model.x[0] == 1)

    # Total number of selected rows must be N
    model.total_rows = Constraint(expr=sum(model.x[i] for i in ROW_IDX) == N)

    # --- New: Fix the first t columns with all possible t-tuples exactly once ---

    # For each t-tuple, find all rows where the first t columns equal that tuple
    first_t_tuple_rows = {
        v: [i for i, row in enumerate(ALL_ROWS) if tuple(row[:t]) == v]
        for v in TUPLES
    }

    # Constraint: each t-tuple appears exactly once in the first t columns
    def first_t_columns_rule(model, *v):
        return sum(model.x[i] for i in first_t_tuple_rows[v]) == λ

    model.first_t_columns_fixed = Constraint(TUPLES, rule=first_t_columns_rule)

    

    # Feasibility objective
    model.obj = Objective(expr=0)


    # Solver configuration
    solver = SolverFactory(solver)
    try:
        start = time.time()
        results = solver.solve(model, tee=verbose, load_solutions=True)
        model.solutions.load_from(results)
        end = time.time()
        runtime = round(end - start, 4)
    except Exception as e:
        if verbose:
            print(f"Error al resolver: {e}")
        return None, None

    # Extraer solución
    selected_rows = [i for i in ROW_IDX if model.x[i].value > 0.5]
    if verbose:
        print(f"Filas seleccionadas: {len(selected_rows)}")
        print(f"Tiempo de ejecución: {runtime} segundos")
    if len(selected_rows) != N:
        if verbose:
            print("No se seleccionó el número correcto de filas.")
        return None, None

    oa_matrix = np.array([ALL_ROWS[i] for i in selected_rows])
    return oa_matrix, runtime

