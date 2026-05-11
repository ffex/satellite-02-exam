; ==========================================================
; PROBLEM: EASY
; ==========================================================

(define (problem satellite-easy)

(:domain satellite)

; ==========================================================
; OBJECTS
(:objects
    star1 noise1 - target
)

; ==========================================================
; INITIAL STATE
(:init
    (pointing N)
    (is-north N) ;

    (visible star1 E)
    (visible noise1 E)

    (hd star1)

    (= (charge) 20)
    (= (memory-used) 0)
    (= (photo-count) 0)
    (= (max-memory) 20)

    (next-right N NE)
    (next-right NE E)
    (next-right E SE)
    (next-right SE S)
    (next-right S SW)
    (next-right SW W)
    (next-right W NW)
    (next-right NW N)

    (next-left N NW)
    (next-left NW W)
    (next-left W SW)
    (next-left SW S)
    (next-left S SE)
    (next-left SE E)
    (next-left E NE)
    (next-left NE N)
)

; ==========================================================
; GOAL STATE
(:goal
    (and
        (sent star1)
    )
)

)