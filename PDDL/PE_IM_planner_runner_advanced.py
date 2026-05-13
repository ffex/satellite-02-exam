# ==========================================================
# PE_IM_planner_runner_advanced.py (CLEAN + SEMANTIC FIX)
# ==========================================================

import subprocess
import time
from pathlib import Path
import re
from plan_render import SemanticPlanRenderer

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DOMAIN_FILE = BASE_DIR / "domain_advanced.pddl"
ENHSP_JAR = BASE_DIR / "enhsp-enhsp-20" / "enhsp.jar"

PLANS_DIR = BASE_DIR / "generated_plans"
LOGS_DIR = BASE_DIR / "planner_logs"

PLANS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# ==========================================================
# PROBLEMS
# ==========================================================

PROBLEMS = {
    "easy": BASE_DIR / "problem_easy_advanced.pddl",
    "medium": BASE_DIR / "problem_medium_advanced.pddl",
    "hard": BASE_DIR / "problem_hard_advanced.pddl",
    "hard_hd": BASE_DIR / "problem_hard_hd_advanced.pddl",
    "extreme": BASE_DIR / "problem_extreme_advanced.pddl",
}

# ==========================================================
# STRATEGIES
# ==========================================================

PLANNERS = {

    #bfs
    "bfs": ["-s", "bfs"],

    # UCS (uniform cost ~ A* senza euristica utile)
    "ucs": ["-s", "astar", "-h", "zero"],  # ENHSP interpreta zero o default cost

    # Greedy best first

    "gbfs_hff": ["-s", "gbfs", "-h", "hff"],

    # A*

    "astar_hff": ["-s", "astar", "-h", "hff"],
    "astar_lmcut": ["-s", "astar", "-h", "lmcut"],

    # A* pesato
    "wastar_hadd": ["-s", "WAStar", "-h", "hadd"],
}

# ==========================================================
# RESET FILE
# ==========================================================

def reset_file(path: Path):
    path.write_text("")

# ==========================================================
# PLAN PARSER
# ==========================================================

def parse_and_print_plan(plan_file: Path, renderer=None):

    print("\nPLAN STEPS")
    print("-" * 60)

    try:
        text = plan_file.read_text().strip()

        if not text:
            print("[!] EMPTY PLAN")
            return False

        steps = []

        for line in text.splitlines():
            line = line.strip()

            if not line or line.startswith(";"):
                continue

            line = re.sub(r"^[0-9\.]+\:\s*", "", line)
            line = line.replace("(", "").replace(")", "")

            steps.append(line)

        if not steps:
            print("[!] NO VALID ACTIONS FOUND")
            return False

        # ==============================
        # SEMANTIC ENRICHMENT
        # ==============================
        if renderer:
            steps = renderer.render(steps)

        for i, s in enumerate(steps, 1):
            print(f"[{i:02}] {s}")

        print(f"\n[PLAN LENGTH]: {len(steps)}")
        return True

    except Exception as e:
        print("[PARSE ERROR]", e)
        return False

# ==========================================================
# EXTRACT INIT FROM PDDL
# ==========================================================

def get_init_from_problem(problem_file: Path):

    lines = problem_file.read_text().splitlines()

    init = []
    inside = False

    for line in lines:
        l = line.strip()

        if "(:init" in l:
            inside = True
            continue

        if inside and l.startswith("(:goal"):
            break

        if inside:
            init.append(l)

    return init

# ==========================================================
# RUN PLANNER
# ==========================================================

def run_planner(problem_name, problem_file, strategy):

    print("\n" + "=" * 80)
    print(f"PROBLEM  : {problem_name}")
    print(f"STRATEGY : {strategy}")
    print("=" * 80)

    plan_file = PLANS_DIR / f"plan_{problem_name}_{strategy}.txt"
    log_file = LOGS_DIR / f"log_{problem_name}_{strategy}.txt"

    reset_file(plan_file)

    cmd = [
        "java", "-jar", str(ENHSP_JAR),
        "-o", str(DOMAIN_FILE),
        "-f", str(problem_file),
        "-sp", str(plan_file),
        *PLANNERS[strategy]
    ]

    print("\nCOMMAND")
    print(" ".join(cmd))

    start = time.time()

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=120
    )

    elapsed = time.time() - start

    log_file.write_text(
        "STDOUT:\n" + result.stdout +
        "\n\nSTDERR:\n" + result.stderr
    )

    print("\nRESULT")
    print("-" * 60)
    print(f"Exit code : {result.returncode}")
    print(f"Time      : {elapsed:.2f}s")

    if "Solution found" not in result.stdout and plan_file.stat().st_size == 0:
        print("\n[NO PLAN FOUND]")
        return None

    print("\n[SUCCESS] Plan generato")
    return plan_file

# ==========================================================
# EXECUTION PIPELINE
# ==========================================================

def execute(problem_name, problem_file, strategy):

    plan_file = run_planner(problem_name, problem_file, strategy)

    if not plan_file:
        print("[SKIP]")
        return

    init_lines = get_init_from_problem(problem_file)

    renderer = SemanticPlanRenderer(init_lines)

    parse_and_print_plan(plan_file, renderer)

# ==========================================================
# MAIN
# ==========================================================

def main():

    for pname, pfile in PROBLEMS.items():

        print("\n" + "#" * 80)
        print(f"RUNNING PROBLEM: {pname}")
        print("#" * 80)

        for strategy in PLANNERS:

            try:
                execute(pname, pfile, strategy)
            except Exception as e:
                print("[FATAL]", pname, strategy)
                print(e)

# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()