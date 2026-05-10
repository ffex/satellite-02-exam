(define (domain satellite-advanced)

; ==========================================================
; SATELLITE DOMAIN - CLEAN FINAL VERSION
;
; MODELLO CORRETTO:
; - qualità esplicita (photo-hd / photo-sd)
; - goal esprime cosa deve essere inviato e in quale qualità
; - memoria è vincolo fisico (non logico)
; - nessun predicato inutile o ridondante
; - planner decide sequenza take/send
; ==========================================================

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
    object direction
)

; ==========================================================
; DIREZIONI COSTANTI
; ==========================================================

(:constants
    n ne e se s sw w nw - direction
)

; ==========================================================
; PREDICATES
; ==========================================================

(:predicates

    ; orientamento satellite
    (pointing ?d - direction)

    ; visibilità oggetti
    (visible ?o - object ?d - direction)

    ; stato oggetti
    (taken ?o - object)
    (sent ?o - object)

    ; qualità foto (decisa dall’azione)
    (photo-hd ?o - object)
    (photo-sd ?o - object)

    ; direzioni
    (next-right ?from ?to - direction)
    (next-left ?from ?to - direction)
)

; ==========================================================
; FUNCTIONS
; ==========================================================

(:functions
    (energy)
    (memory-used)
    (memory-capacity)
    (photo-count)
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
    )

    :effect (and
        (not (pointing ?from))
        (pointing ?to)
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
    )

    :effect (and
        (not (pointing ?from))
        (pointing ?to)
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
        (< (photo-count) 2)
        (<= (+ (memory-used) 10) (memory-capacity))
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
        (<= (+ (memory-used) 3) (memory-capacity))
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

        (when (photo-hd ?o)
            (decrease (memory-used) 10)
        )

        (when (photo-sd ?o)
            (decrease (memory-used) 3)
        )
    )
)

)