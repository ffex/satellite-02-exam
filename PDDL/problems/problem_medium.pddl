; ==========================================================
; PROBLEM: MEDIUM
; ==========================================================

(define (problem satellite-medium)

(:domain satellite)

; ==========================================================
; OBJECTS
(:objects
    star1 planet1 junk1 noise2 - target
)

; ==========================================================
; INITIAL STATE
(:init
    ; Начальное направление
    (pointing S)
    ; Указываем, где Земля
    (is-north N)

    ; Видимость
    (visible star1 E)
    (visible planet1 W)

    ; Требования к качеству (перенесено из Goal)
    (hd star1)
    (hd planet1)

    ; Численные переменные
    (= (memory-used) 0)
    (= (max-memory) 13) ; Объем диска
    (= (charge) 75)     ; Стартовый заряд
    (= (photo-count) 0)

    ; Топология компаса (по часовой стрелке)
    (next-right N NE)
    (next-right NE E)
    (next-right E SE)
    (next-right SE S)
    (next-right S SW)
    (next-right SW W)
    (next-right W NW)
    (next-right NW N)

    ; Топология компаса (против часовой стрелки)
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
    )
)

; ==========================================================
; METRIC
; Ищем самый энергоэффективный маршрут
(:metric maximize (charge))

)