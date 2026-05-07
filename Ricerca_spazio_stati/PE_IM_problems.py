"""
Questo file definisce gli scenari del problema.

  easy   → max_memory = 20
    1 oggetto HD (10 unità). Memoria abbondante, nessun vincolo stringente.
    Serve come baseline senza pressione sulla memoria.

  medium → max_memory = 13
    2 oggetti HD (10 unità ciascuno = 20 totali), ma memoria = 13.
    Non possono stare entrambi in memoria contemporaneamente (10+10=20 > 13).
    Il satellite è costretto a fotografare → inviare → fotografare → inviare.
    Crea un vincolo reale senza rendere il problema irrisolvibile.

  hard   → max_memory = 16
    3 oggetti SD (3 unità ciascuno = 9 totali), memoria = 16.
    Tutti e 3 entrerebbero (9 < 16), ma il vincolo dei 2 slot
    impedisce comunque di tenerli tutti: si possono avere al massimo
    2 foto in memoria. La memoria non è il collo di bottiglia qui,
    lo è il numero di slot. Scenario realistico per SD.

  hard_HD → max_memory = 13
    3 oggetti HD (10 unità ciascuno). Con 13 unità si può tenere
    al massimo 1 foto HD (10 ≤ 13, ma 10+10=20 > 13).
    Il satellite è forzato a un ciclo send dopo ogni singola foto.
    Scenario più stressante: memoria E slot diventano entrambi vincoli.

  extreme → max_memory = 13
    4 oggetti misti: 2 HD (10 unità) + 2 SD (3 unità).
    Oggetti sparsi in 4 direzioni diverse, posizione iniziale opposta al goal.
    Con memoria 13: 1 HD + 1 SD entrano insieme (10+3=13), ma non 2 HD.
    Il satellite deve pianificare l'ordine di scatto per minimizzare i cicli
    send intermedi. Mix di qualità + pressione memoria + molte rotazioni
    lo rende il problema più complesso della suite.
"""


# Un solo oggetto da trovare, memoria abbondante
# EASY
def problem_easy():

    initial = {
        "position": "N",
        "charge": 20,
        "max_memory": 20,       # 1 HD (10) → ampio margine
        "objects": {
            "E": ["star1", "noise1"]
        }
    }

    goal = [("star1", "HD")]

    return initial, goal


# Due oggetti da trovare, memoria che non li contiene entrambi
# MEDIUM
def problem_medium():

    initial = {
        "position": "S",
        "charge": 50,
        "max_memory": 13,       # 2 HD = 20, non ci stanno insieme (10+10 > 13)
        "objects": {
            "E": ["star1", "junk1"],
            "W": ["planet1", "noise2"]
        }
    }

    goal = [("star1", "HD"), ("planet1", "HD")]

    return initial, goal


# Tre oggetti SD, memoria sufficiente ma slot limitati
# HARD
def problem_hard():

    initial = {
        "position": "SW",
        "charge": 75,
        "max_memory": 16,       # 3 SD = 9, entrano in memoria ma non negli slot (max 2)
        "objects": {
            "E": ["star1", "dust1"],
            "S": ["planet1"],
            "NW": ["galaxy1", "junk2"]
        }
    }

    goal = [
        ("star1", "SD"),
        ("planet1", "SD"),
        ("galaxy1", "SD")
    ]

    return initial, goal


# Tre oggetti HD, memoria che ne contiene solo 1 alla volta
# HARD HD
def problem_hard_HD():

    initial = {
        "position": "SW",
        "charge": 100,
        "max_memory": 13,       # 1 HD (10) entra, 2 HD (20) no → ciclo obbligato
        "objects": {
            "E": ["star1", "dust1"],
            "S": ["planet1", "asteroidX"],
            "NW": ["galaxy1", "junk2"]
        }
    }

    goal = [
        ("star1", "HD"),
        ("planet1", "HD"),
        ("galaxy1", "HD")
    ]

    return initial, goal


# 4 oggetti misti HD/SD, memoria stringente
def problem_extreme():

    initial = {
        "position": "N",
        "charge": 120,
        "max_memory": 13,       # HD+SD entra (13), HD+HD no (20 > 13)
        "objects": {
            "SE":  ["star1",   "debris1"],
            "SW":  ["planet1", "dust2"],
            "NE":  ["galaxy1", "junk3"],
            "W":   ["nebula1", "noise3"],
        }
    }

    goal = [
        ("star1",   "HD"),   # 10 unità
        ("planet1", "SD"),   #  3 unità
        ("galaxy1", "HD"),   # 10 unità
        ("nebula1", "SD"),   #  3 unità
    ]

    return initial, goal