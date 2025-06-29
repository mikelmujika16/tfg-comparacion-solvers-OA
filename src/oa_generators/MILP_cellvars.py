from pyomo.environ import *
from itertools import product, combinations
import numpy as np
import time

def generate_oa_cellvars(N, k, s, t, verbose=True, solver='gurobi'):
    λ = N // (s ** t)
    if N != s ** t * λ:
        if verbose:
            print(f"Parámetros inconsistentes: N = {N} ≠ s^t × λ = {s**t * λ}")
        return None, None

    model = ConcreteModel()

    I = range(N)
    J = range(k)
    V = range(s)
    COL_COMBOS = list(combinations(J, t))
    VAL_COMBOS = list(product(V, repeat=t))

    model.x = Var(I, J, V, domain=Binary)
    model.y = Var(I, COL_COMBOS, VAL_COMBOS, domain=Binary)

    model.assign_unique = Constraint(I, J, rule=lambda m, i, j: sum(m.x[i, j, v] for v in V) == 1)

    y_upper_index = [(i, *T, *a, m) for i in I for T in COL_COMBOS for a in VAL_COMBOS for m in range(t)]

    def upper_bound_y(model, i, *args):
        T = args[:t]
        a = args[t:2*t]
        m = args[-1]
        j = T[m]
        v = a[m]
        return model.y[i, T, a] <= model.x[i, j, v]

    model.y_upper = Constraint(y_upper_index, rule=upper_bound_y)

    y_lower_index = [(i, *T, a) for i in I for T in COL_COMBOS for a in VAL_COMBOS]

    def lower_bound_y(model, i, *args):
        T = args[:t]
        a = args[t:2*t]
        return model.y[i, T, a] >= sum(model.x[i, T[m], a[m]] for m in range(t)) - (t - 1)

    model.y_lower = Constraint(y_lower_index, rule=lower_bound_y)

    coverage_index = [(*T, *a) for T in COL_COMBOS for a in VAL_COMBOS]

    def coverage_rule(model, *args):
        T = args[:t]
        a = args[t:2*t]
        return sum(model.y[i, T, a] for i in I) == λ

    model.coverage = Constraint(coverage_index, rule=coverage_rule)

    model.fix_row_0 = Constraint(J, rule=lambda m, j: m.x[0, j, 0] == 1)

    
    FIRST_T_COLS = tuple(range(t))
    for a in VAL_COMBOS:
        model.add_component(
            f"first_t_cov_{a}",
            Constraint(expr=sum(model.y[i, FIRST_T_COLS, a] for i in I) == λ)
        )


    model.obj = Objective(expr=0)

    solver = SolverFactory(solver)
    try:
        start = time.time()
        solver.solve(model, tee=verbose)
        runtime = round(time.time() - start, 4)
    except Exception as e:
        if verbose:
            print(f"Error al resolver: {e}")
        return None, None

    oa_matrix = np.zeros((N, k), dtype=int)
    for i in I:
        for j in J:
            for v in V:
                if model.x[i, j, v].value > 0.5:
                    oa_matrix[i, j] = v
                    break

    return oa_matrix, runtime
