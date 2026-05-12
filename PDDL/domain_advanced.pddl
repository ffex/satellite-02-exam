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

    ; orientamento satellite
    (pointing ?d - direction)

    ; evita oscillazioni
    (last-dir ?d - direction)

    ; visibilità oggetti
    (visible ?o - object ?d - direction)

    ; stato invio
    (taken ?o - object)
    (sent ?o - object)

    ; qualità oggetto (NON della foto)
    (quality-hd ?o - object)
    (quality-sd ?o - object)

    ; grafo direzioni
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
; TAKE PICTURE (UNICA)
; ==========================================================

(:action take-picture

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
        (increase (photo-count) 1)
        (decrease (energy) 2)

        (when (quality-hd ?o)
            (increase (memory-used) 10)
        )

        (when (quality-sd ?o)
            (increase (memory-used) 3)
        )
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

        (when (quality-hd ?o)
            (decrease (memory-used) 10)
        )

        (when (quality-sd ?o)
            (decrease (memory-used) 3)
        )
    )
)

)