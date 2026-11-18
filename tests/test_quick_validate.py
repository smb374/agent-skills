"""Tests for skills/skill-writer/scripts/quick_validate.py."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

VALIDATOR_PATH = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "skill-writer"
    / "scripts"
    / "quick_validate.py"
)

_spec = importlib.util.spec_from_file_location("quick_validate", VALIDATOR_PATH)
quick_validate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(quick_validate)

DESCRIPTION = "Writes reports. Use when asked for a report."


class QuickValidateTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def make_skill(self, name, description=DESCRIPTION, body=""):
        skill_dir = self.root / name
        skill_dir.mkdir()
        skill_md = f"---\nname: {name}\ndescription: {description}\n---\n\n{body}"
        (skill_dir / "SKILL.md").write_text(skill_md)
        return skill_dir

    def validate(self, skill_dir):
        return quick_validate.validate_skill(skill_dir)

    def test_valid_minimal_skill(self):
        skill_dir = self.make_skill("report-writer")

        valid, errors, warnings = self.validate(skill_dir)

        self.assertTrue(valid)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_name_regex_rejected(self):
        skill_dir = self.make_skill("Bad--Name")

        valid, errors, _ = self.validate(skill_dir)

        self.assertFalse(valid)
        pattern = quick_validate.NAME_RE.pattern
        self.assertTrue(any(pattern in error for error in errors), errors)

    def test_name_too_long(self):
        skill_dir = self.make_skill("a" * 65)

        valid, errors, _ = self.validate(skill_dir)

        self.assertFalse(valid)
        self.assertTrue(any("max 64" in error for error in errors), errors)

    def test_description_too_long(self):
        skill_dir = self.make_skill("report-writer", description="a" * 1025)

        valid, errors, _ = self.validate(skill_dir)

        self.assertFalse(valid)
        self.assertTrue(any("max 1024" in error for error in errors), errors)

    def test_description_at_limit(self):
        skill_dir = self.make_skill("report-writer", description="a" * 1024)

        valid, errors, _ = self.validate(skill_dir)

        self.assertTrue(valid)
        self.assertEqual(errors, [])

    def test_long_skill_warns(self):
        skill_dir = self.make_skill("long-skill")
        frontmatter = (skill_dir / "SKILL.md").read_text()
        filler = "Do the step.\n" * (501 - len(frontmatter.splitlines()))
        (skill_dir / "SKILL.md").write_text(frontmatter + filler)

        valid, errors, warnings = self.validate(skill_dir)

        self.assertTrue(valid, errors)
        self.assertEqual(len(warnings), 1, warnings)
        self.assertIn("500", warnings[0])

    def test_missing_provenance_reference(self):
        skill_dir = self.make_skill(
            "report-writer", body="Read PROVENANCE.md for the sources.\n"
        )

        valid, errors, _ = self.validate(skill_dir)

        self.assertFalse(valid)
        self.assertIn("Referenced file not found: PROVENANCE.md", errors)

    def test_spec_md_not_checked(self):
        skill_dir = self.make_skill(
            "report-writer", body="Read SPEC.md for the contract.\n"
        )

        valid, errors, _ = self.validate(skill_dir)

        self.assertTrue(valid, errors)


if __name__ == "__main__":
    unittest.main()
