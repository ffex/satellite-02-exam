; ==========================================================
; PROBLEM MEDIUM
; ==========================================================

(define (problem satellite-medium)

(:domain satellite)

; ==========================================================
; OGGETTI

(:objects

    N E S W NE NW SE SW - direction

    star1 planet1 junk1 noise2 - object
)

; ==========================================================
; STATO INIZIALE

(:init

    ; orientamento iniziale
    (pointing S)

    ; risorse disponibili
    (memory-free)
    (slot-free)

    ; visibilità oggetti
    (visible star1 E)
    (visible junk1 E)

    (visible planet1 W)
    (visible noise2 W)

    ; qualità immagini
    (hd star1)
    (hd planet1)
)

; ==========================================================
; GOAL

(:goal
    (and
        (sent star1)
        (sent planet1)
    )
)

)