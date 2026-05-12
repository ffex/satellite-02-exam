# ==========================================================
# FILE: PE_IM_planner_runner_advanced.py
# ==========================================================
#
# RUNNER COMPLETO PER ENHSP
#
# Questo runner:
#
# 1. Esegue ENHSP
# 2. Salva:
#       - piano generato
#       - stdout/stderr
#       - log debug
# 3. Parse del piano
# 4. Simulazione del piano tramite interpreter
# 5. Validazione finale dello stato
#
# ----------------------------------------------------------
# STRUTTURA OUTPUT
#
# generated_plans/
#   ├── plan_easy_bfs.txt
#   ├── plan_easy_gbfs_hff.txt
#   └── ...
#
# planner_logs/
#   ├── log_easy_bfs.txt
#   └── ...
#
# ----------------------------------------------------------
# PIPELINE
#
# problem.pddl
#      ↓
# ENHSP
#      ↓
# piano.txt
#      ↓
# parse_plan()
#      ↓
# interpreter.run()
#      ↓
# stato finale
#
# ==========================================================

import subprocess
import time
from pathlib import Path

from PE_IM_parse_plan_advanced import parse_plan
from PE_IM_planner_interpreter_advanced import (
    PDDLPlanInterpreterAdvanced
)

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DOMAIN_FILE = BASE_DIR / "domain_advanced.pddl"

ENHSP_JAR = (
    BASE_DIR /
    "enhsp-enhsp-20" /
    "enhsp.jar"
)

# ----------------------------------------------------------
# output folders
# ----------------------------------------------------------

PLANS_DIR = BASE_DIR / "generated_plans"
LOGS_DIR = BASE_DIR / "planner_logs"

PLANS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# ==========================================================
# PROBLEMS
# ==========================================================

PROBLEMS = {

    "easy":
        BASE_DIR / "problem_easy_advanced.pddl",

    "medium":
        BASE_DIR / "problem_medium_advanced.pddl",

    "hard":
        BASE_DIR / "problem_hard_advanced.pddl",

    "hard_hd":
        BASE_DIR / "problem_hard_hd_advanced.pddl",

    "extreme":
        BASE_DIR / "problem_extreme_advanced.pddl",
}

# ==========================================================
# SEARCH STRATEGIES
# ==========================================================

PLANNERS = {

    # ------------------------------------------------------
    # Breadth First Search
    # ricerca non informata per livelli
    # ------------------------------------------------------

    "bfs":
        ["-s", "bfs"],

    # ------------------------------------------------------
    # Greedy Best First Search
    # ------------------------------------------------------

    "gbfs_hadd":
        ["-s", "gbfs", "-h", "hadd"],

    "gbfs_hff":
        ["-s", "gbfs", "-h", "hff"],

    # ------------------------------------------------------
    # A*
    # ------------------------------------------------------

    "astar_hadd":
        ["-s", "astar", "-h", "hadd"],

    "astar_hff":
        ["-s", "astar", "-h", "hff"],

    # ------------------------------------------------------
    # Weighted A*
    # più veloce ma meno ottimale
    # ------------------------------------------------------

    "wastar_hff":
        ["-s", "WAStar", "-h", "hff"],
}

# ==========================================================
# FAILURE ANALYSIS
# ==========================================================

def diagnose_failure(stdout: str,
                     stderr: str):

    """
    Analizza stdout/stderr per capire
    perché ENHSP non ha prodotto un piano.
    """

    text = (stdout + stderr).lower()

    if "unsolvable" in text:
        return "UNSOLVABLE_PROBLEM"

    if "timeout" in text:
        return "TIMEOUT"

    if "parser error" in text:
        return "PDDL_PARSE_ERROR"

    if "undefined" in text:
        return "UNDEFINED_SYMBOL"

    if "cannot parse" in text:
        return "INVALID_PDDL"

    if "heuristic" in text:
        return "HEURISTIC_FAILURE"

    return "UNKNOWN_FAILURE"

# ==========================================================
# RUN ENHSP
# ==========================================================

def run_planner(problem_name: str,
                problem_file: Path,
                strategy: str):

    """
    Esegue ENHSP sul problema selezionato.
    """

    print("\n" + "=" * 80)
    print(f"PROBLEM  : {problem_name}")
    print(f"STRATEGY : {strategy}")
    print("=" * 80)

    # ------------------------------------------------------
    # unique output files
    # ------------------------------------------------------

    plan_file = (
        PLANS_DIR /
        f"plan_{problem_name}_{strategy}.txt"
    )

    log_file = (
        LOGS_DIR /
        f"log_{problem_name}_{strategy}.txt"
    )

    # ------------------------------------------------------
    # cleanup vecchio piano
    # ------------------------------------------------------

    if plan_file.exists():
        plan_file.unlink()

    # ------------------------------------------------------
    # command
    # ------------------------------------------------------

    cmd = [

        "java",
        "-jar",
        str(ENHSP_JAR),

        "-o",
        str(DOMAIN_FILE),

        "-f",
        str(problem_file),

        "-sp",
        str(plan_file),

        *PLANNERS[strategy]
    ]

    print("\nCOMMAND:")
    print(" ".join(cmd))

    # ======================================================
    # EXECUTION
    # ======================================================

    try:

        start = time.time()

        result = subprocess.run(

            cmd,

            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,

            text=True,

            timeout=60
        )

        elapsed = time.time() - start

    except subprocess.TimeoutExpired:

        print("\n[TIMEOUT]")
        print("Planner exceeded 60 seconds")

        return None

    # ------------------------------------------------------
    # ENHSP a volte scrive dopo il termine
    # ------------------------------------------------------

    time.sleep(0.3)

    # ======================================================
    # SAVE COMPLETE LOG
    # ======================================================

    with open(log_file, "w") as f:

        f.write("=" * 80 + "\n")
        f.write("COMMAND\n")
        f.write("=" * 80 + "\n")
        f.write(" ".join(cmd) + "\n\n")

        f.write("=" * 80 + "\n")
        f.write("EXIT CODE\n")
        f.write("=" * 80 + "\n")
        f.write(str(result.returncode) + "\n\n")

        f.write("=" * 80 + "\n")
        f.write("STDOUT\n")
        f.write("=" * 80 + "\n")
        f.write(result.stdout + "\n\n")

        f.write("=" * 80 + "\n")
        f.write("STDERR\n")
        f.write("=" * 80 + "\n")
        f.write(result.stderr + "\n\n")

    # ======================================================
    # DEBUG INFO
    # ======================================================

    print("\n" + "-" * 80)
    print("DEBUG INFO")
    print("-" * 80)

    print(f"Exit code : {result.returncode}")
    print(f"Elapsed   : {elapsed:.3f}s")

    # ------------------------------------------------------
    # stdout preview
    # ------------------------------------------------------

    stdout_preview = result.stdout[-1200:]

    if stdout_preview.strip():

        print("\nSTDOUT PREVIEW")
        print("-" * 40)
        print(stdout_preview)

    # ------------------------------------------------------
    # stderr preview
    # ------------------------------------------------------

    stderr_preview = result.stderr[-1200:]

    if stderr_preview.strip():

        print("\nSTDERR PREVIEW")
        print("-" * 40)
        print(stderr_preview)

    # ======================================================
    # VALIDATE PLAN FILE
    # ======================================================

    if not plan_file.exists():

        print("\n[ERROR] Plan file not generated")

        failure = diagnose_failure(
            result.stdout,
            result.stderr
        )

        print(f"DIAGNOSIS: {failure}")

        return None

    content = plan_file.read_text().strip()

    if not content:

        print("\n[ERROR] Empty plan file")

        failure = diagnose_failure(
            result.stdout,
            result.stderr
        )

        print(f"DIAGNOSIS: {failure}")

        return None

    print("\n[SUCCESS] Plan generated")

    return plan_file

# ==========================================================
# EXECUTION PIPELINE
# ==========================================================

def execute_pipeline(problem_name: str,
                     problem_file: Path,
                     strategy: str):

    # ======================================================
    # RUN PLANNER
    # ======================================================

    plan_file = run_planner(

        problem_name,
        problem_file,
        strategy
    )

    if plan_file is None:

        print(
            f"\n[SKIP] "
            f"{problem_name} / {strategy}"
        )

        return

    # ======================================================
    # PARSE PLAN
    # ======================================================

    print("\n" + "-" * 80)
    print("PLAN PARSING")
    print("-" * 80)

    try:

        plan = parse_plan(str(plan_file))

    except Exception as e:

        print("\n[PARSER ERROR]")
        print(e)

        return

    if not plan:

        print("\n[ERROR] Empty parsed plan")
        return

    # ======================================================
    # PRINT PLAN
    # ======================================================

    print("\n" + "-" * 80)
    print("PLAN STEPS")
    print("-" * 80)

    for idx, (action, params) in enumerate(plan, start=1):

        print(
            f"[{idx:02d}] "
            f"{action} "
            f"{' '.join(params)}"
        )

    # ======================================================
    # INTERPRETER
    # ======================================================

    print("\n" + "-" * 80)
    print("PLAN EXECUTION")
    print("-" * 80)

    try:

        interpreter = (
            PDDLPlanInterpreterAdvanced()
        )

        interpreter.run(plan)

    except Exception as e:

        print("\n[INTERPRETER ERROR]")
        print(e)

        return

    # ======================================================
    # FINAL STATE
    # ======================================================

    print("\n" + "-" * 80)
    print("FINAL STATE")
    print("-" * 80)

    print(interpreter.state)

# ==========================================================
# MAIN
# ==========================================================

def main():

    for problem_name, problem_file in PROBLEMS.items():

        print("\n")
        print("#" * 80)
        print(f"RUNNING PROBLEM: {problem_name}")
        print("#" * 80)

        for strategy in PLANNERS.keys():

            print("\n")
            print("*" * 80)
            print(f"RUNNING STRATEGY: {strategy}")
            print("*" * 80)

            try:

                execute_pipeline(

                    problem_name,
                    problem_file,
                    strategy
                )

            except Exception as e:

                print(
                    f"\n[FATAL ERROR] "
                    f"{problem_name} / {strategy}"
                )

                print(e)

# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()