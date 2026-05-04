# ==========================================================
# PE_IM_run.py (FINAL ROBUST + STATUS HANDLING)
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


# ==========================================================
# PARAMETRI GLOBALI
# ==========================================================
IDS_MAX_DEPTH = 100
TIME_LIMIT = 20
NODE_LIMIT = 50000


# ==========================================================
# TIMEOUT LEGACY (IDS compat)
# ==========================================================
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


# ==========================================================
# WRAPPER SAFE UNIVERSALE
# ==========================================================
def run_limited_search(search_fn, problem, time_limit=10, node_limit=None, *args):

    start = time.time()

    try:
        result = search_fn(problem, *args)

    except Exception as e:
        print("[ERROR SEARCH]", e)
        return None

    elapsed = time.time() - start

    # -------------------------
    # TIME LIMIT
    # -------------------------
    if time_limit is not None and elapsed > time_limit:
        print("[TIME LIMIT] superato")
        return None

    # -------------------------
    # NODE LIMIT
    # -------------------------
    if node_limit is not None and hasattr(problem, "nodes_expanded"):
        if problem.nodes_expanded > node_limit:
            print("[NODE LIMIT] superato")
            return None

    return result


# ==========================================================
# EURISTICA SICURA
# ==========================================================
def safe_heuristic(node, problem, h):
    if h is None:
        return 0
    try:
        return h(node, problem)
    except Exception:
        return 0


# ==========================================================
# FORMAT AZIONI
# ==========================================================
def format_actions(solution, max_len=20):

    if not solution:
        return "()"

    actions = [str(a) for a in solution]

    if len(actions) > max_len:
        actions = actions[:max_len] + ["..."]

    return "(" + ", ".join(actions) + ")"


# ==========================================================
# RUN EXPERIMENT
# ==========================================================
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

        # ==================================================
        # IDS
        # ==================================================
        if algo == "ids":
            print("[IDS] ricerca iterativa")

            result = run_limited_search(
                iterative_deepening_search,
                problem,
                TIME_LIMIT
            )

        # ==================================================
        # BFS
        # ==================================================
        elif algo == "bfts":
            print("[BFS] ricerca in ampiezza")

            result = run_limited_search(
                breadth_first_graph_search,
                problem,
                TIME_LIMIT
            )

        # ==================================================
        # UCS
        # ==================================================
        elif algo == "ucs":
            print("[UCS] costo uniforme")

            result = run_limited_search(
                uniform_cost_search,
                problem,
                TIME_LIMIT
            )

        # ==================================================
        # DLS
        # ==================================================
        elif algo == "dls":
            print("[DLS] profondità limitata")

            result = run_limited_search(
                depth_limited_search,
                problem,
                TIME_LIMIT,
                None,
                IDS_MAX_DEPTH
            )

        # ==================================================
        # A*
        # ==================================================
        elif algo == "astar":
            print("[A*] ricerca informata")

            result = run_limited_search(
                astar_search,
                problem,
                TIME_LIMIT,
                None,
                lambda n: safe_heuristic(n, problem, heuristic)
            )

        else:
            raise ValueError("Algoritmo non valido")

    except Exception as e:
        print("[ERROR RUN]", e)
        result = None

    elapsed = round(time.time() - start_time, 5)

    # ==================================================
    # CASO 1: FAILURE TECNICO
    # ==================================================
    if result is None:
        print("\nFAILURE TECNICO (timeout / crash / errore)")

        return {
            "problem": problem_name,
            "algorithm": algo,
            "heuristic": heuristic.__name__ if heuristic else "None",
            "time": elapsed,
            "nodes_generated": problem.nodes_generated,
            "nodes_expanded": problem.nodes_expanded,
            "depth": None,
            "cost": None,
            "status": "FAILURE",
            "actions": "()"
        }

    # ==================================================
    # CASO 2: RISULTATO NON VALIDO
    # ==================================================
    if not hasattr(result, "solution"):
        print("\nFAILURE TECNICO (tipo risultato invalido)")

        return {
            "problem": problem_name,
            "algorithm": algo,
            "heuristic": heuristic.__name__ if heuristic else "None",
            "time": elapsed,
            "nodes_generated": problem.nodes_generated,
            "nodes_expanded": problem.nodes_expanded,
            "depth": None,
            "cost": None,
            "status": "FAILURE",
            "actions": "()"
        }

    solution = result.solution()

    # ==================================================
    # CASO 3: NO SOLUTION
    # ==================================================
    if solution is None or len(solution) == 0:
        print("\nNO SOLUTION (search completata senza goal)")

        return {
            "problem": problem_name,
            "algorithm": algo,
            "heuristic": heuristic.__name__ if heuristic else "None",
            "time": elapsed,
            "nodes_generated": problem.nodes_generated,
            "nodes_expanded": problem.nodes_expanded,
            "depth": 0,
            "cost": 0,
            "status": "NO_SOLUTION",
            "actions": "()"
        }

    # ==================================================
    # CASO 4: SUCCESSO
    # ==================================================
    actions_str = format_actions(solution)

    print("\nSOLUZIONE TROVATA")

    print("\nSEQUENZA AZIONI:")
    for i, action in enumerate(solution, 1):
        print(f"{i:02d}. {action}")

    print("\nSTATISTICHE:")
    print("DEPTH:", len(solution))
    print("COST :", result.path_cost)

    return {
        "problem": problem_name,
        "algorithm": algo,
        "heuristic": heuristic.__name__ if heuristic else "None",
        "time": elapsed,
        "nodes_generated": problem.nodes_generated,
        "nodes_expanded": problem.nodes_expanded,
        "depth": len(solution),
        "cost": result.path_cost,
        "status": "SUCCESS",
        "actions": actions_str
    }


# ==========================================================
# OUTPUT
# ==========================================================
def print_results(results):
    print("\n================= RISULTATI FINALI =================\n")
    for r in results:
        print(r)


# ==========================================================
# CSV EXPORT
# ==========================================================
def save_csv(results):
    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


# ==========================================================
# MAIN
# ==========================================================
def main():

    problems = [
        ("easy", problem_easy),
        ("medium", problem_medium),
        ("hard", problem_hard),
        ("hard_HD", problem_hard_HD),
    ]

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


# ==========================================================
# ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    main()