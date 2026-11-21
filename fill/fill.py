#!/usr/bin/env python3
"""A small mustache engine: `render(template, data, partials, escape)`.

Supports the six required files of mustache/spec v1.4.3 (comments, delimiters,
interpolation, inverted, partials, sections). Lambdas, inheritance, and dynamic
names are not supported. See PROVENANCE.md.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

WHITESPACE = " \t"
SIGILS = {
    "#": "open",
    "^": "inverted",
    "/": "close",
    "!": "comment",
    ">": "partial",
    "=": "delimiters",
    "&": "raw",
}
STANDALONE_KINDS = ("open", "inverted", "close", "comment", "partial", "delimiters")


class Node(NamedTuple):
    kind: str
    value: str
    indent: str = ""
    children: tuple | list = ()
    offset: int = 0


def html_escape(text):
    # Interpolation spec, "HTML Escaping": & " < > only. `'` stays as it is.
    return (
        text.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def tokenize(template):
    """Yield (kind, value, indent, offset) tokens.

    kind is one of text, var, raw, open, inverted, close, partial.
    indent is the whitespace before a standalone tag, else "".
    offset is where the tag (or text) starts in the template.
    """
    open_delim, close_delim = "{{", "}}"
    pos = 0
    last_tag_end = 0
    while True:
        start = template.find(open_delim, pos)
        if start == -1:
            break
        body_start = start + len(open_delim)
        closer = close_delim
        triple = template.startswith("{", body_start) and open_delim == "{{"
        if triple:
            closer = "}" + close_delim
        elif template.startswith("=", body_start):
            closer = "=" + close_delim
        end = template.find(closer, body_start)
        if end == -1:
            raise ValueError(f"unclosed tag at offset {start}")
        content = template[body_start:end]
        tag_end = end + len(closer)
        sigil = content[:1]
        if triple:
            kind, name = "raw", content[1:].strip()
        elif sigil in SIGILS:
            kind, name = SIGILS[sigil], content[1:].strip()
        else:
            kind, name = "var", content.strip()

        indent = ""
        text_end = start
        if kind in STANDALONE_KINDS:
            line_start = template.rfind("\n", 0, start) + 1
            before = template[line_start:start]
            line_end = template.find("\n", tag_end)
            after = template[tag_end : len(template) if line_end == -1 else line_end]
            if (
                last_tag_end <= line_start
                and before.strip(WHITESPACE) == ""
                and after.strip(WHITESPACE + "\r") == ""
                and (
                    after == ""
                    or after.rstrip(WHITESPACE).endswith("\r")
                    or "\r" not in after
                )
            ):
                text_end = line_start
                indent = before
                tag_end = len(template) if line_end == -1 else line_end + 1
        if text_end > pos:
            yield "text", template[pos:text_end], "", pos
        pos = last_tag_end = tag_end

        if kind == "delimiters":
            parts = name.split()
            if len(parts) != 2:
                raise ValueError("bad delimiter tag")
            open_delim, close_delim = parts
        elif kind != "comment":
            yield kind, name, indent, start
    if pos < len(template):
        yield "text", template[pos:], "", pos


def parse(template):
    """Build a tree of Nodes. A section Node holds its child Nodes in children."""
    root = []
    stack = [("", root)]
    for kind, value, indent, offset in tokenize(template):
        children = stack[-1][1]
        if kind in ("open", "inverted"):
            node = Node(kind, value, children=[], offset=offset)
            children.append(node)
            stack.append((value, node.children))
        elif kind == "close":
            if len(stack) == 1 or stack[-1][0] != value:
                raise ValueError(f"unexpected closing tag: {value}")
            stack.pop()
        else:
            children.append(Node(kind, value, indent, offset=offset))
    if len(stack) > 1:
        raise ValueError(f"unclosed section: {stack[-1][0]}")
    return root


def lookup(name, contexts):
    """Return the value of a dotted name, or "" when it is missing."""
    if name == ".":
        return contexts[-1]
    first, *rest = name.split(".")
    for context in reversed(contexts):
        if isinstance(context, dict) and first in context:
            value = context[first]
            break
    else:
        return ""
    for part in rest:
        if not (isinstance(value, dict) and part in value):
            return ""
        value = value[part]
    return value


def is_falsey(value):
    return (
        value is None
        or value is False
        or value == ""
        or (isinstance(value, list) and not value)
    )


def stringify(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def indent_lines(text, indent):
    if not indent:
        return text
    lines = text.split("\n")
    return "\n".join(indent + line if line else line for line in lines)


def render_nodes(nodes, contexts, partials, escape):
    out = []
    for node in nodes:
        if node.kind == "text":
            out.append(node.value)
        elif node.kind == "var":
            out.append(escape(stringify(lookup(node.value, contexts))))
        elif node.kind == "raw":
            out.append(stringify(lookup(node.value, contexts)))
        elif node.kind == "partial":
            text = indent_lines(partials.get(node.value, ""), node.indent)
            out.append(render_nodes(parse(text), contexts, partials, escape))
        else:
            found = lookup(node.value, contexts)
            if node.kind == "inverted":
                if is_falsey(found):
                    out.append(render_nodes(node.children, contexts, partials, escape))
            elif not is_falsey(found):
                items = found if isinstance(found, list) else [found]
                for item in items:
                    out.append(
                        render_nodes(node.children, contexts + [item], partials, escape)
                    )
    return "".join(out)


def render(template, data, partials=None, escape=html_escape):
    return render_nodes(parse(template), [data], partials or {}, escape)


PRAGMA = "{{! fill: no-escape }}"
COMMENT_LINE = re.compile(r"[ \t]*\{\{!((?:(?!\}\}).)*)\}\}")
VARIABLE_KINDS = ("var", "raw")


def hint_before(text, offset):
    """Return the comment text on the line just before the line of offset."""
    line_start = text.rfind("\n", 0, offset) + 1
    if line_start == 0:
        return ""
    previous = text[text.rfind("\n", 0, line_start - 1) + 1 : line_start - 1]
    if previous.strip() == PRAGMA:
        return ""
    match = COMMENT_LINE.match(previous)
    return match.group(1).strip() if match else ""


def read_utf8(path):
    # Not Path.read_text: its universal newlines would turn \r\n into \n.
    return path.read_bytes().decode("utf-8")


class Use(NamedTuple):
    kind: str
    dot: bool  # an open section whose own body uses {{.}}


def as_variable(uses):
    return any(use.kind in VARIABLE_KINDS for use in uses)


class TemplateScan:
    """A top template and its partials, read and checked, with the key uses."""

    def __init__(self, path):
        self.dir = path.parent
        self.problems = []
        self.broken = False  # a template error or a missing partial hides tag uses
        self.partials = {}
        self.parsed = {}  # partial name -> nodes
        self.stack = []  # partials being walked, to find recursion
        self.uses = {}
        self.hints = {}
        text = read_utf8(path)
        self.text = text
        self.no_escape = text.split("\n", 1)[0] == PRAGMA
        self.check_pragma(text, "template", top=True)
        nodes = self.parse_text(text)
        self.walk_nodes(nodes, text, [])
        self.problems = list(dict.fromkeys(self.problems))

    def check_pragma(self, text, where, top=False):
        for number, line in enumerate(text.split("\n")):
            if PRAGMA in line and not (top and number == 0 and line == PRAGMA):
                self.problems.append(
                    f"{where}: line {number + 1}: '{PRAGMA}' is allowed only"
                    " on line 1 of the top template"
                )

    def fail(self, problem):
        self.broken = True
        self.problems.append(problem)

    def parse_text(self, text, where="template"):
        try:
            return parse(text)
        except ValueError as error:
            self.fail(f"{where}: template error: {error}")
            return []

    def walk_nodes(self, nodes, text, sections):
        """Record the key uses. Return True when a {{.}} belongs to the nearest
        enclosing open section: an inverted section or a partial passes it up."""
        dot = False
        for node in nodes:
            if node.kind == "partial":
                if node.value in self.stack:
                    self.problems.append(f"recursive partial: {node.value}")
                    continue
                partial = self.partial_nodes(node.value)
                self.stack.append(node.value)
                dot |= self.walk_nodes(partial, self.partials[node.value], sections)
                self.stack.pop()
            elif node.value == "." and node.kind != "text":
                if "open" not in sections:
                    self.problems.append("{{.}} must be inside a {{#key}} list section")
                dot = True
            elif node.kind != "text":
                key = node.value
                if "." in key:
                    self.problems.append(f"dotted tag name not allowed: {key}")
                if key not in self.uses:
                    self.hints[key] = hint_before(text, node.offset)
                uses = self.uses.setdefault(key, [])
                inner = self.walk_nodes(node.children, text, [*sections, node.kind])
                uses.append(Use(node.kind, node.kind == "open" and inner))
                if node.kind == "inverted":
                    dot |= inner
        return dot

    def partial_nodes(self, name):
        """Load a partial file once and return its nodes ([] when unusable)."""
        if name in self.parsed:
            return self.parsed[name]
        nodes = []
        path = self.dir / name
        if not path.is_file():
            self.partials[name] = ""
            self.fail(f"partial not found: {name}")
        else:
            text = read_utf8(path)
            self.partials[name] = text
            self.check_pragma(text, f"partial {name}")
            nodes = self.parse_text(text, f"partial {name}")
        self.parsed[name] = nodes
        return nodes

    def field_type(self, key):
        uses = self.uses[key]
        if as_variable(uses):
            return "string"
        return "list" if any(use.dot for use in uses) else "bool"

    def skeleton(self):
        """Return the --fields output: the null skeleton and the key lines."""
        content = json.dumps({key: None for key in self.uses}, indent=2) + "\n"
        lines = []
        for key in self.uses:
            hint = self.hints[key]
            line = f"{key} ({self.field_type(key)}):"
            lines.append(f"{line} {hint}" if hint else line)
        return content, "\n".join(lines)

    def check(self, values):
        problems = []
        for key in self.uses:
            if key not in values:
                problems.append(f"missing key in values: {key}")
        for key, value in values.items():
            uses = self.uses.get(key)
            if uses is None:
                if not self.broken:
                    problems.append(f"unknown key (no tag uses it): {key}")
                continue
            problems += check_value(key, value, uses)
        return problems

    def render(self, values, no_escape):
        escape = (lambda text: text) if no_escape or self.no_escape else html_escape
        return render(self.text, values, self.partials, escape)


def check_value(key, value, uses):
    problems = []
    as_section = any(use.kind in ("open", "inverted") for use in uses)
    if isinstance(value, bool):
        if any(use.kind == "open" and use.dot for use in uses):
            problems.append(f"{key}: a boolean section cannot use {{{{.}}}}")
        if as_variable(uses):
            problems.append(f"{key}: a boolean cannot be used as a variable")
    elif isinstance(value, str):
        if value == "":
            problems.append(f"{key}: empty string")
        if as_section:
            problems.append(f"{key}: a string can be used only as a variable")
    elif isinstance(value, list):
        if not value and not any(use.kind == "inverted" for use in uses):
            problems.append(f"{key}: empty list needs a {{{{^{key}}}}} section")
        if as_variable(uses):
            problems.append(f"{key}: a list cannot be used as a variable")
        if any(use.kind == "open" and not use.dot for use in uses):
            problems.append(f"{key}: every {{{{#{key}}}}} body must use {{{{.}}}}")
        for index, item in enumerate(value):
            if not isinstance(item, str):
                problems.append(f"{key}[{index}]: list items must be strings")
            elif item == "":
                problems.append(f"{key}[{index}]: empty string")
    else:
        problems.append(
            f"{key}: value must be a string, a list of strings, or a boolean"
        )
    return problems


def read_values(path):
    """Return (values, problems)."""
    try:
        values = json.loads(read_utf8(path))
    except (OSError, ValueError) as error:
        return None, [f"cannot read values: {error}"]
    if not isinstance(values, dict):
        return None, ["values must be a JSON object"]
    return values, []


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="fill",
        allow_abbrev=False,
        usage=(
            "fill [--no-escape] <template> <values.json> <out-file>\n"
            "       fill --fields <template> <out-file>"
        ),
    )
    parser.add_argument("--no-escape", action="store_true")
    parser.add_argument("--fields", action="store_true")
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args(argv)
    if args.fields and args.no_escape:
        parser.error("--fields cannot be used with --no-escape")
    if len(args.paths) != (2 if args.fields else 3):
        parser.error("wrong number of arguments")
    template, out = Path(args.paths[0]), Path(args.paths[-1])
    problems = [f"out file exists: {out}"] if os.path.lexists(out) else []
    try:
        scan = TemplateScan(template)
    except (OSError, UnicodeDecodeError) as error:
        scan = None
        problems.append(f"cannot read template: {error}")
    summary = ""
    if scan:
        problems += scan.problems
        if args.fields:
            output, summary = scan.skeleton()
        else:
            values, value_problems = read_values(Path(args.paths[1]))
            problems += value_problems or scan.check(values)
            if not problems:
                output = scan.render(values, args.no_escape)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "x", encoding="utf-8", newline="") as handle:
            handle.write(output)
    except OSError as error:
        print(f"cannot write {out}: {error}", file=sys.stderr)
        return 1
    if summary:
        print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
