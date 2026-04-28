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
    position,       # posizione/orientamento logico iniziale
    orientation,    # dove sta guardando ora il satellite
    charge,         # energia residua
    memory,         # tuple di oggetti fotografati ma non inviati
    sent            # tuple di oggetti già inviati
)

Esempio:

(
    "N",
    "E",
    6,
    ("star1",),
    ("planet1",)
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
    MAX_PHOTOS,
    rotate_left,
    rotate_right
)


class Satellite(Problem):

    DEBUG = False

    # ======================================================
    # COSTRUTTORE
    # ======================================================
    def __init__(self, initial, goal, scenario=None):
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

        self.scenario = scenario

        # statistiche ricerca
        self.nodes_generated = 0
        self.nodes_expanded = 0

        # stato iniziale
        initial_state = (
            initial["position"],      # position
            initial["position"],      # orientation iniziale
            initial["charge"],        # energia
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
    def build_state(self, position, orientation, charge,
                    memory, sent):

        return (
            position,
            orientation,
            charge,
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

        position, orientation, charge, memory, sent = state

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
        # 2) TAKEPIC
        # --------------------------------------------------
        if charge >= COST_TAKEPIC and len(memory) < MAX_PHOTOS:

            visible = self.visible_objects(orientation)

            for obj in visible:

                # evita duplicati
                if obj in sent:
                    continue

                if obj in memory:
                    continue

                acts.append(("TAKEPIC", obj))

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

        position, orientation, charge, memory, sent = state

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
            # TAKE PHOTO
            # ----------------------------------------------
            case ("TAKEPIC", obj):

                if len(memory) < MAX_PHOTOS:
                    memory.append(obj)

                charge -= COST_TAKEPIC

            # ----------------------------------------------
            # SEND
            # ----------------------------------------------
            case ("SEND",):

                if orientation == "N":

                    for obj in memory:
                        if obj not in sent:
                            sent.append(obj)

                    memory.clear()

                charge -= COST_SEND

        return self.build_state(
            position,
            orientation,
            charge,
            memory,
            sent
        )

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

            case ("TAKEPIC", _):
                return c + COST_TAKEPIC

            case ("SEND",):
                return c + COST_SEND

        return c