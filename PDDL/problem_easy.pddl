; ==========================================================
; EASY PROBLEM
; ==========================================================
; Posizione iniziale: N
; Goal: star1 HD inviata
; Oggetti: star1 visibile da E
;
; Il satellite deve:
;   1. ruotare da N verso E (2 passi: N→NE→E oppure N→NW→W→SW→S→SE→E)
;   2. scattare la foto HD
;   3. ruotare verso N
;   4. inviare
; ==========================================================

(define (problem satellite_easy)
  (:domain satellite)

  (:objects
      star1 - object
      N NE E - direction
  )

  (:init
      ; orientamento iniziale
      (pointing N)

      ; adiacenze orarie per le direzioni usate in questo problema
      ; (adjacent ?a ?b) = ruotando a destra da ?a si arriva a ?b
      (adjacent N NE)
      (adjacent NE E)
      (adjacent E NE)   ; serve per rotate-left da E verso NE

      ; risorse iniziali
      (energy-available)
      (memory-available)
      (slot-available)

      ; qualità richiesta
      (hd star1)

      ; visibilità
      (visible star1 E)
  )

  (:goal
      (sent star1)
  )
)
