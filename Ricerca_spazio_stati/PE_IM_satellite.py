from search import Problem
import time

from PE_IM_utils import (
    COST_ROTATE,
    COST_TAKEPIC,
    COST_SEND,
    MAX_MEMORY,
    HD_MEM_COST,
    MEM_SLOT_MAX,
    SD_MEM_COST,
    rotate_left,
    rotate_right
)


class Satellite(Problem):
    """
    Problema del satellite modellato come problema di ricerca.

    Stato = (
        orientation,   # direzione corrente (N, NE, E, ...)
        charge,        # energia residua
        free_memory,   # memoria disponibile
        memory,        # tuple di foto NON inviate
        sent           # tuple di foto inviate
    )

    """

    def __init__(self, initial, goal, time_limit=10, node_limit=50000):

        # Salviamo il goal come tupla
        self._goal = tuple(goal)
        self.goal = self._goal

        # Mappa direzione → oggetti visibili
        self.objects = initial["objects"]

        # Mappa nome oggetto → qualità richiesta (HD / SD)
        self.goal_quality = {name: q for name, q in goal}

        # Limiti per interrompere la ricerca
        self.time_limit = time_limit
        self.node_limit = node_limit

        # Tempo iniziale
        self.start_time = time.time()

        # Contatori per analisi performance
        self.nodes_generated = 0
        self.nodes_expanded = 0

        # -------------------------------------------------------
        # Memoria massima specifica del problema.
        # Se non specificata, si usa il fallback globale MAX_MEMORY.
        # -------------------------------------------------------
        self.max_memory = initial.get("max_memory", MAX_MEMORY)

        # Stato iniziale:
        # - posizione iniziale
        # - energia iniziale
        # - memoria completamente libera (= max_memory del problema)
        # - nessuna foto scattata
        # - nessuna foto inviata
        initial_state = (
            initial["position"],
            initial["charge"],
            self.max_memory,    # <-- usa la memoria del problema, non la costante globale
            tuple(),
            tuple()
        )

        # Costruttore della classe Problem
        super().__init__(initial_state)

    def stopped(self):
        """
        Ferma la ricerca se supera il tempo limite o il numero massimo
        di nodi espansi.
        """
        return (
            time.time() - self.start_time > self.time_limit
            or self.nodes_expanded >= self.node_limit
        )

    def visible_objects(self, orientation):
        """
        Restituisce gli oggetti visibili nella direzione corrente.
        """
        return self.objects.get(orientation, [])

    def actions(self, state):
        """
        Restituisce la lista di azioni possibili da uno stato.

        Vincoli applicati:
        - TAKEPIC: energia sufficiente, meno di 2 foto in memoria,
          abbastanza free_memory per il costo della qualità richiesta,
          oggetto visibile e nel goal
        - SEND: orientamento N, almeno una foto in memoria, energia sufficiente
        - ROTATE: energia sufficiente, ci sono ancora oggetti da completare
          o foto da inviare
        """

        # Se abbiamo superato tempo o nodi, blocchiamo subito:
        if self.stopped():
            return []

        # Contiamo questo stato come un nodo espanso.
        self.nodes_expanded += 1

        # Decomposizione dello stato corrente nei suoi componenti.
        orientation, charge, free_memory, memory, sent = state

        # Lista delle azioni ammissibili che costruiremo.
        acts = []

        # Set dei nomi degli oggetti già inviati a Terra.
        # Serve per non ripetere azioni su oggetti già completati.
        sent_names = {x[0] for x in sent}

        # Set dei nomi degli oggetti attualmente in memoria (foto scattate ma non inviate).
        # Serve per non fotografare due volte lo stesso oggetto.
        memory_names = {x[0] for x in memory}

        # Set dei nomi di tutti gli oggetti che il goal richiede.
        goal_names = {x[0] for x in self._goal}

        # Oggetti che mancano ancora: non inviati E non in memoria.
        # Usato per decidere se ha senso ruotare (se non manca niente
        # e non c'è niente da inviare, ruotare sarebbe uno spreco).
        missing = goal_names - sent_names - memory_names

        # =========================
        # TAKEPIC
        # =========================

        # Controllo:
        # - charge >= COST_TAKEPIC : abbiamo abbastanza energia per scattare
        # - len(memory) < MEM_SLOT_MAX        : c'è almeno uno slot libero (max 2 foto)
        if charge >= COST_TAKEPIC and len(memory) < MEM_SLOT_MAX:

            # Iteriamo sugli oggetti visibili nella direzione corrente.
            # Solo gli oggetti in questa direzione possono essere fotografati ora.
            for obj in self.visible_objects(orientation):

                # Se l'oggetto è già in memoria o già inviato, non serve fotografarlo.
                if obj in sent_names or obj in memory_names:
                    continue

                # Se l'oggetto non è nel goal, non ci interessa fotografarlo.
                # (Potrebbero esserci oggetti "di rumore" nelle stesse direzioni.)
                if obj not in self.goal_quality:
                    continue

                # Recuperiamo la qualità richiesta dal goal (HD o SD).
                quality = self.goal_quality[obj]

                # Calcoliamo il costo in memoria: HD occupa di più di SD.
                mem_cost = HD_MEM_COST if quality == "HD" else SD_MEM_COST

                # Precondizione spazio: la free_memory residua deve bastare
                # per contenere questa foto. Questo vincolo dipende dalla
                # max_memory specifica del problema (non dalla costante globale).
                if free_memory >= mem_cost:
                    acts.append(("TAKEPIC", obj, quality))

        # =========================
        # SEND
        # =========================

        # Controllo:
        # - orientation == "N" : il satellite deve puntare verso la Terra (Nord)
        # - memory             : deve esserci almeno una foto da inviare
        # - charge >= COST_SEND: serve energia per trasmettere
        if orientation == "N" and memory and charge >= COST_SEND:
            # SEND non ha argomenti: invia sempre la prima foto in memoria (FIFO).
            acts.append(("SEND",))

        # =========================
        # ROTATE
        # =========================

        # Controllo:
        # - charge >= COST_ROTATE       : serve energia per ruotare
        # - (missing or memory)         : ha senso ruotare solo se:
        #     * ci sono oggetti da fotografare ancora (missing), oppure
        #     * ci sono foto in memoria da inviare (dobbiamo tornare a N)
        # Se non manca nulla e la memoria è vuota, siamo già al goal:
        # ruotare sarebbe uno spreco di energia e di nodi generati.
        if charge >= COST_ROTATE and (missing or memory):
            acts.append(("ROTATE_LEFT",))   # ruota di uno step in senso antiorario
            acts.append(("ROTATE_RIGHT",))  # ruota di uno step in senso orario

        return acts

    def result(self, state, action):
        """
        Restituisce il nuovo stato dopo aver applicato un'azione.
        Puramente funzionale (no effetti collaterali).
        """
        if self.stopped():
            return state

        self.nodes_generated += 1

        orientation, charge, free_memory, memory, sent = state

        memory = list(memory)
        sent   = list(sent)

        # Aggiorniamo il costo della rotazione!
        if action == ("ROTATE_LEFT",):
            return (
                rotate_left(orientation),
                charge - COST_ROTATE,
                free_memory,
                tuple(memory),
                tuple(sent)
            )

        # Aggiorniamo il costo della rotazione!
        if action == ("ROTATE_RIGHT",):
            return (
                rotate_right(orientation),
                charge - COST_ROTATE,
                free_memory,
                tuple(memory),
                tuple(sent)
            )

        # facciamo la foto e la salviamo nella memoria
        if action[0] == "TAKEPIC":
            _, obj, quality = action
            mem_cost = HD_MEM_COST if quality == "HD" else SD_MEM_COST
            memory.append((obj, quality))
            return (
                orientation,
                charge - COST_TAKEPIC,
                free_memory - mem_cost,
                tuple(memory),
                tuple(sent)
            )
        # Facciamo la pop e la mandiamo, liberando memoria
        if action[0] == "SEND":
            pic      = memory.pop(0)
            mem_cost = HD_MEM_COST if pic[1] == "HD" else SD_MEM_COST
            sent.append(pic)
            return (
                orientation,
                charge - COST_SEND,
                free_memory + mem_cost,
                tuple(memory),
                tuple(sent)
            )

        return state

    def goal_test(self, state):
        """
        Verifica se tutti gli obiettivi sono stati inviati.
        In particolare che sent contenga quello che ha goal
        """
        _, _, _, _, sent = state
        return set(self._goal).issubset(set(sent))

    def path_cost(self, c, state1, action, state2):
        """
        Costo cumulativo del percorso, in cui aggiorniamo i costi!
        """
        if action == ("ROTATE_LEFT",):
            return c + COST_ROTATE
        if action == ("ROTATE_RIGHT",):
            return c + COST_ROTATE
        if action[0] == "TAKEPIC":
            return c + COST_TAKEPIC
        if action == ("SEND",):
            return c + COST_SEND
        return c
