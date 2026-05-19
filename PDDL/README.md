# Satellite PDDL — Documentazione del Progetto

## 1. Descrizione del problema

Un satellite artificiale è orientato in una delle 8 posizioni della rosa dei venti (N, NE, E, SE, S, SW, W, NW). Può ruotare di una posizione alla volta (destra o sinistra). In varie direzioni sono presenti oggetti celesti (stelle, pianeti, galassie, ecc.) che possono essere fotografati se il satellite è orientato nella giusta direzione e la memoria è sufficiente. Le foto possono essere in alta risoluzione (HD, 10 unità) o bassa risoluzione (SD, 3 unità). La memoria massima è 2 foto. Le foto possono essere inviate a Terra (solo da N, costo 2) liberando la memoria, una foto alla volta. L'obiettivo è inviare a Terra un insieme specifico di foto minimizzando il costo totale.

## 2. Domain: scelte implementative

### Tipi

```pddl
(:types direction object quality level)
```

Quattro tipi distinti. Questa separazione è fondamentale perché ogni tipo ha un ruolo diverso nel domain e impedisce di confondere tra loro oggetti che non devono interagire.

- `direction` — le 8 posizioni della rosa dei venti (N, NE, …, NW)
- `object` — gli oggetti celesti fotografabili (star1, planet1, ecc.) e anche i "rumori" (noise1, junk1, ecc.) che esistono nel cielo ma non sono nel goal
- `quality` — hd o sd; definisce il tipo di foto e il suo peso in memoria
- `level` — livelli discreti di memoria libera; il trucco centrale della modellazione (vedi sezione 3)

### Predicati

```pddl
(pointing ?d - direction)
```
Indica la direzione corrente del satellite. Solo una direzione alla volta può avere questo predicato attivo (garantito dalla struttura delle azioni rotate).

```pddl
(next-right ?from - direction ?to - direction)
(next-left  ?from - direction ?to - direction)
```
Codificano il grafo di rotazione della rosa dei venti come lista di fatti. Sono dichiarati nell'init di ogni problem (non nel domain) perché sono dati del problema, non della struttura del domain. Questa scelta permette in linea di principio di cambiare il grafo di rotazione in un problem diverso senza toccare il domain.

```pddl
(is-north ?d - direction)
```
Marca quale direzione è il Nord. Serve come precondizione dell'azione `send`: si invia solo dal Nord. Anche questo è nel problem e non hardcoded nel domain, per flessibilità.

```pddl
(visible ?o - object ?d - direction)
```
Indica che l'oggetto `?o` è visibile dalla direzione `?d`. È un fatto statico (non cambia durante l'esecuzione): viene dichiarato nell'init e nessuna azione lo modifica.

```pddl
(required ?q - quality ?o - object)
```
Indica che per l'oggetto `?o` è richiesta una foto di qualità `?q`. Anche questo è statico. Serve come precondizione di `take-picture` per evitare di scattare foto inutili (di qualità sbagliata o di oggetti non nel goal).

```pddl
(stored ?q - quality ?o - object)
(sent   ?q - quality ?o - object)
```
Tracciano lo stato di ogni foto: se è in memoria (`stored`) o già inviata a Terra (`sent`). La distinzione tra i due è necessaria perché `sent` è il goal e `stored` è lo stato intermedio. L'azione `send` porta dallo `stored` al `sent` e libera memoria.

```pddl
(captured ?o - object)
```
Flag che impedisce di scattare due volte la stessa foto. Una volta che `?o` è stato fotografato (indipendentemente da se la foto è ancora in memoria o già inviata), `captured` resta vero per sempre. Senza questo predicato il planner potrebbe scattare la stessa foto più volte per riempire/svuotare memoria in modo ciclico.

```pddl
(mem-free  ?l - level)
(mem-take  ?q - quality ?from - level ?to - level)
(mem-send  ?q - quality ?from - level ?to - level)
```
Il cuore della modellazione della memoria (vedi sezione 3).

### Azioni

**rotate-right / rotate-left** — costo 1 ciascuna. Cambiano `pointing` da `?from` a `?to` usando il grafo next-right/next-left. Il costo 1 riflette il fatto che ogni rotazione è meno costosa di uno scatto o di un invio.

**take-picture** — costo 2. Precondizioni: il satellite punta nella direzione giusta, l'oggetto è visibile lì, la qualità è quella richiesta, l'oggetto non è già stato catturato, la foto non è già stata inviata, e c'è abbastanza memoria (mem-take da `?from` a `?to` esiste). Effetti: la foto entra in memoria (`stored`), l'oggetto viene marcato come catturato, la memoria si aggiorna.

**send** — costo 2. Precondizioni: il satellite punta a Nord, la foto è in memoria, la qualità e l'oggetto corrispondono al `required`. Effetti: la foto esce dalla memoria e viene marcata come `sent`, la memoria si aggiorna.

## 3. Modellazione della memoria

PDDL strips non ha fluent numerici (o meglio, li ha con `:action-costs` ma solo per il costo totale, non per vincoli nelle precondizioni). Non si può scrivere direttamente `(>= memory-free 10)` come precondizione. Bisogna codificare i vincoli di memoria in modo puramente proposizionale.

### La soluzione: livelli discreti

Si introduce il tipo `level` e i predicati `mem-free`, `mem-take`, `mem-send`. I livelli rappresentano la quantità di memoria libera e formano una catena di transizioni.

`(mem-free ?l)` dice "la memoria libera corrente è il livello `?l`".

`(mem-take ?q ?from ?to)` dice "se la memoria libera è `?from` e scatto una foto di qualità `?q`, la memoria libera diventa `?to`".

`(mem-send ?q ?from ?to)` dice "se la memoria libera è `?from` e invio una foto di qualità `?q`, la memoria libera diventa `?to`".

Il vincolo "massimo 2 foto" e il vincolo "memoria massima N byte" sono entrambi codificati nella catena: se non esiste una transizione `mem-take` dal livello corrente, l'azione `take-picture` è inapplicabile. Non servono controlli espliciti.

### Esempio: problem easy (max_memory = 20, solo HD)

```
l20 (vuoto)  --[take HD]--> l10 (1 HD in memoria)
l10          --[send HD]--> l20
```

Solo due livelli. La catena termina a `l10`: non c'è `mem-take hd l10 ?` quindi non si può scattare una seconda HD senza inviare prima la prima.

### Esempio: problem extreme (max_memory = 13, mix HD+SD)

```
l13 --[take HD]--> l3   l3  --[take SD]--> l0
l13 --[take SD]--> l10  l10 --[take HD]--> l0
l10 --[take SD]--> l7
```

Cinque livelli, dieci transizioni (5 take + 5 send). I livelli rappresentano configurazioni distinte della memoria: `l0` = 1HD+1SD (pieno), `l7` = 2SD, `l3` = 1HD, `l10` = 1SD, `l13` = vuoto. Non esiste un livello per 2HD (che peserebbero 20 byte > 13), quindi quella combinazione è strutturalmente impossibile.

## 4. I file problem

Cinque istanze di difficoltà crescente, tutte sullo stesso domain.

### easy

Posizione iniziale N, un solo oggetto di interesse (star1 a E), qualità HD. Un solo livello di memoria intermedio. Il piano ottimale è banale: ruota a E, scatta, torna a N, invia.

### medium

Posizione iniziale S, due oggetti HD in direzioni opposte (E e W). La memoria permette una sola HD alla volta. Il planner deve ottimizzare l'ordine: andare prima a E o prima a W? Dipende da quante rotazioni costano.

### hard

Posizione iniziale SW, tre oggetti SD in tre direzioni (E, S, NW). La memoria permette due SD contemporaneamente (6 byte su 16 liberi dopo 2 scatti). Il planner deve scegliere quando inviare e quando scattare, gestendo il vincolo delle 2 foto massime.

### hard_hd

Come hard ma con HD invece di SD. Poiché ogni HD occupa 10 byte su 13 disponibili, non ci possono mai essere 2 HD in memoria contemporaneamente. Ogni scatto deve essere seguito da un invio prima del prossimo scatto. Il pattern è obbligato: scatta → invia → ruota → scatta → invia → ...

### extreme

Il problema più complesso: 4 oggetti in 4 direzioni diverse, mix di HD e SD, posizione iniziale N. La catena di memoria ha 5 livelli e permette di tenere in memoria 1HD+1SD oppure 2SD ma mai 2HD. Il planner deve trovare l'ordine ottimale considerando sia i costi di rotazione sia i vincoli di memoria.

### Oggetti "rumore" (noise, junk, dust, debris, asteroid)

In ogni problem ci sono oggetti visibili ma non richiesti dal goal. Sono presenti per due motivi:

1. Rendono la situazione più realistica (il cielo è affollato)
2. Testano che il planner non scatti foto inutili: la precondizione `(required ?q ?o)` di `take-picture` impedisce di fotografare oggetti non nel goal, ma il planner deve comunque ignorarli attivamente

## 5. Animazione Planimate

### Struttura

Il file contiene tre sezioni principali:

**Predicati → effetti visivi** (`(:predicate ...)`) — per ogni predicato del domain, descrive come cambia la visualizzazione quando quel predicato diventa vero o falso.

**Oggetti visivi custom** (`(:visual ...)`) — definisce la posizione, dimensione, immagine e colore di ogni oggetto sulla canvas.

**Immagini** (`(:image ...)`) — dati base64 delle immagini usate.

### Predicati animati

`pointing ?p` — la casella della direzione puntata cambia colore (arancione). Segue il satellite mentre ruota.

`visible ?o ?d` — quando un oggetto celeste è visibile in una direzione, viene visualizzato dentro la casella di quella direzione. Si usa `distribute_within_objects_vertical` con `?d` come ancora: se più oggetti sono visibili nella stessa direzione, si distribuiscono verticalmente uno sotto l'altro.

`stored ?q ?o` — quando una foto è in memoria, l'oggetto celeste si sposta visivamente dentro lo slot della qualità corrispondente (slot HD giallo a x=400, slot SD rosso a x=500). `hd` e `sd` sono gli slot fissi; è l'oggetto celeste che si muove verso di loro.

`sent ?q ?o` — quando una foto viene inviata, l'oggetto celeste si sposta nell'area `sentphotos`. Anche qui si muove solo l'oggetto, non lo slot.

### Perché `hd` e `sd` come `:type predefine`

`hd` e `sd` nel domain sono oggetti di tipo `quality`. Nell'animation sono dichiarati come `:type predefine` invece di `:type custom`. Questo li rende oggetti grafici "preesistenti" con una posizione fissa sulla canvas, che fungono da contenitori visivi per le foto. Se fossero `:type custom` come la Terra, potrebbero non essere riconosciuti correttamente da Planimate come ancore per il distribute.

### Perché le caselle direzione sono 80×80

Le caselle della rosa dei venti (N, NE, ecc.) sono 80×80 pixel, più grandi degli oggetti celesti (40×40). Questo perché `distribute_within_objects_vertical` posiziona gli oggetti celesti dentro la casella direzione che funge da contenitore. Con caselle 80×80 e oggetti 40×40, due oggetti sulla stessa direzione entrano senza uscire dai bordi visivi della casella.

## 6. Costi delle azioni e limitazione del solver

Il domain dichiara `:action-costs` e ogni azione ha un `(increase (total-cost) N)`:

- rotate-right, rotate-left → costo 1
- take-picture → costo 2
- send → costo 2

Ogni problem dichiara `(= (total-cost) 0)` nell'init e `(:metric minimize (total-cost))` come obiettivo.

**Il problema**: BFWS (Best-First Width Search), il solver predefinito su planning.domains, è un planner che ottimizza il numero di azioni (lunghezza del piano), non i costi numerici. Restituisce un piano valido ma il `total-cost` nell'output è sempre 0 o non viene mostrato.

---

## 7. Cosa sembra superfluo ma non lo è

**Il predicato `captured`** — potrebbe sembrare ridondante con `stored` e `sent`. Non lo è: impedisce al planner di scattare la stessa foto due volte (ad esempio: scatta → invia → scatta di nuovo per occupare memoria). Senza `captured`, il planner potrebbe trovare piani ciclici che violano l'intento del problema.

**Il predicato `required`** — potrebbe sembrare ridondante con il goal `(sent ?q ?o)`. In realtà è stato pensato come filtro in `take-picture` per evitare che il planner fotografi oggetti non nel goal (noise, junk, ecc.) o fotografi un oggetto con la qualità sbagliata. Senza `required`, il planner potrebbe sprecare memoria e costi su foto inutili.

**Il predicato `is-north`** — si potrebbe hardcodare `n` come Nord nel domain. Non si fa per mantenere il domain generico: in linea di principio si potrebbe usare lo stesso domain con un grafo di rotazione diverso e un "Nord" diverso.

**Le transizioni `mem-send` nel problem easy** — nel problem easy c'è solo un oggetto da fotografare e inviare, quindi tecnicamente non serve mai liberare memoria per fare spazio a una seconda foto. Le transizioni `mem-send` sono comunque presenti perché l'azione `send` le richiede come precondizione. Senza di esse, `send` sarebbe inapplicabile.

**Gli oggetti rumore** — noise1, junk1, dust1, ecc. non appaiono mai nel goal. Sono presenti per completezza scenica e per testare che i predicati `required` e `captured` funzionino correttamente come filtri.

## 8. Cosa può creare confusione

**`hd` e `sd` sono di tipo `quality`, non `object`** — nel domain, `hd` e `sd` sono la qualità della foto, non gli oggetti celesti. Nell'animation appaiono come rettangoli grafici sulla canvas, che possono far pensare che siano oggetti del cielo. In realtà sono slot di memoria: contenitori visivi verso cui si spostano gli oggetti celesti quando vengono fotografati.

**La catena di livelli varia per ogni problem** — `l20`, `l13`, `l16`, `l10`, `l7`, `l3`, `l0` non sono valori fissi del domain: ogni problem dichiara solo i livelli che gli servono. `l10` in easy significa "10 byte liberi dopo 1 HD"; in extreme significa "10 byte liberi con 1 SD in memoria". Il significato semantico di ogni livello dipende dal contesto del problem.

**`mem-take` e `mem-send` non sono azioni** — sono predicati statici dell'init che codificano quali transizioni di memoria sono possibili. Il planner le usa come "tabella di lookup" nelle precondizioni delle azioni `take-picture` e `send`. Non vengono mai aggiunti o rimossi durante l'esecuzione.

**`visible` è statico, `pointing` è dinamico** — `(visible star1 e)` non cambia mai: star1 è sempre visibile da E. `(pointing e)` invece cambia ad ogni rotazione. La precondizione di `take-picture` richiede entrambi contemporaneamente: il satellite deve puntare esattamente nella direzione in cui l'oggetto è visibile.

**Il goal usa `sent`, non `captured` né `stored`** — una foto scattata e in memoria (`stored`) non soddisfa il goal: deve essere inviata a Terra (`sent`). Questo obbliga il planner a includere l'azione `send` nel piano, anche se il vincolo di memoria non lo richiedesse.