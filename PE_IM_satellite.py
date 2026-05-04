from search import Problem
import time

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

    def __init__(self, initial, goal, time_limit=10, node_limit=50000):

        self._goal = tuple(goal)
        self.goal = self._goal

        self.objects = initial["objects"]
        self.goal_quality = {name: q for name, q in goal}

        self.time_limit = time_limit
        self.node_limit = node_limit
        self.start_time = time.time()

        self.nodes_generated = 0
        self.nodes_expanded = 0

        # VISITED VA GESTITO DAL SEARCH, NON DAL PROBLEM
        self.visited = set()

        initial_state = (
            initial["position"],
            initial["charge"],
            MAX_MEMORY,
            tuple(),
            tuple()
        )

        super().__init__(initial_state)

    # ==================================================
    # STOP
    # ==================================================
    def stopped(self):
        return (
            time.time() - self.start_time > self.time_limit
            or self.nodes_expanded > self.node_limit
        )

    # ==================================================
    # UTILS
    # ==================================================
    def visible_objects(self, orientation):
        return self.objects.get(orientation, [])

    def state_key(self, state):
        # CHARGE NON VA NELLO STATO (rompe IDS inutilmente)
        orientation, charge, free_memory, memory, sent = state

        return (
            orientation,
            free_memory,
            frozenset(memory),
            frozenset(sent)
        )

    # ==================================================
    # ACTIONS (VINCOLI CORRETTI QUI)
    # ==================================================
    def actions(self, state):

        if self.stopped():
            return []

        self.nodes_expanded += 1

        orientation, charge, free_memory, memory, sent = state

        acts = []

        sent_names = {x[0] for x in sent}
        memory_names = {x[0] for x in memory}
        goal_names = {x[0] for x in self._goal}

        missing = goal_names - sent_names - memory_names

        # -------------------------
        # TAKEPIC (MAX 2 FOTO)
        # -------------------------
        if charge >= COST_TAKEPIC and len(memory) < 2:

            for obj in self.visible_objects(orientation):

                if obj in sent_names or obj in memory_names:
                    continue

                if obj not in self.goal_quality:
                    continue

                quality = self.goal_quality[obj]
                mem_cost = HD_MEM_COST if quality == "HD" else SD_MEM_COST

                if free_memory >= mem_cost:
                    acts.append(("TAKEPIC", obj, quality))

        # -------------------------
        # SEND (solo N + almeno 1 foto)
        # -------------------------
        if orientation == "N" and memory and charge >= COST_SEND:
            acts.append(("SEND",))

        # -------------------------
        # ROTATE
        # -------------------------
        if charge >= COST_ROTATE and (missing or memory):
            acts.append(("ROTATE_LEFT",))
            acts.append(("ROTATE_RIGHT",))

        return acts

    # ==================================================
    # RESULT (PURAMENTE FUNZIONALE - FIX CRITICO)
    # ==================================================
    def result(self, state, action):

        if self.stopped():
            return state

        self.nodes_generated += 1

        orientation, charge, free_memory, memory, sent = state

        memory = list(memory)
        sent = list(sent)

        if action == ("ROTATE_LEFT",):
            return (
                rotate_left(orientation),
                charge - COST_ROTATE,
                free_memory,
                tuple(memory),
                tuple(sent)
            )

        if action == ("ROTATE_RIGHT",):
            return (
                rotate_right(orientation),
                charge - COST_ROTATE,
                free_memory,
                tuple(memory),
                tuple(sent)
            )

        if action[0] == "TAKEPIC":
            _, obj, quality = action

            mem_cost = HD_MEM_COST if quality == "HD" else SD_MEM_COST

            memory.append((obj, quality))

            return (
                orientation,
                charge - COST_TAKEPIC,
                free_memory - mem_cost,
                tuple(memory),
                tuple(sent)
            )

        if action[0] == "SEND":
            pic = memory.pop(0)

            mem_cost = HD_MEM_COST if pic[1] == "HD" else SD_MEM_COST

            sent.append(pic)

            return (
                orientation,
                charge - COST_SEND,
                free_memory + mem_cost,
                tuple(memory),
                tuple(sent)
            )

        return state

    # ==================================================
    # GOAL TEST
    # ==================================================
    def goal_test(self, state):
        _, _, _, _, sent = state
        return set(self._goal).issubset(set(sent))

    # ==================================================
    # COST
    # ==================================================
    def path_cost(self, c, state1, action, state2):

        if action == ("ROTATE_LEFT",):
            return c + COST_ROTATE

        if action == ("ROTATE_RIGHT",):
            return c + COST_ROTATE

        if action[0] == "TAKEPIC":
            return c + COST_TAKEPIC

        if action == ("SEND",):
            return c + COST_SEND

        return c