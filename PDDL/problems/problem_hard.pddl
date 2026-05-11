; ==========================================================
; PROBLEM: HARD
; ==========================================================

(define (problem satellite-hard)

(:domain satellite)

; ==========================================================
; OBJECTS
(:objects
    star1 planet1 galaxy1 - target
)

; ==========================================================
; INITIAL STATE
(:init
    ; Начальное направление (Юго-Запад)
    (pointing SW)
    ; Указываем, где находится Земля для отправки
    (is-north N)

    ; Видимость объектов
    (visible star1 E)
    (visible planet1 S)
    (visible galaxy1 NW)

    ; Требования к качеству (перенесено из Goal)
    (sd star1)
    (sd planet1)
    (sd galaxy1)

    ; Численные переменные
    (= (memory-used) 0)
    (= (max-memory) 16) ; Вместимость из оригинального файла
    (= (charge) 75)     ; Заряд (было energy)
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
        (sent galaxy1)
    )
)

; ==========================================================
; METRIC
; Ищем план, который сохранит максимум батареи
(:metric maximize (charge))

)