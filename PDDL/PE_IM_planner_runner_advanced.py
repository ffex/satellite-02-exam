import subprocess
import time
import re
from pathlib import Path

# ==========================================================
# BASE PATH
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DOMAIN_FILE = BASE_DIR / "domain_advanced.pddl"
ENHSP_JAR = BASE_DIR / "enhsp-enhsp-20" / "enhsp.jar"

OUTPUT_DIR = BASE_DIR / "output"

PLANS_BASE = OUTPUT_DIR / "generated_plans"
LOGS_BASE = OUTPUT_DIR / "planner_logs"

# ==========================================================
# STRATEGIES
# ==========================================================

PLANNERS = {
    "bfs": ["-s", "bfs"],
    "ucs": ["-s", "astar", "-h", "zero"],
    "gbfs_hff": ["-s", "gbfs", "-h", "hff"],
    "astar_hff": ["-s", "astar", "-h", "hff"],
    "astar_lmcut": ["-s", "astar", "-h", "lmcut"],
    "wastar_hadd": ["-s", "WAStar", "-h", "hadd"],
}

# ==========================================================
# PROBLEMS
# ==========================================================

PROBLEMS = {
    "easy": BASE_DIR / "problem_easy_advanced.pddl",
    "medium": BASE_DIR / "problem_medium_advanced.pddl",
    "hard": BASE_DIR / "problem_hard_advanced.pddl",
    "extreme": BASE_DIR / "problem_extreme_advanced.pddl",
}

# ==========================================================
# DIRECTORY MANAGEMENT
# ==========================================================

def ensure_clean_dir(path: Path):

    if path.exists():

        for f in path.glob("*"):

            try:

                if f.is_file():
                    f.unlink()

                elif f.is_dir():

                    for sub in f.rglob("*"):
                        if sub.is_file():
                            sub.unlink()

                    for sub in reversed(list(f.rglob("*"))):
                        if sub.is_dir():
                            sub.rmdir()

                    f.rmdir()

            except Exception as e:
                print(f"[WARN] impossibile eliminare {f}: {e}")

    else:

        path.mkdir(parents=True, exist_ok=True)

# ==========================================================
# INIT EXTRACTION
# ==========================================================

def get_init(problem_file: Path):

    lines = problem_file.read_text().splitlines()

    inside = False
    init = []

    for l in lines:

        s = l.strip()

        if "(:init" in s:
            inside = True
            continue

        if inside and s.startswith("(:goal"):
            break

        if inside:
            init.append(s)

    return init

# ==========================================================
# RENDERER IMPORT
# ==========================================================

def load_renderer(init_lines):

    try:

        from PE_IM_plan_render import SemanticPlanRenderer

        return SemanticPlanRenderer(init_lines)

    except Exception as e:

        print("[WARN] Renderer non trovato:", e)

        return None

# ==========================================================
# PLAN PARSER
# ==========================================================

def parse_plan(plan_file: Path, renderer=None):

    text = plan_file.read_text().strip()

    if not text:
        print("[ERROR] PLAN VUOTO")
        return

    steps = []

    for line in text.splitlines():

        line = line.strip()

        if not line or line.startswith(";"):
            continue

        line = re.sub(r"^[0-9\.]+\:\s*", "", line)

        line = line.replace("(", "")
        line = line.replace(")", "")

        steps.append(line)

    if renderer:
        steps = renderer.render(steps)

    print("\nPLAN")
    print("-" * 50)

    for i, s in enumerate(steps, 1):
        print(f"{i:02} {s}")

    print(f"\n[PLAN LENGTH]: {len(steps)}")

# ==========================================================
# RUN PLANNER
# ==========================================================

def run_planner(problem_name, problem_file, strategy):

    print("\n" + "=" * 60)
    print(f"PROBLEM : {problem_name}")
    print(f"STRATEGY: {strategy}")
    print("=" * 60)

    plan_dir = PLANS_BASE / problem_name
    log_dir = LOGS_BASE / problem_name

    plan_file = plan_dir / f"{strategy}.txt"
    log_file = log_dir / f"{strategy}.log"

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

    start = time.time()

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    elapsed = time.time() - start

    # ======================================================
    # SAVE LOG
    # ======================================================

    log_file.write_text(

        "COMMAND:\n"
        + " ".join(cmd)

        + "\n\n"

        + "STDOUT:\n"
        + result.stdout

        + "\n\nSTDERR:\n"
        + result.stderr
    )

    print(f"\nExecution time: {elapsed:.2f}s")

    if not plan_file.exists():
        print("[ERROR] PLAN FILE NON CREATO")
        return None

    if plan_file.stat().st_size == 0:
        print("[WARN] PLAN FILE VUOTO")
        return None

    return plan_file

# ==========================================================
# EXECUTE
# ==========================================================

def execute(problem_name, problem_file, strategy):

    plan_file = run_planner(
        problem_name,
        problem_file,
        strategy
    )

    if not plan_file:
        return

    init_lines = get_init(problem_file)

    renderer = load_renderer(init_lines)

    parse_plan(plan_file, renderer)

# ==========================================================
# MAIN
# ==========================================================

def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    ensure_clean_dir(PLANS_BASE)
    ensure_clean_dir(LOGS_BASE)

    for pname, pfile in PROBLEMS.items():

        print("\n" + "#" * 60)
        print(f"RUNNING PROBLEM: {pname}")
        print("#" * 60)

        problem_plan_dir = PLANS_BASE / pname
        problem_log_dir = LOGS_BASE / pname

        ensure_clean_dir(problem_plan_dir)
        ensure_clean_dir(problem_log_dir)

        problem_plan_dir.mkdir(parents=True, exist_ok=True)
        problem_log_dir.mkdir(parents=True, exist_ok=True)

        for strat in PLANNERS:

            try:

                execute(
                    pname,
                    pfile,
                    strat
                )

            except Exception as e:

                print("\n[FATAL ERROR]")
                print("problem :", pname)
                print("strategy:", strat)
                print("error   :", e)

# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()