; ==========================================================
; DOMAIN: SATELLITE
;
; Il satellite può:
;   - ruotare
;   - fotografare oggetti
;   - inviare immagini
;
; Vincoli modellati:
;   - orientamento
;   - memoria
;   - slot immagini
;   - qualità HD / SD
;
; Compatibile con Fast Downward
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

(:types
    direction
    object
)

; ==========================================================
; PREDICATI


(:constants
    N NE E SE S SW W NW - direction
)

(:predicates

    ; orientamento corrente
    (pointing ?d - direction)

    ; oggetto visibile da una direzione
    (visible ?o - object ?d - direction)

    ; foto salvata in memoria
    (stored ?o - object)

    ; foto inviata alla Terra
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
; ROTAZIONE DESTRA


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
; ROTAZIONE SINISTRA

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
; FOTO HD

(:action take-picture-hd

    :parameters (?o - object ?d - direction)

    :precondition
    (and
        (pointing ?d)
        (visible ?o ?d)

        (hd ?o)

        (not (stored ?o))
        (not (sent ?o))

        (memory-free)
        (slot-free)
    )

    :effect
    (and
        (stored ?o)

        (not (memory-free))
        (not (slot-free))
    )
)

; ==========================================================
; FOTO SD

(:action take-picture-sd

    :parameters (?o - object ?d - direction)

    :precondition
    (and
        (pointing ?d)
        (visible ?o ?d)

        (sd ?o)

        (not (stored ?o))
        (not (sent ?o))

        (memory-free)
        (slot-free)
    )

    :effect
    (and
        (stored ?o)

        (not (memory-free))
        (not (slot-free))
    )
)

; ==========================================================
; INVIO HD

(:action send-hd

    :parameters (?o - object ?north - direction)

    :precondition
    (and
        (pointing ?north)

        (stored ?o)
        (hd ?o)
    )

    :effect
    (and
        (not (stored ?o))
        (sent ?o)

        (memory-free)
        (slot-free)
    )
)

; ==========================================================
; INVIO SD

(:action send-sd

    :parameters (?o - object ?north - direction)

    :precondition
    (and
        (pointing ?north)

        (stored ?o)
        (sd ?o)
    )

    :effect
    (and
        (not (stored ?o))
        (sent ?o)

        (memory-free)
        (slot-free)
    )
)

)