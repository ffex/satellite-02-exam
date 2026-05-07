# ==========================================================
# FILE: heuristics.py
# ==========================================================
"""
EURISTICHE SEMPLIFICATE PER IL PLANNING PDDL

Queste euristiche sono pensate per un approccio planning,
non per una ricerca dettagliata nello spazio degli stati.

IDEA PRINCIPALE
----------------------------------------------------------
Stimare quanto il goal sia distante usando:
    - energia residua
    - memoria disponibile
    - numero di obiettivi mancanti

Le euristiche NON simulano:
    - sequenze complete di rotazioni
    - percorso ottimale
    - ordine esatto delle azioni

Questo approccio è più vicino alle euristiche rilassate
tipiche dei planner PDDL.

Tutte le costanti vengono importate da utils.py,
così il dominio resta centralizzato.
"""

from utils import (
    COST_ROTATE,
    COST_TAKEPIC,
    COST_SEND,
    HD_MEM_COST,
    SD_MEM_COST,
    MEM_SLOT_MAX
)


# ==========================================================
# H1 — GOAL COUNT
# ==========================================================
def h_goal_count(state, goals):
    """
    Euristica minimale.

    Conta semplicemente quanti goal
    non sono ancora stati completati.

    IDEA:
        Ogni obiettivo richiederà almeno:
            - una foto
            - un invio

    Non considera:
        - energia
        - memoria
        - posizione

    Molto semplice ma velocissima.
    """

    sent = state["sent"]

    missing = 0

    for goal in goals:
        if goal not in sent:
            missing += 1

    return missing


# ==========================================================
# H2 — ENERGY ESTIMATION
# ==========================================================
def h_energy(state, goals):
    """
    Stima il costo energetico residuo.

    Assumiamo che ogni obiettivo richieda:
        TAKEPIC + SEND

    Ignoriamo volutamente le rotazioni
    per mantenere l'euristica semplice.
    """

    sent = state["sent"]

    missing = 0

    for goal in goals:
        if goal not in sent:
            missing += 1

    estimated_energy = missing * (
        COST_TAKEPIC + COST_SEND
    )

    return estimated_energy


# ==========================================================
# H3 — MEMORY PRESSURE
# ==========================================================
def h_memory(state, goals):
    """
    Euristica basata sulla memoria residua.

    IDEA:
        Se resta poca memoria rispetto
        alle foto ancora da scattare,
        saranno necessari SEND intermedi.

    L'obiettivo NON è simulare il piano,
    ma penalizzare gli stati con memoria
    insufficiente.
    """

    sent = state["sent"]
    free_memory = state["free_memory"]

    missing = []

    for goal in goals:
        if goal not in sent:
            missing.append(goal)

    if not missing:
        return 0

    # Memoria necessaria stimata
    required_memory = 0

    for _, quality in missing:

        if quality == "HD":
            required_memory += HD_MEM_COST
        else:
            required_memory += SD_MEM_COST

    # Se la memoria basta
    if free_memory >= required_memory:
        return len(missing)

    # Penalità memoria
    memory_gap = required_memory - free_memory

    return len(missing) + memory_gap


# ==========================================================
# H4 — SLOT PRESSURE
# ==========================================================
def h_slots(state, goals):
    """
    Euristica basata sul numero massimo
    di foto memorizzabili contemporaneamente.

    Anche se la memoria numerica basta,
    il satellite può conservare solo
    MEM_SLOT_MAX immagini alla volta.

    Questa euristica penalizza gli stati
    in cui gli obiettivi mancanti superano
    gli slot disponibili.
    """

    memory = state["memory"]
    sent = state["sent"]

    current_slots = len(memory)

    missing = 0

    for goal in goals:
        if goal not in sent:
            missing += 1

    free_slots = MEM_SLOT_MAX - current_slots

    if missing <= free_slots:
        return missing

    overflow = missing - free_slots

    return missing + overflow


# ==========================================================
# H5 — RESOURCE COMBINATION
# ==========================================================
def h_resources(state, goals):
    """
    Euristica combinata.

    Unisce:
        - energia
        - memoria
        - pressione slot

    Prendiamo il massimo per restare
    conservativi ed evitare sovrastime
    troppo aggressive.
    """

    return max(
        h_energy(state, goals),
        h_memory(state, goals),
        h_slots(state, goals)
    )