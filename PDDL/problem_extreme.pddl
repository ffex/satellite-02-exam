; ==========================================================
; EXTREME PROBLEM
; ==========================================================
; Posizione iniziale: N
; Goal: star1 HD (SE), planet1 SD (SW), galaxy1 HD (NE), nebula1 SD (W)
;
; 4 oggetti misti HD/SD in 4 direzioni diverse.
; Memoria 13: HD+SD entrano insieme (13), HD+HD no (20 > 13).
; Il planner deve trovare l'ordine ottimale di scatto/invio.
; ==========================================================

(define (problem satellite_extreme)
  (:domain satellite)

  (:objects
      star1 planet1 galaxy1 nebula1 - object
      N NE E SE S SW W NW - direction
  )

  (:init
      ; orientamento iniziale
      (pointing N)

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
      (sd planet1)
      (hd galaxy1)
      (sd nebula1)

      ; visibilità
      (visible star1 SE)
      (visible planet1 SW)
      (visible galaxy1 NE)
      (visible nebula1 W)
  )

  (:goal
      (and
          (sent star1)
          (sent planet1)
          (sent galaxy1)
          (sent nebula1)
      )
  )
)
