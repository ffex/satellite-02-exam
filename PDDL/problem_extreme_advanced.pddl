(define (problem satellite-extreme)
(:domain satellite-advanced)

(:objects
    star1 planet1 galaxy1 nebula1 - object
)

(:init

    (pointing n)

    ; visibilità
    (visible star1 se)
    (visible planet1 sw)
    (visible galaxy1 ne)
    (visible nebula1 w)

    ; qualità
    (quality-hd star1)
    (quality-sd planet1)
    (quality-hd galaxy1)
    (quality-sd nebula1)

    ; 🔴 SOLO OGGETTI DEL GOAL
    (goal-object star1)
    (goal-object planet1)
    (goal-object galaxy1)
    (goal-object nebula1)

    ; risorse
    (= (energy) 120)
    (= (memory-used) 0)
    (= (memory-capacity) 13)
    (= (photo-count) 0)
    (= (rotation-cost) 0)

    ; direzioni
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
)

(:goal
    (and
        (sent star1)
        (sent planet1)
        (sent galaxy1)
        (sent nebula1)
    )
)

(:metric minimize (+ (energy) (rotation-cost)))
)