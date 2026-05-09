; ==========================================================
; PROBLEM EASY
; ==========================================================

(define (problem satellite-easy)

(:domain satellite)

; ==========================================================
; OGGETTI

(:objects

    star1 noise1 - object
)

; ==========================================================
; STATO INIZIALE

(:init

    ; orientamento iniziale
    (pointing N)

    ; memoria disponibile
    (memory-free)

    ; slot disponibile
    (slot-free)

    ; visibilità
    (visible star1 E)
    (visible noise1 E)

    ; qualità richiesta
    (hd star1)
)

; ==========================================================
; GOAL

(:goal
    (and
        (sent star1)
    )
)

)