; ==========================================================
; DOMAIN: SATELLITE
; ==========================================================
;
; MODELLO:
;   - il satellite può puntare in 8 direzioni (rosa dei venti)
;   - può fotografare oggetti visibili nella direzione corrente
;   - può trasmettere le foto a Terra solo se punta verso N
;   - la memoria accetta al massimo 2 foto (slot-available x2)
;   - le risorse sono modellate in modo binario/fluente semplificato
;
; PREDICATI CHIAVE:
;   (pointing ?d)        — il satellite punta verso ?d
;   (adjacent ?a ?b)     — ?b è la direzione adiacente a destra di ?a
;   (visible ?o ?d)      — l'oggetto ?o è visibile dalla direzione ?d
;   (stored ?o)          — foto di ?o è in memoria (non ancora inviata)
;   (sent ?o)            — foto di ?o è stata trasmessa a Terra
;   (hd ?o)/(sd ?o)      — qualità richiesta per ?o
;   (energy-available)   — il satellite ha energia per agire
;   (memory-available)   — c'è spazio in memoria per una nuova foto
;   (slot-available)     — c'è uno slot libero (max 2 foto)
;
; AZIONI:
;   rotate-right         — ruota di uno step in senso orario
;   rotate-left          — ruota di uno step in senso antiorario
;   take-picture-hd      — scatta foto HD (occupa più memoria)
;   take-picture-sd      — scatta foto SD
;   send-photo           — trasmette la prima foto in memoria
; ==========================================================

(define (domain satellite)

(:requirements
    :strips
    :typing
    :negative-preconditions
)

(:types
    direction
    object
)

(:predicates

    ; orientamento corrente del satellite
    (pointing ?d - direction)

    ; adiacenza tra direzioni (usata per le rotazioni)
    ; (adjacent ?a ?b) significa: ruotando a destra da ?a si arriva a ?b
    (adjacent ?a - direction ?b - direction)

    ; visibilità: ?o è fotografabile quando si punta ?d
    (visible ?o - object ?d - direction)

    ; stato delle foto
    (stored ?o - object)       ; foto scattata, in memoria
    (sent ?o - object)         ; foto trasmessa a Terra

    ; qualità richiesta dal goal
    (hd ?o - object)
    (sd ?o - object)

    ; risorse
    (energy-available)         ; energia sufficiente per agire
    (memory-available)         ; spazio in memoria (unità fisiche)
    (slot-available)           ; slot libero (max 2 foto in memoria)
)


; ==========================================================
; ROTATE RIGHT — ruota in senso orario
; ==========================================================
; Precondizioni:
;   - il satellite punta ?from
;   - ?to è la direzione adiacente (oraria) a ?from
;   - c'è energia
; Effetti:
;   - non punta più ?from
;   - punta ora ?to
; ==========================================================
(:action rotate-right
    :parameters (?from - direction ?to - direction)
    :precondition (and
        (pointing ?from)
        (adjacent ?from ?to)
        (energy-available)
    )
    :effect (and
        (not (pointing ?from))
        (pointing ?to)
    )
)


; ==========================================================
; ROTATE LEFT — ruota in senso antiorario
; ==========================================================
; Simmetrico a rotate-right: usa la relazione inversa.
; (adjacent ?to ?from) significa che ?from è a destra di ?to,
; quindi ?to è a sinistra di ?from.
; ==========================================================
(:action rotate-left
    :parameters (?from - direction ?to - direction)
    :precondition (and
        (pointing ?from)
        (adjacent ?to ?from)
        (energy-available)
    )
    :effect (and
        (not (pointing ?from))
        (pointing ?to)
    )
)


; ==========================================================
; TAKE-PICTURE-HD — scatta una foto ad alta risoluzione
; ==========================================================
; Precondizioni:
;   - punta verso la direzione di ?o
;   - ?o richiede qualità HD
;   - ?o non è già stato fotografato o inviato
;   - c'è energia, memoria disponibile e uno slot libero
; Effetti:
;   - ?o finisce in memoria (stored)
;   - la memoria e lo slot vengono occupati
;
; Nota: HD occupa più memoria di SD.
; Modelliamo la differenza HD/SD come due azioni separate,
; con precondizioni sulla memoria diverse (coerente con
; il fatto che HD occupa 10 unità e SD solo 3 nel modello Python).
; ==========================================================
(:action take-picture-hd
    :parameters (?o - object ?d - direction)
    :precondition (and
        (pointing ?d)
        (visible ?o ?d)
        (hd ?o)
        (not (stored ?o))
        (not (sent ?o))
        (energy-available)
        (memory-available)
        (slot-available)
    )
    :effect (and
        (stored ?o)
        (not (memory-available))
        (not (slot-available))
    )
)


; ==========================================================
; TAKE-PICTURE-SD — scatta una foto a bassa risoluzione
; ==========================================================
; Identico a HD nelle precondizioni logiche, ma SD occupa
; meno memoria: modelliamo questo lasciando memory-available
; attivo dopo uno scatto SD (SD piccola, memoria ancora usabile).
; Il vincolo slot rimane invece sempre consumato.
; ==========================================================
(:action take-picture-sd
    :parameters (?o - object ?d - direction)
    :precondition (and
        (pointing ?d)
        (visible ?o ?d)
        (sd ?o)
        (not (stored ?o))
        (not (sent ?o))
        (energy-available)
        (slot-available)
    )
    :effect (and
        (stored ?o)
        (not (slot-available))
    )
)


; ==========================================================
; SEND-PHOTO — trasmette una foto a Terra
; ==========================================================
; Precondizioni:
;   - punta verso N (unica direzione di trasmissione)
;   - c'è almeno una foto in memoria (?o stored)
;   - c'è energia
; Effetti:
;   - ?o non è più in memoria
;   - ?o risulta inviato
;   - lo slot si libera
;   - la memoria si libera (pronta per altra foto)
; ==========================================================
(:action send-photo
    :parameters (?o - object)
    :precondition (and
        (pointing N)
        (stored ?o)
        (energy-available)
    )
    :effect (and
        (not (stored ?o))
        (sent ?o)
        (slot-available)
        (memory-available)
    )
)

)
