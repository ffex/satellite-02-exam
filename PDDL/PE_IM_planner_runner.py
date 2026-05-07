"""
==========================================================
PLANNER RUNNER
==========================================================

Esegue planner Fast Downward con 3 strategie:
- blind
- hmax
- lmcut

Gestisce:
- fallimenti planner
- parsing sicuro
- animazione
==========================================================
"""

import subprocess
from PE_IM_parser import parse_plan
from PE_IM_animation import animate_plan


# ==========================================================
# CONFIG
# ==========================================================

DOMAIN = "domain.pddl"
PROBLEM = "problem_easy.pddl"
PLAN_FILE = "sas_plan"


# ==========================================================
# PLANNER STRATEGIES
# ==========================================================

PLANNERS = {
    "blind": "astar(blind())",
    "hmax": "astar(hmax())",
    "lmcut": "astar(lmcut())"
}


# ==========================================================
# RUN PLANNER
# ==========================================================

def run_planner(strategy="lmcut"):
    """
    Esegue Fast Downward.
    """

    print("\n########################################")
    print(f"PLANNER: {strategy}")
    print("########################################")

    search = PLANNERS[strategy]

    command = [
        "./downward/fast-downward.py",
        DOMAIN,
        PROBLEM,
        "--search",
        search
    ]

    print("\nESECUZIONE:", search)

    result = subprocess.run(command)

    if result.returncode != 0:
        print("\n❌ Planner fallito")
        return False

    return True


# ==========================================================
# MAIN
# ==========================================================

def main():

    for strategy in PLANNERS:

        ok = run_planner(strategy)

        plan = parse_plan(PLAN_FILE)

        if not plan:
            print("[MAIN] Nessun piano generato\n")
            continue

        print("\nPIANO GENERATO:\n")

        for p in plan:
            print(p)

        animate_plan(plan)


if __name__ == "__main__":
    main()