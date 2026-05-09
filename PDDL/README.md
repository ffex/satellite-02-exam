STRUTTURA DEL PROGETTO

Il progetto è composto da tre livelli separati che lavorano insieme:

(1) Modello PDDL (domain + problem)
Definisce:

il mondo (satellite, direzioni, oggetti)
le azioni possibili (rotate, take-picture, send)
i vincoli logici (visibilità, direzione, invio a nord)
il costo delle azioni (total-cost)

È la parte “formale” che Fast Downward usa per pianificare.

(2) Planner (Fast Downward)
File: PE_IM_planner_runner.py

Si occupa di:

lanciare Fast Downward con varie strategie (A*, greedy, BFS, ecc.)
leggere il piano prodotto (sas_plan)
orchestrare tutta la pipeline

(3) Interpreter (simulazione piano)
File: PDDLPlanInterpreter

Serve a:

simulare passo-passo il piano trovato
aggiornare stato interno (slot, direzione, invii)
debug visivo del comportamento del piano

NON influenza il planner, è solo debug.

2. MODELLO DEL DOMINIO (SATELLITE)

Il dominio rappresenta:

Spazio
8 direzioni: N, NE, E, SE, S, SW, W, NW
movimento tramite:
rotate-right
rotate-left

Fotografia
Oggetti (star1, ecc.)
Due tipi:
HD
SD

Regola:

puoi fotografare solo se:
sei orientato correttamente
l’oggetto è visibile
non è già stato fotografato o inviato

MEMORY (MODELLO ATTUALE)

slot1-free, slot2-free
stored-hd, stored-sd
hd-in-memory

memoria = massimo 2 slot
HD viene “limitato logicamente” con flag

La traccia dice:
Memory occupies:

SD = 3 units
HD = 10 units
max memory capacity constraint

NON SIAMO MODELLANDO LE UNITÀ NUMERICHE.
binario (slot-based)
non quantitativo

CONSEGUENZA

Il planner:

NON sa che HD “costa di più”
NON sa che SD+HD = 13 limite
NON usa questo per heuristics

le euristiche NON vedono il vero costo dello stato

3. TAKE-PICTURE E VINCOLI
Vincoli rispettati:
visibilità
direzione corretta
no duplicati
max 2 foto (implicitamente)

NON rispettato formalmente:

La traccia dice:

TakePic not possible if not enough memory
NOI:

sempre possibile se slot libero( forse va bene)
non dipende da capacità numerica

4. SEND

deve essere a Nord
invia 1 foto alla volta
libera slot



5. COSTI AZIONI

rotate = 1 
take-picture = 2 
send = 2 


6. INTERPRETER (simulazione piano)

L’interpreter:

NON replica la logica PDDL
aggiorna solo stato simbolico:
slot1 / slot2
sent set

serve solo debugging

7. COSA NON RISPETTA PERFETTAMENTE LA TRACCIA

Ecco i punti critici reali:

(1) MEMORY NON NUMERICA

La traccia richiede:

SD = 3 unità
HD = 10 unità
max memory constraint


slot-based
nessuna somma reale
nessun vincolo numerico

(2) EURISTICHE NON INFORMATE SULLA MEMORIA

Poiché non hai fluent numerici:

LM-CUT / FF / HMAX NON vedono:
costo memoria
trade-off HD vs SD

planner “non capisce” il problema reale

(3) VINCOLO “NOT ENOUGH MEMORY”

Non esiste davvero nel dominio:

è simulato indirettamente con slot + flag

8. Serve modello con :fluents
    Secondo me non supportato, non sono riuscito a usarlo

Quindi ho usato encoding simbolico 