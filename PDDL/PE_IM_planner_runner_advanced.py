# ==========================================================
# FILE: PE_IM_planner_runner_advanced.py
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

ENHSP_JAR = BASE_DIR / "enhsp-enhsp-20" / "enhsp.jar"

# cartelle output
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
# STRATEGIES
# ==========================================================

PLANNERS = {

    # ------------------------------------------------------
    # uninformed
    # ------------------------------------------------------

    "bfs":
        ["-s", "bfs"],

    # ------------------------------------------------------
    # greedy
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
    # weighted A*
    # ------------------------------------------------------

    "wastar_hff":
        ["-s", "WAStar", "-h", "hff"],
}

# ==========================================================
# FAILURE DIAGNOSIS
# ==========================================================

def diagnose_failure(stdout: str,
                     stderr: str):

    text = (stdout + stderr).lower()

    # ------------------------------------------------------
    # unsolvable
    # ------------------------------------------------------

    if "unsolvable" in text:
        return "UNSOLVABLE_PROBLEM"

    # ------------------------------------------------------
    # timeout
    # ------------------------------------------------------

    if "timeout" in text:
        return "TIMEOUT"

    # ------------------------------------------------------
    # parse/domain errors
    # ------------------------------------------------------

    if "parser error" in text:
        return "PDDL_PARSE_ERROR"

    if "undefined" in text:
        return "UNDEFINED_SYMBOL"

    if "cannot parse" in text:
        return "INVALID_PDDL"

    # ------------------------------------------------------
    # heuristic issues
    # ------------------------------------------------------

    if "heuristic" in text:
        return "HEURISTIC_FAILURE"

    # ------------------------------------------------------
    # no idea
    # ------------------------------------------------------

    return "UNKNOWN_FAILURE"

# ==========================================================
# RUN PLANNER
# ==========================================================

def run_planner(problem_name: str,
                problem_file: Path,
                strategy: str):

    print("\n" + "=" * 70)
    print(f"PROBLEM : {problem_name}")
    print(f"STRATEGY: {strategy}")
    print("=" * 70)

    # ------------------------------------------------------
    # unique plan file
    # ------------------------------------------------------

    plan_file = (
        PLANS_DIR /
        f"plan_{problem_name}_{strategy}.txt"
    )

    # ------------------------------------------------------
    # unique log file
    # ------------------------------------------------------

    log_file = (
        LOGS_DIR /
        f"log_{problem_name}_{strategy}.txt"
    )

    # ------------------------------------------------------
    # cleanup old plan
    # ------------------------------------------------------

    if plan_file.exists():
        plan_file.unlink()

    # ------------------------------------------------------
    # ENHSP command
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

        print("\n[TIMEOUT] Planner exceeded 60 seconds")

        return None

    # ------------------------------------------------------
    # ENHSP sometimes writes later
    # ------------------------------------------------------

    time.sleep(0.3)

    # ======================================================
    # SAVE DEBUG LOG
    # ======================================================

    with open(log_file, "w") as f:

        f.write("=" * 70 + "\n")
        f.write("COMMAND\n")
        f.write("=" * 70 + "\n")
        f.write(" ".join(cmd) + "\n\n")

        f.write("=" * 70 + "\n")
        f.write("EXIT CODE\n")
        f.write("=" * 70 + "\n")
        f.write(str(result.returncode) + "\n\n")

        f.write("=" * 70 + "\n")
        f.write("STDOUT\n")
        f.write("=" * 70 + "\n")
        f.write(result.stdout + "\n\n")

        f.write("=" * 70 + "\n")
        f.write("STDERR\n")
        f.write("=" * 70 + "\n")
        f.write(result.stderr + "\n\n")

    # ======================================================
    # DEBUG PRINTS
    # ======================================================

    print("\n" + "-" * 70)
    print("DEBUG")
    print("-" * 70)

    print(f"Exit code : {result.returncode}")
    print(f"Elapsed   : {elapsed:.2f}s")

    # ------------------------------------------------------
    # stdout preview
    # ------------------------------------------------------

    stdout_preview = result.stdout[-1500:]

    if stdout_preview.strip():

        print("\nSTDOUT PREVIEW:")
        print("-" * 40)
        print(stdout_preview)

    # ------------------------------------------------------
    # stderr preview
    # ------------------------------------------------------

    stderr_preview = result.stderr[-1500:]

    if stderr_preview.strip():

        print("\nSTDERR PREVIEW:")
        print("-" * 40)
        print(stderr_preview)

    # ======================================================
    # CHECK PLAN
    # ======================================================

    if not plan_file.exists():

        print("\n[ERROR] Plan file NOT created")

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
# EXECUTE PIPELINE
# ==========================================================

def execute_pipeline(problem_name: str,
                     problem_file: Path,
                     strategy: str):

    # ------------------------------------------------------
    # RUN ENHSP
    # ------------------------------------------------------

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

    plan = parse_plan(str(plan_file))

    print("\n" + "-" * 70)
    print("PLAN")
    print("-" * 70)

    for step in plan:
        print(step)

    # ======================================================
    # INTERPRETER
    # ======================================================

    print("\n" + "-" * 70)
    print("EXECUTION")
    print("-" * 70)

    interpreter = PDDLPlanInterpreterAdvanced()

    interpreter.run(plan)

# ==========================================================
# MAIN
# ==========================================================

def main():

    for problem_name, problem_file in PROBLEMS.items():

        print("\n")
        print("#" * 70)
        print(f"RUNNING PROBLEM: {problem_name}")
        print("#" * 70)

        for strategy in PLANNERS.keys():

            print("\n")
            print("*" * 70)
            print(f"RUNNING STRATEGY: {strategy}")
            print("*" * 70)

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