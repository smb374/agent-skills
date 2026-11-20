"""The shipped plan template of the to-impl-plan skill works with fill."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILL = ROOT / "fill" / "fill.py"
PLAN = ROOT / "skills" / "to-impl-plan" / "assets" / "plan.md"
KEYS = [
    "title",
    "ticket",
    "current_state",
    "out_of_scope",
    "commands",
    "behavior",
    "rules",
    "stages",
    "open_questions",
]
OPTIONAL_LISTS = ("out_of_scope", "rules", "open_questions")


class PlanTemplateTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)

    def fill(self, *args):
        return subprocess.run(
            [sys.executable, str(FILL), *map(str, args)],
            check=False,
            capture_output=True,
            text=True,
        )

    def values(self, **changes):
        skeleton = self.dir / "skeleton.json"
        result = self.fill("--fields", PLAN, skeleton)
        self.assertEqual(result.returncode, 0, result.stderr)
        values = json.loads(skeleton.read_text())
        self.assertEqual(list(values), KEYS)
        for key, line in zip(values, result.stdout.splitlines()):
            self.assertTrue(line.startswith(f"{key} ("), line)
            self.assertNotEqual(line.split(":", 1)[1], "", f"no hint: {line}")
            values[key] = ["<b>x</b>"] if "(list)" in line else "a & <b>"
        values.update(changes)
        path = self.dir / "values.json"
        path.write_text(json.dumps(values))
        return path

    def test_fields_and_render(self):
        out = self.dir / "plan.md"
        stages = ["### Stage 1: one", "### Stage 2: two"]
        result = self.fill(PLAN, self.values(stages=stages), out)
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = out.read_text()
        self.assertIn("# a & <b>: implementation plan\n", plan)
        self.assertIn("## Common verification commands\n\n- `<b>x</b>`\n", plan)
        self.assertIn(
            "## Stages\n\n### Stage 1: one\n\n### Stage 2: two\n\n## Open questions\n",
            plan,
        )
        self.assertIn("\n## Builder contract\n", plan)
        self.assertIn("\nstatus: done|failed, stage: <N>\n", plan)
        self.assertNotIn("{{", plan)
        self.assertTrue(
            plan.endswith(
                "\nBefore you start, load the `handoff` skill, and follow its rules"
                " to receive a handoff.\n"
            )
        )

    def test_optional_lists_render_none(self):
        out = self.dir / "plan.md"
        empty = {key: [] for key in OPTIONAL_LISTS}
        result = self.fill(PLAN, self.values(**empty), out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("## Out of scope\n\nNone\n", out.read_text())

    def test_stages_and_commands_must_not_be_empty(self):
        result = self.fill(
            PLAN, self.values(stages=[], commands=[]), self.dir / "plan.md"
        )
        self.assertEqual(
            result.stderr.splitlines(),
            [
                "commands: empty list needs a {{^commands}} section",
                "stages: empty list needs a {{^stages}} section",
            ],
        )


if __name__ == "__main__":
    unittest.main()
