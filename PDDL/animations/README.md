# Planimation - Animation Framework

Visualize satellite planning solutions with step-by-step animations.

## Quick Start

View animation for a problem after planning:
```bash
python3 animations/generate_planimation.py easy sas_plan
```

Export as JSON:
```bash
python3 animations/generate_planimation.py easy sas_plan --output easy.json
```

## Usage

```bash
python3 animations/generate_planimation.py [PROBLEM] [PLAN_FILE] [OPTIONS]
```

**Problems:** `easy`, `medium`, `hard`, `hardHD`, `extreme`

**Options:**
- `--output PATH` - Save animation as JSON
- `--no-render` - Export without displaying
- `--delay SECONDS` - Delay between frames (default: 0)

## How It Works

1. **Parse** - Read plan file from Fast Downward
2. **Simulate** - Apply each action to satellite state
3. **Display** - Show each step with resulting state
4. **Export** - Save as JSON for later use

## State Display

Each frame shows:
- **Direction** - Satellite orientation (N, NE, E, SE, S, SW, W, NW)
- **Stored** - Photos in memory
- **Sent** - Photos transmitted
- **Memory** - Used / Total (0-100 bytes)
- **Slots** - Used slots (0-2)

## Actions

- `turn-right` / `turn-left` - Rotate 45°
- `take-picture-hd` - Capture HD photo (80 memory)
- `take-picture-sd` - Capture SD photo (40 memory)
- `send-hd` / `send-sd` - Transmit photo

## Files

- `core.py` - State simulation and rendering
- `problems.py` - Problem metadata
- `animate_*.py` - Per-problem entry points
- `generate_planimation.py` - CLI tool

