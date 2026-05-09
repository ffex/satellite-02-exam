; ==========================================================
; PROBLEM HARD HD
; ==========================================================

(define (problem satellite-hard-hd)

(:domain satellite)

; ==========================================================
; OGGETTI

(:objects

    star1 planet1 galaxy1 dust1 junk2 asteroidX - object
)

; ==========================================================
; STATO INIZIALE

(:init

    ; orientamento iniziale
    (pointing SW)

    ; risorse
    (memory-free)
    (slot-free)

    ; visibilità
    (visible star1 E)
    (visible dust1 E)

    (visible planet1 S)
    (visible asteroidX S)

    (visible galaxy1 NW)
    (visible junk2 NW)

    ; qualità immagini
    (hd star1)
    (hd planet1)
    (hd galaxy1)
)

; ==========================================================
; GOAL

(:goal
    (and
        (sent star1)
        (sent planet1)
        (sent galaxy1)
    )
)

)