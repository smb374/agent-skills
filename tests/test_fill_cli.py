import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

FILL = Path(__file__).resolve().parent.parent / "fill" / "fill.py"
PRAGMA = "{{! fill: no-escape }}"


class FillCliTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.out = self.dir / "out.md"

    def template(self, text, name="t.md"):
        path = self.dir / name
        path.write_text(text)
        return path

    def values(self, data):
        path = self.dir / "v.json"
        path.write_text(data if isinstance(data, str) else json.dumps(data))
        return path

    def fill(self, *args, timeout=None):
        return subprocess.run(
            [sys.executable, str(FILL), *map(str, args)],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

    def render(self, text, data, *flags, timeout=None):
        args = (*flags, self.template(text), self.values(data), self.out)
        return self.fill(*args, timeout=timeout)

    def assert_problems(self, result, *lines):
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr.splitlines(), list(lines))
        self.assertFalse(self.out.exists())

    def assert_out_exists_problem(self, result):
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stderr.splitlines(), [f"out file exists: {self.out}"])
        self.assertEqual(self.out.read_text(), "old")

    def assert_rendered(self, result, expected):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((result.stdout, result.stderr), ("", ""))
        self.assertEqual(self.out.read_text(), expected)

    def test_render_ok(self):
        self.assert_rendered(self.render("Hi {{name}}", {"name": "Ann"}), "Hi Ann")

    def test_runs_without_interpreter(self):
        # The skills run fill.py directly, so that one permission rule can allow it.
        args = (
            FILL,
            self.template("Hi {{name}}"),
            self.values({"name": "Ann"}),
            self.out,
        )
        result = subprocess.run(
            list(map(str, args)), check=False, capture_output=True, text=True
        )
        self.assert_rendered(result, "Hi Ann")

    def test_escape_default(self):
        self.assert_rendered(self.render("{{v}}", {"v": "<b>&"}), "&lt;b&gt;&amp;")

    def test_no_escape_flag(self):
        result = self.render("{{v}}", {"v": "<b>&"}, "--no-escape")
        self.assert_rendered(result, "<b>&")

    def test_pragma_line_one(self):
        result = self.render(PRAGMA + "\n{{v}}", {"v": "<b>&"})
        self.assert_rendered(result, "<b>&")

    def test_pragma_elsewhere(self):
        result = self.render("a\n" + PRAGMA + "\n{{v}}", {"v": "x"})
        self.assert_problems(
            result,
            f"template: line 2: '{PRAGMA}' is allowed only on line 1 of the top template",
        )

    def test_pragma_in_partial(self):
        self.template(PRAGMA + "\n{{v}}", "part.md")
        self.assert_problems(
            self.render("{{> part.md}}", {"v": "x"}),
            f"partial part.md: line 1: '{PRAGMA}' is allowed only on line 1 of the"
            " top template",
        )

    def test_partial_escape_follows_top(self):
        self.template("{{v}}", "part.md")
        result = self.render(PRAGMA + "\n{{> part.md}}", {"v": "<b>"})
        self.assert_rendered(result, "<b>")

    def test_partial_loads_from_template_dir(self):
        self.template("[{{v}}]", "part.md")
        result = self.fill(
            self.template("{{> part.md}}"), self.values({"v": "x"}), self.out
        )
        self.assert_rendered(result, "[x]")

    def test_missing_partial(self):
        self.assert_problems(
            self.render("{{> nope.md}}", {}), "partial not found: nope.md"
        )

    def test_missing_key(self):
        self.assert_problems(self.render("{{name}}", {}), "missing key in values: name")

    def test_unknown_key(self):
        self.assert_problems(
            self.render("{{name}}", {"name": "x", "extra": "y"}),
            "unknown key (no tag uses it): extra",
        )

    def test_missing_section_key(self):
        self.assert_problems(
            self.render("{{#items}}{{.}}{{/items}}", {}),
            "missing key in values: items",
        )

    def test_missing_inverted_key(self):
        self.assert_problems(
            self.render("{{^empty}}none{{/empty}}", {}),
            "missing key in values: empty",
        )

    def test_dot_exempt(self):
        result = self.render("{{#items}}- {{.}}\n{{/items}}", {"items": ["a", "b"]})
        self.assert_rendered(result, "- a\n- b\n")

    def test_string_as_section(self):
        self.assert_problems(
            self.render("{{#title}}x{{/title}}", {"title": "s"}),
            "title: a string can be used only as a variable",
        )

    def test_list_as_variable(self):
        self.assert_problems(
            self.render("{{items}}", {"items": ["s"]}),
            "items: a list cannot be used as a variable",
        )

    def test_list_section_without_dot(self):
        self.assert_problems(
            self.render("{{#items}}x{{/items}}", {"items": ["s"]}),
            "items: every {{#items}} body must use {{.}}",
        )

    def test_list_non_string_item(self):
        result = self.render("{{#items}}{{.}}{{/items}}", {"items": ["a", 1]})
        self.assert_problems(result, "items[1]: list items must be strings")

    def test_bool_as_variable(self):
        self.assert_problems(
            self.render("{{flag}}", {"flag": True}),
            "flag: a boolean cannot be used as a variable",
        )

    def test_bool_section(self):
        text = "{{#a}}yes{{/a}}{{^a}}no{{/a}}"
        self.assert_rendered(self.render(text, {"a": True}), "yes")
        self.out.unlink()
        self.assert_rendered(self.render(text, {"a": False}), "no")

    def assert_bad_type(self, value):
        self.assert_problems(
            self.render("{{title}}", {"title": value}),
            "title: value must be a string, a list of strings, or a boolean",
        )

    def test_null_value(self):
        self.assert_bad_type(None)

    def test_number_value(self):
        self.assert_bad_type(1)

    def test_object_value(self):
        self.assert_bad_type({})

    def test_empty_string(self):
        self.assert_problems(
            self.render("{{title}}", {"title": ""}), "title: empty string"
        )

    def test_empty_string_in_list(self):
        result = self.render("{{#items}}{{.}}{{/items}}", {"items": ["a", ""]})
        self.assert_problems(result, "items[1]: empty string")

    def test_empty_list_without_inverted(self):
        self.assert_problems(
            self.render("{{#items}}{{.}}{{/items}}", {"items": []}),
            "items: empty list needs a {{^items}} section",
        )

    def test_empty_list_with_inverted(self):
        text = "{{#items}}{{.}}{{/items}}{{^items}}none{{/items}}"
        self.assert_rendered(self.render(text, {"items": []}), "none")

    def test_existing_out_file(self):
        self.out.write_text("old")
        self.assert_out_exists_problem(self.render("x", {}))

    def test_creates_parent_dirs(self):
        out = self.dir / "a" / "b" / "out.md"
        result = self.fill(self.template("x"), self.values({}), out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(out.read_text(), "x")

    def test_fields_skeleton(self):
        template = self.template(
            "{{! the name }}\n{{name}}\n{{#items}}{{.}}{{/items}}\n"
            "{{! on or off }}\n{{#flag}}x{{/flag}}\n{{name}}\n"
        )
        result = self.fill("--fields", template, self.out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                "name (string): the name",
                "items (list):",
                "flag (bool): on or off",
            ],
        )
        written = self.out.read_text()
        self.assertEqual(
            json.loads(written), {"name": None, "items": None, "flag": None}
        )
        self.assertEqual(list(json.loads(written)), ["name", "items", "flag"])

    def test_fields_existing_out_file(self):
        self.out.write_text("old")
        result = self.fill("--fields", self.template("{{title}}"), self.out)
        self.assert_out_exists_problem(result)

    def test_all_problems_listed(self):
        result = self.render("{{title}}{{name}}", {"extra": "x", "name": ""})
        self.assert_problems(
            result,
            "missing key in values: title",
            "unknown key (no tag uses it): extra",
            "name: empty string",
        )

    def test_usage_exit_2(self):
        self.assertEqual(self.fill().returncode, 2)
        result = self.fill("--bogus", self.template("x"), self.values({}), self.out)
        self.assertEqual(result.returncode, 2)

    def test_bad_json_values(self):
        self.assert_problems(
            self.render("x", "not json"),
            "cannot read values: Expecting value: line 1 column 1 (char 0)",
        )

    def test_values_not_object(self):
        self.assert_problems(self.render("x", []), "values must be a JSON object")

    def test_fields_with_no_escape_usage(self):
        result = self.fill("--fields", "--no-escape", self.template("{{a}}"), self.out)
        self.assertEqual(result.returncode, 2)

    def test_nested_partial(self):
        self.template("[{{> b.md}}]", "a.md")
        self.template("{{v}}", "b.md")
        result = self.render("{{> a.md}}", {"v": "x"})
        self.assert_rendered(result, "[x]")

    def test_fields_recursive_partial(self):
        self.template("{{name}}{{> a.md}}", "a.md")
        result = self.fill(
            "--fields", self.template("{{> a.md}}"), self.out, timeout=10
        )
        self.assert_problems(result, "recursive partial: a.md")

    def test_render_recursive_partial(self):
        self.template("{{name}}{{> b.md}}", "a.md")
        self.template("{{> a.md}}", "b.md")
        result = self.render("{{> a.md}}", {"name": "x"}, timeout=10)
        self.assert_problems(result, "recursive partial: a.md")

    def test_dot_in_partial_counts_for_section(self):
        self.template("- {{.}}\n", "row.md")
        text = "{{#items}}{{> row.md}}{{/items}}"
        self.assert_rendered(self.render(text, {"items": ["a"]}), "- a\n")
        self.out.unlink()
        result = self.fill("--fields", self.template(text), self.out)
        self.assertEqual(result.stdout.splitlines(), ["items (list):"])

    def test_template_error_no_unknown_key_problem(self):
        result = self.render("{{#flag}}x", {"flag": True})
        self.assert_problems(result, "template: template error: unclosed section: flag")

    def test_fields_hint_stops_at_comment_end(self):
        result = self.fill(
            "--fields", self.template("{{! the name }}{{g}}\n{{name}}"), self.out
        )
        self.assertEqual(
            result.stdout.splitlines(), ["g (string):", "name (string): the name"]
        )

    def test_fields_hint_ignores_pragma(self):
        result = self.fill("--fields", self.template(PRAGMA + "\n{{title}}"), self.out)
        self.assertEqual(result.stdout.splitlines(), ["title (string):"])

    def test_dotted_name(self):
        self.assert_problems(
            self.render("{{user.name}}", {"user.name": "x"}),
            "dotted tag name not allowed: user.name",
        )

    def test_dot_outside_list_section(self):
        self.assert_problems(
            self.render("{{^items}}{{.}}{{/items}}", {"items": []}),
            "{{.}} must be inside a {{#key}} list section",
        )
        self.assert_problems(
            self.render("{{#flag}}{{.}}{{/flag}}", {"flag": True}),
            "flag: a boolean section cannot use {{.}}",
        )

    def test_out_path_blocked_by_file(self):
        (self.dir / "f").write_text("x")
        out = self.dir / "f" / "x.md"
        result = self.fill(self.template("x"), self.values({}), out)
        self.assertEqual(result.returncode, 1)
        lines = result.stderr.splitlines()
        self.assertEqual(len(lines), 1, result.stderr)
        # The OS error text after the prefix differs by platform.
        self.assertTrue(lines[0].startswith(f"cannot write {out}: "), lines[0])

    def test_fields_partial_and_inverted(self):
        self.template("{{#items}}{{.}}{{/items}}", "p.md")
        template = self.template("{{b}}\n{{> p.md}}\n{{^items}}none{{/items}}\n{{a}}")
        result = self.fill("--fields", template, self.out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(),
            ["b (string):", "items (list):", "a (string):"],
        )
        self.assertEqual(list(json.loads(self.out.read_text())), ["b", "items", "a"])

    def test_fields_creates_parent_dirs(self):
        out = self.dir / "a" / "b" / "f.json"
        result = self.fill("--fields", self.template("{{a}}"), out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(out.read_text()), {"a": None})

    def test_dot_belongs_to_nearest_section(self):
        text = "{{#flag}}{{#items}}{{.}}{{/items}}{{/flag}}"
        data = {"flag": True, "items": ["a"]}
        self.assert_rendered(self.render(text, data), "a")
        self.out.unlink()
        result = self.fill("--fields", self.template(text), self.out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["flag (bool):", "items (list):"])

    def test_dot_in_inverted_counts_for_list(self):
        text = "{{#items}}{{^x}}{{.}}{{/x}}{{/items}}"
        data = {"items": ["a"], "x": False}
        self.assert_rendered(self.render(text, data), "a")
        self.out.unlink()
        result = self.fill("--fields", self.template(text), self.out)
        self.assertEqual(result.stdout.splitlines(), ["items (list):", "x (bool):"])

    def test_problems_in_document_order(self):
        self.template("{{.}}\n" + PRAGMA, "row.md")
        text = "{{#items}}{{user.name}}{{> row.md}}{{> nope.md}}{{/items}}"
        lines = (
            "dotted tag name not allowed: user.name",
            f"partial row.md: line 2: '{PRAGMA}' is allowed only on line 1 of the"
            " top template",
            "partial not found: nope.md",
        )
        data = {"items": ["a"], "user.name": "x"}
        self.assert_problems(self.render(text, data), *lines)
        result = self.fill("--fields", self.template(text), self.out)
        self.assert_problems(result, *lines)


if __name__ == "__main__":
    unittest.main()
