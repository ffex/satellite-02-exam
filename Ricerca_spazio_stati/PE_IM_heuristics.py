"""
EURISTICHE PER IL PROBLEMA DEL SATELLITE

Un'euristica h(n) stima il costo minimo per raggiungere il goal.

Costo reale composto da:
- ROTATE
- TAKEPIC
- SEND

PROPRIETÀ

AMMISSIBILE:
    h(n) ≤ costo reale → garantisce ottimalità A*

CONSISTENTE:
    h(n) ≤ c(n,n') + h(n') → A* più efficiente
"""

from PE_IM_utils import (
    COST_TAKEPIC,
    COST_SEND,
    COST_ROTATE,
    SD_MEM_COST,
    min_rotation_distance,
)


# H1 - COUNTING HEURISTIC
def h1(node, problem):
    """
    IDEA:
    Ogni oggetto mancante deve almeno:
        - essere fotografato (TAKEPIC) se non già in memoria
        - essere inviato (SEND)

    NON considera:
        - rotazioni
        - posizione
        - vincolo 2 foto in memoria

    Ammissibile e Consistente, ma debole
    """
    _, _, _, memory, sent = node.state

    sent_names  = {x[0] for x in sent}
    memory_names = {x[0] for x in memory}
    goal_names  = {g[0] for g in problem._goal}

    missing = goal_names - sent_names

    cost = 0
    for obj in missing:
        if obj in memory_names:
            cost += COST_SEND
        else:
            cost += COST_TAKEPIC + COST_SEND

    return cost


# H2 - COUNTING + ROTAZIONE MINIMA
def h2(node, problem):
    """
    Aggiunge a h1 una stima minima delle rotazioni necessarie.
    - costo base foto + invio come h1
    - aggiungiamo UNA rotazione minima verso la direzione utile più vicina

    NON forziamo il movimento verso N direttamente
    (evita sovrastime per oggetti già vicini).

    Ammissibile
    """
    orientation, _, _, memory, sent = node.state

    sent_names   = {x[0] for x in sent}
    memory_names = {x[0] for x in memory}
    goal_names   = {g[0] for g in problem._goal}

    missing = goal_names - sent_names

    if not missing:
        return 0

    cost = 0

    # costo base (come h1)
    for obj in missing:
        if obj in memory_names:
            cost += COST_SEND
        else:
            cost += COST_TAKEPIC + COST_SEND

    # una rotazione minima verso la direzione utile più vicina
    min_rot = float("inf")
    for direction, objects in problem.objects.items():
        if any(obj in missing for obj in objects):
            dist = min_rotation_distance(orientation, direction)
            min_rot = min(min_rot, dist)

    if min_rot != float("inf"):
        cost += min_rot * COST_ROTATE

    return cost


# H3 - GEOMETRICA (rotazione + foto, ignora SEND)
def h3(node, problem):
    """
    Usa la struttura spaziale:
    - stima la rotazione minima verso un oggetto mancante
    - aggiunge il costo TAKEPIC per tutti i mancanti

    NON considera:
    - ordine ottimale
    - SEND
    - memoria

    ✔ Ammissibile (sottostima molto, ma non sovrastima mai)
    """
    orientation, _, _, _, sent = node.state

    sent_names = {x[0] for x in sent}
    goal_names = {g[0] for g in problem._goal}

    missing = goal_names - sent_names

    if not missing:
        return 0

    min_rotation = float("inf")
    for direction, objects in problem.objects.items():
        if any(obj in missing for obj in objects):
            dist = min_rotation_distance(orientation, direction)
            min_rotation = min(min_rotation, dist)

    if min_rotation == float("inf"):
        min_rotation = 0

    return len(missing) * 2 + min_rotation * COST_ROTATE


# H4 - MEMORY PRESSURE HEURISTIC (CORRETTA E INFORMATIVA)
def h4(node, problem):
    """
    Stima il costo aggiuntivo imposto dal vincolo di 2 foto in memoria.
    Considera DUE vincoli che limitano quante foto si possono accumulare:
      1) Slot: al massimo 2 foto in memoria contemporaneamente
      2) Spazio: la free_memory non può scendere sotto 0

    Il numero massimo di foto che entrano "in un batch" è il minimo
    tra i 2 slot disponibili e quante foto entrano nella free_memory
    corrente in base alla qualità richiesta.

    Se ci sono più oggetti da fotografare di quanti ne entrano nel batch,
    siamo costretti a fare cicli intermedi di SEND verso N.

    Stima:
    - costo base: TAKEPIC + SEND per ogni oggetto da fotografare,
      solo SEND per quelli già in memoria
    - batch_size: min(slot liberi, foto che entrano nella free_memory)
    - overflow: oggetti che non entrano nel batch corrente
    - per ogni ciclo send extra: SEND + rotazione minima verso N

    Ammissibile: non sovrastima mai il costo reale
    Più informativa di h1 e h2: usa sia il vincolo slot che quello
      di spazio, e sfrutta problem.max_memory specifico del problema
    """
    orientation, _, free_memory, memory, sent = node.state

    sent_names   = {x[0] for x in sent}
    memory_names = {x[0] for x in memory}
    goal_names   = {g[0] for g in problem._goal}

    missing = goal_names - sent_names

    if not missing:
        return 0

    # Oggetti che devono ancora essere fotografati (non in memoria, non inviati)
    to_photograph = [obj for obj in missing if obj not in memory_names]
    # Oggetti già in memoria, pronti per SEND
    to_send_now   = [obj for obj in missing if obj in memory_names]

    # Costo base: TAKEPIC + SEND per ogni mancante
    cost = len(to_photograph) * (COST_TAKEPIC + COST_SEND)
    cost += len(to_send_now) * COST_SEND

    # Slot liberi (vincolo numero foto)
    free_slots = 2 - len(memory)

    # Stima di quante foto entrano nella free_memory corrente.
    # Usiamo il costo minimo (SD = 3) per non sovrastimare.
    photos_by_space = free_memory // SD_MEM_COST if SD_MEM_COST > 0 else free_slots

    # Batch size = il minore tra i due vincoli
    batch_size = min(free_slots, photos_by_space)
    batch_size = max(0, batch_size)  # non negativo

    # Oggetti che non entrano nel batch corrente
    overflow = max(0, len(to_photograph) - batch_size)

    if overflow > 0:
        # Ogni ciclo send intermedio libera spazio per un altro batch.
        # Usiamo batch_size minimo di 1 per evitare divisioni per zero.
        effective_batch = max(1, batch_size)
        extra_sends = (overflow + effective_batch - 1) // effective_batch

        # Rotazione minima verso N dall'orientamento corrente
        rot_to_N = min_rotation_distance(orientation, "N")

        # Per ogni ciclo extra: rotazione verso N + SEND
        # Non includiamo il ritorno per restare ammissibili
        cost += extra_sends * (COST_SEND + rot_to_N * COST_ROTATE)

    return cost


# ==========================================================
# H_MAX - COMBINAZIONE
# ==========================================================
def h_max(node, problem):
    """
    Combina tutte le euristiche prendendo il massimo.

    Ammissibile solo se tutte le componenti lo sono (sì, qui lo sono)
    Consistente solo se tutte lo sono (sì)
    Domina tutte le singole euristiche → meno nodi espansi in A*

    Con la nuova h4, ogni euristica può ora "vincere" in scenari diversi:
    - h1: pochi oggetti, nessuna rotazione necessaria
    - h2: oggetti lontani dall'orientamento corrente
    - h3: molte rotazioni, pochi invii
    - h4: molti oggetti, vincolo memoria stringente
    """
    return max(
        h1(node, problem),
        h2(node, problem),
        h3(node, problem),
        h4(node, problem),
    )
