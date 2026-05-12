# ==========================================================
# PE_IM_planner_runner_clean.py
# ==========================================================

import subprocess
import time
from pathlib import Path
import re

# ==========================================================
# CONFIG
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DOMAIN_FILE = BASE_DIR / "domain_advanced.pddl"
ENHSP_JAR = BASE_DIR / "enhsp-enhsp-20" / "enhsp.jar"

PLANS_DIR = BASE_DIR / "generated_plans"
LOGS_DIR = BASE_DIR / "planner_logs"

PLANS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

DEBUG_LOG = False
VERBOSE = False

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
# FILE RESET
# ==========================================================

def reset_file(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        pass

# ==========================================================
# ERROR DETECTION
# ==========================================================

def detect_failure(stdout, stderr):
    text = (stdout + stderr).lower()

    keywords = [
        "error",
        "exception",
        "failed",
        "unsolvable",
        "numeric error"
    ]

    return any(k in text for k in keywords)

# ==========================================================
# PLAN PARSER (ROBUSTO)
# ==========================================================

def parse_and_print_plan(plan_file: Path):

    print("\nPLAN STEPS")
    print("-" * 60)

    try:
        with open(plan_file, "r") as f:
            lines = f.readlines()

        steps = []

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if line.startswith(";"):
                continue

            # rimuove timestamp ENHSP
            line = re.sub(r"^[0-9\.]+\s*:\s*", "", line)

            # rimuove formato [01]
            line = re.sub(r"^\[\d+\]\s*", "", line)

            # pulizia parentesi
            line = line.replace("(", "").replace(")", "").strip()

            # filtri rumore ENHSP
            if any(x in line.lower() for x in [
                "numeric error",
                "grounding",
                "problem parsed",
                "heuristic"
            ]):
                continue

            if line:
                steps.append(line)

        if not steps:
            print("[!] Plan vuoto o non valido")
            return False

        for i, s in enumerate(steps):
            print(f"[{i+1:02}] {s}")

        print(f"\n[PLAN LENGTH]: {len(steps)}")
        return True

    except Exception as e:
        print("\n[PARSE ERROR]")
        print(e)
        return False

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

    # reset totale
    reset_file(plan_file)
    reset_file(log_file)

    cmd = [
        "java",
        "-jar",
        str(ENHSP_JAR),
        "-o", str(DOMAIN_FILE),
        "-f", str(problem_file),
        "-sp", str(plan_file),
        *PLANNERS[strategy]
    ]

    if VERBOSE:
        print("\nCOMMAND")
        print(" ".join(cmd))

    start = time.time()

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=60
    )

    elapsed = time.time() - start

    # ======================================================
    # LOG MANAGEMENT
    # ======================================================

    if DEBUG_LOG:
        log_file.write_text(result.stdout + "\n\n" + result.stderr)
    else:
        log_file.write_text(result.stderr if result.stderr else result.stdout)

    # ======================================================
    # OUTPUT
    # ======================================================

    print("\nRESULT")
    print("-" * 60)
    print(f"Exit code : {result.returncode}")
    print(f"Time      : {elapsed:.2f}s")

    # detection errori reali
    if result.returncode != 0 or detect_failure(result.stdout, result.stderr):
        print("\n[PLANNER ERROR / WARNING]")
        print(result.stderr[-1000:])
        return None

    # ======================================================
    # PLAN CHECK
    # ======================================================

    if not plan_file.exists() or plan_file.stat().st_size == 0:
        print("\n[ERROR] Plan non generato")
        print(result.stdout[-1000:])
        return None

    print("\n[SUCCESS] Plan generato")

    return plan_file

# ==========================================================
# EXECUTE SINGLE RUN
# ==========================================================

def execute(problem_name, problem_file, strategy):

    plan_file = run_planner(problem_name, problem_file, strategy)

    if not plan_file:
        print("\n[SKIP]")
        return

    ok = parse_and_print_plan(plan_file)

    if not ok:
        print("\n[WARNING] Plan problematico")

# ==========================================================
# MAIN LOOP
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
                print("\n[FATAL ERROR]")
                print(f"{pname} / {strategy}")
                print(e)

# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()