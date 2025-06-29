import sys
import os

from oa_utils import export_oa_to_csv, validate_oa_csv, oa_strength, log_oa_result, check_oa_existence
from oa_generators.MILP_row_selection import generate_oa_row_selection
from oa_generators.MILP_cellvars import generate_oa_cellvars
from oa_generators.MILP_column_by_column import generate_oa_with_backtracking
from oa_generators.ORT_row_selection import generate_row_ORT
from oa_generators.ORT_column_by_column import generate_oa_with_backtracking_ORT
from oa_generators.hexaly_column_by_column import generate_oa_hexaly_column_by_column
from oa_generators.hexaly_row_bool import generate_oa_row_selection_hexaly

import csv

def main_menu():
    while True:
        print("\n=== Orthogonal Array Toolkit ===")
        print("1. Generar OA")
        print("2. Validar OA desde archivo CSV")
        print("3. Existe OA con parametros específicos")
        print("4. Salir")
        choice = input("Elige opción [1/2/3/4]: ").strip()
        if choice == "1":
            generar_oa()
        elif choice == "2":
            validar_oa()
        elif choice == "3":
            check_existence()
        elif choice == "4":
            sys.exit(0)
        else:
            print("Opción no válida.")

def check_existence():
    k = int(input("k (columnas): "))
    s = int(input("s (símbolos por columna): "))
    t = int(input("t (fuerza): "))
    λ = int(input("λ (veces que debe aparecer cada t-tupla): "))
    N = λ * (s ** t)
    print(f"\n📐 Calculado: N = λ × s^t = {N}")
    check_oa_existence(N,k,s,t)
        

def generar_oa():
    instancias_predef = [
        (9, 4, 3, 2),
        (50, 5, 5, 2),
        (49, 4, 7, 2),
        (81, 4, 9, 2),
        (343, 5, 7, 2),
        (128, 6, 4, 3),
        (256, 5, 4, 3),
        (512, 5, 8, 2),
        (512, 5, 8, 3),
    ]

    print("\nSelecciona una instancia OA(N,k,s,t) predefinida o introduce parámetros manualmente:")
    for idx, (N, k, s, t) in enumerate(instancias_predef):
        print(f"{idx+1}. OA({N},{k},{s},{t})")
    print(f"{len(instancias_predef)+1}. Introducir parámetros manualmente")

    try:
        opcion = int(input("Elige una opción: "))
        if 1 <= opcion <= len(instancias_predef):
            N, k, s, t = instancias_predef[opcion - 1]
            λ = N // (s ** t)
        elif opcion == len(instancias_predef) + 1:
            k = int(input("k (columnas): "))
            s = int(input("s (símbolos por columna): "))
            t = int(input("t (fuerza): "))
            λ = int(input("λ (veces que debe aparecer cada t-tupla): "))
            N = λ * (s ** t)
            print(f"\n📐 Calculado: N = λ × s^t = {N}")
        else:
            print("⚠️ Opción no válida.")
            return
    except ValueError:
        print("⚠️ Entrada inválida. Introduce números enteros.")
        return

    print("\nMétodo de generación:")
    print("1. Gurobi (Selección de filas - MILP)")
    print("2. Gurobi (Variables de celda - MILP)")
    print("3. Gurobi (Columna por columna - MILP)")
    print("4. CPLEX (Selección de filas - MILP)")
    print("5. CPLEX (Columna por columna - MILP)")
    print("6. CBC (Selección de filas - MILP)")
    print("7. CBC (Columna por columna - MILP)")
    print("8. OR-Tools (Selección de filas)")
    print("9. OR-Tools (Columna por columna)")
    print("10. Hexaly (Selección de filas)")
    print("11. Hexaly (Columna por columns)")

    metodo = input("Elige método [1/2/3/4/5/6/7/8/9/10/11]: ").strip()

    if metodo == "1":
        oa, runtime = generate_oa_row_selection(N, k, s, t, verbose=True, solver='gurobi')
        metodo_nombre = "gurobi_row_selection"
    elif metodo == "2":
        oa, runtime = generate_oa_cellvars(N, k, s, t, verbose=True, solver='gurobi')
        metodo_nombre = "gurobi_cell_vars"
    elif metodo == "3":
        oa, runtime = generate_oa_with_backtracking(N, k, s, t, solver='gurobi')
        metodo_nombre = "gurobi_column_by_column"
    elif metodo == "4":
        oa, runtime = generate_oa_row_selection(N, k, s, t, verbose=True, solver='cplex')
        metodo_nombre = "cplex_row_selection"
    elif metodo == "5":
        oa, runtime = generate_oa_with_backtracking(N, k, s, t, solver='cplex')
        metodo_nombre = "cplex_column_by_column"
    elif metodo == "6":
        oa, runtime = generate_oa_row_selection(N, k, s, t, verbose=True, solver='cbc')
        metodo_nombre = "cbc_row_selection"
    elif metodo == "7":
        oa, runtime = generate_oa_with_backtracking(N, k, s, t, solver='cbc')
        metodo_nombre = "cbc_column_by_column"
    elif metodo == "8":
        oa, runtime = generate_row_ORT(N, k, s, t)
        metodo_nombre = "OR-Tools_row_selection"
    elif metodo == "9":
        oa, runtime = generate_oa_with_backtracking_ORT(N, k, s, t)
        metodo_nombre = "OR-Tools_column_by_column"
    elif metodo == "10":
        oa, runtime = generate_oa_row_selection_hexaly(N, k, s, t)
        metodo_nombre = "hexaly_row_selection"
    elif metodo == "11":
        oa, runtime = generate_oa_hexaly_column_by_column(N, k, s, t)
        metodo_nombre = "hexaly_column_by_column"
    else:
        print("⚠️ Método no válido.")
        return

    if oa is not None:
        mostrar = input("¿Mostrar OA generado? [s/N]: ").strip().lower()
        if mostrar == "s":
            print("\nOA generado:")
            for fila in oa:
                print(fila)

        fname = input(f"Nombre para exportar (defecto: oa_{N}_{k}_{s}_{t}_{metodo_nombre}.csv): ").strip()
        if not fname:
            fname = f"oa_{N}_{k}_{s}_{t}_{metodo_nombre}.csv"
        export_oa_to_csv(oa, fname)
        print(f"✅ OA exportado a 'data/{fname}' en {runtime} segundos.")

        # Validación y logging
        t_detected = oa_strength(oa)
        feasible = t_detected >= t
        log_oa_result(N, k, s, t, metodo_nombre, runtime, feasible, quality=None, notes="generado vía CLI")
    else:
        print("❌ No se pudo generar un OA para esos parámetros.")


def validar_oa():
    print("Archivos en la carpeta data/:")
    archivos = [f for f in os.listdir(os.path.join("..", "data")) if f.endswith(".csv")]
    if not archivos:
        print("No hay archivos CSV en data/.")
        return
    for idx, fname in enumerate(archivos):
        print(f"{idx+1}. {fname}")
    try:
        elec = int(input("Elige el número del archivo a validar: "))
        if 1 <= elec <= len(archivos):
            archivo = archivos[elec-1]
        else:
            print("Selección no válida.")
            return
    except ValueError:
        print("Selección no válida.")
        return
    mostrar = input("¿Mostrar OA cargado? [s/N]: ").strip().lower()
    if mostrar == "s":
        print("\nOA cargado:")
        with open(os.path.join("..", "data", archivo), newline='') as csvfile:
            reader = csv.reader(csvfile)
            for fila in reader:
                print(fila)
    validate_oa_csv(archivo)

if __name__ == "__main__":
    # Crear carpeta data si no existe
    os.makedirs(os.path.join("..", "data"), exist_ok=True)
    main_menu()
