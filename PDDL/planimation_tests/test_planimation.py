import json
import tempfile
import unittest
from pathlib import Path

from animations.animate_easy import PROBLEM_KEY as EASY_KEY
from animations.animate_extreme import PROBLEM_KEY as EXTREME_KEY
from animations.animate_hard import PROBLEM_KEY as HARD_KEY
from animations.animate_hardHD import PROBLEM_KEY as HARD_HD_KEY
from animations.animate_medium import PROBLEM_KEY as MEDIUM_KEY
from animations.core import build_frames, export_planimation, normalize_plan_source
from animations.problems import PROBLEM_KEYS, get_problem_config


class PlanimationSmokeTests(unittest.TestCase):
    def test_problem_modules_are_registered(self):
        self.assertEqual(PROBLEM_KEYS, ("easy", "medium", "hard", "hardHD", "extreme"))
        self.assertEqual(EASY_KEY, "easy")
        self.assertEqual(MEDIUM_KEY, "medium")
        self.assertEqual(HARD_KEY, "hard")
        self.assertEqual(HARD_HD_KEY, "hardHD")
        self.assertEqual(EXTREME_KEY, "extreme")

    def test_normalize_plan_source_keeps_arguments(self):
        steps = normalize_plan_source(
            [
                "0: (rotate-left N NE) [1]",
                "1: (take-picture-hd star1 E) [2]",
                "2: (send-hd star1 E) [1]",
            ]
        )
        self.assertEqual(steps[0].name, "rotate-left")
        self.assertEqual(steps[0].args, ("N", "NE"))
        self.assertEqual(steps[1].args, ("star1", "E"))
        self.assertEqual(steps[2].name, "send-hd")

    def test_build_frames_updates_state(self):
        config = get_problem_config("easy")
        frames = build_frames(
            [
                "0: (rotate-left N NE) [1]",
                "1: (take-picture-hd star1 E) [2]",
                "2: (send-hd star1 E) [1]",
            ],
            config,
        )
        self.assertEqual(frames[0].state.direction, "N")
        self.assertEqual(frames[-1].state.direction, "NE")
        self.assertEqual(frames[-1].state.stored, [])
        self.assertEqual([photo.object_name for photo in frames[-1].state.sent], ["star1"])

    def test_export_planimation_writes_json(self):
        config = get_problem_config("medium")
        frames = build_frames(
            ["0: (rotate-right S SW) [1]", "1: (take-picture-hd star1 E) [2]"],
            config,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "planimation.json"
            export_planimation(frames, config, output)
            data = json.loads(output.read_text())
            self.assertEqual(data["problem"], "problem_medium.pddl")
            self.assertGreaterEqual(len(data["frames"]), 2)


if __name__ == "__main__":
    unittest.main()

