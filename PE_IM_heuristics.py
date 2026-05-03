# ==========================================================
# FILE: PE_IM_heuristics.py
# ==========================================================
"""
EURISTICHE PER A*

Usiamo lo stato:

(
    orientation,
    charge,
    free_memory,
    memory,
    sent
)
"""

from PE_IM_utils import (
    COST_ROTATE,
    COST_TAKEPIC,
    COST_SEND,
    min_rotation_distance
)


# ----------------------------------------------------------
# H1
# Conta oggetti mancanti
# ----------------------------------------------------------
def h1(node, problem):

    _, _, _, _, sent = node.state
    sent_names = [item[0] for item in sent]

    missing = [obj for obj in problem._goal if obj not in sent_names]

    return len(missing)


# ----------------------------------------------------------
# H2
# Stima più informata
# ----------------------------------------------------------
def h2(node, problem):

    orientation, charge, free_memory, memory, sent = node.state
    sent_names = [item[0] for item in sent]

    missing = [obj for obj in problem._goal if obj not in sent_names]

    base = len(missing) * 2

    # se non guardi nord servirà ruotare
    north_penalty = 1 if orientation != "N" else 0

    # se hai memoria piena sei più vincolato
    memory_penalty = 1 if len(memory) == 2 else 0

    # energia bassa
    energy_penalty = 2 if charge <= 3 else 0

    return base + north_penalty + memory_penalty + energy_penalty



# ----------------------------------------------------------
# HMAX
# ----------------------------------------------------------
def h_max(node, problem):
    return max(
        h1(node, problem),
        h2(node, problem)
    )
