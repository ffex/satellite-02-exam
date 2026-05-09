; ==========================================================
; DOMAIN: SATELLITE
; ==========================================================
; MODELLO COMPLESSIVO:
;   - 8 direzioni con grafo (next-right/next-left) nell'init
;   - max 2 foto (slot1, slot2)
;   - max 1 foto HD (hd-in-memory)
;   - trasmissione solo da Nord (is-north nell'init)
;   - costi: rotate=1, take-picture=2, send=2
; ==========================================================

(define (domain satellite)

(:requirements
    :strips
    :typing
    :negative-preconditions
    :action-costs
)

(:types direction object)

; Funzione numerica obbligatoria con :action-costs
(:functions
    (total-cost)
)

(:predicates

    ; orientamento corrente del satellite
    (pointing ?d - direction)

    ; grafo di rotazione: dichiarato nell'init di ogni problem file
    ; (next-right ?a ?b) = ruotando a destra da ?a si arriva a ?b
    (next-right ?from - direction ?to - direction)
    (next-left  ?from - direction ?to - direction)

    ; marcatore Nord: (is-north n) nell'init evita di usare 'n'
    ; come costante hardcoded nel domain (causa "Undefined object")
    (is-north ?d - direction)

    ; visibilità: ?o è fotografabile quando il satellite punta ?d
    (visible ?o - object ?d - direction)

    ; qualità richiesta per ogni oggetto del goal
    (required-hd ?o - object)
    (required-sd ?o - object)

    ; slot di memoria fisici (max 2 foto contemporaneamente)
    (slot1-free)
    (slot2-free)

    ; flag: c'è una foto HD in memoria
    ; impedisce HD+HD (10+10=20 > max_memory=13 nei problemi hard)
    ; ma non impedisce HD+SD (10+3=13 ≤ max_memory)
    (hd-in-memory)

    ; stato delle foto per tipo (separato per gestire send correttamente)
    (stored-hd ?o - object)
    (stored-sd ?o - object)
    (sent ?o - object)
)


; ==========================================================
; ROTATE RIGHT — ruota in senso orario (costo 1)
; ==========================================================
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


; ==========================================================
; ROTATE LEFT — ruota in senso antiorario (costo 1)
; ==========================================================
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


; ==========================================================
; TAKE-PICTURE-HD — foto HD in slot 1 (costo 2)
;
; Precondizioni chiave:
;   - punta verso ?d e ?o visibile da ?d
;   - qualità richiesta è HD
;   - ?o non già in memoria né inviato (no duplicati)
;   - slot1 libero
;   - nessuna foto HD già presente (HD+HD non entra in memoria)
; ==========================================================
(:action take-picture-hd-s1
 :parameters (?o - object ?d - direction)
 :precondition (and
    (pointing ?d)
    (visible ?o ?d)
    (required-hd ?o)
    (not (stored-hd ?o))
    (not (stored-sd ?o))
    (not (sent ?o))
    (slot1-free)
    (not (hd-in-memory))
 )
 :effect (and
    (stored-hd ?o)
    (not (slot1-free))
    (hd-in-memory)
    (increase (total-cost) 2)
 )
)


; ==========================================================
; TAKE-PICTURE-HD — foto HD in slot 2 (costo 2)
;
; Usata solo se slot1 è già occupato (not slot1-free).
; Garantisce che slot2 venga riempito in ordine.
; ==========================================================
(:action take-picture-hd-s2
 :parameters (?o - object ?d - direction)
 :precondition (and
    (pointing ?d)
    (visible ?o ?d)
    (required-hd ?o)
    (not (stored-hd ?o))
    (not (stored-sd ?o))
    (not (sent ?o))
    (not (slot1-free))
    (slot2-free)
    (not (hd-in-memory))
 )
 :effect (and
    (stored-hd ?o)
    (not (slot2-free))
    (hd-in-memory)
    (increase (total-cost) 2)
 )
)


; ==========================================================
; TAKE-PICTURE-SD — foto SD in slot 1 (costo 2)
;
; SD occupa 3 unità: può coesistere con una foto HD (10+3=13).
; Non richiede (not hd-in-memory).
; ==========================================================
(:action take-picture-sd-s1
 :parameters (?o - object ?d - direction)
 :precondition (and
    (pointing ?d)
    (visible ?o ?d)
    (required-sd ?o)
    (not (stored-hd ?o))
    (not (stored-sd ?o))
    (not (sent ?o))
    (slot1-free)
 )
 :effect (and
    (stored-sd ?o)
    (not (slot1-free))
    (increase (total-cost) 2)
 )
)


; ==========================================================
; TAKE-PICTURE-SD — foto SD in slot 2 (costo 2)
; ==========================================================
(:action take-picture-sd-s2
 :parameters (?o - object ?d - direction)
 :precondition (and
    (pointing ?d)
    (visible ?o ?d)
    (required-sd ?o)
    (not (stored-hd ?o))
    (not (stored-sd ?o))
    (not (sent ?o))
    (not (slot1-free))
    (slot2-free)
 )
 :effect (and
    (stored-sd ?o)
    (not (slot2-free))
    (increase (total-cost) 2)
 )
)


; ==========================================================
; SEND-HD-S1 — trasmette foto HD da slot 1 (costo 2)
;
; Precondizioni:
;   - punta verso Nord (is-north ?n, non costante hardcoded)
;   - ?o è una foto HD in memoria
;   - slot1 occupato (questa foto è in slot1)
; Effetti:
;   - ?o risulta inviato, slot1 si libera
;   - hd-in-memory azzerato (nessuna HD più in memoria)
; ==========================================================
(:action send-hd-s1
 :parameters (?o - object ?n - direction)
 :precondition (and
    (pointing ?n)
    (is-north ?n)
    (stored-hd ?o)
    (not (slot1-free))
 )
 :effect (and
    (not (stored-hd ?o))
    (sent ?o)
    (slot1-free)
    (not (hd-in-memory))
    (increase (total-cost) 2)
 )
)


; ==========================================================
; SEND-HD-S2 — trasmette foto HD da slot 2 (costo 2)
; ==========================================================
(:action send-hd-s2
 :parameters (?o - object ?n - direction)
 :precondition (and
    (pointing ?n)
    (is-north ?n)
    (stored-hd ?o)
    (slot1-free)
    (not (slot2-free))
 )
 :effect (and
    (not (stored-hd ?o))
    (sent ?o)
    (slot2-free)
    (not (hd-in-memory))
    (increase (total-cost) 2)
 )
)


; ==========================================================
; SEND-SD-S1 — trasmette foto SD da slot 1 (costo 2)
;
; Non azzera hd-in-memory: una foto HD potrebbe ancora
; essere presente nell'altro slot.
; ==========================================================
(:action send-sd-s1
 :parameters (?o - object ?n - direction)
 :precondition (and
    (pointing ?n)
    (is-north ?n)
    (stored-sd ?o)
    (not (slot1-free))
 )
 :effect (and
    (not (stored-sd ?o))
    (sent ?o)
    (slot1-free)
    (increase (total-cost) 2)
 )
)


; ==========================================================
; SEND-SD-S2 — trasmette foto SD da slot 2 (costo 2)
; ==========================================================
(:action send-sd-s2
 :parameters (?o - object ?n - direction)
 :precondition (and
    (pointing ?n)
    (is-north ?n)
    (stored-sd ?o)
    (slot1-free)
    (not (slot2-free))
 )
 :effect (and
    (not (stored-sd ?o))
    (sent ?o)
    (slot2-free)
    (increase (total-cost) 2)
 )
)

)
