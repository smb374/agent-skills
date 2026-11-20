"""Tests for the mustache engine in fill/fill.py, against the vendored mustache/spec v1.4.3."""

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("fill", ROOT / "fill" / "fill.py")
fill = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fill)
SPEC_DIR = ROOT / "tests" / "mustache_spec"


class SpecCases(unittest.TestCase):
    def run_spec(self, name):
        cases = json.loads((SPEC_DIR / f"{name}.json").read_text())["tests"]
        for case in cases:
            with self.subTest(case["name"]):
                got = fill.render(
                    case["template"], case["data"], case.get("partials", {})
                )
                self.assertEqual(got, case["expected"])

    def test_spec_comments(self):
        self.run_spec("comments")

    def test_spec_delimiters(self):
        self.run_spec("delimiters")

    def test_spec_interpolation(self):
        self.run_spec("interpolation")

    def test_spec_inverted(self):
        self.run_spec("inverted")

    def test_spec_partials(self):
        self.run_spec("partials")

    def test_spec_sections(self):
        self.run_spec("sections")


class EscapeArgument(unittest.TestCase):
    def test_escape_argument(self):
        got = fill.render("{{a}}|{{{a}}}", {"a": "<b>"}, {}, lambda s: "[" + s + "]")
        self.assertEqual(got, "[<b>]|<b>")
