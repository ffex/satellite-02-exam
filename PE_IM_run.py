# ==========================================================
# PE_IM_run.py
# VERSIONE COMPLETA CON STAMPA RISULTATI + CSV
# ==========================================================

"""
Questo file esegue tutti gli esperimenti del Satellite Problem.

OBIETTIVO:
- Testare IDS e A*
- Confrontare euristiche
- Stampare risultati in console
- Salvare risultati in CSV

IMPORTANTE:
Alla fine richiamiamo print_results(results),
così i risultati tornano visibili.
"""

# ==========================================================
# IMPORT
# ==========================================================

from search import breadth_first_graph_search, breadth_first_tree_search, iterative_deepening_search, astar_search

from PE_IM_satellite import Satellite
from PE_IM_problems import *
from PE_IM_heuristics import *

import time
import csv


# ==========================================================
# SAFE HEURISTIC WRAPPER
# ==========================================================

def safe_heuristic(node, problem, heuristic):
    """
    Esegue l’euristica in modo sicuro.

    Se l’euristica genera errore:
    - stampa messaggio debug
    - restituisce 0

    Questo evita il crash di A*.
    """

    if heuristic is None:
        return 0

    try:
        return heuristic(node, problem)

    except Exception as e:
        print("[HEURISTIC ERROR]", e)
        return 0


# ==========================================================
# ESECUZIONE SINGOLO TEST
# ==========================================================

def run_experiment(problem_name,
                   problem_func,
                   heuristic=None,
                   algo="astar"):
    """
    Esegue un singolo esperimento.

    Parametri:
    - problem_name : nome problema
    - problem_func : funzione che genera initial, goal
    - heuristic    : euristica A*
    - algo         : ids oppure astar

    Restituisce:
    dict con statistiche finali
    """

    print("\n===================================")
    print("PROBLEM :", problem_name)
    print("ALGO    :", algo)
    print("===================================")

    # --------------------------------------------------
    # Generazione problema
    # --------------------------------------------------

    initial, goal = problem_func()

    print("DEBUG INITIAL:", initial)
    print("DEBUG GOAL   :", goal)

    # --------------------------------------------------
    # Creazione istanza Satellite
    # --------------------------------------------------

    problem = Satellite(initial, goal)

    # --------------------------------------------------
    # Timer start
    # --------------------------------------------------

    start = time.time()

    # --------------------------------------------------
    # IDS
    # --------------------------------------------------

    if algo == "ids":

        result = iterative_deepening_search(problem)

    # --------------------------------------------------
    # BD
    # --------------------------------------------------

    elif algo == "bfts":

        result = breadth_first_graph_search(problem)

    # --------------------------------------------------
    # A*
    # --------------------------------------------------

    elif algo == "astar":

        result = astar_search(
            problem,
            lambda n: safe_heuristic(n, problem, heuristic)
        )

    else:
        raise ValueError("Algoritmo non valido")

    # --------------------------------------------------
    # Timer stop
    # --------------------------------------------------

    end = time.time()

    elapsed = round(end - start, 5)

    # --------------------------------------------------
    # Statistiche base
    # --------------------------------------------------

    print("NODES GENERATED:", problem.nodes_generated)
    print("NODES EXPANDED :", problem.nodes_expanded)

    # --------------------------------------------------
    # Se trovata soluzione
    # --------------------------------------------------

    if result:

        solution = result.solution()

        print("DEPTH:", len(solution))
        print("COST :", result.path_cost)

        print("PLAN :")
        for step in solution:
            print("   ", step)

    else:

        solution = None

        print("RESULT = None")

    # --------------------------------------------------
    # Riga risultati
    # --------------------------------------------------

    return {
        "problem": problem_name,
        "algorithm": algo,
        "heuristic": heuristic.__name__ if heuristic else "None",
        "time": elapsed,
        "nodes_generated": problem.nodes_generated,
        "nodes_expanded": problem.nodes_expanded,
        "depth": len(solution) if solution else None,
        "cost": result.path_cost if result else None
    }


# ==========================================================
# STAMPA TABELLA RISULTATI
# ==========================================================

def print_results(results):
    """
    Stampa tutti i risultati finali.
    """

    print("\n\n=================================================")
    print("=============== RISULTATI FINALI ================")
    print("=================================================\n")

    for row in results:
        print(row)


# ==========================================================
# SALVATAGGIO CSV
# ==========================================================

def save_to_csv(results):
    """
    Salva i risultati nel file results.csv
    """

    with open("results.csv", "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "problem",
                "algorithm",
                "heuristic",
                "time",
                "nodes_generated",
                "nodes_expanded",
                "depth",
                "cost"
            ]
        )

        writer.writeheader()
        writer.writerows(results)


# ==========================================================
# MAIN
# ==========================================================

def main():
    """
    Esegue batteria completa test.
    """

    # --------------------------------------------------
    # Problemi
    # --------------------------------------------------

    problems = [
        ("easy", problem_easy),
        ("medium", problem_medium),
        ("hard", problem_hard),
        ("hard_HD", problem_hard_HD),
#        ("low_energy", variant_low_energy),
#        ("many_objects", variant_many_objects),
#        ("memory_stress", variant_memory_stress)
    ]

    # --------------------------------------------------
    # Euristiche
    # --------------------------------------------------

    heuristics_list = [h1,h2,h_max]

    # --------------------------------------------------
    # Lista risultati finali
    # --------------------------------------------------

    results = []

    # --------------------------------------------------
    # Loop principale
    # --------------------------------------------------

    for problem_name, prob in problems:

            # IDS
         results.append(
            run_experiment(
                problem_name,
                prob,
                algo="ids"
            )
         )
         results.append(
            run_experiment(
                problem_name,
                prob,
                algo="bfts"
            )
         )
            # A*
         for heuristic in heuristics_list:

            results.append(
                run_experiment(
                    problem_name,
                    prob,
                    heuristic=heuristic,
                    algo="astar"
                )
            )

    # --------------------------------------------------
    # OUTPUT FINALE
    # --------------------------------------------------

    print_results(results)

    save_to_csv(results)

    print("\nFile salvato: results.csv")


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()
