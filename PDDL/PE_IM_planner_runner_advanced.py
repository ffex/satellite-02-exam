# ==========================================================
# PE_IM_planner_runner_advanced.py (FIXED & CLEAN)
# ==========================================================

import subprocess
import time
from pathlib import Path
import re

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
    "bfs": ["-s", "bfs"],
    "gbfs_hadd": ["-s", "gbfs", "-h", "hadd"],
    "gbfs_hff": ["-s", "gbfs", "-h", "hff"],
    "astar_hff": ["-s", "astar", "-h", "hff"],
    "wastar_hff": ["-s", "WAStar", "-h", "hff"],
}

# ==========================================================
# UTIL: RESET FILE
# ==========================================================

def reset_file(path: Path):
    path.write_text("")

# ==========================================================
# FIXED PARSER (ENHSP SAFE)
# ==========================================================

def parse_and_print_plan(plan_file: Path):
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

            # ENHSP format cleanup
            line = re.sub(r"^[0-9\.]+\:\s*", "", line)
            line = line.replace("(", "").replace(")", "")

            steps.append(line)

        if not steps:
            print("[!] NO VALID ACTIONS FOUND")
            return False

        for i, s in enumerate(steps, 1):
            print(f"[{i:02}] {s}")

        print(f"\n[PLAN LENGTH]: {len(steps)}")
        return True

    except Exception as e:
        print("[PARSE ERROR]", e)
        return False

# ==========================================================
# RUN PLANNER (FIXED LOGIC)
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
        "java",
        "-jar",
        str(ENHSP_JAR),
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

    # ======================================================
    # LOGGING FULL OUTPUT
    # ======================================================

    log_file.write_text(
        "STDOUT:\n" + result.stdout +
        "\n\nSTDERR:\n" + result.stderr
    )

    # ======================================================
    # OUTPUT
    # ======================================================

    print("\nRESULT")
    print("-" * 60)
    print(f"Exit code : {result.returncode}")
    print(f"Time      : {elapsed:.2f}s")

    # ⚠ FIX IMPORTANTISSIMO
    # ENHSP spesso ritorna 0 anche se non trova piano utile
    # quindi NON usare returncode come criterio unico

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

    parse_and_print_plan(plan_file)

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