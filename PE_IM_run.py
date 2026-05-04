# ==========================================================
# PE_IM_run.py
# ==========================================================

from search import (
    breadth_first_graph_search,
    iterative_deepening_search,
    astar_search,
    uniform_cost_search,
    depth_limited_search
)

from PE_IM_satellite import Satellite
from PE_IM_problems import *
from PE_IM_heuristics import *

import time
import csv
import signal


# Questi parametri servono per id, per non fare andare in loop all'infinito
IDS_MAX_DEPTH = 100
TIME_LIMIT = 300

class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException()


def run_with_timeout(func, timeout, *args):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)

    try:
        return func(*args)
    except TimeoutException:
        print("[TIMEOUT] algoritmo interrotto")
        return None
    finally:
        signal.alarm(0)


# Per motivi di compilazione, facciamo un wrapper dell'euristiche
def safe_heuristic(node, problem, h):
    if h is None:
        return 0
    try:
        return h(node, problem)
    except:
        return 0


# Eseguiamo i problemi, uno alla volta, di tutti gli scenari, con i vari algoritmi
def run_experiment(problem_name, problem_fn, algo="astar", heuristic=None):

    print("\n==================================================")
    print(f"PROBLEMA   : {problem_name}")
    print(f"ALGORITMO  : {algo}")
    print(f"EURISTICA  : {heuristic.__name__ if heuristic else 'None'}")
    print("==================================================")

    initial, goal = problem_fn()
    problem = Satellite(initial, goal)

    start_time = time.time()
    result = None

    try:

        match algo:

            # ---------------- IDS ----------------
            case "ids":
                print("[IDS] ricerca iterativa")
                result = run_with_timeout(
                    iterative_deepening_search,
                    TIME_LIMIT,
                    problem
                )

            # ---------------- BFS ----------------
            case "bfts":
                print("[BFS] ricerca in ampiezza")
                result = breadth_first_graph_search(problem)

            # ---------------- UCS ----------------
            case "ucs":
                print("[UCS] costo uniforme")
                result = uniform_cost_search(problem)

            # ---------------- DLS ----------------
            case "dls":
                print("[DLS] profondità limitata")
                result = depth_limited_search(problem, IDS_MAX_DEPTH)

            # ---------------- A* ----------------
            case "astar":
                print("[A*] ricerca informata")
                result = astar_search(
                    problem,
                    lambda n: safe_heuristic(n, problem, heuristic)
                )

            case _:
                raise ValueError("Algoritmo non valido")

    except Exception as e:
        print("[ERROR]", e)
        result = None

    elapsed = round(time.time() - start_time, 5)

    # Se non c'è soluzione
    if not result:
        print("\nRISULTATO: FALLIMENTO / NESSUNA SOLUZIONE")

        return {
            "problem": problem_name,
            "algorithm": algo,
            "heuristic": heuristic.__name__ if heuristic else "None",
            "time": elapsed,
            "nodes_generated": problem.nodes_generated,
            "nodes_expanded": problem.nodes_expanded,
            "depth": None,
            "cost": None,
            "branching_factor": None,
            "efficiency": None,
            "depth_ratio": None
        }

    # Se la trovo, la salvo
    solution = result.solution()

    print("\nSOLUZIONE TROVATA")

    print("\nSEQUENZA AZIONI:")
    for i, action in enumerate(solution, 1):
        print(f"{i:02d}. {action}")

    # Stampo le statistiche
    print("\nSTATISTICHE:")
    print("DEPTH:", len(solution))
    print("COST :", result.path_cost)

    nodes_generated = problem.nodes_generated
    nodes_expanded = problem.nodes_expanded

    return {
        "problem": problem_name,
        "algorithm": algo,
        "heuristic": heuristic.__name__ if heuristic else "None",
        "time": elapsed,
        "nodes_generated": nodes_generated,
        "nodes_expanded": nodes_expanded,
        "depth": len(solution),
        "cost": result.path_cost,
        "branching_factor": nodes_generated / nodes_expanded if nodes_expanded else 0,
        "efficiency": nodes_expanded / elapsed if elapsed else 0,
        "depth_ratio": len(solution) / result.path_cost if result.path_cost else None
    }


# Stampe dei risultati
def print_results(results):
    print("\n================= RISULTATI FINALI =================\n")
    for r in results:
        print(r)

# Stampe nel .csv
def save_csv(results):
    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


# Punto di ingressa
def main():
    # I problemi
    problems = [
        ("easy", problem_easy),
        ("medium", problem_medium),
        ("hard", problem_hard),
        ("hard_HD", problem_hard_HD),
    ]
    # Le euristiche
    heuristics = [h1, h2, h3, h4, h_max]

    results = []

    for name, fn in problems:
        results.append(run_experiment(name, fn, "ids"))
        results.append(run_experiment(name, fn, "bfts"))
        results.append(run_experiment(name, fn, "ucs"))
        results.append(run_experiment(name, fn, "dls"))

        for h in heuristics:
            results.append(run_experiment(name, fn, "astar", h))

    print_results(results)
    save_csv(results)

    print("\nFile CSV salvato correttamente")


if __name__ == "__main__":
    main()