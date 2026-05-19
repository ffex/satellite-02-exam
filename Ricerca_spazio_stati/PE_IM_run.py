"""
ORCHESTRATORE DEGLI ESPERIMENTI — PROBLEMA DEL SATELLITE

Questo file si occupa di eseguire tutti gli algoritmi di ricerca
su tutti i problemi definiti in PE_IM_problems.py, raccogliere
i risultati e salvarli in un file CSV per l'analisi comparativa.

STRUTTURA GENERALE:
    main()
      └── per ogni problema (easy, medium, hard, hard_HD, extreme)
            ├── IDS   — ricerca iterativa in profondità
            ├── BFS   — ricerca in ampiezza (graph search)
            ├── UCS   — costo uniforme
            ├── DLS   — profondità limitata (limite = IDS_MAX_DEPTH)
            └── A*    — con ognuna delle euristiche:
                        h1, h2, h3, h4, h_energy, h_memory, h_max

FUNZIONI PRINCIPALI:
    run_experiment(problem_name, problem_fn, algo, heuristic)
        Esegue un singolo esperimento e restituisce un dizionario
        con tutte le metriche: tempo, nodi, profondità, costo, status.

    run_limited_search(search_fn, problem, time_limit, node_limit, *args)
        Wrapper che chiama la funzione di ricerca AIMA e verifica
        i limiti di tempo e nodi DOPO la terminazione.
        Nota: il controllo interno avviene tramite Satellite.stopped().

    safe_heuristic(node, problem, h)
        Chiama l'euristica in modo sicuro: se h è None o lancia
        un'eccezione, restituisce 0 (comportamento UCS).

    format_actions(solution, max_len)
        Formatta la sequenza di azioni per la stampa e il CSV,
        troncando con "..." se la soluzione supera max_len passi.

GESTIONE DEI RISULTATI:
    Ogni esperimento restituisce uno tra tre status:
        SUCCESS    — soluzione trovata, metriche complete
        NO_SOLUTION — ricerca terminata senza trovare il goal
        FAILURE    — timeout, node limit superato, o crash

"""

import sys
import os
import subprocess
import shutil
from pathlib import Path


def _find_python_312():
    # 1) py.exe -3.12 (Windows launcher)
    py = shutil.which("py.exe") or shutil.which("py")
    if py:
        try:
            r = subprocess.run(
                [py, "-3.12", "-c", "import sys; print(sys.executable)"],
                capture_output=True, text=True, timeout=5,
            )
            if r.returncode == 0:
                exe = r.stdout.strip()
                if exe and Path(exe).exists():
                    return exe
        except Exception:
            pass

    # 2) percorsi standard Windows / Unix
    candidates = [
        Path.home() / "AppData" / "Local" / "Programs" / "Python" / "Python312" / "python.exe",
        Path.home() / "AppData" / "Roaming" / "Python" / "Python312" / "python.exe",
        Path("C:/Python312/python.exe"),
        Path("C:/Program Files/Python312/python.exe"),
        Path("/usr/bin/python3.12"),
        Path("/usr/local/bin/python3.12"),
    ]
    for c in candidates:
        if c.exists():
            return str(c)

    return None


if sys.version_info[:2] != (3, 12):
    _py312 = _find_python_312()
    if _py312:
        print(f"[INFO] interprete corrente: Python {sys.version_info.major}.{sys.version_info.minor}")
        print(f"[INFO] re-exec con Python 3.12: {_py312}")
        result = subprocess.run([_py312, __file__, *sys.argv[1:]])
        sys.exit(result.returncode)
    else:
        print(f"[WARN] Python 3.12 non trovato, proseguo con {sys.version.split()[0]}")


from search import (
    breadth_first_graph_search,
    iterative_deepening_search,
    astar_search,
    uniform_cost_search,
    depth_limited_search
)

from PE_IM_satellite import Satellite
from PE_IM_problems import (
    problem_easy,
    problem_medium,
    problem_hard,
    problem_hard_HD,
    problem_extreme,
)
from PE_IM_heuristics import h1, h2, h3, h4, h_energy, h_memory, h_max

import csv
import signal
import time


# ==========================================================
# PARAMETRI GLOBALI
# ==========================================================
IDS_MAX_DEPTH  = 300
TIME_LIMIT     = 20
NODE_LIMIT     = 30000
IDS_NODE_LIMIT = 50000     # IDS e' esponenziale: limite piu' largo


class TimeoutException(Exception):
    pass


# signal.SIGALRM esiste solo su UNIX. Su Windows i timeout
# vengono gestiti dal solo controllo nodes_expanded interno.
HAS_SIGALRM = hasattr(signal, "SIGALRM")


def _timeout_handler(signum, frame):
    raise TimeoutException()



# WRAPPER SAFE UNIVERSALE
def run_limited_search(search_fn, problem, time_limit=10, node_limit=None, *args):

    start = time.time()

    try:
        result = search_fn(problem, *args)

    except Exception as e:
        print("[ERROR SEARCH]", e)
        return None

    elapsed = time.time() - start

    if time_limit is not None and elapsed > time_limit:
        print("[TIME LIMIT] superato")
        return None

    if node_limit is not None and hasattr(problem, "nodes_expanded"):
        if problem.nodes_expanded > node_limit:
            print("[NODE LIMIT] superato")
            return None

    return result


# Gestione euristica
def safe_heuristic(node, problem, h):
    if h is None:
        return 0
    try:
        return h(node, problem)
    except Exception:
        return 0


# Azioni definite come soluzione in .CVS
def format_actions(solution, max_len=20):
    if not solution:
        return "()"
    actions = [str(a) for a in solution]
    if len(actions) > max_len:
        actions = actions[:max_len] + ["..."]
    return "(" + ", ".join(actions) + ")"


# Funzione che esegue i test con gli algoritmi
def run_experiment(problem_name, problem_fn, algo="astar", heuristic=None):

    print("\n==================================================")
    print(f"PROBLEMA   : {problem_name}")
    print(f"ALGORITMO  : {algo}")
    print(f"EURISTICA  : {heuristic.__name__ if heuristic else 'None'}")
    print("==================================================")

    initial, goal = problem_fn()

    # IDS usa un node limit più alto per dare una chance ai problemi complessi
    n_limit = IDS_NODE_LIMIT if algo == "ids" else NODE_LIMIT
    problem = Satellite(initial, goal, time_limit=TIME_LIMIT, node_limit=n_limit)

    start_time = time.time()
    result = None

    try:

        # IDS — su UNIX usiamo signal per garantire il timeout
        # (iterative_deepening_search non passa per stopped() in
        # modo affidabile su tutti i backend AIMA). Su Windows
        # ci si affida al solo controllo nodi/tempo interno.
        if algo == "ids":
            print("[IDS] ricerca iterativa")
            if HAS_SIGALRM:
                signal.signal(signal.SIGALRM, _timeout_handler)
                signal.alarm(TIME_LIMIT)
            try:
                result = run_limited_search(
                    iterative_deepening_search,
                    problem, TIME_LIMIT, IDS_NODE_LIMIT,
                )
            except TimeoutException:
                print("[TIMEOUT] IDS interrotto")
                result = None
            finally:
                if HAS_SIGALRM:
                    signal.alarm(0)

        elif algo == "bfts":
            print("[BFS] ricerca in ampiezza")
            result = run_limited_search(breadth_first_graph_search, problem, TIME_LIMIT)

        elif algo == "ucs":
            print("[UCS] costo uniforme")
            result = run_limited_search(uniform_cost_search, problem, TIME_LIMIT)

        elif algo == "dls":
            print("[DLS] profondita' limitata")
            result = run_limited_search(depth_limited_search, problem, TIME_LIMIT, None, IDS_MAX_DEPTH)

        elif algo == "astar":
            print("[A*] ricerca informata")
            result = run_limited_search(
                astar_search, problem, TIME_LIMIT, None,
                lambda n: safe_heuristic(n, problem, heuristic),
            )

        else:
            raise ValueError("Algoritmo non valido")

    except Exception as e:
        print("[ERROR RUN]", e)
        result = None

    elapsed = round(time.time() - start_time, 5)

    # ==================================================
    # FAILURE
    # ==================================================
    if result is None or not hasattr(result, "solution"):
        print("\nFAILURE (timeout / node limit / crash)")
        return {
            "problem":         problem_name,
            "algorithm":       algo,
            "heuristic":       heuristic.__name__ if heuristic else "None",
            "time":            elapsed,
            "nodes_generated": problem.nodes_generated,
            "nodes_expanded":  problem.nodes_expanded,
            "depth":           None,
            "cost":            None,
            "status":          "FAILURE",
            "actions":         "()"
        }

    solution = result.solution()

    # ==================================================
    # NO SOLUTION
    # ==================================================
    if solution is None or len(solution) == 0:
        print("\nNO SOLUTION")
        return {
            "problem":         problem_name,
            "algorithm":       algo,
            "heuristic":       heuristic.__name__ if heuristic else "None",
            "time":            elapsed,
            "nodes_generated": problem.nodes_generated,
            "nodes_expanded":  problem.nodes_expanded,
            "depth":           0,
            "cost":            0,
            "status":          "NO_SOLUTION",
            "actions":         "()"
        }

    # ==================================================
    # SUCCESSO
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
        "problem":         problem_name,
        "algorithm":       algo,
        "heuristic":       heuristic.__name__ if heuristic else "None",
        "time":            elapsed,
        "nodes_generated": problem.nodes_generated,
        "nodes_expanded":  problem.nodes_expanded,
        "depth":           len(solution),
        "cost":            result.path_cost,
        "status":          "SUCCESS",
        "actions":         actions_str
    }


# Output resultato
def print_results(results):
    print("\n================= RISULTATI FINALI =================\n")
    for r in results:
        print(r)


# CSV export
def save_csv(results):
    output_path = Path(__file__).resolve().parent / "results.csv"

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"[INFO] CSV salvato in: {output_path}")


# ==========================================================
# MAIN
# ==========================================================
def main():

    problems = [
        ("easy",     problem_easy),
        ("medium",   problem_medium),
        ("hard",     problem_hard),
        ("hard_HD",  problem_hard_HD),
        ("extreme",  problem_extreme),
    ]

    heuristics = [h1, h2, h3, h4, h_energy, h_memory, h_max]

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
