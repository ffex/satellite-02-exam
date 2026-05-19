; ==============================================================
; PROBLEM EXTREME  (BFWS v3)
; --------------------------------------------------------------
; Configurazione AIMA equivalente:
;     position    : N
;     charge      : 120
;     max_memory  : 13         (HD+SD = 13 ENTRA; HD+HD = 20 NON)
;     objects     : { SE : [star1,   debris1],
;                     SW : [planet1, dust2],
;                     NE : [galaxy1, junk3],
;                     W  : [nebula1, noise3] }
;     goal        : [ (star1,   HD),    ; 10 unita'
;                     (planet1, SD),    ;  3 unita'
;                     (galaxy1, HD),    ; 10 unita'
;                     (nebula1, SD) ]   ;  3 unita'
;
; CATENA DI LIVELLI MEMORIA (max_memory = 13)
;   l13 : memoria vuota         (free = 13, 0 foto)
;   l10 : 1 SD                  (free = 10, 1 foto)
;   l3  : 1 HD                  (free =  3, 1 foto)
;   l0  : 1 HD + 1 SD           (free =  0, 2 foto)
;   l7  : 2 SD                  (free =  7, 2 foto)
;
; Combinazioni proibite (non hanno transizione corrispondente):
;   - 2 HD : 20 byte > 13      -> non c'e' un livello per 2 HD
;   - 3 foto : violerebbe lo slot=2 -> nessuna transizione l7-> ?
;     ne l0 -> ? di take
; ==============================================================

(define (problem satellite-extreme-v3)

    (:domain satellite-v3)

    (:objects
        n ne e se s sw w nw - direction
        star1 planet1 galaxy1 nebula1 debris1 dust2 junk3 noise3 - object
        hd sd - quality
        l13 l10 l7 l3 l0 - level
    )

    (:init

        ; ---- ORIENTAMENTO INIZIALE -----------------------------
        (pointing n)
        (is-north n)

        ; ---- VISIBILITA' ---------------------------------------
        (visible star1 se)
        (visible debris1 se)
        (visible planet1 sw)
        (visible dust2 sw)
        (visible galaxy1 ne)
        (visible junk3 ne)
        (visible nebula1 w)
        (visible noise3 w)

        ; ---- QUALITA' RICHIESTA --------------------------------
        (required hd star1)
        (required sd planet1)
        (required hd galaxy1)
        (required sd nebula1)

        ; ---- STATO MEMORIA INIZIALE ----------------------------
        (mem-free l13)

        ; -- transizioni TAKE: scenarios validi (sum_byte <= 13, slot <= 2)
        ;    HD
        (mem-take hd l13 l3) ;  vuoto -> 1HD
        (mem-take hd l10 l0) ;  1SD   -> 1HD + 1SD
        ;    SD
        (mem-take sd l13 l10) ;  vuoto -> 1SD
        (mem-take sd l3 l0) ;  1HD   -> 1HD + 1SD
        (mem-take sd l10 l7) ;  1SD   -> 2SD

        ; -- transizioni SEND: l'inversa delle take
        ;    HD (rilascia 10 byte)
        (mem-send hd l3 l13) ;  1HD          -> vuoto
        (mem-send hd l0 l10) ;  1HD + 1SD    -> 1SD
        ;    SD (rilascia 3 byte)
        (mem-send sd l10 l13) ;  1SD          -> vuoto
        (mem-send sd l0 l3) ;  1HD + 1SD    -> 1HD
        (mem-send sd l7 l10) ;  2SD          -> 1SD

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
            (sent sd planet1)
            (sent hd galaxy1)
            (sent sd nebula1)
        )
    )

    (:metric minimize
        (total-cost)
    )

)