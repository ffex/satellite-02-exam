"""Planimation entry point for problem_hard.pddl."""

from __future__ import annotations

if __package__ is None or __package__ == "":
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parents[1]))

from animations.core import build_frames, render_frames
from animations.problems import get_problem_config

PROBLEM_KEY = "hard"


def animate(plan_source="sas_plan", export_path=None, delay: float = 0.0):
    config = get_problem_config(PROBLEM_KEY)
    frames = build_frames(plan_source, config)
    if export_path is not None:
        from animations.core import export_planimation

        export_planimation(frames, config, export_path)
    render_frames(frames, config, delay=delay)
    return frames


def main():
    animate()


if __name__ == "__main__":
    main()
