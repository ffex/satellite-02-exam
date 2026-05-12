(define (problem satellite-extreme)

(:domain satellite-advanced)

(:objects
    star1 planet1 galaxy1 nebula1 - object
)

(:init

    (pointing n)

    (visible star1 se)
    (visible planet1 sw)
    (visible galaxy1 ne)
    (visible nebula1 w)

    (= (memory-used) 0)
    (= (memory-capacity) 13)

    (= (energy) 120)
    (= (photo-count) 0)

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

(:metric minimize (energy))

)