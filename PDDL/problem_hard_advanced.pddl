(define (problem satellite-hard)
(:domain satellite-advanced)

(:objects
    star1 planet1 galaxy1 dust1 junk2 - object
)

(:init

    (pointing sw)
    (last-dir sw)

    (visible star1 e)
    (visible planet1 s)
    (visible galaxy1 nw)

    (quality-sd star1)
    (quality-sd planet1)
    (quality-sd galaxy1)

    (= (energy) 75)
    (= (memory-used) 0)
    (= (memory-capacity) 16)
    (= (photo-count) 0)
    (= (rotation-cost) 0)

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
    )
)

(:metric minimize (+ (energy) (rotation-cost)))
)