# ==========================================================
# FILE: PE_IM_heuristics.py
# ==========================================================
"""
EURISTICHE PER A*

Usiamo lo stato:

(
    position,
    orientation,
    charge,
    memory,
    sent
)
"""


# ----------------------------------------------------------
# H1
# Conta oggetti mancanti
# ----------------------------------------------------------
def h1(node, problem):

    _, _, _, _, sent = node.state

    missing = [
        obj for obj in problem._goal
        if obj not in sent
    ]

    return len(missing)


# ----------------------------------------------------------
# H2
# Stima più informata
# ----------------------------------------------------------
def h2(node, problem):

    _, orientation, charge, memory, sent = node.state

    missing = [
        obj for obj in problem._goal
        if obj not in sent
    ]

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