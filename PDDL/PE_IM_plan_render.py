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

        for obj in re.findall(r"\(quality-hd\s+([^\s\)]+)\)", text):
            quality[obj] = "HD"

        for obj in re.findall(r"\(quality-sd\s+([^\s\)]+)\)", text):
            quality[obj] = "SD"

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

                obj = tokens[1]

                direction = (
                    tokens[2]
                    if len(tokens) > 2
                    else self.current_direction
                )

                direction = self.human_direction(direction)

                quality = self.quality_map.get(obj)

                if quality is None:
                    quality = "UNSPECIFIED"

                rendered.append(
                    f"take-picture {obj} {direction} {quality}"
                )

                continue

            # ==========================================
            # SEND
            # ==========================================

            if action == "send":

                obj = tokens[1]

                direction = self.human_direction(
                    self.current_direction
                )

                quality = self.quality_map.get(obj)

                if quality is None:
                    quality = "UNSPECIFIED"

                rendered.append(
                    f"send {obj} {direction} {quality}"
                )

                continue

            rendered.append(step)

        return rendered