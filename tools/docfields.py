"""Add Sphinx reST field lists (and missing docstrings) to functions, from a table of descriptions.

The table maps ``"qualified.name" -> (summary, {param: description}, returns)``.  ``summary`` is used only when the
function has no docstring (otherwise the existing text is kept verbatim and the fields are appended).  Every
parameter the function has must be described, so a table can never silently leave one out.

Usage::

    python tools/docfields.py modules/aizawa_attractor/maths.py specs/aizawa.py
"""
from __future__ import annotations
import ast
import inspect
import runpy
import sys


def _render(text: str, fields: list[str], indent: str) -> str:
    body = text.strip("\n")
    if fields:
        body = (body + "\n\n" if body else "") + "\n".join(fields)
    quote = 'r"""' if "\\" in body else '"""'
    lines = body.split("\n")
    if len(lines) == 1:
        return f"{indent}{quote}{lines[0]}\"\"\"\n"
    out = [f"{indent}{quote}{lines[0]}"] + [(indent + l) if l.strip() else "" for l in lines[1:]]
    return "\n".join(out) + f"\n{indent}\"\"\"\n"


def patch(path: str, spec: dict) -> int:
    src = open(path, encoding="utf-8").read()
    lines = src.splitlines(keepends=True)
    tree = ast.parse(src)
    edits = []

    def walk(node, prefix=""):
        for n in node.body:
            if isinstance(n, ast.ClassDef):
                yield prefix + n.name, n
                yield from walk(n, prefix + n.name + ".")
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                yield prefix + n.name, n

    for q, n in walk(tree):
        if q not in spec:
            continue
        summary, params, returns = spec[q]
        names = [a.arg for a in n.args.args + n.args.kwonlyargs if a.arg not in ("self", "cls")]
        missing = [p for p in names if p not in params]
        extra = [p for p in params if p not in names]
        if missing or extra:
            raise SystemExit(f"{q}: params missing {missing}, unknown {extra}")
        fields = [f":param {p}: {params[p]}" for p in names]
        if returns:
            fields.append(f":returns: {returns}")
        first = n.body[0]
        has_doc = isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant) and isinstance(first.value.value, str)
        body_line = first.lineno
        if has_doc:
            text = inspect.cleandoc(first.value.value)
            indent = " " * first.col_offset
            edits.append((first.lineno, first.end_lineno, _render(text, fields, indent)))
        else:
            if body_line == n.lineno:
                raise SystemExit(f"{q}: one-line def, split it first")
            indent = " " * first.col_offset
            edits.append((body_line, body_line - 1, _render(summary or "", fields, indent)))
    for start, end, new in sorted(edits, reverse=True):
        lines[start - 1:end] = [new]
    open(path, "w", encoding="utf-8").write("".join(lines))
    ast.parse("".join(lines))
    return len(edits)


if __name__ == "__main__":
    spec = runpy.run_path(sys.argv[2])["SPEC"]
    print(sys.argv[1], patch(sys.argv[1], spec), "docstrings written")
