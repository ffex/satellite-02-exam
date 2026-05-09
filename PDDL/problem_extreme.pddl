; ==========================================================
; PROBLEM EXTREME
; ==========================================================

(define (problem satellite-extreme)

(:domain satellite)

; ==========================================================
; OGGETTI

(:objects

    star1 planet1 galaxy1 nebula1
    debris1 dust2 junk3 noise3 - object
)

; ==========================================================
; STATO INIZIALE

(:init

    ; orientamento iniziale
    (pointing N)

    ; risorse
    (memory-free)
    (slot-free)

    ; visibilità
    (visible star1 SE)
    (visible debris1 SE)

    (visible planet1 SW)
    (visible dust2 SW)

    (visible galaxy1 NE)
    (visible junk3 NE)

    (visible nebula1 W)
    (visible noise3 W)

    ; qualità immagini
    (hd star1)
    (sd planet1)

    (hd galaxy1)
    (sd nebula1)
)

; ==========================================================
; GOAL

(:goal
    (and
        (sent star1)
        (sent planet1)
        (sent galaxy1)
        (sent nebula1)
    )
)

)