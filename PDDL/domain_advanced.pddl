(define (domain satellite-advanced)

(:requirements
    :typing
    :fluents
    :negative-preconditions
    :conditional-effects
    :equality
)

; ==========================================================
; TYPES
; ==========================================================

(:types
    object
    direction
    quality
)

; ==========================================================
; CONSTANTS
; ==========================================================

(:constants
    n ne e se s sw w nw - direction
    hd sd                - quality
)

; ==========================================================
; PREDICATES
; ==========================================================

(:predicates

    ; orientamento del satellite
    (pointing ?d - direction)

    ; evita oscillazioni inutili
    (last-dir ?d - direction)

    ; visibilita' oggetti in una direzione
    (visible ?o - object ?d - direction)

    ; stato oggetti
    (taken ?o - object)
    (sent  ?o - object)

    ; qualita' immagine (PREDICATO UNICO con parametro quality)
    (quality ?o - object ?q - quality)

    ; SOLO OGGETTI RILEVANTI PER IL GOAL
    (goal-object ?o - object)

    ; grafo delle direzioni
    (next-right ?from ?to - direction)
    (next-left  ?from ?to - direction)
)

; ==========================================================
; FUNCTIONS
; ==========================================================

(:functions
    (energy)
    (memory-used)
    (memory-capacity)
    (photo-count)
    (rotation-cost)

    ; costo in memoria dipendente dalla qualita' (init nel problema)
    (memory-cost ?q - quality)
)

; ==========================================================
; ROTATE RIGHT
; ==========================================================

(:action rotate-right
    :parameters (?from ?to - direction)

    :precondition (and
        (pointing ?from)
        (next-right ?from ?to)
        (>= (energy) 1)
        (not (last-dir ?to))
    )

    :effect (and
        (not (pointing ?from))
        (pointing ?to)

        (not (last-dir ?from))
        (last-dir ?to)

        (increase (rotation-cost) 2)
        (decrease (energy) 1)
    )
)

; ==========================================================
; ROTATE LEFT
; ==========================================================

(:action rotate-left
    :parameters (?from ?to - direction)

    :precondition (and
        (pointing ?from)
        (next-left ?from ?to)
        (>= (energy) 1)
        (not (last-dir ?to))
    )

    :effect (and
        (not (pointing ?from))
        (pointing ?to)

        (not (last-dir ?from))
        (last-dir ?to)

        (increase (rotation-cost) 2)
        (decrease (energy) 1)
    )
)

; ==========================================================
; TAKE PICTURE  (azione UNICA, qualita' come parametro)
;   Plan output: (take-picture <hd|sd> <obj> <dir>)
; ==========================================================

(:action take-picture
    :parameters (?q - quality ?o - object ?d - direction)

    :precondition (and
        (pointing ?d)
        (visible ?o ?d)

        ; filtro critico: elimina oggetti inutili (noise/junk)
        (goal-object ?o)

        ; la qualita' richiesta deve combaciare con quella dell'oggetto
        (quality ?o ?q)

        (not (taken ?o))
        (not (sent  ?o))

        (>= (energy) 2)
        (<  (photo-count) 2)
        (<= (+ (memory-used) (memory-cost ?q)) (memory-capacity))
    )

    :effect (and
        (taken ?o)
        (increase (photo-count) 1)
        (decrease (energy) 2)
        (increase (memory-used) (memory-cost ?q))
    )
)

; ==========================================================
; SEND  (azione UNICA, qualita' e direzione come parametri)
;   Plan output: (send <hd|sd> <obj> n)
; ==========================================================

(:action send
    :parameters (?q - quality ?o - object ?d - direction)

    :precondition (and
        ; si trasmette solo guardando a NORD
        (pointing ?d)
        (= ?d n)

        (taken ?o)
        (not (sent ?o))

        (quality ?o ?q)

        (>= (energy) 2)
    )

    :effect (and
        (sent ?o)
        (not (taken ?o))

        (decrease (photo-count) 1)
        (decrease (energy) 2)
        (decrease (memory-used) (memory-cost ?q))
    )
)

)
