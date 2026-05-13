(define (problem satellite-easy)
(:domain satellite-advanced)

(:objects
    star1 noise1 - object
)

(:init

    ; ======================================================
    ; STATO SATELLITE
    ; ======================================================
    (pointing n)
    (last-dir n)

    ; ======================================================
    ; VISIBILITÀ
    ; ======================================================
    (visible star1 e)
    (visible noise1 e)

    ; ======================================================
    ; QUALITÀ IMMAGINI
    ; ======================================================
    (quality-hd star1)

    ; ======================================================
    ; GOAL SEMANTICO: SOLO STAR1 È RILEVANTE
    ; ======================================================
    (goal-object star1)

    ; ======================================================
    ; RISORSE
    ; ======================================================
    (= (energy) 20)
    (= (memory-used) 0)
    (= (memory-capacity) 20)
    (= (photo-count) 0)
    (= (rotation-cost) 0)

    ; ======================================================
    ; GRAFO DIREZIONI
    ; ======================================================
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
    )
)

(:metric minimize (+ (energy) (rotation-cost)))

)