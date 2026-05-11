"""Planner runner for satellite planning problems.

Runs ENHSP on all problems in problems/ directory iteratively.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from PE_IM_animation import animate_plan
from PE_IM_parser import parse_plan


DOMAIN = "domain.pddl"
DEFAULT_PROBLEM = "problem_easy.pddl"
PLAN_DIR = Path("plans")
PROBLEMS_DIR = Path("problems")

PLANNERS = {
    "wastar": "WAStar",
    "greedy": "gbfs",
}


def _problem_key(problem_path: str) -> str:
    name = Path(problem_path).stem
    return name.replace("problem_", "")


def _plan_file(problem_path: str, strategy: str) -> Path:
    PLAN_DIR.mkdir(parents=True, exist_ok=True)
    return PLAN_DIR / f"plan_{_problem_key(problem_path)}_{strategy}.txt"


def run_planner(strategy: str = "wastar", problem: str = DEFAULT_PROBLEM) -> tuple[bool, Path]:
    """Run ENHSP for one problem/strategy pair."""

    print("\n########################################")
    print(f"PLANNER: ENHSP ({strategy})")
    print(f"PROBLEM: {problem}")
    print("########################################")

    search_algo = PLANNERS[strategy]
    plan_file = _plan_file(problem, strategy)

    command = [
        "java",
        "-jar", "enhsp-20.jar",
        "-o", DOMAIN,
        "-f", problem,
        "-s", search_algo,
        "-sp", str(plan_file)
    ]

    print("\nESECUZIONE:", " ".join(command))

    result = subprocess.run(command, capture_output=True, text=True)

    if "Problem unsolvable" in result.stdout or result.returncode != 0:
        print("\n❌ Planner fallito")
        print("\n".join(result.stdout.splitlines()[-15:]))
        return False, plan_file

    if not plan_file.exists():
        print(f"\n❌ File {plan_file} not created")
        print(result.stdout)
        return False, plan_file

    print(f"✅ Plan saved to: {plan_file}")

    return True, plan_file


def _discover_problems() -> list[Path]:
    """Find all problem_*.pddl files in problems/ directory."""
    if not PROBLEMS_DIR.exists():
        print(f"❌ Directory {PROBLEMS_DIR} not found!")
        return []

    problems = sorted(PROBLEMS_DIR.glob("problem_*.pddl"))
    if not problems:
        print(f"❌ No problem_*.pddl files found in {PROBLEMS_DIR}/")
        return []

    print(f"✅ Found {len(problems)} problems:")
    for p in problems:
        print(f"   - {p.name}")

    return problems


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run ENHSP on all problems.")
    parser.add_argument(
        "problem",
        nargs="?",
        default=None,
        help="Single problem (e.g. problem_easy.pddl); if not specified, runs all in problems/",
    )
    parser.add_argument(
        "--strategy",
        choices=tuple(PLANNERS.keys()) + ("all",),
        default="all",
        help="Strategy to run (default: all)",
    )
    return parser


def main(argv: list[str] | None = None):
    args = build_arg_parser().parse_args(argv)

    # Decide which problems to run
    if args.problem:
        # Single problem specified
        if not args.problem.startswith("problems/"):
            args.problem = f"problems/{args.problem}"
        problems_to_run = [args.problem]
    else:
        # Auto-discover all problems in problems/
        discovered = _discover_problems()
        problems_to_run = [str(p) for p in discovered]

    if not problems_to_run:
        print("❌ No problems to run!")
        return

    print(f"\n{'='*60}")
    print(f"Running {len(problems_to_run)} problem(s)")
    print(f"{'='*60}\n")

    # Run each problem with all strategies
    for problem in problems_to_run:
        print(f"\n{'='*60}")
        print(f"PROBLEM: {Path(problem).name}")
        print(f"{'='*60}")

        strategies = PLANNERS.keys() if args.strategy == "all" else (args.strategy,)

        for strategy in strategies:
            ok, plan_file = run_planner(strategy, problem)
            if not ok:
                continue

            plan = parse_plan(plan_file)
            if not plan:
                print(f"[MAIN] No plan in {plan_file}\n")
                continue

            print("\nPLAN:\n")
            for p in plan:
                print(p)

            animate_plan(plan)

    print(f"\n{'='*60}")
    print("✅ All done!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()