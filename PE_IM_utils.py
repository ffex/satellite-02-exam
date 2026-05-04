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


# Le otto posizioni del satellite, assumiamo che se il satellite è in punto, lo guarda.
DIRECTIONS = [
    "N", "NE", "E", "SE",
    "S", "SW", "W", "NW"
]


# Rotazione: sinistra e destra
def rotate_left(pos):
    """
    Ruota di uno step in senso antiorario.
    """
    i = DIRECTIONS.index(pos)
    return DIRECTIONS[(i - 1) % len(DIRECTIONS)]

def rotate_right(pos):
    """
    Ruota di uno step in senso orario.
    """
    i = DIRECTIONS.index(pos)
    return DIRECTIONS[(i + 1) % len(DIRECTIONS)]

# Funzione per tornare i costi di memoria
def memory_cost(quality):
    # Ritorna il costo delle foto
    return HD_MEM_COST if quality == "HD" else SD_MEM_COST


# Costo minimo riferito alle rotazioni
def angular_distance(a, b):
    i = DIRECTIONS.index(a)
    j = DIRECTIONS.index(b)
    diff = abs(i - j)
    return min(diff, len(DIRECTIONS) - diff)

# Serve per il debug dell'output
def has_extra_outputs(self, state):
    """
    Verifica se lo stato finale contiene output inutili.

    Serve solo per logging / debug / metriche.
    """
    _, _, _, _, sent = state

    sent_set = set(sent)
    goal_set = set(self._goal)

    return not sent_set == goal_set



# Costi azioni

COST_ROTATE = 1
COST_TAKEPIC = 2
COST_SEND = 2

# Memoria

MAX_MEMORY = 20

HD_MEM_COST = 10
SD_MEM_COST = 3
