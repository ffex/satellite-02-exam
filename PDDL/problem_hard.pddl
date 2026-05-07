; ==========================================================
; HARD PROBLEM (SD)
; ==========================================================
; Posizione iniziale: SW
; Goal: star1 SD (E), planet1 SD (S), galaxy1 SD (NW)
;
; Tre oggetti SD: tutti entrano in memoria (3+3=6 < 16),
; ma il vincolo dei 2 slot rimane il collo di bottiglia.
; ==========================================================

(define (problem satellite_hard)
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
      (sd star1)
      (sd planet1)
      (sd galaxy1)

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
