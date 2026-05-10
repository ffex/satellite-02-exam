(define (problem satellite-medium)

(:domain satellite-advanced)

(:objects
    star1 planet1 junk1 noise2 - object
)

(:init

    (pointing s)

    (visible star1 e)
    (visible planet1 w)

    (= (memory-used) 0)
    (= (memory-capacity) 200)

    (= (energy) 400)
    (= (photo-count) 0)

)

(:goal
    (and
        (sent star1)
        (photo-hd star1)

        (sent planet1)
        (photo-hd planet1)
    )
)

(:metric minimize (energy))

)