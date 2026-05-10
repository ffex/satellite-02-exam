(define (problem satellite-hard)

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
    (= (memory-capacity) 16)

    (= (energy) 75)
    (= (photo-count) 0)

)

(:goal
    (and
        (sent star1)
        (photo-sd star1)

        (sent planet1)
        (photo-sd planet1)

        (sent galaxy1)
        (photo-sd galaxy1)
    )
)

(:metric minimize (energy))

)