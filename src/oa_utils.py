import os
import csv
import numpy as np
from itertools import combinations, product
import time
import pandas as pd
import oapackage

def check_oa_existence(N,k,s,t):
    level_vector = [s] * k
    
    array_class = oapackage.arraydata_t(level_vector,N,t,k)

    root = array_class.create_root()
    current_list = [root]


    for _ in range(k-t):
        current_list = oapackage.extend_arraylist(current_list, array_class)
        print(current_list)
        if len(current_list) == 0:
            print(f"No OA({N}, {k}, {s}, {t}) exists")
            return False
        
    print(f"OA({N}, {k}, {s}, {t}) exists! Found {len(current_list)} arrays")
    return True   

def log_oa_result(N, k, s, t, method, runtime, feasible, quality=None, notes="", filename="oa_metrics.csv"):
    """
    Guarda un registro de resultados de generación OA en results/oa_metrics.csv.
    Crea el archivo si no existe y evita duplicados por clave (N,k,s,t,method).
    """
    results_dir = os.path.join("..", "results")
    os.makedirs(results_dir, exist_ok=True)
    file_path = os.path.join(results_dir, filename)

    # Estructura del nuevo resultado
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "N": N,
        "k": k,
        "s": s,
        "t": t,
        "method": method,
        "runtime_sec": round(runtime, 4),
        "feasible": feasible,
        "quality": quality,
        "notes": notes
    }

    # Si el archivo existe, cargarlo para evitar duplicados
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        is_duplicate = ((df["N"] == N) & (df["k"] == k) & (df["s"] == s) &
                        (df["t"] == t) & (df["method"] == method)).any()
        if is_duplicate:
            print(f"[log_oa_result] Resultado duplicado (N={N}, k={k}, s={s}, t={t}, method={method}), no se guarda.")
            return
    else:
        df = pd.DataFrame()

    # Agregar nueva fila
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(file_path, index=False)
    print(f"[log_oa_result] Resultado registrado en {file_path}")

def export_oa_to_csv(oa_matrix, filename="oa_output.csv"):
    """
    Exporta una matriz OA a un archivo CSV dentro de la carpeta ../data/.
    Si la carpeta no existe, la crea automáticamente.
    """
    output_dir = os.path.join("..", "data")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)

    # Convierte a lista de listas si es array de NumPy
    if isinstance(oa_matrix, np.ndarray):
        data = oa_matrix.tolist()
    else:
        data = oa_matrix

    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    print(f"OA exportada a '{file_path}'")

def load_oa_csv(filename):
    """
    Carga una matriz OA desde un CSV (busca siempre en data/).
    Devuelve un array NumPy.
    """
    file_path = os.path.join("..", "data", filename)
    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        oa = np.array([list(map(int, row)) for row in reader])
    return oa

def oa_strength(oa):
    """
    Detecta la fuerza máxima t para la que la matriz oa es un Orthogonal Array.
    """
    N, k = oa.shape
    s = len(set(oa.flatten()))
    max_t = k
    found_t = 0
    for t in range(1, k + 1):
        λ_expected = N // (s ** t)
        if N != s ** t * λ_expected:
            break  # No puede tener fuerza t
        valid = True
        for cols in combinations(range(k), t):
            count = {}
            for row in oa:
                key = tuple(row[i] for i in cols)
                count[key] = count.get(key, 0) + 1
            for val in product(range(s), repeat=t):
                if count.get(val, 0) != λ_expected:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            found_t = t
        else:
            break
    return found_t

def validate_oa_csv(filename):
    """
    Valida un archivo CSV de OA (buscando siempre en data/).
    Imprime dimensiones, símbolos, fuerza máxima y si es OA válida.
    """
    oa = load_oa_csv(filename)
    N, k = oa.shape
    s = len(set(oa.flatten()))
    t = oa_strength(oa)
    print(f"Dimensiones OA: N = {N}, k = {k}, símbolos distintos s = {s}")
    print(f"Fuerza t máxima detectada: {t}")
    if t > 0:
        print(f"La matriz es una OA válida de fuerza t = {t}.")
    else:
        print("La matriz NO es una OA válida (no cumple fuerza t >= 1).")
