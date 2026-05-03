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
    sent_names = {val[0] for val in sent}

    goal_names = {g[0] if isinstance(g, tuple) else g for g in problem._goal}
    remaining = len(goal_names - sent_names)

    return remaining * COST_SEND

# ----------------------------------------------------------
# H2
# Stima più informata
# ----------------------------------------------------------
def h2(node, problem):

    orientation, charge, free_memory, memory, sent = node.state

    sent_names   = {item[0] for item in sent}
    memory_names = {item[0] for item in memory}
    goal_names   = {g[0] if isinstance(g, tuple) else g for g in problem._goal}

    missing = goal_names - sent_names
    if not missing:
        return 0

    in_memory  = missing & memory_names       # already photographed, only need SEND
    need_photo = missing - memory_names        # need TAKEPIC + SEND

    cost = (len(in_memory)  * COST_SEND +
            len(need_photo) * (COST_TAKEPIC + COST_SEND))

    # at least one trip to N required to send anything
    cost += min_rotation_distance(orientation, "N")

    return cost



# ----------------------------------------------------------
# HMAX
# ----------------------------------------------------------
def h_max(node, problem):
    return max(
        h1(node, problem),
        h2(node, problem)
    )
