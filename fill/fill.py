"""A small mustache engine: `render(template, data, partials, escape)`.

Supports the six required files of mustache/spec v1.4.3 (comments, delimiters,
interpolation, inverted, partials, sections). Lambdas, inheritance, and dynamic
names are not supported. See PROVENANCE.md.
"""

WHITESPACE = " \t"


def html_escape(text):
    # Interpolation spec, "HTML Escaping": & " < > only. `'` stays as it is.
    return (
        text.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def tokenize(template):
    """Yield (kind, value, indent) tokens.

    kind is one of text, var, raw, open, inverted, close, partial.
    indent is the whitespace before a standalone partial tag, else "".
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
        elif sigil and sigil in "#^/!>=&":
            kind, name = sigil, content[1:].strip()
        else:
            kind, name = "var", content.strip()

        indent = ""
        standalone_kinds = ("#", "^", "/", "!", ">", "=")
        text_end = start
        if kind in standalone_kinds:
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
            yield "text", template[pos:text_end], ""
        pos = last_tag_end = tag_end

        if kind == "#":
            yield "open", name, ""
        elif kind == "^":
            yield "inverted", name, ""
        elif kind == "/":
            yield "close", name, ""
        elif kind == ">":
            yield "partial", name, indent
        elif kind in ("&", "raw"):
            yield "raw", name, ""
        elif kind == "var":
            yield "var", name, ""
        elif kind == "=":
            parts = name.split()
            if len(parts) != 2:
                raise ValueError("bad delimiter tag")
            open_delim, close_delim = parts
        # "!" yields nothing.
    if pos < len(template):
        yield "text", template[pos:], ""


def parse(template):
    """Build a tree of (kind, value, extra) nodes. Sections hold a child list in extra."""
    root = []
    stack = [("", root)]
    for kind, value, indent in tokenize(template):
        children = stack[-1][1]
        if kind in ("open", "inverted"):
            node = (kind, value, [])
            children.append(node)
            stack.append((value, node[2]))
        elif kind == "close":
            if len(stack) == 1 or stack[-1][0] != value:
                raise ValueError(f"unexpected closing tag: {value}")
            stack.pop()
        else:
            children.append((kind, value, indent))
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
    for kind, value, extra in nodes:
        if kind == "text":
            out.append(value)
        elif kind == "var":
            out.append(escape(stringify(lookup(value, contexts))))
        elif kind == "raw":
            out.append(stringify(lookup(value, contexts)))
        elif kind == "partial":
            text = indent_lines(partials.get(value, ""), extra)
            out.append(render_nodes(parse(text), contexts, partials, escape))
        else:
            found = lookup(value, contexts)
            if kind == "inverted":
                if is_falsey(found):
                    out.append(render_nodes(extra, contexts, partials, escape))
            elif not is_falsey(found):
                items = found if isinstance(found, list) else [found]
                for item in items:
                    out.append(render_nodes(extra, contexts + [item], partials, escape))
    return "".join(out)


def render(template, data, partials=None, escape=html_escape):
    return render_nodes(parse(template), [data], partials or {}, escape)
