; ==========================================================
; HARD HD PROBLEM
; ==========================================================
; 3 oggetti HD
; solo 1 HD alla volta possibile
; ==========================================================

(define (problem satellite-hard-hd)

(:domain satellite)

(:objects

    n ne e se s sw w nw - direction

    star1 planet1 galaxy1 dust1 asteroidX junk2 - object
)

(:init

    (pointing sw)

    (is-north n)

    (slot1-free)
    (slot2-free)

    ; qualità
    (required-hd star1)
    (required-hd planet1)
    (required-hd galaxy1)

    ; visibilità
    (visible star1 e)
    (visible dust1 e)

    (visible planet1 s)
    (visible asteroidX s)

    (visible galaxy1 nw)
    (visible junk2 nw)

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
    )
)

(:metric minimize (total-cost))

)