; ==========================================================
; HARD HD PROBLEM
; ==========================================================
; Posizione iniziale: SW
; Goal: star1 HD (E), planet1 HD (S), galaxy1 HD (NW)
;
; Tre oggetti HD: con memoria 13 può tenerne solo 1 alla volta
; (10+10=20 > 13), ciclo send obbligato dopo ogni scatto.
; ==========================================================

(define (problem satellite_hard_hd)
  (:domain satellite)

  (:objects
      star1 planet1 galaxy1 - object
      N NE E SE S SW W NW - direction
  )

  (:init
      ; orientamento iniziale
      (pointing SW)

      ; adiacenze orarie (rosa completa)
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
      (hd galaxy1)

      ; visibilità
      (visible star1 E)
      (visible planet1 S)
      (visible galaxy1 NW)
  )

  (:goal
      (and
          (sent star1)
          (sent planet1)
          (sent galaxy1)
      )
  )
)
