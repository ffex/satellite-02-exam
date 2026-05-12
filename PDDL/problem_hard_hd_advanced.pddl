(define (problem satellite-hard-hd)

(:domain satellite-advanced)

(:objects
    star1 planet1 galaxy1 - object
)

(:init

    (pointing sw)

    ;; visibility
    (visible star1 e)
    (visible planet1 s)
    (visible galaxy1 nw)

    ;; numeric fluents
    (= (energy) 100)

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
        (photo-hd planet1)

        (sent galaxy1)
        (photo-hd galaxy1)
    )
)

(:metric minimize
    (+ (energy)
       (rotation-cost))
)

)