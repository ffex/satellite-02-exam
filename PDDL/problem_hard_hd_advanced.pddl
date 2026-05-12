(define (problem satellite-hard-hd)

(:domain satellite-advanced)

(:objects
    star1 planet1 galaxy1 - object
)

(:init

    (pointing sw)

    (visible star1 e)
    (visible planet1 s)
    (visible galaxy1 nw)

    (= (memory-used) 0)
    (= (memory-capacity) 13)

    (= (energy) 100)
    (= (photo-count) 0)

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

(:metric minimize (energy))

)