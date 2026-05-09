"""CLI utility to export a planimation file for a chosen problem."""

from __future__ import annotations

if __package__ is None or __package__ == "":
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
from pathlib import Path

from animations.core import build_frames, export_planimation, render_frames
from animations.problems import PROBLEM_KEYS, get_problem_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a planimation file from a plan.")
    parser.add_argument("problem", choices=PROBLEM_KEYS, help="Problem key to animate")
    parser.add_argument("plan_file", help="Path to sas_plan or another plan file")
    parser.add_argument(
        "--output",
        help="Path to the exported planimation JSON file",
        default=None,
    )
    parser.add_argument(
        "--no-render",
        action="store_true",
        help="Export the JSON file without printing the animation",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="Optional delay in seconds between frames when rendering",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = get_problem_config(args.problem)
    frames = build_frames(args.plan_file, config)

    output_path = args.output
    if output_path is None:
        output_path = Path("planimation_exports") / f"{config.problem_file}.json"

    export_planimation(frames, config, output_path)

    if not args.no_render:
        render_frames(frames, config, delay=args.delay)

    print(f"\nExported planimation to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
