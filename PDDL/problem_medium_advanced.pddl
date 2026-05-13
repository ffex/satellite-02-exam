(define (problem satellite-medium)
(:domain satellite-advanced)

(:objects
    star1 planet1 junk1 noise2 - object
)

(:init

    (pointing s)
    (last-dir s)

    (visible star1 e)
    (visible planet1 w)

    (quality-hd star1)
    (quality-sd planet1)

    ; 🔴 SOLO OGGETTI DEL GOAL
    (goal-object star1)
    (goal-object planet1)

    (= (energy) 50)
    (= (memory-used) 0)
    (= (memory-capacity) 13)
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
    )
)

(:metric minimize (+ (energy) (rotation-cost)))
)