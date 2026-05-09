# ==========================================================
# FILE: PE_IM_planner_runner.py
# ==========================================================
# RESPONSABILITÀ:
#   1. Esegue Fast Downward con diverse strategie
#   2. Legge il piano generato
#   3. Ricostruisce lo stato iniziale dal PDDL
#   4. Simula l'esecuzione del piano tramite interpreter
# ==========================================================

import subprocess

from PE_IM_parse_plan import *
from PE_IM_planner_interpreter import PDDLPlanInterpreter


# ==========================================================
# CONFIGURAZIONE FILE PDDL
# ==========================================================

DOMAIN_FILE = "domain.pddl"
PROBLEM_FILE = "problem_easy.pddl"
PLAN_FILE = "sas_plan"


# ==========================================================
# STRATEGIE DI SEARCH FAST DOWNWARD
# ==========================================================

PLANNERS = {
    "blind": "astar(blind())",
    "astar_hmax": "astar(hmax())",
    "astar_lmcut": "astar(lmcut())",
    "greedy_hmax": "eager_greedy([hmax()])",
    "greedy_lmcut": "eager_greedy([lmcut()])",
}


# ==========================================================
# ESECUZIONE PLANNER
# ==========================================================

def run_planner(strategy: str) -> bool:
    """
    Esegue Fast Downward con la strategia scelta.

    Returns:
        bool: True se il planner termina correttamente
    """

    print("\n" + "=" * 60)
    print(f"RUNNING PLANNER STRATEGY: {strategy}")
    print("=" * 60)

    search_strategy = PLANNERS[strategy]

    command = [
        "./downward/fast-downward.py",
        DOMAIN_FILE,
        PROBLEM_FILE,
        "--search",
        search_strategy
    ]

    result = subprocess.run(command)

    return result.returncode == 0


# ==========================================================
# COSTRUZIONE STATO INIZIALE
# ==========================================================

def build_initial_state(problem_file: str = PROBLEM_FILE):
    """
    Estrae lo stato iniziale direttamente dal file PDDL.

    IMPORTANTE:
    - Non contiene logica del dominio
    - Non inferisce nulla
    - Replica solo i fatti dichiarati nel PDDL
    """

    return parse_init_state(problem_file)


# ==========================================================
# ESECUZIONE COMPLETA PIPELINE
# ==========================================================

def execute_pipeline(strategy: str):
    """
    Pipeline completa:

    1. Run planner
    2. Parse plan
    3. Build initial state
    4. Execute plan step-by-step
    """

    success = run_planner(strategy)

    if not success:
        print(f"[ERROR] Planner failed with strategy: {strategy}")
        return

    # ------------------------------------------------------
    # PARSING PLAN
    # ------------------------------------------------------
    plan = parse_plan(PLAN_FILE)

    print("\n" + "-" * 60)
    print("GENERATED PLAN")
    print("-" * 60)

    for step in plan:
        print(step)

    # ------------------------------------------------------
    # INITIAL STATE
    # ------------------------------------------------------
    initial_state = build_initial_state()

    # ------------------------------------------------------
    # INTERPRET EXECUTION
    # ------------------------------------------------------
    interpreter = PDDLPlanInterpreter(initial_state)

    print("\n" + "-" * 60)
    print("PLAN EXECUTION")
    print("-" * 60)

    interpreter.run(plan)


# ==========================================================
# MAIN LOOP
# ==========================================================

def main():

    for strategy in PLANNERS.keys():
        execute_pipeline(strategy)


if __name__ == "__main__":
    main()