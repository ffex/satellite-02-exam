# ==========================================================
# PE_IM_run.py
# Complete version with results printing + CSV
# ==========================================================

"""
This file runs all Satellite Problem experiments.

OBJECTIVE:
- Test IDS and A*
- Compare heuristics
- Print results to console
- Save results to CSV

NOTE:
All problems have explicit photo quality (no scenarios).
"""

# ==========================================================
# IMPORT
# ==========================================================

from search import iterative_deepening_search, astar_search

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
    Execute heuristic safely.

    If heuristic generates error:
    - print debug message
    - return 0

    This prevents A* from crashing.
    """

    if heuristic is None:
        return 0

    try:
        return heuristic(node, problem)

    except Exception as e:
        print("[HEURISTIC ERROR]", e)
        return 0


# ==========================================================
# RUN SINGLE EXPERIMENT
# ==========================================================

def run_experiment(problem_name,
                   problem_func,
                   heuristic=None,
                   algo="astar"):
    """
    Run a single experiment.

    Parameters:
    - problem_name : problem name
    - problem_func : function that generates initial, goal
    - heuristic    : A* heuristic
    - algo         : ids or astar

    Returns:
    dict with final statistics
    """

    print("\n===================================")
    print("PROBLEM :", problem_name)
    print("ALGO    :", algo)
    print("===================================")

    # --------------------------------------------------
    # Generate problem
    # --------------------------------------------------

    initial, goal = problem_func()

    print("DEBUG INITIAL:", initial)
    print("DEBUG GOAL   :", goal)

    # --------------------------------------------------
    # Create Satellite instance
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
    # A*
    # --------------------------------------------------

    elif algo == "astar":

        result = astar_search(
            problem,
            lambda n: safe_heuristic(n, problem, heuristic)
        )

    else:
        raise ValueError("Invalid algorithm")

    # --------------------------------------------------
    # Timer stop
    # --------------------------------------------------

    end = time.time()

    elapsed = round(end - start, 5)

    # --------------------------------------------------
    # Base statistics
    # --------------------------------------------------

    print("NODES GENERATED:", problem.nodes_generated)
    print("NODES EXPANDED :", problem.nodes_expanded)

    # --------------------------------------------------
    # If solution found
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
    # Results row
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
# PRINT RESULTS TABLE
# ==========================================================

def print_results(results):
    """
    Print all final results.
    """

    print("\n\n=================================================")
    print("=============== FINAL RESULTS ================")
    print("=================================================\n")

    for row in results:
        print(row)


# ==========================================================
# SAVE TO CSV
# ==========================================================

def save_to_csv(results):
    """
    Save results to results.csv file
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
    Run complete test suite.
    """

    # --------------------------------------------------
    # Problems
    # --------------------------------------------------

    problems = [
        ("easy", problem_easy),
        ("medium", problem_medium),
        ("hard", problem_hard),
        ("low_energy", variant_low_energy),
        ("many_objects", variant_many_objects),
        # ("memory_stress", variant_memory_stress)
    ]

    # --------------------------------------------------
    # Heuristics
    # --------------------------------------------------

    heuristics_list = [h_takepic_only, h_takepic_send, h_max]

    # --------------------------------------------------
    # Final results list
    # --------------------------------------------------

    results = []

    # --------------------------------------------------
    # Main loop
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
    # FINAL OUTPUT
    # --------------------------------------------------

    print_results(results)

    save_to_csv(results)

    print("\nFile saved: results.csv")


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()