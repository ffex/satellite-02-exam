; ==========================================================
; MEDIUM PROBLEM
; ==========================================================
; 2 oggetti HD
; memoria insufficiente per tenerli insieme
; il satellite deve fare:
;
;   take → send → take → send
;
; ==========================================================

(define (problem satellite-medium)

(:domain satellite)

(:objects

    n ne e se s sw w nw - direction

    star1 planet1 junk1 noise2 - object
)

(:init

    ; posizione iniziale
    (pointing s)

    ; nord
    (is-north n)

    ; slot memoria
    (slot1-free)
    (slot2-free)

    ; qualità richiesta
    (required-hd star1)
    (required-hd planet1)

    ; visibilità
    (visible star1 e)
    (visible junk1 e)

    (visible planet1 w)
    (visible noise2 w)

    ; rotazioni right
    (next-right n ne)
    (next-right ne e)
    (next-right e se)
    (next-right se s)
    (next-right s sw)
    (next-right sw w)
    (next-right w nw)
    (next-right nw n)

    ; rotazioni left
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
        (sent star1)
        (sent planet1)
    )
)

(:metric minimize (total-cost))

)