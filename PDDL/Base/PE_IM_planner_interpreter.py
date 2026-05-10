class PDDLPlanInterpreter:

    def __init__(self, init_state):
        self.state = {
            "pointing": None,
            "slot1_free": True,
            "slot2_free": True,
            "slot1": None,
            "slot2": None,
            "sent": set()
        }

        self.state.update(init_state)

    # ======================================================
    def run(self, plan):
        for action, params in plan:
            print("\n----------------------------------")
            print(f"ACTION: {action} {params}")
            print("----------------------------------")

            self.execute(action, params)

            print("STATE:", self.state)

    # ======================================================
    def execute(self, action, params):

        if "rotate-right" in action or "rotate-left" in action:
            self.rotate(params)

        elif "take-picture" in action:
            self.take_picture(action, params)

        elif "send" in action:
            self.send_picture(params)

        else:
            print("[WARN] unknown action:", action)

    # ======================================================
    def rotate(self, params):
        if len(params) < 2:
            return

        # params: [from, to]
        self.state["pointing"] = params[1]

    # ======================================================
    def take_picture(self, action, params):

        if not params:
            return

        obj = params[0]

        kind = "hd" if "hd" in action else "sd"

        # SLOT 1 FIRST
        if self.state["slot1"] is None:
            self.state["slot1"] = (kind, obj)
            self.state["slot1_free"] = False

        # SLOT 2 SECOND
        elif self.state["slot2"] is None:
            self.state["slot2"] = (kind, obj)
            self.state["slot2_free"] = False

    # ======================================================
    def send_picture(self, params):

        if not params:
            return

        obj = params[0]

        # remove from slots
        for slot in ["slot1", "slot2"]:
            if self.state[slot] and self.state[slot][1] == obj:
                self.state[slot] = None
                self.state[f"{slot}_free"] = True

        self.state["sent"].add(obj)

        # recompute emptiness
        if self.state["slot1"] is None and self.state["slot2"] is None:
            pass