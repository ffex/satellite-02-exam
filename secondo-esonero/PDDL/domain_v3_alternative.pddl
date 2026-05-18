; ==============================================================
; DOMAIN: SATELLITE  (BFWS v3.1)
; --------------------------------------------------------------
; OBIETTIVI DI MODELLAZIONE (rispetto a v1 / v2):
;
;   - take-picture e send sono AZIONI UNIVOCHE
;     parametrizzate dalla qualita' (hd / sd come oggetti del
;     tipo "quality"). Niente piu' 4 varianti per quality x slot.
;
;   - La qualita' richiesta e' espressa dal goal tramite
;     (required ?q ?o). Il pianificatore sceglie la quality che
;     deve essere fotografata in base a questo predicato; senza
;     "required" l'oggetto e' rumore e non puo' essere scattato.
;
;   - Niente flag ridondanti (hd-in-memory, took-photo, visited,
;     sent-any) che inquinavano il grafo di stato della v2.
;
;   - Aggiunto il predicato generale:
;
;         (captured ?o)
;
;     che marca gli oggetti gia' fotografati almeno una volta.
;     Questo elimina simmetrie inutili tra qualita'/slot e
;     impedisce fotografie duplicate dello stesso oggetto.
;
;     Benefici:
;       - meno stati raggiungibili
;       - meno grounding
;       - meno branching factor
;       - novelty BFWS piu' pulita
;       - encoding STRIPS piu' planner-oriented
;
;   - I vincoli di MEMORIA e SLOT (max 2 foto, somma <= max_memory
;     specifica del problema) sono uniformemente incapsulati in
;     una CATENA DI LIVELLI DI MEMORIA dichiarata nel problema.
;
;       - (mem-free ?l)             stato corrente di memoria libera
;       - (mem-take ?q ?from ?to)   transizione lecita per take
;       - (mem-send ?q ?from ?to)   transizione lecita per send
;
;     Il problema dichiara solo le transizioni che rispettano:
;       (1)  somma_byte_in_memoria <= max_memory
;       (2)  numero_foto_in_memoria <= 2     (vincolo "slot")
;
;     Cosi' max_memory e il limite di 2 slot non vivono nel
;     dominio, ma derivano dalla configurazione del problema.
;     Il dominio resta generale.
;
;   - I costi delle azioni sono identici al modello AIMA:
;     rotate=1, take-picture=2, send=2 (gestiti con :action-costs).
;
;   - La CARICA del satellite non e' modellata come fluente
;     esplicito (BFWS non supporta numeric fluents oltre
;     :action-costs). Il budget energia dei problemi AIMA e'
;     comunque rispettato in pratica grazie a :metric minimize
;     total-cost (il planner restituisce piani che minimizzano
;     il consumo). Il budget AIMA originale e' annotato come
;     commento in ogni problem file per riferimento.
;
;   - La direzione "Nord" non e' una costante hardcoded; viene
;     marcata da (is-north ?d) nell'init, cosi' il dominio non
;     dipende dal nome dell'oggetto direzione.
; ==============================================================

(define (domain satellite-v3)

(:requirements
    :strips
    :typing
    :negative-preconditions
    :action-costs
)

; --------------------------------------------------------------
; TIPI
;   direction : i nodi della "compass rose" (n, ne, e, ...)
;   object    : stelle, pianeti, rumore, ... presenti nel cielo
;   quality   : il livello di risoluzione (hd, sd)
;   level     : i nodi della catena di stati di memoria libera
; --------------------------------------------------------------
(:types direction object quality level)


(:predicates

    ; ----------------------------------------------------------
    ; ORIENTAMENTO E GRAFO ROTAZIONI
    ; ----------------------------------------------------------
    (pointing    ?d - direction)            ; direzione corrente
    (next-right  ?from - direction ?to - direction)
    (next-left   ?from - direction ?to - direction)
    (is-north    ?d - direction)            ; marker per send

    ; ----------------------------------------------------------
    ; OGGETTI NEL CIELO
    ; ----------------------------------------------------------
    (visible     ?o - object ?d - direction)
    (required    ?q - quality ?o - object)  ; qualita' richiesta
                                            ; dal goal per ?o

    ; ----------------------------------------------------------
    ; STATO FOTO
    ; ----------------------------------------------------------
    (stored      ?q - quality ?o - object)  ; ?o in mem con qualita' ?q
    (sent        ?o - object)               ; ?o inviato a Terra

    ; ----------------------------------------------------------
    ; PREDICATO DI CONTROLLO FOTOGRAFIE
    ;
    ; (captured ?o)
    ;   vero se ?o e' gia' stato fotografato almeno una volta.
    ;
    ; Serve a:
    ;   - evitare fotografie duplicate dello stesso oggetto
    ;   - ridurre branching e simmetrie
    ;   - migliorare BFWS/LAPKT
    ; ----------------------------------------------------------
    (captured    ?o - object)

    ; ----------------------------------------------------------
    ; CATENA DEI LIVELLI DI MEMORIA LIBERA
    ;
    ; Stato corrente (un solo livello a tempo):
    ;   (mem-free ?l)
    ;
    ; Transizioni dichiarate nell'init del problema:
    ;   (mem-take ?q ?from ?to)
    ;   (mem-send ?q ?from ?to)
    ;
    ; Il problema dichiara SOLO le transizioni valide rispetto a
    ;     max_memory  E  max 2 foto contemporanee.
    ; ----------------------------------------------------------
    (mem-free    ?l - level)
    (mem-take    ?q - quality ?from - level ?to - level)
    (mem-send    ?q - quality ?from - level ?to - level)
)


; Costo cumulativo: obbligatorio con :action-costs
(:functions
    (total-cost)
)


; ==============================================================
; ROTATE RIGHT  (costo 1)
;   ruota di una posizione in senso orario, secondo la catena
;   next-right dichiarata nell'init.
; ==============================================================
(:action rotate-right
 :parameters (?from - direction ?to - direction)
 :precondition (and
    (pointing ?from)
    (next-right ?from ?to)
 )
 :effect (and
    (not (pointing ?from))
    (pointing ?to)
    (increase (total-cost) 1)
 )
)


; ==============================================================
; ROTATE LEFT  (costo 1)
;   ruota di una posizione in senso antiorario.
; ==============================================================
(:action rotate-left
 :parameters (?from - direction ?to - direction)
 :precondition (and
    (pointing ?from)
    (next-left ?from ?to)
 )
 :effect (and
    (not (pointing ?from))
    (pointing ?to)
    (increase (total-cost) 1)
 )
)


; ==============================================================
; TAKE PICTURE  (costo 2)
;   Azione univoca parametrizzata dalla qualita' ?q.
;
;   Precondizioni:
;     - il satellite punta verso ?d e ?o e' visibile da ?d
;     - il goal richiede esattamente la qualita' ?q per ?o
;     - ?o non e' gia' stato fotografato
;     - ?o non e' gia' inviato
;     - la transizione di memoria libera ?from -> ?to per la
;       qualita' ?q e' dichiarata lecita nel problema
;
;   Effetti:
;     - ?o entra in memoria con qualita' ?q
;     - ?o viene marcato come fotografato
;     - la memoria libera passa da ?from a ?to
;     - +2 al total-cost
; ==============================================================
(:action take-picture
 :parameters (?q - quality ?o - object ?d - direction
              ?from - level ?to   - level)
 :precondition (and
    (pointing ?d)
    (visible ?o ?d)
    (required ?q ?o)

    ; evita fotografie duplicate
    (not (captured ?o))

    ; evita ri-fotografia dopo invio
    (not (sent ?o))

    (mem-free ?from)
    (mem-take ?q ?from ?to)
 )
 :effect (and
    (stored ?q ?o)
    (captured ?o)

    (not (mem-free ?from))
    (mem-free ?to)

    (increase (total-cost) 2)
 )
)


; ==============================================================
; SEND  (costo 2)
;   Azione univoca parametrizzata dalla qualita' ?q.
;   Trasmette UNA foto alla volta da memoria a Terra.
;
;   Precondizioni:
;     - il satellite punta a Nord
;     - ?o e' in memoria con qualita' ?q
;     - il goal richiede ?o nella qualita' ?q
;       (DOPPIA CONFERMA: e' gia' implicito che lo stored
;        avesse ?q corretta perche' la take richiedeva
;        (required ?q ?o), ma esplicitarlo qui blinda
;        l'azione contro eventuali stato spuri)
;     - la transizione di memoria libera ?from -> ?to per la
;       qualita' ?q e' dichiarata lecita nel problema
;
;   Effetti:
;     - ?o non e' piu' in memoria
;     - ?o e' marcato come inviato
;     - la memoria libera passa da ?from a ?to
;     - +2 al total-cost
; ==============================================================
(:action send
 :parameters (?q - quality ?o - object ?n - direction
              ?from - level ?to   - level)
 :precondition (and
    (pointing ?n)
    (is-north ?n)

    (stored ?q ?o)
    (required ?q ?o)

    (mem-free ?from)
    (mem-send ?q ?from ?to)
 )
 :effect (and
    (not (stored ?q ?o))
    (sent ?o)

    (not (mem-free ?from))
    (mem-free ?to)

    (increase (total-cost) 2)
 )
)

)