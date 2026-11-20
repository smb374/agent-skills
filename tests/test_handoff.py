"""The shipped session template of the handoff skill works with fill."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILL = ROOT / "fill" / "fill.py"
SESSION = ROOT / "skills" / "handoff" / "assets" / "session.md"
KEYS = [
    "goal",
    "state",
    "decisions",
    "superseded",
    "open_questions",
    "artifacts",
    "next_action",
    "done_when",
    "suggested_skills",
]
OPTIONAL_LISTS = (
    "decisions",
    "superseded",
    "open_questions",
    "artifacts",
    "suggested_skills",
)


class SessionTemplateTest(unittest.TestCase):
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
        result = self.fill("--fields", SESSION, skeleton)
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
        out = self.dir / "brief.md"
        result = self.fill(SESSION, self.values(), out)
        self.assertEqual(result.returncode, 0, result.stderr)
        brief = out.read_text()
        self.assertIn("## Goal\n\na & <b>\n", brief)
        self.assertIn("## Done when\n\n- <b>x</b>\n", brief)
        self.assertNotIn("{{", brief)

    def test_optional_lists_render_none(self):
        out = self.dir / "brief.md"
        empty = {key: [] for key in OPTIONAL_LISTS}
        result = self.fill(SESSION, self.values(**empty), out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("## Decisions\n\nNone\n", out.read_text())

    def test_done_when_must_not_be_empty(self):
        result = self.fill(SESSION, self.values(done_when=[]), self.dir / "brief.md")
        self.assertEqual(
            result.stderr.splitlines(),
            ["done_when: empty list needs a {{^done_when}} section"],
        )


if __name__ == "__main__":
    unittest.main()
