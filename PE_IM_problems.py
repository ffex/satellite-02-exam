# ==========================================================
# FILE: PE_IM_problems.py
# ==========================================================
"""
PROBLEMI DI TEST

Formato:

(
    initial,
    goal
)
"""


def problem_easy():
    return {
        "position": "N",
        "charge": 10,
        "objects": {
            "E": ["star1"]
        }
    }, ["star1"]

def problem_medium():
    return {
        "position": "S",
        "charge": 20,
        "objects": {
            "E": ["star1"],
            "W": ["planet1"]
        }
    }, ["star1", "planet1"]

def problem_hard():
    return {
        "position": "SW",
        "charge": 100,
        "objects": {
            "E": ["star1"],
            "S": ["planet1"],
            "NW": ["galaxy1"]
        }
    }, [("star1","SD"), ("planet1","SD"), ("galaxy1","SD")]
def problem_hard_HD():
    return {
        "position": "SW",
        "charge": 100,
        "objects": {
            "E": ["star1"],
            "S": ["planet1"],
            "NW": ["galaxy1"]
        }
    }, [("star1","HD"), ("planet1","HD"), ("galaxy1","HD")]


def variant_low_energy():
    return {
        "position": "S",
        "charge": 6,
        "objects": {
            "E": ["star1"],
            "W": ["planet1"]
        }
    }, ["star1", "planet1"]


def variant_many_objects():
    return {
        "position": "E",
        "charge": 50,
        "objects": {
            "E": ["star1", "planet1"],
            "W": ["galaxy1"]
        }
    }, ["star1", "planet1", "galaxy1"]


def variant_memory_stress():
    return {
        "position": "N",
        "charge": 50,
        "objects": {
            "E": ["star1"],
            "S": ["planet1"],
            "W": ["galaxy1"],
            "NE": ["star2"]
        }
    }, ["star1", "planet1", "galaxy1", "star2"]
