# ==========================================================
# FILE: PE_IM_parser.py
# ==========================================================
"""
PLAN PARSER (FAST DOWNWARD COMPATIBLE)

Questo modulo legge il piano generato dal planner PDDL
(es. Fast Downward) e lo converte in una lista pulita di azioni.

FORMATI SUPPORTATI:
----------------------------------------
Fast Downward produce tipicamente:

    0: (rotate-right N NE) [1]
    1: (take-picture-hd star1 E) [2]

oppure versioni semplificate:

    (rotate-right N NE)
    (take-picture-hd star1 E)

OBIETTIVO:
----------------------------------------
Restituire:

    ["rotate-right", "take-picture-hd", ...]

cioè solo il nome dell'azione, ignorando parametri e costi.
"""

import os
import re


def parse_plan(filename):
    """
    Parsing robusto del file piano generato dal planner.
    """

    # ======================================================
    # VERIFICA FILE
    # ======================================================

    if not os.path.exists(filename):
        print(f"[PARSER] File non trovato: {filename}")
        return []

    actions = []

    # ======================================================
    # LETTURA FILE
    # ======================================================

    with open(filename, "r") as f:

        for line in f:

            line = line.strip()

            # IGNORA COMMENTI O RIGHE VUOTE
            if not line or line.startswith(";"):
                continue

            # ==================================================
            # CASO 1: formato Fast Downward con indice e costo
            #    0: (action-name args...) [cost]
            # ==================================================

            match = re.search(r"\(([^() ]+)", line)
            if match:
                action = match.group(1)
                actions.append(action)
                continue

            # ==================================================
            # CASO 2: formato già pulito
            #    action-name args...
            # ==================================================

            parts = line.split()
            if parts:
                actions.append(parts[0])

    return actions