; ==========================================================
; DOMAIN: SATELLITE
; ==========================================================
;
; Il satellite può:
;   - ruotare
;   - fotografare oggetti
;   - inviare immagini
;
; Il tipo HD / SD è modellato come proprietà dell’oggetto.
;
; ==========================================================

(define (domain satellite)

(:requirements
    :strips
    :typing
    :negative-preconditions
)

; ==========================================================
; TIPI
; ==========================================================

(:types
    direction
    object
)

; ==========================================================
; PREDICATI
; ==========================================================

(:predicates

    ; orientamento corrente
    (pointing ?d - direction)

    ; oggetto visibile in una direzione
    (visible ?o - object ?d - direction)

    ; foto presente in memoria
    (stored ?o - object)

    ; foto inviata
    (sent ?o - object)

    ; qualità richiesta
    (hd ?o - object)
    (sd ?o - object)

    ; memoria disponibile
    (memory-free)

    ; slot disponibile
    (slot-free)
)

; ==========================================================
; ROTATE RIGHT
; ==========================================================

(:action rotate-right

    :parameters (?from - direction ?to - direction)

    :precondition
    (pointing ?from)

    :effect
    (and
        (not (pointing ?from))
        (pointing ?to)
    )
)

; ==========================================================
; ROTATE LEFT
; ==========================================================

(:action rotate-left

    :parameters (?from - direction ?to - direction)

    :precondition
    (pointing ?from)

    :effect
    (and
        (not (pointing ?from))
        (pointing ?to)
    )
)

; ==========================================================
; TAKE PICTURE
; ==========================================================

(:action take-picture

    :parameters (?o - object ?d - direction)

    :precondition
    (and
        (pointing ?d)
        (visible ?o ?d)

        (not (stored ?o))
        (not (sent ?o))

        (memory-free)
        (slot-free)
    )

    :effect
    (and
        (stored ?o)

        ; memoria occupata
        (not (memory-free))

        ; slot occupato
        (not (slot-free))
    )
)

; ==========================================================
; SEND
; ==========================================================

(:action send

    :parameters (?o - object ?north - direction)

    :precondition
    (and
        (pointing ?north)

        (stored ?o)
    )

    :effect
    (and
        (not (stored ?o))

        (sent ?o)

        ; memoria liberata
        (memory-free)

        ; slot liberato
        (slot-free)
    )
)

)