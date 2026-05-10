class PDDLPlanInterpreterAdvanced:

    def __init__(self):

        self.state = {

            "pointing": None,
            "energy": 20,
            "memory_used": 0,

            "stored": set(),
            "sent": set(),

            "object_type": {}
        }

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

        if "rotate" in action:
            self.rotate(params)

        elif "take" in action:
            self.take_picture(params)

        elif "send" in action:
            self.send(params)

    # ======================================================

    def rotate(self, params):

        self.state["pointing"] = params[1]
        self.state["energy"] -= 1

    # ======================================================

    def take_picture(self, params):

        obj = params[0]

        if self.state["energy"] < 2:
            raise Exception("Not enough energy")

        self.state["energy"] -= 2
        self.state["stored"].add(obj)

        # FIX: più coerente col domain
        if obj in ["star1", "obj_hd"]:
            obj_type = "hd"
            self.state["memory_used"] += 10
        else:
            obj_type = "sd"
            self.state["memory_used"] += 3

        self.state["object_type"][obj] = obj_type

    # ======================================================

    def send(self, params):

        obj = params[0]

        if obj not in self.state["stored"]:
            return

        obj_type = self.state["object_type"].get(obj, "sd")

        self.state["stored"].remove(obj)
        self.state["sent"].add(obj)

        self.state["energy"] -= 2

        if obj_type == "hd":
            self.state["memory_used"] -= 10
        else:
            self.state["memory_used"] -= 3