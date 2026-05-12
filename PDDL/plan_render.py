import re
from dataclasses import dataclass


class SemanticPlanRenderer:

    def __init__(self, pddl_init_lines=None):
        """
        pddl_init_lines: righe del blocco :init del problema
        """
        self.quality_map = self._parse_quality(pddl_init_lines or [])
        self.current_direction = None

    # ======================================================
    # PARSE QUALITY DAL PDDL
    # ======================================================

    def _parse_quality(self, lines):
        quality = {}

        for line in lines:
            line = line.strip()

            # (quality-hd star1)
            m_hd = re.match(r"\(quality-hd\s+([^\s\)]+)\)", line)
            if m_hd:
                obj = m_hd.group(1)
                quality[obj] = "HD"

            # (quality-sd noise1)
            m_sd = re.match(r"\(quality-sd\s+([^\s\)]+)\)", line)
            if m_sd:
                obj = m_sd.group(1)
                quality[obj] = "SD"

        return quality

    # ======================================================
    # MAIN
    # ======================================================

    def render(self, steps):
        rendered = []

        for step in steps:
            tokens = step.split()
            if not tokens:
                continue

            action = tokens[0]

            # ------------------------------------------
            # ROTATE
            # ------------------------------------------
            if "rotate" in action:
                self.current_direction = tokens[-1]
                rendered.append(step)
                continue

            # ------------------------------------------
            # TAKE PICTURE
            # ------------------------------------------
            if action == "take-picture":
                obj = tokens[1]
                direction = tokens[2] if len(tokens) > 2 else self.current_direction
                quality = self.quality_map.get(obj, "UNKNOWN")

                rendered.append(f"take-picture {obj} {direction} {quality}")
                continue

            # ------------------------------------------
            # SEND
            # ------------------------------------------
            if action == "send":
                obj = tokens[1]
                direction = self.current_direction or "UNKNOWN"
                quality = self.quality_map.get(obj, "UNKNOWN")

                rendered.append(f"send {obj} {direction} {quality}")
                continue

            rendered.append(step)

        return rendered