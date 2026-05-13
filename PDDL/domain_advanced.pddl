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

    ; orientamento del satellite
    (pointing ?d - direction)

    ; evita oscillazioni inutili
    (last-dir ?d - direction)

    ; visibilità oggetti in una direzione
    (visible ?o - object ?d - direction)

    ; stato oggetti
    (taken ?o - object)
    (sent ?o - object)

    ; qualità immagine (per rendering/semantica)
    (quality-hd ?o - object)
    (quality-sd ?o - object)

    ; SOLO OGGETTI RILEVANTI PER IL GOAL
    (goal-object ?o - object)

    ; grafo delle direzioni
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
; TAKE PICTURE (SOLO OGGETTI DEL GOAL)
; ==========================================================

(:action take-picture
    :parameters (?o - object ?d - direction)

    :precondition (and
        (pointing ?d)
        (visible ?o ?d)

        ;FILTRO CRITICO: elimina oggetti inutili (noise1 ecc.)
        (goal-object ?o)

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