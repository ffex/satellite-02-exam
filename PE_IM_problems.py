# ==========================================================
# FILE: PE_IM_problems.py
# ==========================================================

"""
Questo file definisce gli scenari del problema.
Per ogni istanza riportiamo anche il MINIMO TEORICO DI ENERGIA (E_min).
È un LOWER BOUND → non considera inefficienze o vincoli extra.

E_min =

    (numero oggetti goal x (TAKEPIC + SEND))
    + (numero direzioni utili x ROTATE)

- ogni oggetto deve essere fotografato e inviato almeno 1 volta
- per ogni direzione con oggetti utili serve almeno 1 rotazione

"""

from PE_IM_utils import (
    COST_ROTATE,
    COST_TAKEPIC,
    COST_SEND
)


def problem_easy():

    initial = {
        "position": "N",
        "charge": 20,
        "objects": {
            "E": ["star1", "noise1"]
        }
    }

    goal = [("star1", "HD")]

    # -------------------------------
    # CALCOLO E_MIN
    # -------------------------------
    # oggetti goal = 1
    # direzioni utili = 1 (E contiene star1)
    #
    # TAKEPIC = 1
    # SEND = 1
    # ROTATE = 1
    #
    # E_min = (1 * (COST_TAKEPIC + COST_SEND)) + (1 * COST_ROTATE)
    # E_min = (1 × (2 + 3)) + (1 × 1)
    # E_min = 5 + 1 = 6
    # -------------------------------

    return initial, goal


# ==========================================================
# MEDIUM
# ==========================================================

def problem_medium():

    initial = {
        "position": "S",
        "charge": 50,
        "objects": {
            "E": ["star1", "junk1"],
            "W": ["planet1", "noise2"]
        }
    }

    goal = [("star1", "HD"), ("planet1", "HD")]

    # -------------------------------
    # CALCOLO E_MIN
    # -------------------------------
    # oggetti goal = 2
    # direzioni utili = 2 (E e W)
    #
    # E_min = (2 * (COST_TAKEPIC + COST_SEND)) + (2 * COST_ROTATE)    # E_min = (2 × (2 + 3)) + (2 × 1)
    # E_min = 10 + 2 = 12
    # -------------------------------


    return initial, goal


# ==========================================================
# HARD
# ==========================================================

def problem_hard():

    initial = {
        "position": "SW",
        "charge": 75,
        "objects": {
            "E": ["star1", "dust1"],
            "S": ["planet1"],
            "NW": ["galaxy1", "junk2"]
        }
    }

    goal = [
        ("star1", "SD"),
        ("planet1", "SD"),
        ("galaxy1", "SD")
    ]

    # -------------------------------
    # CALCOLO E_MIN
    # -------------------------------
    # oggetti goal = 3
    # direzioni utili = 3 (E, S, NW)
    #
    # E_min = (3 * (COST_TAKEPIC + COST_SEND)) + (3 * COST_ROTATE)
    # E_min = (3 × (2 + 3)) + (3 × 1)
    # E_min = 15 + 3 = 18
    # -------------------------------

    return initial, goal


# ==========================================================
# HARD HD
# ==========================================================

def problem_hard_HD():

    initial = {
        "position": "SW",
        "charge": 100,
        "objects": {
            "E": ["star1", "dust1"],
            "S": ["planet1", "asteroidX"],
            "NW": ["galaxy1", "junk2"]
        }
    }

    goal = [
        ("star1", "HD"),
        ("planet1", "HD"),
        ("galaxy1", "HD")
    ]

    # -------------------------------
    # CALCOLO E_MIN
    # -------------------------------
    # E_min = (3 * (COST_TAKEPIC + COST_SEND)) + (3 * COST_ROTATE)

    # oggetti goal = 3
    # direzioni utili = 3
    #
    # E_min = 18
    # -------------------------------

    return initial, goal