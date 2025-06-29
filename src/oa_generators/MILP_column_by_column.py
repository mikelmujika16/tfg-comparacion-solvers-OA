import numpy as np
import pyomo.environ as pyo
from itertools import combinations, product
import time

def select_next_column(fixed, s, t, λ, forbidden=None, solver='gurobi'):
    """
    Solve a MILP to construct one new column that extends the fixed array.
    
    Parameters:
    - fixed: np.array (N, p-1), current partial OA.
    - s: number of symbols.
    - t: strength.
    - λ: multiplicity factor (N = λ * s^t).
    - forbidden: list of previous column vectors to exclude.
    - solver: MILP solver (default 'gurobi').

    Returns:
    - newcol: np.array(N,) if feasible, otherwise None.
    """
    N, p_minus_1 = fixed.shape
    if forbidden is None:
        forbidden = []

    subsets = list(combinations(range(p_minus_1), t-1))
    classes = {}
    for u_idx, U in enumerate(subsets):
        block = fixed[:, U]  # (N, t-1)
        for v_fixed in product(range(s), repeat=t-1):
            rows = np.where((block == v_fixed).all(axis=1))[0]
            classes[(u_idx, v_fixed)] = rows

    model = pyo.ConcreteModel()
    model.I = pyo.RangeSet(0, N-1)
    model.V = pyo.RangeSet(0, s-1)
    model.x = pyo.Var(model.I, model.V, domain=pyo.Binary)

    model.one_symbol = pyo.Constraint(model.I,
        rule=lambda m,i: sum(m.x[i,v] for v in m.V) == 1)

    model.balance = pyo.Constraint(model.V,
        rule=lambda m,v: sum(m.x[i,v] for i in m.I) == N // s)

    model.first = pyo.Var(model.V, domain=pyo.NonNegativeIntegers, bounds=(0, N-1))
    model.first_pos = pyo.ConstraintList()
    for v in range(s):
        for i in range(N):
            model.first_pos.add(model.first[v] <= i + (1 - model.x[i, v]) * N)

    model.symmetry = pyo.ConstraintList()
    for v in range(s - 1):
        model.symmetry.add(model.first[v] <= model.first[v + 1] - 1)
    model.symmetry.add(model.x[0, 0] == 1)

    model.ortho = pyo.ConstraintList()
    for (u_idx, v_fixed), rows in classes.items():
        for v_new in range(s):
            model.ortho.add(
                sum(model.x[i, v_new] for i in rows) == λ
            )

    model.forbid = pyo.ConstraintList()
    for fcol in forbidden:
        model.forbid.add(sum(model.x[i, int(fcol[i])] for i in model.I) <= N - 1)

    model.obj = pyo.Objective(expr=0)

    sol = pyo.SolverFactory(solver).solve(model, tee=False)
    if sol.solver.termination_condition != pyo.TerminationCondition.optimal:
        return None

    newcol = np.zeros(N, dtype=int)
    for i in range(N):
        for v in range(s):
            if pyo.value(model.x[i, v]) > 0.5:
                newcol[i] = v
    return newcol

def backtrack_build(fixed, N, k, s, t, λ, solver='gurobi'):
    """
    Recursively attempts to extend a partially built OA to k columns.
    Returns the complete OA if successful, or None if failed.
    """
    p = fixed.shape[1]
    if p == k:
        return fixed

    print(f"Intentando extender con nuevas columnas... (fijas: {p}, objetivo: {k})")
    print("Fijas (filas):", [list(map(int, row)) for row in fixed])

    forbidden = []
    while True:
        newcol = select_next_column(fixed, s, t, λ, forbidden, solver)
        if newcol is None:
            return None

        candidate = np.hstack((fixed, newcol.reshape(-1,1)))
        result = backtrack_build(candidate, N, k, s, t, λ, solver)
        if result is not None:
            return result
        print("Columna fallida:", list(map(int, newcol)))
        forbidden.append(newcol)

def generate_oa_with_backtracking(N, k, s, t, solver='gurobi'):
    """
    Entrypoint for generating a complete OA using the column-by-column method.
    
    Parameters:
    - N: number of rows.
    - k: number of columns.
    - s: number of symbols.
    - t: strength.
    - solver: MILP solver to use.

    Returns:
    - OA as a NumPy array.
    """
    λ = N // (s ** t)
    if N != λ * (s ** t):
        raise ValueError("Parámetros incoherentes: N ≠ λ·s^t")

    base = np.array(list(product(range(s), repeat=t)))
    fixed = np.repeat(base, λ, axis=0)

    start = time.time()
    OA = backtrack_build(fixed, N, k, s, t, λ, solver)
    runtime = time.time() - start

    if OA is None:
        raise RuntimeError("No se encontró OA factible aunque con backtracking.")
    return OA, round(runtime, 4)
