(define (problem satellite-easy)

(:domain satellite-advanced)

(:objects
    star1 noise1 - object
)

(:init

    (pointing n)

    (visible star1 e)
    (visible noise1 e)

    (= (memory-used) 0)
    (= (memory-capacity) 20)

    (= (energy) 20)
    (= (photo-count) 0)

    (next-right n ne)
    (next-right ne e)
    (next-right e se)
    (next-right se s)
    (next-right s sw)
    (next-right sw w)
    (next-right w nw)
    (next-right nw n)

    (next-left n nw)
    (next-left nw w)
    (next-left w sw)
    (next-left sw s)
    (next-left s se)
    (next-left se e)
    (next-left e ne)
    (next-left ne n)

)

(:goal
    (and
        (sent star1)
        (photo-hd star1)
    )
)

(:metric minimize (energy))

)