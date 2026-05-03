# ==========================================================
# FILE: PE_IM_utils.py
# ==========================================================
"""
COSTANTI E FUNZIONI DI SUPPORTO
"""

# ----------------------------------------------------------
# DIREZIONI
# ----------------------------------------------------------
DIRECTIONS = [
    "N", "NE", "E", "SE",
    "S", "SW", "W", "NW"
]


def rotate_left(pos):
    """
    Ruota in senso antiorario.
    """
    i = DIRECTIONS.index(pos)
    return DIRECTIONS[(i - 1) % len(DIRECTIONS)]


def rotate_right(pos):
    """
    Ruota in senso orario.
    """
    i = DIRECTIONS.index(pos)
    return DIRECTIONS[(i + 1) % len(DIRECTIONS)]


def min_rotation_distance(pos1, pos2):
    """
    Minimum rotation steps between two directions (clockwise or counter-clockwise).
    """
    i = DIRECTIONS.index(pos1)
    j = DIRECTIONS.index(pos2)
    diff = abs(i - j)
    return min(diff, len(DIRECTIONS) - diff)


# ----------------------------------------------------------
# COSTI
# ----------------------------------------------------------
COST_ROTATE = 1
COST_TAKEPIC = 2
COST_SEND = 2

# ----------------------------------------------------------
# MEMORIA
# ----------------------------------------------------------
MAX_MEMORY = 20
HD_MEM_COST = 10
SD_MEM_COST = 3
