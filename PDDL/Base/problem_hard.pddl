; ==========================================================
; HARD PROBLEM
; ==========================================================
; 3 oggetti SD
; memoria sufficiente
; MA solo 2 slot disponibili
; ==========================================================

(define (problem satellite-hard)

(:domain satellite)

(:objects

    n ne e se s sw w nw - direction

    star1 planet1 galaxy1 dust1 junk2 - object
)

(:init

    (pointing sw)

    (is-north n)

    (slot1-free)
    (slot2-free)

    ; qualità
    (required-sd star1)
    (required-sd planet1)
    (required-sd galaxy1)

    ; visibilità
    (visible star1 e)
    (visible dust1 e)

    (visible planet1 s)

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