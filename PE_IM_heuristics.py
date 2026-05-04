# ==========================================================
# FILE: PE_IM_heuristics.py
# ==========================================================
from math import ceil
from PE_IM_utils import COST_TAKEPIC, COST_SEND, MAX_PHOTOS, memory_usage, photo_size

"""
Heuristics for A*.

State layout:
(
    position,
    orientation,
    charge,
    memory,
    sent
)
"""


# ----------------------------------------------------------
# HELPERS
# ----------------------------------------------------------
def _goal_missing(node, problem):
    _, _, _, memory, sent = node.state
    goal = getattr(problem, "_goal", tuple(problem.goal) if problem.goal else tuple())
    missing = [obj for obj in goal if obj not in sent]
    return missing, memory, sent


def _quality_for_problem(problem, obj):
    if hasattr(problem, "photo_quality_for"):
        return problem.photo_quality_for(obj)
    return "SD"


def _photo_requirements(node, problem):
    missing, memory, sent = _goal_missing(node, problem)
    memory_objs = {obj for obj, _ in memory}
    unphotographed = [obj for obj in missing if obj not in memory_objs]
    return missing, unphotographed, memory


# ----------------------------------------------------------
# H1
# Count missing objects
# ----------------------------------------------------------
def h1(node, problem):
    _, _, _, _, sent = node.state
    missing = [obj for obj in problem._goal if obj not in sent]
    return len(missing)


# ----------------------------------------------------------
# H2
# More informed estimate
# ----------------------------------------------------------
def h2(node, problem):
    _, orientation, _, memory, sent = node.state
    missing = [obj for obj in problem._goal if obj not in sent]
    base = len(missing) * 2
    north_penalty = 1 if orientation != "N" else 0
    memory_penalty = 1 if len(memory) == MAX_PHOTOS else 0
    return base + north_penalty + memory_penalty


# ----------------------------------------------------------
# H3
# Only remaining photos
# ----------------------------------------------------------
def h_takepic_only(node, problem):
    _, unphotographed, _ = _photo_requirements(node, problem)
    return len(unphotographed) * COST_TAKEPIC


# ----------------------------------------------------------
# H4
# Photos + send cost, with memory awareness
# ----------------------------------------------------------
def h_takepic_send(node, problem):
    _, unphotographed, memory = _photo_requirements(node, problem)
    if not unphotographed and not memory:
        return 0

    cost_photos = len(unphotographed) * COST_TAKEPIC
    total_photos_to_handle = len(memory) + len(unphotographed)
    min_sends = ceil(total_photos_to_handle / MAX_PHOTOS)
    future_weight = sum(photo_size(_quality_for_problem(problem, obj)) for obj in unphotographed)
    memory_penalty = 1 if memory_usage(memory) + future_weight > 0 else 0
    return cost_photos + (min_sends * COST_SEND) + memory_penalty


# ----------------------------------------------------------
# H5
# Maximum of the two custom heuristics
# ----------------------------------------------------------
def h_max(node, problem):
    return max(h_takepic_only(node, problem), h_takepic_send(node, problem))
