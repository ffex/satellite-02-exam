; ==========================================================
; PROBLEM: EXTREME
; ==========================================================

(define (problem satellite-extreme)

(:domain satellite)

; ==========================================================
; OBJECTS
(:objects
    star1 planet1 galaxy1 nebula1 - target
)

; ==========================================================
; INITIAL STATE
(:init
    (pointing N)
    (is-north N)

    (visible star1 SE)
    (visible planet1 SW)
    (visible galaxy1 NE)
    (visible nebula1 W)

    ; Требования к качеству фотографий (перенесены из Goal)
    (hd star1)
    (sd planet1)
    (hd galaxy1)
    (sd nebula1)

    ; Численные переменные
    (= (memory-used) 0)
    (= (max-memory) 13) ; Вместимость из твоего файла
    (= (charge) 120)    ; Заряд (было energy)
    (= (photo-count) 0)

    ; Топология компаса
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
        (sent planet1)
        (sent galaxy1)
        (sent nebula1)
    )
)

; Ищем план, в котором останется как можно больше энергии
(:metric maximize (charge))

)