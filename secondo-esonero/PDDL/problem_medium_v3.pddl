; ==============================================================
; PROBLEM MEDIUM  (BFWS v3)
; --------------------------------------------------------------
; Configurazione AIMA equivalente:
;     position    : S
;     charge      : 50         (consumo atteso ~16-20: budget largo)
;     max_memory  : 13         (1 HD entra, 2 HD = 20 > 13 NON entrano)
;     objects     : { E : [star1, junk1],
;                     W : [planet1, noise2] }
;     goal        : [ (star1, HD), (planet1, HD) ]
;
; CATENA DI LIVELLI MEMORIA (max_memory = 13)
;   l13 : memoria vuota   (free = 13)
;   l3  : 1 HD in memoria (free = 3)
; Non c'e' un livello che rappresenti 2 HD: la catena lo proibisce
; rendendo il vincolo max_memory parte della struttura del problema.
; ==============================================================

(define (problem satellite-medium-v3)

(:domain satellite-v3)

(:objects
    n ne e se s sw w nw         - direction
    star1 planet1 junk1 noise2  - object
    hd sd                       - quality
    l13 l3                      - level
)

(:init

    ; ---- ORIENTAMENTO INIZIALE -----------------------------
    (pointing s)
    (is-north n)

    ; ---- VISIBILITA' ---------------------------------------
    (visible star1 e)
    (visible junk1 e)
    (visible planet1 w)
    (visible noise2 w)

    ; ---- QUALITA' RICHIESTA --------------------------------
    (required hd star1)
    (required hd planet1)

    ; ---- STATO MEMORIA INIZIALE ----------------------------
    (mem-free l13)

    ; transizioni: solo HD perche' il goal e' solo HD
    (mem-take hd l13 l3)
    (mem-send hd l3  l13)

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
))

(:metric minimize (total-cost))

)
