; ==========================================================
; EXTREME PROBLEM
; ==========================================================
; 4 oggetti misti HD/SD
; pianificazione complessa
; ==========================================================

(define (problem satellite-extreme)

(:domain satellite)

(:objects

    n ne e se s sw w nw - direction

    star1 planet1 galaxy1 nebula1
    debris1 dust2 junk3 noise3 - object
)

(:init

    (pointing n)

    (is-north n)

    (slot1-free)
    (slot2-free)

    ; qualità
    (required-hd star1)
    (required-sd planet1)
    (required-hd galaxy1)
    (required-sd nebula1)

    ; visibilità
    (visible star1 se)
    (visible debris1 se)

    (visible planet1 sw)
    (visible dust2 sw)

    (visible galaxy1 ne)
    (visible junk3 ne)

    (visible nebula1 w)
    (visible noise3 w)

    ; rotazioni
    (next-right n ne)
    (next-right ne e)
    (next-right e se)
    (next-right se s)
    (next-right s sw)
    (next-right sw w)
    (next-right w nw)
    (next-right nw n)

    (next-left ne n)
    (next-left e ne)
    (next-left se e)
    (next-left s se)
    (next-left sw s)
    (next-left w sw)
    (next-left nw w)
    (next-left n nw)

    (= (total-cost) 0)
)

(:goal
    (and
        (sent star1)
        (sent planet1)
        (sent galaxy1)
        (sent nebula1)
    )
)

(:metric minimize (total-cost))

)