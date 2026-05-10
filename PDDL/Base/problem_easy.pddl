; ==========================================================
; EASY PROBLEM
; ==========================================================
; Posizione iniziale : N
; Carica             : sufficiente (non modellata numericamente)
; Goal               : star1 HD inviata
;
; Oggetti: star1 (HD) visibile da E, noise1 non nel goal
;
; Piano atteso:
;   rotate-right n ne → rotate-right ne e
;   take-picture-hd-s1 star1 e
;   rotate-left e ne → rotate-left ne n
;   send-hd-s1 star1 n
;
; ==========================================================

(define (problem satellite-easy)

(:domain satellite)

(:objects
    n ne e se s sw w nw - direction
    star1 noise1 - object
)

(:init

    ; orientamento iniziale
    (pointing n)

    ; (is-north n): marcatore che indica qual è la direzione Nord.
    ; Serve perché nel domain 'n' è un oggetto, non una costante:
    ; non si può scrivere (pointing n) come precondizione nel domain.
    (is-north n)

    ; slot di memoria inizialmente liberi
    (slot1-free)
    (slot2-free)

    ; qualità richiesta
    (required-hd star1)

    ; visibilità degli oggetti per direzione
    (visible star1 e)
    (visible noise1 e)

    ; grafo di rotazione oraria (next-right)
    (next-right n  ne)
    (next-right ne e)
    (next-right e  se)
    (next-right se s)
    (next-right s  sw)
    (next-right sw w)
    (next-right w  nw)
    (next-right nw n)

    ; grafo di rotazione antioraria (next-left)
    (next-left ne n)
    (next-left e  ne)
    (next-left se e)
    (next-left s  se)
    (next-left sw s)
    (next-left w  sw)
    (next-left nw w)
    (next-left n  nw)

    ; costo iniziale azzerato
    (= (total-cost) 0)
)

(:goal
    (sent star1)
)

; minimizza il costo totale (energia spesa)
(:metric minimize (total-cost))

)
