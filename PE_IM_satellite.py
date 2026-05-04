# ==========================================================
# FILE: PE_IM_satellite.py
# ==========================================================
"""
Satellite search problem.

State layout:
(
    position,
    orientation,
    charge,
    memory,
    sent
)

memory stores tuples of the form:
    (object_name, quality)
"""

from search import Problem

from PE_IM_utils import (
    COST_ROTATE,
    COST_TAKEPIC,
    COST_SEND,
    MAX_PHOTOS,
    normalize_photo_quality,
    memory_usage,
    can_store_photo,
    rotate_left,
    rotate_right,
)


class Satellite(Problem):

    DEBUG = False

    # ======================================================
    # CONSTRUCTOR
    # ======================================================
    def __init__(self, initial, goal, scenario=None):
        self._goal = tuple(goal)
        self.goal = self._goal
        self.objects = initial["objects"]
        self.scenario = scenario
        self.nodes_generated = 0
        self.nodes_expanded = 0

        initial_state = (
            initial["position"],
            initial["position"],
            initial["charge"],
            tuple(),
            tuple(),
        )

        super().__init__(initial_state)

    # ======================================================
    # SUPPORT HELPERS
    # ======================================================
    def photo_quality_for(self, obj):
        """Return the deterministic photo quality for an object."""
        # Search for explicit quality in the objects map
        for items in self.objects.values():
            for entry in items:
                if isinstance(entry, dict):
                    if entry.get("name") == obj:
                        return normalize_photo_quality(entry.get("quality", "SD"))
                elif isinstance(entry, (tuple, list)) and len(entry) == 2:
                    if entry[0] == obj:
                        return normalize_photo_quality(entry[1])
                elif entry == obj:
                    break

        # Default fallback
        return "SD"

    def _object_name(self, entry):
        if isinstance(entry, dict):
            return entry.get("name")
        if isinstance(entry, (tuple, list)) and len(entry) == 2:
            return entry[0]
        return entry

    def visible_objects(self, orientation):
        return self.objects.get(orientation, [])

    def build_state(self, position, orientation, charge, memory, sent):
        return (position, orientation, charge, tuple(memory), tuple(sent))

    def memory_used(self, memory):
        return memory_usage(memory)

    # ======================================================
    # ACTIONS(state)
    # ======================================================
    def actions(self, state):
        self.nodes_expanded += 1

        position, orientation, charge, memory, sent = state
        memory = list(memory)
        sent = list(sent)
        acts = []

        if charge >= COST_ROTATE:
            acts.append(("RL",))
            acts.append(("RR",))

        if charge >= COST_TAKEPIC and len(memory) < MAX_PHOTOS:
            visible = self.visible_objects(orientation)
            for entry in visible:
                obj = self._object_name(entry)
                if obj in sent:
                    continue
                if any(photo_obj == obj for photo_obj, _ in memory):
                    continue
                quality = self.photo_quality_for(obj)
                if can_store_photo(memory, quality):
                    acts.append(("TAKEPIC", obj))

        if orientation == "N" and len(memory) > 0 and charge >= COST_SEND:
            acts.append(("SEND",))

        return acts

    # ======================================================
    # RESULT(state, action)
    # ======================================================
    def result(self, state, action):
        self.nodes_generated += 1

        position, orientation, charge, memory, sent = state
        memory = list(memory)
        sent = list(sent)

        match action:
            case ("RL",):
                orientation = rotate_left(orientation)
                charge -= COST_ROTATE

            case ("RR",):
                orientation = rotate_right(orientation)
                charge -= COST_ROTATE

            case ("TAKEPIC", obj):
                quality = self.photo_quality_for(obj)
                if can_store_photo(memory, quality):
                    memory.append((obj, quality))
                charge -= COST_TAKEPIC

            case ("SEND",):
                if orientation == "N" and memory:
                    obj, _quality = memory.pop(0)
                    if obj not in sent:
                        sent.append(obj)
                charge -= COST_SEND

        return self.build_state(position, orientation, charge, memory, sent)

    # ======================================================
    # GOAL TEST
    # ======================================================
    def goal_test(self, state):
        _, _, _, _, sent = state
        return set(self._goal).issubset(set(sent))

    # ======================================================
    # PATH COST
    # ======================================================
    def path_cost(self, c, state1, action, state2):
        match action:
            case ("RL",) | ("RR",):
                return c + COST_ROTATE
            case ("TAKEPIC", _):
                return c + COST_TAKEPIC
            case ("SEND",):
                return c + COST_SEND

