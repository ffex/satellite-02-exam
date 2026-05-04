# ==========================================================
# FILE: PE_IM_problems.py
# ==========================================================
"""
Test problems for the satellite domain.

Each problem returns (initial, goal).
All objects have explicit quality (SD or HD).
"""


def problem_easy():
    return {
        "position": "N",
        "charge": 100,
        "objects": {
            "E": [("star1", "SD")]
        }
    }, ["star1"]


def problem_medium():
    return {
        "position": "S",
        "charge": 50,
        "objects": {
            "E": [("star1", "HD")],
            "W": [("planet1", "SD")]
        }
    }, ["star1", "planet1"]


def problem_hard():
    return {
        "position": "SW",
        "charge": 40,
        "objects": {
            "E": [("star1", "HD")],
            "S": [("planet1", "SD")],
            "NW": [("galaxy1", "HD")]
        }
    }, ["star1", "planet1", "galaxy1"]


def variant_low_energy():
    return {
        "position": "S",
        "charge": 6,
        "objects": {
            "E": [("star1", "SD")],
            "W": [("planet1", "SD")]
        }
    }, ["star1", "planet1"]


def variant_many_objects():
    return {
        "position": "E",
        "charge": 50,
        "objects": {
            "E": [("star1", "HD"), ("planet1", "SD")],
            "W": [("galaxy1", "HD")]
        }
    }, ["star1", "planet1", "galaxy1"]


def variant_memory_stress():
    return {
        "position": "N",
        "charge": 50,
        "objects": {
            "E": [("star1", "HD")],
            "S": [("planet1", "HD")],
            "W": [("galaxy1", "SD")],
            "NE": [("star2", "HD")]
        }
    }, ["star1", "planet1", "galaxy1", "star2"]


all_problems = [
    problem_easy,
    problem_medium,
    problem_hard,
    variant_low_energy,
    variant_many_objects,
    variant_memory_stress,
]
