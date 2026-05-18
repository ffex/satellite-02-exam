; ==============================================================
; PROBLEM HARD  (BFWS v3)
; --------------------------------------------------------------
; Configurazione AIMA equivalente:
;     position    : SW
;     charge      : 75
;     max_memory  : 16   (3 SD = 9 entrerebbero in memoria,
;                         ma vincolo "2 foto" forza un ciclo send
;                         intermedio)
;     objects     : { E  : [star1,   dust1],
;                     S  : [planet1],
;                     NW : [galaxy1, junk2] }
;     goal        : [ (star1, SD), (planet1, SD), (galaxy1, SD) ]
;
; CATENA DI LIVELLI MEMORIA (max_memory = 16)
;   l16 : memoria vuota   (free = 16)
;   l13 : 1 SD            (free = 13)
;   l10 : 2 SD            (free = 10)
;   Niente livello per 3 SD: il vincolo slot=2 fa terminare
;   la catena qui. Per scattare la 3a SD serve un send prima.
; ==============================================================

(define (problem satellite-hard-v3)

(:domain satellite-v3)

(:objects
    n ne e se s sw w nw                       - direction
    star1 planet1 galaxy1 dust1 junk2         - object
    hd sd                                     - quality
    l16 l13 l10                               - level
)

(:init

    ; ---- ORIENTAMENTO INIZIALE -----------------------------
    (pointing sw)
    (is-north n)

    ; ---- VISIBILITA' ---------------------------------------
    (visible star1 e )
    (visible dust1 e )
    (visible planet1 s )
    (visible galaxy1 nw)
    (visible junk2 nw)

    ; ---- QUALITA' RICHIESTA --------------------------------
    (required sd star1)
    (required sd planet1)
    (required sd galaxy1)

    ; ---- STATO MEMORIA INIZIALE ----------------------------
    (mem-free l16)

    ; transizioni: solo SD perche' il goal e' solo SD
    (mem-take sd l16 l13)
    (mem-take sd l13 l10)
    (mem-send sd l13 l16)
    (mem-send sd l10 l13)

    ; ---- GRAFO ROTAZIONE -----------------------------------
    (next-right n  ne) (next-right ne e ) (next-right e  se)
    (next-right se s ) (next-right s  sw) (next-right sw w )
    (next-right w  nw) (next-right nw n )

    (next-left  ne n ) (next-left  e  ne) (next-left  se e )
    (next-left  s  se) (next-left  sw s ) (next-left  w  sw)
    (next-left  nw w ) (next-left  n  nw)

    (= (total-cost) 0)
)

(:goal (and
    (sent star1)
    (sent planet1)
    (sent galaxy1)
))

(:metric minimize (total-cost))

)
