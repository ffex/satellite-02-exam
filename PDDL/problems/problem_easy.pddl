; ==============================================================
; PROBLEM EASY  (BFWS v3)
; --------------------------------------------------------------
; Configurazione AIMA equivalente:
;     position    : N
;     charge      : 20         (consumo atteso ~8: largo budget)
;     max_memory  : 20         (1 HD = 10 entra comodo)
;     objects     : { E : [star1, noise1] }
;     goal        : [ (star1, HD) ]
;
; CATENA DI LIVELLI MEMORIA (max_memory = 20)
;   l20 : memoria vuota   (free = 20)
;   l10 : 1 HD in memoria (free = 10)
;
; CATENA DI ROTAZIONE
;   le 8 direzioni di una compass rose, con next-right/next-left
;   dichiarate nell'init come grafo del satellite.
; ==============================================================

(define (problem satellite-easy-v3)

    (:domain satellite-v3)

    (:objects
        ; direzioni della compass rose
        n ne e se s sw w nw - direction
        ; oggetti nel cielo
        star1 noise1 - object
        ; qualita' disponibili
        hd sd - quality
        ; livelli di memoria libera reachable per questo problema
        l20 l10 - level
    )

    (:init

        ; ---- ORIENTAMENTO INIZIALE -----------------------------
        (pointing n)
        (is-north n) ; marker: send si fa da qui

        ; ---- VISIBILITA' ---------------------------------------
        (visible star1 e)
        (visible noise1 e) ; rumore: non e' nel goal

        ; ---- QUALITA' RICHIESTA DAL GOAL -----------------------
        (required hd star1)

        ; ---- STATO MEMORIA INIZIALE ----------------------------
        ; memoria vuota -> max_memory libero (l20)
        (mem-free l20)

        ; transizioni di take (qui basta HD: nessun oggetto SD richiesto)
        (mem-take hd l20 l10) ; scatto HD da vuoto -> 10 free
        ; transizioni di send
        (mem-send hd l10 l20) ; libero la foto HD -> 20 free

        ; ---- GRAFO DI ROTAZIONE (orario) -----------------------
        (next-right n ne)
        (next-right ne e)
        (next-right e se)
        (next-right se s)
        (next-right s sw)
        (next-right sw w)
        (next-right w nw)
        (next-right nw n)

        ; ---- GRAFO DI ROTAZIONE (antiorario) -------------------
        (next-left ne n)
        (next-left e ne)
        (next-left se e)
        (next-left s se)
        (next-left sw s)
        (next-left w sw)
        (next-left nw w)
        (next-left n nw)

        ; ---- COSTO INIZIALE ------------------------------------
        (= (total-cost) 0)
    )

    (:goal
        (sent hd star1)
    )

    (:metric minimize
        (total-cost)
    )

)