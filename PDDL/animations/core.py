"""Shared planimation core for satellite animations."""

from __future__ import annotations

import copy
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from PE_IM_utils import DIRECTIONS, HD_MEM_COST, MAX_MEMORY, MEM_SLOT_MAX, SD_MEM_COST


_ACTION_RE = re.compile(r"\(([^()]+)\)")


@dataclass(frozen=True)
class ActionStep:
    name: str
    args: tuple[str, ...] = ()
    raw: str = ""


@dataclass
class PhotoRecord:
    object_name: str
    quality: str
    direction: str | None = None
    memory_cost: int = 0


@dataclass
class SatelliteState:
    direction: str
    memory_total: int = MAX_MEMORY
    slot_total: int = MEM_SLOT_MAX
    stored: list[PhotoRecord] = field(default_factory=list)
    sent: list[PhotoRecord] = field(default_factory=list)

    @property
    def memory_used(self) -> int:
        return sum(photo.memory_cost for photo in self.stored)

    @property
    def slots_used(self) -> int:
        return len(self.stored)


@dataclass
class Frame:
    step_index: int
    action: ActionStep | None
    state: SatelliteState
    note: str = ""


def _normalize_symbol(token: str) -> str:
    text = token.strip().strip(")(")
    if text.upper() in DIRECTIONS:
        return text.upper()
    return text


def parse_action_step(raw_step) -> ActionStep | None:
    if raw_step is None:
        return None

    if isinstance(raw_step, ActionStep):
        return raw_step

    if isinstance(raw_step, Mapping):
        name = str(raw_step.get("name", "")).strip()
        if not name:
            return None
        args = tuple(_normalize_symbol(str(arg)) for arg in raw_step.get("args", ()))
        raw = str(raw_step.get("raw", "")).strip()
        return ActionStep(name=name, args=args, raw=raw or f"({name} {' '.join(args)})".strip())

    text = str(raw_step).strip()
    if not text or text.startswith(";"):
        return None

    match = _ACTION_RE.search(text)
    if match:
        parts = match.group(1).split()
    else:
        parts = text.split()
        if parts and parts[0].endswith(":"):
            parts = parts[1:]

    if not parts:
        return None

    name = parts[0]
    args = tuple(_normalize_symbol(arg) for arg in parts[1:])
    return ActionStep(name=name, args=args, raw=text)


def normalize_plan_source(plan_source) -> list[ActionStep]:
    if isinstance(plan_source, (str, Path)):
        path = Path(plan_source)
        if path.exists():
            raw_lines = path.read_text().splitlines()
        else:
            raw_lines = str(plan_source).splitlines()
        items = raw_lines
    else:
        items = plan_source

    steps: list[ActionStep] = []
    for item in items:
        step = parse_action_step(item)
        if step is not None:
            steps.append(step)
    return steps


def _find_candidate(stored: list[PhotoRecord], object_name: str | None, quality: str | None) -> PhotoRecord | None:
    for photo in stored:
        if object_name is not None and photo.object_name != object_name:
            continue
        if quality is not None and photo.quality != quality:
            continue
        return photo
    return None


def apply_action(state: SatelliteState, action: ActionStep) -> str:
    name = action.name.lower()
    args = tuple(action.args)

    if name in {"rotate-right", "rotate-left"}:
        if len(args) >= 2:
            state.direction = _normalize_symbol(args[1])
            return f"rotated to {state.direction}"
        if len(args) == 1:
            state.direction = _normalize_symbol(args[0])
            return f"rotated to {state.direction}"
        return "rotation kept the current direction"

    if name in {"take-picture-hd", "take-picture-sd"}:
        quality = "HD" if "hd" in name else "SD"
        object_name = args[0] if args else "?"
        direction = _normalize_symbol(args[1]) if len(args) > 1 else state.direction
        memory_cost = HD_MEM_COST if quality == "HD" else SD_MEM_COST
        if state.slots_used >= state.slot_total:
            return "cannot take picture: all slots are busy"
        photo = PhotoRecord(
            object_name=object_name,
            quality=quality,
            direction=direction,
            memory_cost=memory_cost,
        )
        state.stored.append(photo)
        return f"stored {object_name} as {quality} photo"

    if name in {"send-hd", "send-sd", "send-photo"}:
        quality = None
        if "hd" in name:
            quality = "HD"
        elif "sd" in name:
            quality = "SD"
        object_name = args[0] if args else None
        photo = _find_candidate(state.stored, object_name, quality)
        if photo is None:
            return "nothing to send"
        state.stored.remove(photo)
        state.sent.append(photo)
        return f"sent {photo.object_name}"

    return "action not modeled in planimation core"


def build_frames(plan_source, config) -> list[Frame]:
    steps = normalize_plan_source(plan_source)
    state = SatelliteState(
        direction=_normalize_symbol(config.initial_direction),
        memory_total=config.memory_total,
        slot_total=config.slot_total,
    )
    frames: list[Frame] = [Frame(step_index=0, action=None, state=copy.deepcopy(state), note="initial state")]

    for index, action in enumerate(steps, 1):
        note = apply_action(state, action)
        frames.append(Frame(step_index=index, action=action, state=copy.deepcopy(state), note=note))

    return frames


def _format_photos(photos: Sequence[PhotoRecord]) -> str:
    if not photos:
        return "none"
    return ", ".join(
        f"{photo.object_name}:{photo.quality}@{photo.direction or '?'}"
        for photo in photos
    )


def render_frames(frames: Sequence[Frame], config, delay: float = 0.0) -> None:
    print("\n======================================")
    print(f"PLANIMATION: {config.title}")
    print("======================================")
    print(f"Problem file: {config.problem_file}")
    print(f"Scenario: {config.description}")

    for frame in frames:
        if frame.step_index == 0:
            print("\n--- INITIAL STATE ---")
        else:
            action_text = frame.action.raw or frame.action.name
            print(f"\n--- STEP {frame.step_index} ---")
            print(f"ACTION: {action_text}")
            print(f"NOTE: {frame.note}")

        print(f"Direction: {frame.state.direction}")
        print(f"Stored: {_format_photos(frame.state.stored)}")
        print(f"Sent: {_format_photos(frame.state.sent)}")
        print(f"Memory: {frame.state.memory_used}/{frame.state.memory_total}")
        print(f"Slots: {frame.state.slots_used}/{frame.state.slot_total}")

        if delay:
            import time

            time.sleep(delay)

    print("\nMISSION COMPLETE")


def export_planimation(frames: Sequence[Frame], config, output_path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "problem": config.problem_file,
        "title": config.title,
        "description": config.description,
        "initial_direction": config.initial_direction,
        "goal_objects": list(config.goal_objects),
        "frames": [
            {
                "step_index": frame.step_index,
                "action": None
                if frame.action is None
                else {
                    "name": frame.action.name,
                    "args": list(frame.action.args),
                    "raw": frame.action.raw,
                },
                "state": {
                    "direction": frame.state.direction,
                    "memory_total": frame.state.memory_total,
                    "memory_used": frame.state.memory_used,
                    "slot_total": frame.state.slot_total,
                    "slots_used": frame.state.slots_used,
                    "stored": [asdict(photo) for photo in frame.state.stored],
                    "sent": [asdict(photo) for photo in frame.state.sent],
                },
                "note": frame.note,
            }
            for frame in frames
        ],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return path

