# Project Changes and Architecture

## Overview

This document explains what was changed in the project and why.

## Problem

The project was transitioning from state-space search to PDDL-based planning. The PDDL model had synchronization issues that prevented the planner from working correctly.

## Changes Made

### 1. Fixed PDDL Model (domain.pddl and problem files)

**Problem:** 
- Directions were declared in both `domain.pddl` (`:constants`) AND in every `problem_*.pddl` file (`:objects`)
- Fast Downward translator failed with "Undefined object: N" error
- This is because a constant should not be redeclared as an object

**Solution:**
- Removed all direction declarations from problem files
- Kept single definition in `domain.pddl` `:constants` section
- Now directions are the single source of truth

**Files changed:**
- `domain.pddl` - No changes needed (already correct)
- `problem_easy.pddl` - Removed direction objects
- `problem_medium.pddl` - Removed direction objects
- `problem_hard.pddl` - Removed direction objects
- `problem_hardHD.pddl` - Removed direction objects
- `problem_extreme.pddl` - Removed direction objects

### 2. Created Animation Framework (animations/ package)

**Why:**
- Need visual representation of plans
- Using planimation approach: parse → simulate → render

**What was created:**

#### Core Files:
- `animations/__init__.py` - Package exports
- `animations/core.py` (~280 lines)
  - `SatelliteState` dataclass - Tracks satellite state
  - `ActionStep` dataclass - Parsed action from plan
  - `Frame` dataclass - Snapshot of world state
  - `parse_action_step()` - Converts raw plan text to structured action
  - `normalize_plan_source()` - Handles multiple input formats
  - `apply_action()` - Core state transition logic (implements 6 PDDL actions)
  - `build_frames()` - Generates sequence of frames from plan
  - `render_frames()` - Pretty-prints animation to console
  - `export_planimation()` - Saves frames as JSON

- `animations/problems.py` (~90 lines)
  - `ProblemConfig` dataclass - Problem metadata
  - `PROBLEMS` dict - Configs for all 5 problems
  - `get_problem_config()` - Lookup by problem key

- `animations/animate_easy.py`, `animate_medium.py`, `animate_hard.py`, `animate_hardHD.py`, `animate_extreme.py`
  - Per-problem entry points
  - Can run directly: `python3 animations/animate_easy.py`
  - Needed bootstrap code to handle Python import paths correctly

- `animations/generate_planimation.py` (~60 lines)
  - CLI tool for exporting animations
  - Usage: `python3 animations/generate_planimation.py easy sas_plan --output easy.json`

- `animations/README.md`
  - Simple user guide for animations

## How It Works

### 1. Planning Phase
```
python3 PE_IM_planner_runner.py problem_easy.pddl
↓
Fast Downward generates sas_plan
```

### 2. Animation Phase
```
sas_plan (raw action list)
↓
parse_action_step() - Convert each line to ActionStep
↓
build_frames() - Simulate state changes
↓
SatelliteState objects track:
  - direction (N, NE, E, SE, S, SW, W, NW)
  - stored photos (with quality and direction)
  - sent photos
  - memory usage (0-100 bytes)
  - slot usage (0-2 slots)
↓
Frame objects created with snapshots
↓
render_frames() - Display to console
export_planimation() - Save to JSON
```

## Key Design Decisions

### 1. Single Source of Truth for Directions
- Directions defined only in `domain.pddl` `:constants`
- Problem files don't redeclare them
- Prevents conflicts with planner translator

### 2. Per-Problem Entry Points
- Each problem has its own `animate_*.py` file
- Allows problem-specific configuration without factory pattern complexity
- Trade-off: small code duplication vs better clarity

### 3. Shared Core Engine
- All problems use same `core.py` simulation logic
- `problems.py` holds metadata only
- Easy to extend to new problems

### 4. State Simulation Approach
- Each frame computed independently using `copy.deepcopy()`
- Immutable snapshots prevent mutation bugs
- Can replay from JSON without rerunning planner

### 5. Flexible Input Handling
- `normalize_plan_source()` handles:
  - File paths: `"sas_plan"`
  - List of strings: `["(action1)", "(action2)"]`
  - JSON objects: Already-parsed action dicts
- Supports multiple output formats from Fast Downward


## Actions Implemented

The animation engine understands all 6 actions in the domain:

1. **turn-right** - Rotate 45° clockwise
   - Changes direction
   - No state cost

2. **turn-left** - Rotate 45° counter-clockwise
   - Changes direction
   - No state cost

3. **take-picture-hd** - Capture high-definition photo
   - Stores in memory (80 bytes)
   - Uses 1 slot
   - Requires matching direction

4. **take-picture-sd** - Capture standard-definition photo
   - Stores in memory (40 bytes)
   - Uses 1 slot
   - Requires matching direction

5. **send-hd** - Transmit HD photo to ground
   - Frees 80 bytes memory
   - Frees 1 slot
   - Moves photo to "sent" list

6. **send-sd** - Transmit SD photo to ground
   - Frees 40 bytes memory
   - Frees 1 slot
   - Moves photo to "sent" list

## State Display Format

Each frame shows:
```
Direction: N                # Current orientation
Stored: star1:HD@N         # Photos in memory (object:quality@direction)
Sent: star2:SD@S           # Transmitted photos
Memory: 80/100             # Used / Total bytes
Slots: 1/2                 # Used / Available slots
```

## JSON Export Format

Plans are exported as JSON for replay without replanning:

```json
{
  "metadata": {
    "problem": "problem_easy.pddl",
    "title": "EASY mission"
  },
  "frames": [
    {
      "step_index": 0,
      "action": null,
      "state": {
        "direction": "N",
        "memory_used": 0,
        "memory_total": 100,
        "slots_used": 0,
        "slot_total": 2,
        "stored": [],
        "sent": []
      },
      "note": "initial state"
    },
    {
      "step_index": 1,
      "action": {
        "name": "take-picture-hd",
        "args": ["star1", "N"],
        "raw": "(take-picture-hd star1 N)"
      },
      "state": {...},
      "note": "stored star1 as HD photo"
    }
  ]
}
```

## Next Steps

To use the system:

1. **Generate a plan:**
   ```bash
   ./downward/fast-downward.py domain.pddl problem_easy.pddl --search "astar(lmcut())"
   ```

2. **Animate the plan:**
   ```bash
   python3 animations/generate_planimation.py easy sas_plan
   ```

3. **Export to JSON (optional):**
   ```bash
   python3 animations/generate_planimation.py easy sas_plan --output easy.json
   ```

## Testing

Basic smoke tests in `planimation_tests/test_planimation.py` verify:
- Module imports work
- Plan parsing handles various formats
- State updates are correct
- JSON export produces valid output

Run with: `python3 -m pytest planimation_tests/`

## Architecture Rationale

### Why separate core and per-problem files?
- **core.py**: Reusable simulation logic, no problem-specific code
- **animate_*.py**: Entry points that know about specific problems
- Allows different rendering strategies per problem without forcing inheritance
- Easier to understand than factory pattern

### Why immutable frame snapshots?
- State mutations are hard to debug
- `copy.deepcopy()` ensures independence
- Can implement "rewind" feature later
- Suitable for JSON serialization

### Why JSON export?
- Can replay without running planner
- Enables GUI/web tools to visualize animations
- No dependency on Fast Downward for visualization
- Easy to store and version control

## Future Enhancements

Possible improvements:
- Batch runner script to plan all problems at once
- Web UI for planimation playback with interactive timeline
- Comparison view for multiple plan solutions
- Export to animated GIF or video
- Performance metrics (total time, actions, memory usage)
- Custom rendering templates per problem

