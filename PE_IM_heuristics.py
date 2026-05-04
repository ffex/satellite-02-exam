# ==========================================================
# FILE: PE_IM_heuristics.py
# ==========================================================
"""

Un'euristica h(n) è una funzione che stima il costo minimo
necessario per raggiungere lo stato goal a partire dallo stato n.

Formalmente:

    h(n) ≈ costo minimo reale da n a goal

Nel nostro caso il costo reale è composto da:

1. ROTAZIONI del satellite (ROTATE)
2. SCATTO foto (TAKEPIC)
3. INVIO a terra (SEND)

Un euristica ha almeno due proprietà:

AMMISSIBILITÀ:
    h(n) NON deve mai sovrastimare il costo reale.

CONSISTENZA (più forte):
    h(n) ≤ costo(n → n') + h(n')

Se consistente ⇒ A* è ottimale e più efficiente.

----------------------------------------------------------
STRATEGIA DELLE EURISTICHE
----------------------------------------------------------

- h1 → stima minimale (conteggio puro)
- h2 → aggiunge vincoli del problema
- h3 → usa struttura spaziale (direzioni)
- h_max → combina tutte (massimo valore)

"""

from PE_IM_utils import (
    COST_TAKEPIC,
    COST_SEND,
    COST_ROTATE,
    SD_MEM_COST,
    HD_MEM_COST,
    MAX_MEMORY,
    angular_distance
)

# ==========================================================
# H1 - STIMA BASE (COUNTING HEURISTIC)
# ==========================================================

def h1(node, problem):
    """
    IDEA:
    Ogni oggetto mancante deve almeno:
        - essere fotografato (TAKEPIC)
        - essere inviato (SEND)

    Ignoriamo completamente:
        - rotazioni
        - posizione del satellite
        - vincoli di memoria

    ⇒ stiamo stimando un LOWER BOUND molto semplice
    """

    _, _, _, memory, sent = node.state

    # oggetti già inviati
    sent_names = {x[0] for x in sent}

    # oggetti già fotografati ma non inviati
    memory_names = {x[0] for x in memory}

    # obiettivi totali
    goal_names = {g[0] for g in problem._goal}

    # oggetti ancora da completare
    missing = goal_names - sent_names

    cost = 0

    # --------------------------------------------------
    # Per ogni oggetto mancante:
    # --------------------------------------------------
    for obj in missing:

        if obj in memory_names:
            # già fotografato → serve solo SEND
            cost += COST_SEND
        else:
            # non fotografato → TAKEPIC + SEND
            cost += COST_TAKEPIC + COST_SEND

    return cost


# ==========================================================
# H2 - STIMA CON VINCOLI REALI
# ==========================================================

def h2(node, problem):
    """
    Aggiungiamo vincoli REALI del problema:

    1. SEND è possibile SOLO a Nord, quindi serve rotazione
    2. memoria può essere piena

    euristica informata ma non formalmente provata come consistente in ogni caso
    """

    orientation, charge, free_memory, memory, sent = node.state

    sent_names   = {x[0] for x in sent}
    memory_names = {x[0] for x in memory}
    goal_names   = {g[0] for g in problem._goal}

    missing = goal_names - sent_names

    if not missing:
        return 0

    cost = 0

    # --------------------------------------------------
    # 1. costo base oggetti (come h1)
    # --------------------------------------------------
    for obj in missing:

        if obj in memory_names:
            cost += COST_SEND
        else:
            cost += COST_TAKEPIC + COST_SEND

    # --------------------------------------------------
    # 2. costo minimo per raggiungere Nord
    # --------------------------------------------------
    # SEND richiede orientamento N
    cost += angular_distance(orientation, "N") * COST_ROTATE

    # --------------------------------------------------
    # 3. vincolo memoria (caso limite)
    # --------------------------------------------------
    # se memoria piena → serve almeno una azione extra
    if len(memory) == 2 and (missing - memory_names):
        cost += COST_ROTATE

    return cost


# ==========================================================
# H3 - STIMA SPAZIALE (GEOMETRICA)
# ==========================================================

def h3(node, problem):
    """
    Qui usiamo la geometria del problema:

    - Oggetti sono distribuiti nelle 8 direzioni
    - Il satellite deve ruotare per raggiungerli

    STIMA: costo foto + rotazione minima verso una direzione utile
    MA:
    - non considera sequenza ottimale tra più oggetti
    - assume sempre miglior scelta locale
    """

    orientation, charge, free_memory, memory, sent = node.state

    sent_names = {x[0] for x in sent}
    goal_names = {g[0] for g in problem._goal}

    missing = goal_names - sent_names

    if not missing:
        return 0

    object_positions = problem.objects

    min_rotation = float("inf")

    # --------------------------------------------------
    # cerchiamo la direzione migliore verso un goal
    # --------------------------------------------------
    for direction, objects in object_positions.items():

        if any(obj in missing for obj in objects):

            dist = angular_distance(orientation, direction)

            min_rotation = min(min_rotation, dist)

    # fallback
    if min_rotation == float("inf"):
        min_rotation = 0

    # costo minimo:
    # foto + rotazione
    return len(missing) * COST_TAKEPIC + min_rotation * COST_ROTATE

# ==========================================================
# H4 - STIMA MEMORIA
# ==========================================================
def h4(node, problem):
    """
    Stimiamo se la memoria corrente è sufficiente
    a contenere tutte le foto necessarie senza forcing SEND.

    Se non basta, almeno un SEND sarà necessario.
    """

    orientation, charge, free_memory, memory, sent = node.state

    sent_names = {x[0] for x in sent}
    goal_names = {g[0] for g in problem._goal}

    memory_load = sum(
        HD_MEM_COST if x[1] == "HD" else SD_MEM_COST
        for x in memory
    )

    missing = goal_names - sent_names
    if not missing:
        return 0

    # --------------------------------------------------
    # 1. costo base minimo (foto + invio)
    # --------------------------------------------------
    cost = 0
    for obj in missing:
        # assumiamo caso minimo (SD = sottostima)
        cost += COST_TAKEPIC + COST_SEND

    # --------------------------------------------------
    # 2. stima spazio necessario per completare tutto
    # --------------------------------------------------
    estimated_required_memory = 0

    for obj in missing:
        quality = problem.goal_quality[obj]
        estimated_required_memory += (
            HD_MEM_COST if quality == "HD" else SD_MEM_COST
        )

    # --------------------------------------------------
    # 3. vincolo realistico: se non ci sta tutto
    #    almeno un SEND intermedio sarà necessario
    # --------------------------------------------------
    if memory_load + estimated_required_memory > MAX_MEMORY:
        cost += COST_SEND  # flush obbligatorio minimo

    return cost


# ==========================================================
# HMAX - COMBINAZIONE EURISTICHE
# ==========================================================

def h_max(node, problem):
    """
    Combina tutte le euristiche prendendo il massimo:

        h_max = max(h1, h2, h3)

    IDEA:
    usare sempre la stima più informata.

    PROPRIETÀ:
    - ammissibile se tutte lo sono
    - NON necessariamente consistente
    """

    return max(
        h1(node, problem),
        h2(node, problem),
        h3(node, problem),
        h4(node, problem)

    )
