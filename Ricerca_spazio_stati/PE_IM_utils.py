# ==========================================================
# FILE: PE_IM_utils.py
# ==========================================================
"""
FUNZIONI DI SUPPORTO E COSTANTI GLOBALI

1) direzioni della bussola
2) funzioni di rotazione
3) distanza minima tra orientamenti
4) costi delle azioni
5) costi di memoria HD / SD

"""


# Le otto posizioni del satellite
DIRECTIONS = [
    "N", "NE", "E", "SE",
    "S", "SW", "W", "NW"
]


def rotate_left(pos):
    """Ruota di uno step in senso antiorario."""
    i = DIRECTIONS.index(pos)
    return DIRECTIONS[(i - 1) % len(DIRECTIONS)]


def rotate_right(pos):
    """Ruota di uno step in senso orario."""
    i = DIRECTIONS.index(pos)
    return DIRECTIONS[(i + 1) % len(DIRECTIONS)]


def min_rotation_distance(pos1, pos2):
    """
    Restituisce il numero minimo di rotazioni per passare da pos1 a pos2.
    Usata sia per le euristiche che per angular_distance (erano identiche).
    """
    i = DIRECTIONS.index(pos1)
    j = DIRECTIONS.index(pos2)
    diff = abs(i - j)
    return min(diff, len(DIRECTIONS) - diff)

# Costi azioni
COST_ROTATE = 1
COST_TAKEPIC = 2
COST_SEND = 2

# Memoria
# MAX_MEMORY è un fallback di sicurezza usato se il problema
# non specifica un valore proprio in initial["max_memory"].
MAX_MEMORY = 20
HD_MEM_COST = 10
SD_MEM_COST = 3
MEM_SLOT_MAX = 2
