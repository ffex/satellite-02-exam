import re


class SemanticPlanRendererBFWSv3:

    def __init__(self, pddl_init_lines=None):
        self.current_direction = self._extract_pointing(pddl_init_lines or [])

        self.direction_map = {
            "n": "north",
            "ne": "north-east",
            "e": "east",
            "se": "south-east",
            "s": "south",
            "sw": "south-west",
            "w": "west",
            "nw": "north-west",
        }

    def _extract_pointing(self, lines):
        text = " ".join(lines)
        m = re.search(r"\(pointing\s+([^\s\)]+)\)", text)
        return m.group(1).lower() if m else None

    def human_direction(self, direction):
        if not direction:
            return "unknown-direction"
        return self.direction_map.get(direction.lower(), direction)

    def render(self, steps):

        rendered = []

        for step in steps:
            tokens = step.split()
            if not tokens:
                continue

            action = tokens[0].lower()

            # =========================
            # ROTATE
            # =========================
            if action.startswith("rotate"):
                if len(tokens) >= 3:
                    from_dir = self.human_direction(tokens[1])
                    to_dir   = self.human_direction(tokens[2])
                    self.current_direction = tokens[2]
                    rendered.append(f"{action} {from_dir} -> {to_dir}")
                else:
                    rendered.append(step)
                continue

            # =========================
            # TAKE
            # =========================
            if action == "take-picture":
                if len(tokens) >= 4:
                    quality = tokens[1].upper()
                    obj     = tokens[2]
                    direction = self.human_direction(tokens[3])

                    extra = ""
                    if len(tokens) >= 6:
                        extra = f"  (mem {tokens[4]} -> {tokens[5]})"

                    rendered.append(
                        f"take-picture {obj} {direction} {quality}{extra}"
                    )
                else:
                    rendered.append(step)
                continue

            # =========================
            # SEND
            # =========================
            if action == "send":
                if len(tokens) >= 4:
                    quality = tokens[1].upper()
                    obj     = tokens[2]
                    direction = self.human_direction(tokens[3])

                    extra = ""
                    if len(tokens) >= 6:
                        extra = f"  (mem {tokens[4]} -> {tokens[5]})"

                    rendered.append(
                        f"send {obj} {direction} {quality}{extra}"
                    )
                else:
                    rendered.append(step)
                continue

            rendered.append(step)

        return rendered