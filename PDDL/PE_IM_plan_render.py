import re

class SemanticPlanRenderer:

    def __init__(self, pddl_init_lines=None):

        self.quality_map = self._parse_quality(pddl_init_lines or [])
        self.current_direction = None

        # ==========================================
        # HUMAN READABLE DIRECTIONS
        # ==========================================

        self.direction_map = {
            "n": "north",
            "ne": "north-east",
            "e": "east",
            "se": "south-east",
            "s": "south",
            "sw": "south-west",
            "w": "west",
            "nw": "north-west"
        }

    # ======================================================
    # QUALITY PARSER
    # ======================================================

    def _parse_quality(self, lines):

        quality = {}

        text = " ".join(lines)

        # ---- formato VECCHIO: (quality-hd star1) / (quality-sd planet1) ----
        for obj in re.findall(r"\(quality-hd\s+([^\s\)]+)\)", text):
            quality[obj] = "HD"

        for obj in re.findall(r"\(quality-sd\s+([^\s\)]+)\)", text):
            quality[obj] = "SD"

        # ---- formato NUOVO: (quality star1 hd) / (quality planet1 sd) ----
        for obj, q in re.findall(
            r"\(quality\s+([^\s\)]+)\s+(hd|sd)\)", text, re.IGNORECASE
        ):
            quality[obj] = q.upper()

        return quality

    # ======================================================
    # DIRECTION TRANSLATOR
    # ======================================================

    def human_direction(self, direction):

        if direction is None:
            return "unknown-direction"

        return self.direction_map.get(direction, direction)

    # ======================================================
    # MAIN RENDER
    # ======================================================

    def render(self, steps):

        rendered = []

        for step in steps:

            tokens = step.split()

            if not tokens:
                continue

            action = tokens[0]

            # ==========================================
            # ROTATE
            # ==========================================

            if "rotate" in action:

                self.current_direction = tokens[-1]

                from_dir = self.human_direction(tokens[-2])
                to_dir = self.human_direction(tokens[-1])

                rendered.append(
                    f"{action} {from_dir} -> {to_dir}"
                )

                continue

            # ==========================================
            # TAKE PICTURE
            # ==========================================

            if action == "take-picture":

                # nuova firma: (take-picture <quality> <obj> <dir>)
                quality = (tokens[1].upper() if len(tokens) > 1 else "UNSPECIFIED")
                obj     = tokens[2] if len(tokens) > 2 else "UNKNOWN"

                raw_dir = (
                    tokens[3]
                    if len(tokens) > 3
                    else self.current_direction
                )

                direction = self.human_direction(raw_dir)

                # fallback: se la quality_map ha info diverse, lascia priorita' al piano
                if not quality:
                    quality = self.quality_map.get(obj, "UNSPECIFIED")

                rendered.append(
                    f"take-picture {obj} {direction} {quality}"
                )

                continue

            # ==========================================
            # SEND
            # ==========================================

            if action == "send":

                # nuova firma: (send <quality> <obj> <dir>)
                quality = (tokens[1].upper() if len(tokens) > 1 else "UNSPECIFIED")
                obj     = tokens[2] if len(tokens) > 2 else "UNKNOWN"

                raw_dir = (
                    tokens[3]
                    if len(tokens) > 3
                    else self.current_direction
                )

                direction = self.human_direction(raw_dir)

                if not quality:
                    quality = self.quality_map.get(obj, "UNSPECIFIED")

                rendered.append(
                    f"send {obj} {direction} {quality}"
                )

                continue

            rendered.append(step)

        return rendered