# ==========================================================
# FILE: PE_IM_planner_interpreter_advanced.py
# ==========================================================

class PDDLPlanInterpreterAdvanced:

    # ======================================================
    # INIT
    # ======================================================

    def __init__(self,
                 initial_energy=20,
                 memory_capacity=20,
                 object_types=None):

        if object_types is None:
            object_types = {}

        self.state = {

            "pointing": "n",

            "energy": initial_energy,

            "memory_used": 0,

            "memory_capacity": memory_capacity,

            "photo_count": 0,

            "stored": set(),

            "sent": set(),

            # object -> hd/sd
            "object_type": object_types.copy()
        }

    # ======================================================
    # RUN
    # ======================================================

    def run(self, plan):

        print("\n" + "=" * 80)
        print("PLAN EXECUTION")
        print("=" * 80)

        for step, (action, params) in enumerate(plan, start=1):

            print("\n" + "-" * 50)
            print(f"[{step}] ACTION: {action} {params}")
            print("-" * 50)

            try:

                self.execute(action, params)

                print("STATE:")
                print(self.state)

            except Exception as e:

                print("\n[EXECUTION ERROR]")
                print(str(e))

                print("\nCURRENT STATE:")
                print(self.state)

                return False

        print("\n" + "=" * 80)
        print("FINAL STATE")
        print("=" * 80)

        print(self.state)

        return True

    # ======================================================
    # DISPATCH
    # ======================================================

    def execute(self, action, params):

        if action.startswith("rotate"):

            self.rotate(action, params)

        elif action.startswith("take-picture"):

            self.take_picture(action, params)

        elif action == "send":

            self.send(params)

        else:

            raise Exception(
                f"Unknown action: {action}"
            )

    # ======================================================
    # ROTATE
    # ======================================================

    def rotate(self, action, params):

        if self.state["energy"] < 1:

            raise Exception(
                "Not enough energy to rotate"
            )

        from_dir = params[0]
        to_dir = params[1]

        if self.state["pointing"] != from_dir:

            raise Exception(
                f"Satellite not pointing at {from_dir}"
            )

        self.state["pointing"] = to_dir

        self.state["energy"] -= 1

    # ======================================================
    # TAKE PICTURE
    # ======================================================

    def take_picture(self, action, params):

        obj = params[0]

        # --------------------------------------------------
        # energy
        # --------------------------------------------------

        if self.state["energy"] < 2:

            raise Exception(
                "Not enough energy for picture"
            )

        # --------------------------------------------------
        # already stored
        # --------------------------------------------------

        if obj in self.state["stored"]:

            raise Exception(
                f"{obj} already stored"
            )

        # --------------------------------------------------
        # slots
        # --------------------------------------------------

        if self.state["photo_count"] >= 2:

            raise Exception(
                "Photo slots full"
            )

        # --------------------------------------------------
        # determine quality
        # --------------------------------------------------

        if "hd" in action:

            quality = "hd"
            memory_cost = 10

        else:

            quality = "sd"
            memory_cost = 3

        # --------------------------------------------------
        # memory constraint
        # --------------------------------------------------

        if (
            self.state["memory_used"]
            + memory_cost
            >
            self.state["memory_capacity"]
        ):

            raise Exception(
                "Memory capacity exceeded"
            )

        # --------------------------------------------------
        # apply effects
        # --------------------------------------------------

        self.state["energy"] -= 2

        self.state["memory_used"] += memory_cost

        self.state["photo_count"] += 1

        self.state["stored"].add(obj)

        self.state["object_type"][obj] = quality

    # ======================================================
    # SEND
    # ======================================================

    def send(self, params):

        obj = params[0]

        # --------------------------------------------------
        # pointing north
        # --------------------------------------------------

        if self.state["pointing"] != "n":

            raise Exception(
                "Send requires pointing north"
            )

        # --------------------------------------------------
        # object exists
        # --------------------------------------------------

        if obj not in self.state["stored"]:

            raise Exception(
                f"{obj} not in storage"
            )

        # --------------------------------------------------
        # energy
        # --------------------------------------------------

        if self.state["energy"] < 2:

            raise Exception(
                "Not enough energy for send"
            )

        # --------------------------------------------------
        # determine quality
        # --------------------------------------------------

        quality = self.state[
            "object_type"
        ].get(obj)

        if quality == "hd":

            memory_cost = 10

        else:

            memory_cost = 3

        # --------------------------------------------------
        # apply effects
        # --------------------------------------------------

        self.state["energy"] -= 2

        self.state["memory_used"] -= memory_cost

        self.state["photo_count"] -= 1

        self.state["stored"].remove(obj)

        self.state["sent"].add(obj)