; ==========================================================
; FILE: domain_advanced.pddl
; ==========================================================
; SATELLITE ADVANCED DOMAIN
;
; VERSIONE STABILE ANTI-OSCILLAZIONE
;
; OBIETTIVI DEL MODELLO:
;
; 1. Ridurre oscillazioni inutili del planner
; 2. Modellare memoria come vero vincolo decisionale
; 3. Distinguere foto HD / SD
; 4. Penalizzare rotazioni eccessive
; 5. Evitare loop locali n <-> ne <-> n
;
; STRATEGIA:
;
; - rotation-cost viene minimizzato nella metric
; - last-dir impedisce ritorno immediato
; - memoria e slot sono hard constraints
; ==========================================================

(define (domain satellite-advanced)

(:requirements
    :typing
    :fluents
    :negative-preconditions
    :conditional-effects
    :equality
)

; ==========================================================
; TYPES
; ==========================================================

(:types
    object
    direction
)

; ==========================================================
; DIRECTIONS
; ==========================================================

(:constants
    n ne e se s sw w nw - direction
)

; ==========================================================
; PREDICATES
; ==========================================================

(:predicates

    ; orientamento corrente
    (pointing ?d - direction)

    ; ultima direzione visitata
    ; usata per evitare oscillazioni immediate
    (last-dir ?d - direction)

    ; oggetto visibile dalla direzione
    (visible ?o - object ?d - direction)

    ; stato immagini
    (taken ?o - object)
    (sent ?o - object)

    ; qualità fotografia
    (photo-hd ?o - object)
    (photo-sd ?o - object)

    ; grafo direzioni
    (next-right ?from ?to - direction)
    (next-left ?from ?to - direction)
)

; ==========================================================
; FUNCTIONS
; ==========================================================

(:functions

    ; energia residua
    (energy)

    ; memoria occupata
    (memory-used)

    ; capacità massima memoria
    (memory-capacity)

    ; massimo 2 foto contemporaneamente
    (photo-count)

    ; penalità rotazioni
    (rotation-cost)
)

; ==========================================================
; ROTATE RIGHT
; ==========================================================

(:action rotate-right

    :parameters (?from ?to - direction)

    :precondition (and

        (pointing ?from)
        (next-right ?from ?to)

        (>= (energy) 1)

        ; evita oscillazione immediata
        (not (last-dir ?to))
    )

    :effect (and

        (not (pointing ?from))
        (pointing ?to)

        ; aggiorna memoria direzione
        (not (last-dir ?from))
        (last-dir ?to)

        ; penalizza rotazioni
        (increase (rotation-cost) 2)

        ; costo energetico
        (decrease (energy) 1)
    )
)

; ==========================================================
; ROTATE LEFT
; ==========================================================

(:action rotate-left

    :parameters (?from ?to - direction)

    :precondition (and

        (pointing ?from)
        (next-left ?from ?to)

        (>= (energy) 1)

        (not (last-dir ?to))
    )

    :effect (and

        (not (pointing ?from))
        (pointing ?to)

        (not (last-dir ?from))
        (last-dir ?to)

        (increase (rotation-cost) 2)

        (decrease (energy) 1)
    )
)

; ==========================================================
; TAKE PICTURE HD
; ==========================================================

(:action take-picture-hd

    :parameters (?o - object ?d - direction)

    :precondition (and

        (pointing ?d)
        (visible ?o ?d)

        (not (taken ?o))
        (not (sent ?o))

        (>= (energy) 2)

        ; massimo 2 foto
        (< (photo-count) 2)

        ; controllo memoria reale
        (<= (+ (memory-used) 10)
            (memory-capacity))
    )

    :effect (and

        (taken ?o)
        (photo-hd ?o)

        (increase (memory-used) 10)
        (increase (photo-count) 1)

        (decrease (energy) 2)
    )
)

; ==========================================================
; TAKE PICTURE SD
; ==========================================================

(:action take-picture-sd

    :parameters (?o - object ?d - direction)

    :precondition (and

        (pointing ?d)
        (visible ?o ?d)

        (not (taken ?o))
        (not (sent ?o))

        (>= (energy) 2)

        (< (photo-count) 2)

        (<= (+ (memory-used) 3)
            (memory-capacity))
    )

    :effect (and

        (taken ?o)
        (photo-sd ?o)

        (increase (memory-used) 3)
        (increase (photo-count) 1)

        (decrease (energy) 2)
    )
)

; ==========================================================
; SEND
; ==========================================================

(:action send

    :parameters (?o - object)

    :precondition (and

        ; invio possibile solo verso Terra
        (pointing n)

        (taken ?o)
        (not (sent ?o))

        (>= (energy) 2)
    )

    :effect (and

        (sent ?o)

        (not (taken ?o))

        (decrease (photo-count) 1)

        (decrease (energy) 2)

        ; libera memoria HD
        (when (photo-hd ?o)
            (decrease (memory-used) 10)
        )

        ; libera memoria SD
        (when (photo-sd ?o)
            (decrease (memory-used) 3)
        )
    )
)

)