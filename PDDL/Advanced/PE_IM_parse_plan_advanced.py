# ==========================================================
# PARSER PIANI ENHSP
# ==========================================================

import re


def parse_plan(plan_file: str):

    plan = []

    with open(plan_file, "r") as f:

        for line in f:

            line = line.strip().lower()

            if not line:
                continue

            if line.startswith(";"):
                continue

            # rimuove timestamp:
            # 0.000: (rotate-right n ne) [1.000]
            line = re.sub(r"^[0-9\.]+\:\s*", "", line)

            # rimuove duration
            line = re.sub(r"\[[0-9\.]+\]", "", line)

            line = line.replace("(", "").replace(")", "")

            parts = line.split()

            if not parts:
                continue

            action = parts[0]
            params = parts[1:]

            plan.append((action, params))

    return plan