"""Problem metadata used by the planimation animation layer."""

from dataclasses import dataclass

from PE_IM_utils import MAX_MEMORY, MEM_SLOT_MAX


@dataclass(frozen=True)
class ProblemConfig:
    key: str
    problem_file: str
    title: str
    initial_direction: str
    description: str
    goal_objects: tuple[str, ...]
    memory_total: int = MAX_MEMORY
    slot_total: int = MEM_SLOT_MAX


PROBLEMS = {
    "easy": ProblemConfig(
        key="easy",
        problem_file="problem_easy.pddl.pddl",
        title="EASY mission",
        initial_direction="N",
        description="One HD target with a simple capture/send sequence.",
        goal_objects=("star1",),
    ),
    "medium": ProblemConfig(
        key="medium",
        problem_file="problem_medium.pddl",
        title="MEDIUM mission",
        initial_direction="S",
        description="Two HD targets and a longer routing sequence.",
        goal_objects=("star1", "planet1"),
    ),
    "hard": ProblemConfig(
        key="hard",
        problem_file="problem_hard.pddl",
        title="HARD mission",
        initial_direction="SW",
        description="Three SD targets with more orientation changes.",
        goal_objects=("star1", "planet1", "galaxy1"),
    ),
    "hardHD": ProblemConfig(
        key="hardHD",
        problem_file="problem_hardHD.pddl",
        title="HARD HD mission",
        initial_direction="SW",
        description="Three HD targets with the same navigation layout.",
        goal_objects=("star1", "planet1", "galaxy1"),
    ),
    "extreme": ProblemConfig(
        key="extreme",
        problem_file="problem_extreme.pddl",
        title="EXTREME mission",
        initial_direction="N",
        description="Mixed HD/SD mission with four targets.",
        goal_objects=("star1", "planet1", "galaxy1", "nebula1"),
    ),
}

PROBLEM_KEYS = tuple(PROBLEMS.keys())


def get_problem_config(key: str) -> ProblemConfig:
    try:
        return PROBLEMS[key]
    except KeyError as exc:
        raise KeyError(f"Unknown problem key: {key}") from exc

