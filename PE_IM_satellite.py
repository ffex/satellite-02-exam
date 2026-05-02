# ==========================================================
# FILE: PE_IM_satellite.py
# ==========================================================
"""
SATELLITE SEARCH PROBLEM
==========================================================

In questo dominio modelliamo un satellite che deve:

1) ruotare nello spazio
2) osservare oggetti astronomici
3) fotografarli
4) inviare i dati verso la base

----------------------------------------------------------
RAPPRESENTAZIONE DELLO STATO
----------------------------------------------------------

STATE = (
    orientation,    # dove sta guardando ora il satellite
    charge,         # energia residua
    free_memory,    # memoria ancora libera
    memory,         # tuple di oggetti fotografati ma non inviati
    sent            # tuple di oggetti già inviati
)

Esempio:

(
    "E",
    6,
    10,
    (("star1","HD"),),
    (("planet1","SD"),)
)

----------------------------------------------------------
VINCOLI
----------------------------------------------------------

- per fotografare un oggetto bisogna guardare la sua direzione
- SEND si può fare SOLO guardando NORD
- memoria massima = 2 oggetti
- ogni azione consuma energia
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

        goal:
        ["star1", "planet1"]
        """

        self._goal = tuple(goal)
        self.goal = self._goal

        # mappa spaziale degli oggetti
        self.objects = initial["objects"]

        # statistiche ricerca
        self.nodes_generated = 0
        self.nodes_expanded = 0

        # stato iniziale
        initial_state = (
            initial["position"],      # orientation iniziale
            initial["charge"],        # energia
            MAX_MEMORY,
            tuple(),                  # memory vuota
            tuple()                   # sent vuoto
        )

        super().__init__(initial_state)

    # ======================================================
    # FUNZIONE SUPPORTO
    # ======================================================
    def visible_objects(self, orientation):
        """
        Restituisce tutti gli oggetti visibili
        nella direzione corrente.
        """
        return self.objects.get(orientation, [])

    # ======================================================
    # BUILD STATE
    # ======================================================
    def build_state(self, orientation, charge,
                    free_memory, memory, sent):

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
        """
        Restituisce le azioni legali dallo stato corrente.
        """

        self.nodes_expanded += 1

        orientation, charge, free_memory, memory, sent = state

        memory = list(memory)
        sent = list(sent)

        acts = []

        # --------------------------------------------------
        # 1) ROTAZIONI
        # --------------------------------------------------
        if charge >= COST_ROTATE:
            acts.append(("RL",))
            acts.append(("RR",))

        # --------------------------------------------------
        # 2) TAKEPIC HD
        # --------------------------------------------------
        if charge >= COST_TAKEPIC and free_memory >= HD_MEM_COST:

            visible = self.visible_objects(orientation)
            sent_names = [item[0] for item in sent]
            memory_names = [item[0] for item in memory]

            for obj in visible:

                # evita duplicati
                if obj in sent_names:
                    continue

                if obj in memory_names:
                    continue

                acts.append(("TAKEPICHD", obj))

        # --------------------------------------------------
        # 2) TAKEPIC SD
        # --------------------------------------------------
        if charge >= COST_TAKEPIC and free_memory >= SD_MEM_COST:

            visible = self.visible_objects(orientation)
            sent_names = [item[0] for item in sent]
            memory_names = [item[0] for item in memory]

            for obj in visible:

                # evita duplicati
                if obj in sent_names:
                    continue

                if obj in memory_names:
                    continue

                acts.append(("TAKEPICSD", obj))

        # --------------------------------------------------
        # 3) SEND
        # --------------------------------------------------
        if (
            orientation == "N"
            and len(memory) > 0
            and charge >= COST_SEND
        ):
            acts.append(("SEND",))

        return acts

    # ======================================================
    # RESULT(state, action)
    # ======================================================
    def result(self, state, action):
        """
        Applica una azione e produce il nuovo stato.
        """

        self.nodes_generated += 1

        orientation, charge, free_memory, memory, sent = state

        memory = list(memory)
        sent = list(sent)

        match action:

            # ----------------------------------------------
            # ROTATE LEFT
            # ----------------------------------------------
            case ("RL",):
                orientation = rotate_left(orientation)
                charge -= COST_ROTATE

            # ----------------------------------------------
            # ROTATE RIGHT
            # ----------------------------------------------
            case ("RR",):
                orientation = rotate_right(orientation)
                charge -= COST_ROTATE

            # ----------------------------------------------
            # TAKE PHOTO HD
            # ----------------------------------------------
            case ("TAKEPICHD", obj):
                if free_memory >= HD_MEM_COST:
                    memory.append((obj,"HD"))
                    free_memory -= HD_MEM_COST
                    charge -= COST_TAKEPIC

            # ----------------------------------------------
            # TAKE PHOTO SD
            # ----------------------------------------------
            case ("TAKEPICSD", obj):
                if free_memory >= SD_MEM_COST:
                    memory.append((obj,"SD"))
                    free_memory -= SD_MEM_COST
                    charge -= COST_TAKEPIC

            # ----------------------------------------------
            # SEND
            # ----------------------------------------------
            case ("SEND",):

                if orientation == "N":
                    pic_to_send = memory.pop()
                    if pic_to_send[1]=="HD":
                        free_memory += HD_MEM_COST
                    else:
                        free_memory += SD_MEM_COST
                    sent.append(pic_to_send)
                    charge -= COST_SEND

        return self.build_state(
            orientation,
            charge,
            free_memory,
            memory,
            sent
        )

    # ======================================================
    # GOAL TEST
    # ======================================================
    def goal_test(self, state):

        _, _, _, _, sent = state

#        return set(self._goal).issubset(set(sent))
        goal_set = set(self._goal)
        # Check if the first element of the goal is a tuple or a single value
        if isinstance(self._goal[0], tuple):
            # Standard subset check for tuples
            return goal_set.issubset(set(sent))
        else:
            # Compare single values against the first element of each sent tuple
            return goal_set.issubset(val[0] for val in sent)

    # ======================================================
    # COSTO CAMMINO
    # ======================================================
    def path_cost(self, c, state1, action, state2):

        match action:

            case ("RL",) | ("RR",):
                return c + COST_ROTATE

            case ("TAKEPICHD", _) | ("TAKEPICSD", _):
                return c + COST_TAKEPIC

            case ("SEND",):
                return c + COST_SEND

        return c
