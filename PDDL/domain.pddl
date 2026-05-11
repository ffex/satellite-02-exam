; ==========================================================
; DOMAIN: SATELLITE (ENHSP FIXED)
; ==========================================================

(define (domain satellite)

(:requirements
    :typing
    :negative-preconditions
    :fluents
)

; ==========================================================
;
(:types
    direction
    target ;
)

(:constants
    N NE E SE S SW W NW - direction
)

; ==========================================================
;
(:predicates
    (pointing ?d - direction)
    (visible ?t - target ?d - direction)
    (stored ?t - target)
    (sent ?t - target)

    (hd ?t - target)
    (sd ?t - target)

    (next-right ?from - direction ?to - direction)
    (next-left ?from - direction ?to - direction)

    ;
    (is-north ?d - direction)
)

; ==========================================================
;
(:functions
    (charge)
    (memory-used)
    (max-memory)
    (photo-count)
)

; ==========================================================
;
(:action rotate-right
    :parameters (?from - direction ?to - direction)
    :precondition
    (and
        (pointing ?from)
        (next-right ?from ?to)
        (>= (charge) 1)
    )
    :effect
    (and
        (not (pointing ?from))
        (pointing ?to)
        (decrease (charge) 1)
    )
)

(:action rotate-left
    :parameters (?from - direction ?to - direction)
    :precondition
    (and
        (pointing ?from)
        (next-left ?from ?to)
        (>= (charge) 1)
    )
    :effect
    (and
        (not (pointing ?from))
        (pointing ?to)
        (decrease (charge) 1)
    )
)

; ==========================================================
(:action take-picture-hd
    :parameters (?t - target ?d - direction)
    :precondition
    (and
        (pointing ?d)
        (visible ?t ?d)
        (hd ?t)
        (not (stored ?t))
        (not (sent ?t))

        (>= (charge) 2)
        (<= (photo-count) 1) ;
        (<= (+ (memory-used) 10) (max-memory))
    )
    :effect
    (and
        (stored ?t)
        (decrease (charge) 2)
        (increase (photo-count) 1)
        (increase (memory-used) 10)
    )
)

(:action take-picture-sd
    :parameters (?t - target ?d - direction)
    :precondition
    (and
        (pointing ?d)
        (visible ?t ?d)
        (sd ?t)
        (not (stored ?t))
        (not (sent ?t))

        (>= (charge) 2)
        (<= (photo-count) 1) ;
        (<= (+ (memory-used) 3) (max-memory))
    )
    :effect
    (and
        (stored ?t)
        (decrease (charge) 2)
        (increase (photo-count) 1)
        (increase (memory-used) 3)
    )
)

; ==========================================================
(:action send-hd
    :parameters (?t - target ?d - direction)
    :precondition
    (and
        (pointing ?d)
        (is-north ?d)
        (stored ?t)
        (hd ?t)
        (>= (charge) 2)
    )
    :effect
    (and
        (not (stored ?t))
        (sent ?t)

        (decrease (charge) 2)
        (decrease (photo-count) 1)
        (decrease (memory-used) 10)
    )
)

(:action send-sd
    :parameters (?t - target ?d - direction)
    :precondition
    (and
        (pointing ?d)
        (is-north ?d)
        (stored ?t)
        (sd ?t)
        (>= (charge) 2)
    )
    :effect
    (and
        (not (stored ?t))
        (sent ?t)

        (decrease (charge) 2)
        (decrease (photo-count) 1)
        (decrease (memory-used) 3)
    )
)
)