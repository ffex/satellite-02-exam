; ==========================================================
; MEDIUM PROBLEM
; ==========================================================
; Posizione iniziale: S
; Goal: star1 HD (visibile da E) e planet1 HD (visibile da W)
;
; La memoria da 13 unità non contiene due HD insieme (10+10=20),
; quindi il satellite deve fare un ciclo send intermedio.
; ==========================================================

(define (problem satellite_medium)
  (:domain satellite)

  (:objects
      star1 planet1 - object
      N NE E W NW S SW SE - direction
  )

  (:init
      ; orientamento iniziale
      (pointing S)

      ; adiacenze orarie (rosa completa per permettere
      ; al planner di trovare qualsiasi percorso)
      (adjacent N NE)
      (adjacent NE E)
      (adjacent E SE)
      (adjacent SE S)
      (adjacent S SW)
      (adjacent SW W)
      (adjacent W NW)
      (adjacent NW N)

      ; risorse iniziali
      (energy-available)
      (memory-available)
      (slot-available)

      ; qualità richiesta
      (hd star1)
      (hd planet1)

      ; visibilità
      (visible star1 E)
      (visible planet1 W)
  )

  (:goal
      (and
          (sent star1)
          (sent planet1)
      )
  )
)
