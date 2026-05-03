# ==========================================================
# FILE: PE_IM_satellite.py
# ==========================================================
"""
SATELLITE SEARCH PROBLEM

STATE = (
    orientation,    # current satellite direction
    charge,         # remaining energy
    free_memory,    # available memory units
    memory,         # tuple of (name, quality) photographed but not sent
    sent            # tuple of (name, quality) already sent
)

CONSTRAINTS:
- TAKEPIC requires facing the object's direction and enough free memory
- SEND only allowed facing North
- every action consumes energy
"""

from search import Problem

from PE_IM_utils import (
    COST_ROTATE,
    COST_TAKEPIC,
    COST_SEND,
    MAX_MEMORY,
    HD_MEM_COST,
    SD_MEM_COST,
    rotate_left,
    rotate_right
)


class Satellite(Problem):

    DEBUG = False

    # ======================================================
    # COSTRUTTORE
    # ======================================================
    def __init__(self, initial, goal):
        """
        initial:
        {
            "position": "N",
            "charge": 8,
            "objects": {
                "E": ["star1"],
                "W": ["planet1"]
            }
        }

        goal: list of (name, quality) tuples
        [("star1", "HD"), ("planet1", "SD")]
        """

        self._goal = tuple(goal)
        self.goal  = self._goal

        # mappa spaziale degli oggetti
        self.objects = initial["objects"]

        # quick lookup: object name -> required quality
        self.goal_quality = {name: quality for name, quality in self._goal}

        # statistiche ricerca
        self.nodes_generated = 0
        self.nodes_expanded  = 0

        initial_state = (
            initial["position"],
            initial["charge"],
            MAX_MEMORY,
            tuple(),
            tuple()
        )

        super().__init__(initial_state)

    # ======================================================
    # FUNZIONE SUPPORTO
    # ======================================================
    def visible_objects(self, orientation):
        return self.objects.get(orientation, [])

    # ======================================================
    # BUILD STATE
    # ======================================================
    def build_state(self, orientation, charge, free_memory, memory, sent):
        return (
            orientation,
            charge,
            free_memory,
            tuple(memory),
            tuple(sent)
        )

    # ======================================================
    # ACTIONS(state)
    # ======================================================
    def actions(self, state):

        self.nodes_expanded += 1

        orientation, charge, free_memory, memory, sent = state

        memory = list(memory)
        sent   = list(sent)

        acts = []

        # --------------------------------------------------
        # 1) ROTAZIONI
        # --------------------------------------------------
        if charge >= COST_ROTATE:
            acts.append(("RL",))
            acts.append(("RR",))

        # --------------------------------------------------
        # 2) TAKEPIC
        # Quality is determined by the goal — no reason to
        # photograph at a quality that won't satisfy the goal.
        # --------------------------------------------------
        if charge >= COST_TAKEPIC:

            visible      = self.visible_objects(orientation)
            sent_names   = {item[0] for item in sent}
            memory_names = {item[0] for item in memory}

            for obj in visible:

                if obj in sent_names or obj in memory_names:
                    continue

                if obj not in self.goal_quality:
                    continue

                quality  = self.goal_quality[obj]
                mem_cost = HD_MEM_COST if quality == "HD" else SD_MEM_COST

                if free_memory >= mem_cost:
                    acts.append(("TAKEPIC", obj, quality))

        # --------------------------------------------------
        # 3) SEND
        # --------------------------------------------------
        if orientation == "N" and len(memory) > 0 and charge >= COST_SEND:
            acts.append(("SEND",))

        return acts

    # ======================================================
    # RESULT(state, action)
    # ======================================================
    def result(self, state, action):

        self.nodes_generated += 1

        orientation, charge, free_memory, memory, sent = state

        memory = list(memory)
        sent   = list(sent)

        match action:

            case ("RL",):
                orientation = rotate_left(orientation)
                charge -= COST_ROTATE

            case ("RR",):
                orientation = rotate_right(orientation)
                charge -= COST_ROTATE

            case ("TAKEPIC", obj, quality):
                mem_cost = HD_MEM_COST if quality == "HD" else SD_MEM_COST
                if free_memory >= mem_cost:
                    memory.append((obj, quality))
                    free_memory -= mem_cost
                    charge -= COST_TAKEPIC

            case ("SEND",):
                if orientation == "N":
                    pic = memory.pop()
                    free_memory += HD_MEM_COST if pic[1] == "HD" else SD_MEM_COST
                    sent.append(pic)
                    charge -= COST_SEND

        return self.build_state(orientation, charge, free_memory, memory, sent)

    # ======================================================
    # GOAL TEST
    # ======================================================
    def goal_test(self, state):
        _, _, _, _, sent = state
        return set(self._goal).issubset(set(sent))

    # ======================================================
    # COSTO CAMMINO
    # ======================================================
    def path_cost(self, c, state1, action, state2):

        match action:

            case ("RL",) | ("RR",):
                return c + COST_ROTATE

            case ("TAKEPIC", _, _):
                return c + COST_TAKEPIC

            case ("SEND",):
                return c + COST_SEND

        return c
