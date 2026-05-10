import re
import ast


def parse_plan(plan_file: str):
    """
    Parser robusto per Fast Downward + debug tuple format.
    Restituisce: [(action, [params])]
    """

    plan = []

    with open(plan_file, "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith(";"):
                continue

            # -----------------------------------------
            # CASO 1: tuple Python-like
            # ('action', ['p1','p2'])
            # -----------------------------------------
            if line.startswith("(") and "'" in line:
                try:
                    action, params = ast.literal_eval(line)
                    plan.append((action, list(params)))
                    continue
                except Exception:
                    pass

            # -----------------------------------------
            # CASO 2: Fast Downward standard
            # rotate-right n ne (1)
            # -----------------------------------------
            line = re.sub(r"\(\d+\)", "", line).strip()
            line = line.replace("(", "").replace(")", "")
            parts = line.split()

            if not parts:
                continue

            action = parts[0]
            params = parts[1:]

            plan.append((action, params))

    return plan

def parse_init_state(problem_file: str):

    state = {
        "pointing": None,
        "slot1_free": True,
        "slot2_free": True,
        "slot1": None,
        "slot2": None,
        "sent": set(),
        "has_hd": False,
        "has_sd": False
    }

    with open(problem_file, "r") as f:
        content = f.read()

    init_block = re.search(r":init(.*?)\(:goal", content, re.DOTALL)
    if not init_block:
        raise ValueError("Missing :init block")

    tokens = re.findall(r"\((.*?)\)", init_block.group(1))

    for t in tokens:
        parts = t.split()
        if not parts:
            continue

        pred = parts[0]

        # ------------------------
        # orientation
        # ------------------------
        if pred == "pointing":
            state["pointing"] = parts[1]

        # ------------------------
        # sent facts
        # ------------------------
        elif pred == "sent" and len(parts) > 1:
            state["sent"].add(parts[1])

        # ------------------------
        # memory flags (NON logica)
        # ------------------------
        elif pred == "stored-hd":
            state["has_hd"] = True

        elif pred == "stored-sd":
            state["has_sd"] = True

        # ------------------------
        # slot state (safe)
        # ------------------------
        elif pred == "slot1-free":
            state["slot1_free"] = True

        elif pred == "slot2-free":
            state["slot2_free"] = True

    return state