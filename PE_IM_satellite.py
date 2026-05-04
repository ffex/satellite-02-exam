# ==========================================================
# FILE: PE_IM_satellite.py
# ==========================================================

from search import Problem

from PE_IM_utils import (
    COST_ROTATE,
    COST_TAKEPIC,
    COST_SEND,
    MAX_MEMORY,
    HD_MEM_COST,
    SD_MEM_COST,
    rotate_left,
    rotate_right
)


class Satellite(Problem):

    def __init__(self, initial, goal):

        self._goal = tuple(goal)
        self.goal = self._goal

        self.objects = initial["objects"]

        self.goal_quality = {name: q for name, q in goal}

        # statistiche
        self.nodes_generated = 0
        self.nodes_expanded = 0

        # Cache state (PRUNING GLOBALE)
        self.closed = {}

        # Stato iniziale
        initial_state = (
            initial["position"],
            initial["charge"],
            MAX_MEMORY,
            tuple(),
            tuple()
        )

        super().__init__(initial_state)


    # Definisce gli oggetti visibili
    def visible_objects(self, orientation):
        return self.objects.get(orientation, [])


    # Convertiamo lo stato in una chiave, per vedere se l'abbiamo già esplorata
    def state_key(self, state):
        """
        Stato ridotto per caching.

        Due stati sono uguali se hanno:
        - stessa orientazione
        - stessi oggetti processati
        - stessa "situazione logica"

        Ignoriamo ordine interno (set/frozenset).
        """

        orientation, charge, free_memory, memory, sent = state

        return (
            orientation,
            frozenset(memory),
            frozenset(sent)
        )


    # Il concetto di Pruning viene definito qui
    def is_dominated(self, state):
        """
        Uno stato è inutile se:
        - abbiamo già visto stesso stato logico
        - ma con più energia o più progresso sul goal
        """

        key = self.state_key(state)

        _, charge, _, memory, sent = state

        sent_score = len(sent)  # progresso sul goal

        # Se non c'è match
        if key not in self.closed:
            return False

        # Recupera dallo stato già esplorato key la vecchia carica del satellite
        # e gli oggetti già inviati.
        old_charge, old_sent = self.closed[key]

        # stato peggiore viene scartato
        if charge <= old_charge and sent_score <= old_sent:
            return True

        return False


    # Definizione di stato
    def build_state(self, orientation, charge, free_memory, memory, sent):

        return (
            orientation,
            charge,
            free_memory,
            tuple(memory),
            tuple(sent)
        )


    # Definiamo le azioni del satellite
    def actions(self, state):

        # Aggiorniamo il conteggio dei nodi
        self.nodes_expanded += 1

        # Definiamo lo stato
        orientation, charge, free_memory, memory, sent = state

        acts = []

        # Mappe locali
        sent_names = {x[0] for x in sent}
        memory_names = {x[0] for x in memory}

        goal_names = {x[0] for x in self._goal}
        missing = goal_names - sent_names - memory_names

        # ==================================================
        # TAKEPIC
        # ==================================================

        # Dobbiamo avere abbastanza energia
        if charge >= COST_TAKEPIC:

            # Controlliamo se l'oggetto è visibile 
            for obj in self.visible_objects(orientation):
                
                # Scartiamo gli oggetti non necessari
                if obj not in self.goal_quality:
                    continue
                
                # Se abbiamo ancora qualcosa da fotografare
                if obj in sent_names or obj in memory_names:
                    continue
                
                # Determiniamo la qualità
                quality = self.goal_quality[obj]

                # Aggiorniamo il costo
                mem_cost = HD_MEM_COST if quality == "HD" else SD_MEM_COST

                # Controlliamo se abbiamo memoria
                if free_memory >= mem_cost:
                    acts.append(("TAKEPIC", obj, quality))

        # ==================================================
        # SEND
        # ==================================================

        # Controlliamo se siamo a Nord , controlliamo di avere carica
        if orientation == "N" and memory and charge >= COST_SEND:
            acts.append(("SEND",))

        # ==================================================
        # ROTAZIONE

        # evita rotazioni inutili quando:
        # - non ci sono obiettivi
        # - e non c'è memoria da svuotare
        
        # Controllo se ho energia e se ho qualcosa da fotografare
        if charge >= COST_ROTATE and (missing or memory):

            # evita backtracking immediato (riduce loop RL/RR)
            last_action_block = getattr(self, "last_action", None)
            
            # Controllo se non ripeto l'ultima azione
            if last_action_block != "RR":
                acts.append(("RL",))

            if last_action_block != "RL":
                acts.append(("RR",))

        return acts


    # Definisco il risultato
    def result(self, state, action):
        
        # Aggiorno il nodo generato
        self.nodes_generated += 1

        # Definisco lo stato
        orientation, charge, free_memory, memory, sent = state

        memory = list(memory)
        sent = list(sent)

        # salva ultima azione per evitare loop
        self.last_action = action[0]

        # applicazione azione
        match action:

            case ("RL",):
                orientation = rotate_left(orientation)
                charge -= COST_ROTATE

            case ("RR",):
                orientation = rotate_right(orientation)
                charge -= COST_ROTATE

            case ("TAKEPIC", obj, quality):

                mem_cost = HD_MEM_COST if quality == "HD" else SD_MEM_COST

                memory.append((obj, quality))
                free_memory -= mem_cost
                charge -= COST_TAKEPIC

            case ("SEND",):

                pic = memory.pop(0)

                mem_cost = HD_MEM_COST if pic[1] == "HD" else SD_MEM_COST

                free_memory += mem_cost
                sent.append(pic)
                charge -= COST_SEND

        # Il nuovo stato costruito
        new_state = self.build_state(
            orientation,
            charge,
            free_memory,
            memory,
            sent
        )


        # Controllo sul pruning
        if self.is_dominated(new_state):
            return state


        # Aggiorno la cache
        key = self.state_key(new_state)

        sent_score = len(sent)

        if key not in self.closed:
            self.closed[key] = (charge, sent_score)

        return new_state


    def goal_test(self, state):
        """
        Verifica se lo stato corrente soddisfa il goal del problema.

        Il goal NON è uno stato specifico, ma una condizione:
        tutti gli oggetti richiesti in self._goal devono risultare
        presenti nell'insieme degli elementi inviati (sent).

        In altre parole:
            il problema è risolto quando:
                self._goal ⊆ sent

        dove:
        - self._goal = insieme degli obiettivi da completare
        - sent = insieme degli oggetti già inviati a terra

        Questo implica che l'ordine delle azioni non è rilevante,
        ma solo il completamento di tutti i task richiesti.
        """

        _, _, _, _, sent = state
        return set(self._goal).issubset(set(sent))


    # Definizione dei costi
    def path_cost(self, c, state1, action, state2):

        match action:
            # Costo per ruotare
            case ("RL",) | ("RR",):
                return c + COST_ROTATE
            # Costo per fare la foto, di cosa e della qualità non ci importa
            case ("TAKEPIC", _, _):
                return c + COST_TAKEPIC
            # Costo per mandare la foto
            case ("SEND",):
                return c + COST_SEND

        return c