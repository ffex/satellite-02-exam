(define (problem satellite-extreme)

(:domain satellite-advanced)

(:objects
    star1 planet1 galaxy1 nebula1 - object
)

(:init

    (pointing n)

    ;; visibility
    (visible star1 se)
    (visible planet1 sw)
    (visible galaxy1 ne)
    (visible nebula1 w)

    ;; numeric fluents
    (= (energy) 120)

    (= (memory-used) 0)

    (= (memory-capacity) 13)

    (= (photo-count) 0)

    (= (rotation-cost) 0)

    ;; direction graph
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
        (photo-hd star1)

        (sent planet1)
        (photo-sd planet1)

        (sent galaxy1)
        (photo-hd galaxy1)

        (sent nebula1)
        (photo-sd nebula1)
    )
)

(:metric minimize
    (+ (energy)
       (rotation-cost))
)

)