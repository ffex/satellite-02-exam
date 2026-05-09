# Plan for PDDL animation with planimation

## Goal

Build a separate animation layer for each `problem_*.pddl` file, using a planimation-style workflow:

`Fast Downward` → `sas_plan` → parser/normalizer → problem-specific animation module → rendered frames

The result should be a set of animation files that are easy to extend and easy to compare across problems.

## File structure we want

```text
animations/
  __init__.py
  core.py
  problems.py
  animate_easy.py
  animate_medium.py
  animate_hard.py
  animate_hardHD.py
  animate_extreme.py
  generate_planimation.py
  README.md
```

## What each file does

### `animations/core.py`
Shared satellite-state simulation and frame rendering:
- current direction
- stored photos
- sent photos
- memory usage
- slot usage
- step-by-step frame generation

### `animations/problems.py`
Problem metadata:
- initial orientation
- target quality mix
- display title
- problem name
- scenario description

### `animations/animate_easy.py`
Dedicated animation entry point for `problem_easy.pddl`.

### `animations/animate_medium.py`
Dedicated animation entry point for `problem_medium.pddl`.

### `animations/animate_hard.py`
Dedicated animation entry point for `problem_hard.pddl`.

### `animations/animate_hardHD.py`
Dedicated animation entry point for `problem_hardHD.pddl`.

### `animations/animate_extreme.py`
Dedicated animation entry point for `problem_extreme.pddl`.

### `animations/generate_planimation.py`
CLI utility that reads a plan and produces a reusable planimation file, so the animation can be replayed later without rerunning the planner.

## Expected workflow

1. Run the planner.
2. Save the generated plan in `sas_plan`.
3. Convert the raw plan into a structured animation model.
4. Render the animation for the chosen problem.
5. Optionally export the frames to a file for replay.

## What the animation should show

For every step, the animation should print or export:
- step number
- action name
- action arguments
- current orientation
- stored photos
- sent photos
- memory state
- slot state
- a small problem-specific header

## Important design rule

Each problem should have its own animation module, but all modules should reuse the same simulation core.

That gives us:
- one common engine
- five problem-specific entry points
- consistent output format
- easier debugging

## Suggested commit stages

### Stage 1: define the contract
- create this document
- decide file layout
- agree on state fields and rendering format

Commit message:
`docs(animation): define planimation workflow`

### Stage 2: add the shared animation core
- create `animations/core.py`
- create `animations/problems.py`
- create problem-specific modules
- add a generator/replay utility

Commit message:
`feat(animation): add planimation core and per-problem modules`

### Stage 3: add tests
- verify all animation modules import
- verify the core builds frames from a sample plan
- verify each problem file maps to the correct module

Commit message:
`test(animation): add planimation smoke tests`

## Notes

This stage does **not** change the planner or parser yet.
It only defines the animation architecture so the next commits can be implemented safely.

