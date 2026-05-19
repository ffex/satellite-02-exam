; ==============================================================
; PROBLEM HARD_HD  (BFWS v3)
; --------------------------------------------------------------
; Configurazione AIMA equivalente:
;     position    : SW
;     charge      : 100
;     max_memory  : 13       (10 + 10 = 20 > 13 -> mai 2 HD)
;     objects     : { E  : [star1, dust1],
;                     S  : [planet1, asteroidX],
;                     NW : [galaxy1, junk2] }
;     goal        : [ (star1, HD), (planet1, HD), (galaxy1, HD) ]
;
; CATENA DI LIVELLI MEMORIA (max_memory = 13)
;   l13 : memoria vuota   (free = 13)
;   l3  : 1 HD in memoria (free = 3)
; Niente l-7: due HD non entrano. Ogni HD richiede un send
; intermedio prima della prossima.
; ==============================================================

(define (problem satellite-hard-hd-v3)

    (:domain satellite-v3)

    (:objects
        n ne e se s sw w nw - direction
        star1 planet1 galaxy1 dust1 asteroidX junk2 - object
        hd sd - quality
        l13 l3 - level
    )

    (:init

        ; ---- ORIENTAMENTO INIZIALE -----------------------------
        (pointing sw)
        (is-north n)

        ; ---- VISIBILITA' ---------------------------------------
        (visible star1 e)
        (visible dust1 e)
        (visible planet1 s)
        (visible asteroidX s)
        (visible galaxy1 nw)
        (visible junk2 nw)

        ; ---- QUALITA' RICHIESTA --------------------------------
        (required hd star1)
        (required hd planet1)
        (required hd galaxy1)

        ; ---- STATO MEMORIA INIZIALE ----------------------------
        (mem-free l13)

        ; transizioni: solo HD
        (mem-take hd l13 l3)
        (mem-send hd l3 l13)

        ; ---- GRAFO ROTAZIONE -----------------------------------
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

        (= (total-cost) 0)
    )

    (:goal
        (and
            (sent hd star1)
            (sent hd planet1)
            (sent hd galaxy1)
        )
    )

    (:metric minimize
        (total-cost)
    )

)