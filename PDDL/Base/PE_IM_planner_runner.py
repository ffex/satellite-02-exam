# ==========================================================
# FILE: PE_IM_planner_runner.py
# ==========================================================
# RESPONSABILITÀ:
#   1. Esegue Fast Downward con diverse strategie
#   2. Supporta MULTI-PROBLEM
#   3. Legge il piano generato
#   4. Ricostruisce lo stato iniziale dal PDDL
#   5. Simula l'esecuzione del piano tramite interpreter
# ==========================================================

import subprocess

from pathlib import Path

from PE_IM_parse_plan import *
from PE_IM_planner_interpreter import PDDLPlanInterpreter


# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent


# ==========================================================
# FAST DOWNWARD
# ==========================================================

FAST_DOWNWARD = (
    BASE_DIR /
    "downward" /
    "fast-downward.py"
)


# ==========================================================
# DOMAIN
# ==========================================================

DOMAIN_FILE = BASE_DIR / "domain.pddl"


# ==========================================================
# PLAN FILE
# ==========================================================

PLAN_FILE = BASE_DIR / "sas_plan"


# ==========================================================
# PROBLEMI DISPONIBILI
# ==========================================================

PROBLEMS = {

    "easy":
        BASE_DIR / "problem_easy.pddl",

    "medium":
        BASE_DIR / "problem_medium.pddl",

    "hard":
        BASE_DIR / "problem_hard.pddl",

    "hard_hd":
        BASE_DIR / "problem_hard_hd.pddl",

    "extreme":
        BASE_DIR / "problem_extreme.pddl",
}


# ==========================================================
# STRATEGIE FAST DOWNWARD
# ==========================================================

PLANNERS = {

    # ======================================================
    # BASELINE
    # ======================================================

    "blind_astar":
        "astar(blind())",

    "bfs":
        "breadth_first_search()",

    "dfs":
        "depth_first_search()",


    # ======================================================
    # HEURISTICHE CLASSICHE
    # ======================================================

    "astar_hmax":
        "astar(hmax())",

    "astar_ff":
        "astar(ff())",

    "astar_cea":
        "astar(cea())",


    # ======================================================
    # HEURISTICHE MODERNE
    # ======================================================

    "astar_lmcut":
        "astar(lmcut())",

    "eager_lmcut":
        "eager_greedy([lmcut()])",

    "astar_add":
        "astar(add())",

    "eager_add":
        "eager_greedy([add()])",


    # ======================================================
    # GREEDY
    # ======================================================

    "greedy_hmax":
        "eager_greedy([hmax()])",

    "greedy_ff":
        "eager_greedy([ff()])",

    "greedy_lmcut":
        "eager_greedy([lmcut()])",


    # ======================================================
    # MULTI-HEURISTIC
    # ======================================================

    "eager_combo":
        "eager_greedy([ff(), hmax(), lmcut()])",

    "astar_combo":
        "astar([ff(), hmax(), lmcut()])",


    # ======================================================
    # WEIGHTED A*
    # ======================================================

    "wastar_ff":
        "lazy_wastar([ff()], w=2)",

    "wastar_lmcut":
        "lazy_wastar([lmcut()], w=2)",


    # ======================================================
    # LAZY GREEDY
    # ======================================================

    "lazy_greedy_ff":
        "lazy_greedy([ff()])",

    "lazy_greedy_lmcut":
        "lazy_greedy([lmcut()])",
}


# ==========================================================
# RUN PLANNER
# ==========================================================

def run_planner(
    strategy: str,
    problem_file: Path
) -> bool:
    """
    Esegue Fast Downward sul problema scelto.
    """

    print("\n" + "=" * 60)
    print(f"PLANNER STRATEGY: {strategy}")
    print("=" * 60)

    search_strategy = PLANNERS[strategy]

    command = [

        str(FAST_DOWNWARD),

        str(DOMAIN_FILE),

        str(problem_file),

        "--search",

        search_strategy
    ]

    print("\nCOMMAND:")
    print(" ".join(command))

    result = subprocess.run(command)

    return result.returncode == 0


# ==========================================================
# BUILD INITIAL STATE
# ==========================================================

def build_initial_state(problem_file: Path):
    """
    Costruisce lo stato iniziale dal PDDL.
    """

    return parse_init_state(str(problem_file))


# ==========================================================
# PIPELINE COMPLETA
# ==========================================================

def execute_pipeline(
    problem_name: str,
    problem_file: Path,
    strategy: str
):
    """
    Pipeline completa:

    1. Planner
    2. Parse plan
    3. Build state
    4. Execute
    """

    print("\n" + "#" * 70)
    print(f"PROBLEM: {problem_name.upper()}")
    print(f"STRATEGY: {strategy}")
    print("#" * 70)

    success = run_planner(strategy, problem_file)

    if not success:

        print(
            f"[ERROR] Planner failed "
            f"for {problem_name} with {strategy}"
        )

        return

    # ------------------------------------------------------
    # PARSE PLAN
    # ------------------------------------------------------

    plan = parse_plan(str(PLAN_FILE))

    print("\n" + "-" * 60)
    print("GENERATED PLAN")
    print("-" * 60)

    for step in plan:
        print(step)

    # ------------------------------------------------------
    # INITIAL STATE
    # ------------------------------------------------------

    initial_state = build_initial_state(problem_file)

    # ------------------------------------------------------
    # EXECUTION
    # ------------------------------------------------------

    interpreter = PDDLPlanInterpreter(initial_state)

    print("\n" + "-" * 60)
    print("PLAN EXECUTION")
    print("-" * 60)

    interpreter.run(plan)


# ==========================================================
# MAIN
# ==========================================================

def main():

    for problem_name, problem_file in PROBLEMS.items():

        print("\n" + "\n" + "=" * 70)
        print(f"RUNNING PROBLEM: {problem_name.upper()}")
        print("=" * 70)

        for strategy in PLANNERS.keys():

            execute_pipeline(
                problem_name,
                problem_file,
                strategy
            )


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    main()