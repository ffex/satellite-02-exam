import os
import re
import sys
import shutil
import subprocess
import time
from pathlib import Path


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DOMAIN_FILE = BASE_DIR / "domain.pddl"
PROBLEMS_DIR = BASE_DIR / "Problems"

OUTPUT_DIR = BASE_DIR / "output"
PLANS_BASE = OUTPUT_DIR / "generated_plans"
LOGS_BASE = OUTPUT_DIR / "planner_logs"


PROBLEMS = {
    "easy":    PROBLEMS_DIR / "problem_easy.pddl",
    "medium":  PROBLEMS_DIR / "problem_medium.pddl",
    "hard":    PROBLEMS_DIR / "problem_hard.pddl",
    "hard_hd": PROBLEMS_DIR / "problem_hard_hd.pddl",
    "extreme": PROBLEMS_DIR / "problem_extreme.pddl",
}


# ==========================================================
# LAPKT SETUP
# ==========================================================

LAPKT_DLL_DIR = None

if os.name == "nt":
    try:
        import lapkt as _probe_lapkt
        cand = Path(_probe_lapkt.__file__).parent / "core" / "lib"
        if cand.exists():
            LAPKT_DLL_DIR = str(cand)
            os.add_dll_directory(LAPKT_DLL_DIR)
    except Exception as e:
        print(f"[WARN] DLL setup lapkt fallito: {e}")


def detect_lapkt_cmd():
    for name in ("lapkt_cmd.exe", "lapkt_cmd", "lapkt_cmd.py"):
        found = shutil.which(name)
        if found:
            return found

    scripts = Path(sys.executable).parent / "Scripts"
    for name in ("lapkt_cmd.exe", "lapkt_cmd.py"):
        cand = scripts / name
        if cand.exists():
            return str(cand)

    return "lapkt_cmd.py"


LAPKT_CMD = detect_lapkt_cmd()


def detect_lapkt_python():
    py = shutil.which("py.exe") or shutil.which("py")
    if py:
        return [py]
    return [sys.executable]


LAPKT_PYTHON = detect_lapkt_python()


# ==========================================================
# STRATEGIES
# ==========================================================

PLANNERS = {
    "k_bfws": "k-BFWS",
    "dual_bfws": "DUAL-BFWS",
    "bfws_f5": "BFWS-f5",
    "bfws_f5_landmarks": "BFWS-f5-landmarks",
    "bfws_goalcount": "BFWS-goalcount-only",
}

RUN_TIMEOUT = 120


# ==========================================================
# FILESYSTEM
# ==========================================================

def ensure_clean_dir(path: Path):
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True, exist_ok=True)


# ==========================================================
# PDDL PARSER (UNCHANGED)
# ==========================================================

def get_init(problem_file: Path):
    lines = problem_file.read_text(encoding="utf-8").splitlines()
    inside, init = False, []
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


def load_renderer(init_lines):
    try:
        from PE_IM_plan_render import SemanticPlanRendererBFWSv3
        return SemanticPlanRendererBFWSv3(init_lines)
    except Exception as e:
        print("[WARN] Renderer v3 non trovato:", e)
        return None


def parse_plan(plan_file: Path, renderer=None):
    text = plan_file.read_text(encoding="utf-8").strip()
    if not text:
        print("[ERROR] PLAN VUOTO")
        return

    steps = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        line = re.sub(r"^[0-9\.]+\s*[:\.]\s*", "", line)
        line = line.replace("(", "").replace(")", "").strip()
        if line:
            steps.append(line)

    if not steps:
        print("[ERROR] PLAN SENZA AZIONI")
        return

    if renderer:
        steps = renderer.render(steps)

    print("\nPLAN")
    print("-" * 50)
    for i, s in enumerate(steps, 1):
        print(f"{i:02} {s}")
    print(f"\n[PLAN LENGTH]: {len(steps)}")


# ==========================================================
# LAPKT COMMAND
# ==========================================================

def build_command(problem_file: Path, search_type: str,
                  plan_file: Path, log_file: Path):

    # FORZATO python + script (evita WinError 193)
    cmd = [
        *LAPKT_PYTHON,
        str(LAPKT_CMD),
        "BFWS",
        "--domain", str(DOMAIN_FILE),
        "--problem", str(problem_file),
        "--plan_file", str(plan_file),
        "--log_file", str(log_file),
        "--search_type", search_type,
    ]

    return cmd


# ==========================================================
# CORE EXECUTION
# ==========================================================

def run_planner(problem_name, problem_file, strategy):

    print("\n" + "=" * 60)
    print(f"PROBLEM : {problem_name}")
    print(f"STRATEGY: {strategy}")
    print("=" * 60)

    plan_dir = PLANS_BASE / problem_name
    log_dir = LOGS_BASE / problem_name

    plan_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    plan_file = plan_dir / f"{strategy}.txt"
    log_file = log_dir / f"{strategy}.log"

    cmd = build_command(problem_file, PLANNERS[strategy], plan_file, log_file)

    env = os.environ.copy()
    if LAPKT_DLL_DIR:
        env["PATH"] = LAPKT_DLL_DIR + os.pathsep + env.get("PATH", "")

    start = time.time()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT,
            env=env,
        )

        elapsed = time.time() - start

        with open(log_file, "a", encoding="utf-8") as f:
            f.write("\n\nCOMMAND:\n")
            f.write(" ".join(cmd))
            f.write("\n\n===== STDOUT =====\n")
            f.write(result.stdout or "")
            f.write("\n===== STDERR =====\n")
            f.write(result.stderr or "")
            f.write(f"\n===== exit_code={result.returncode} time={elapsed:.2f}s =====\n")

        print(f"\nExecution time: {elapsed:.2f}s")

        if result.returncode != 0:
            print("[WARN] BFWS errore. Vedi log:", log_file)
            return None

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        print(f"[TIMEOUT] dopo {elapsed:.1f}s")
        return None

    except Exception as e:
        print("\n[DEBUG EXCEPTION]")
        print(e)
        raise

    if not plan_file.exists() or plan_file.stat().st_size == 0:
        print("[ERROR] PLAN NON GENERATO")
        return None

    return plan_file


# ==========================================================
# EXECUTE
# ==========================================================

def execute(problem_name, problem_file, strategy):
    plan_file = run_planner(problem_name, problem_file, strategy)
    if not plan_file:
        return

    init_lines = get_init(problem_file)
    renderer = load_renderer(init_lines)

    parse_plan(plan_file, renderer)


# ==========================================================
# MAIN
# ==========================================================

def main():

    print(f"LAPKT_CMD   : {LAPKT_CMD}")
    print(f"LAPKT_PYTHON: {' '.join(LAPKT_PYTHON)}")
    print(f"DOMAIN      : {DOMAIN_FILE}")

    ensure_clean_dir(PLANS_BASE)
    ensure_clean_dir(LOGS_BASE)

    for pname, pfile in PROBLEMS.items():

        print("\n" + "#" * 60)
        print(f"RUNNING PROBLEM: {pname}")
        print("#" * 60)

        for strat in PLANNERS:
            try:
                execute(pname, pfile, strat)
            except Exception as e:
                print("\n[FATAL ERROR]")
                print("problem :", pname)
                print("strategy:", strat)
                print("error   :", e)

    print("\n[DONE] Output in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()