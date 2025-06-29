import hexaly.optimizer
from itertools import product, combinations

# Parameters for the Orthogonal Array
N = 343       # number of rows
k = 5         # number of columns
s = 7         # number of symbols
t = 2         # strength
λ = N // (s ** t)

with hexaly.optimizer.HexalyOptimizer() as optimizer:
    
    model = optimizer.model

    ALL_ROWS = list(product(range(s), repeat=k))
    ROW_IDX = range(len(ALL_ROWS))
    COL_COMBOS = list(combinations(range(k), t))
    TUPLES = list(product(range(s), repeat=t))

    rows = model.set(len(ALL_ROWS))

    model.constraint(model.count(rows) == N)

    for cj in COL_COMBOS:
        for vj in TUPLES:
            contributions = model.array([tuple(row[col] for col in cj) == vj for row in ALL_ROWS])
            model.constraint(
                model.sum(rows, model.lambda_function(lambda i: contributions[i])) == λ
            )

    # Symmetry breaking: first row is all zeros
    
    
    model.minimize(0)
    model.close()

    optimizer.solve()

    if optimizer.solution.status in [hexaly.optimizer.HxSolutionStatus.FEASIBLE, hexaly.optimizer.HxSolutionStatus.OPTIMAL]:
        print("Solution found:")
        print([var for var in rows.value])
        print("Orthogonal Array:")
        oa_matrix = [[ALL_ROWS[i][j] for j in range(k)] for i in rows.value]
        for row in oa_matrix:
            print(row) 

    