# ==========================================================
# FILE: PE_IM_parse_plan_advanced.py
# ==========================================================

import re


def parse_plan(plan_file: str):

    plan = []

    with open(plan_file, "r") as f:

        for raw_line in f:

            line = raw_line.strip().lower()

            # ----------------------------------------------
            # skip empty/comments
            # ----------------------------------------------

            if not line:
                continue

            if line.startswith(";"):
                continue

            # ----------------------------------------------
            # remove timestamps
            # 0.000: (rotate-right n ne) [1.000]
            # ----------------------------------------------

            line = re.sub(
                r"^[0-9\.]+\:\s*",
                "",
                line
            )

            # ----------------------------------------------
            # remove duration
            # ----------------------------------------------

            line = re.sub(
                r"\[[0-9\.]+\]",
                "",
                line
            )

            # ----------------------------------------------
            # remove parentheses
            # ----------------------------------------------

            line = (
                line
                .replace("(", "")
                .replace(")", "")
                .strip()
            )

            if not line:
                continue

            parts = line.split()

            action = parts[0]
            params = parts[1:]

            plan.append(
                (action, params)
            )

    return plan