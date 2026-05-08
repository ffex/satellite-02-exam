; ==========================================================
; PROBLEM HARD

(define (problem satellite-hard)

(:domain satellite)

; ==========================================================
; OGGETTI

(:objects

    N E S W NE NW SE SW - direction

    star1 planet1 galaxy1 dust1 junk2 - object
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

    (visible galaxy1 NW)
    (visible junk2 NW)

    ; qualità immagini
    (sd star1)
    (sd planet1)
    (sd galaxy1)
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