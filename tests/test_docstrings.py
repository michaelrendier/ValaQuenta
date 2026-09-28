"""Documentation contract: the public API is documented in Sphinx reST field lists."""
import ast
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
INHERITED = {"name", "display_name", "version", "description", "confidence_floor", "formulary",
             "run", "viewer_data", "on_register", "shell_commands", "summary",
             "process_description", "manifest"}   # documented once on EquationModule
FIELD = re.compile(r"^\s*:(param|returns?|raises)\b", re.M)


def package_files():
    files = [p for p in ROOT.glob("*.py") if p.name not in {"__main__.py", "verify_install.py"}]
    files += list((ROOT / "engine").glob("*.py"))
    files += list((ROOT / "modules").glob("*/*.py"))
    return sorted(files)


def public_nodes(tree):
    def walk(node, prefix=""):
        for n in node.body:
            if isinstance(n, ast.ClassDef) and not n.name.startswith("_"):
                yield prefix + n.name, n
                yield from walk(n, prefix + n.name + ".")
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and not n.name.startswith("_"):
                yield prefix + n.name, n
    yield "<module>", tree
    yield from walk(tree)


def test_every_public_name_has_a_docstring():
    missing = []
    for p in package_files():
        tree = ast.parse(p.read_text())
        for q, n in public_nodes(tree):
            inherited = "." in q and q.rsplit(".", 1)[1] in INHERITED and p.name == "tools.py"
            if not ast.get_docstring(n) and not inherited:
                missing.append(f"{p.relative_to(ROOT)}::{q}")
    assert missing == []


def test_functions_with_parameters_use_field_lists():
    plain = []
    for p in package_files():
        tree = ast.parse(p.read_text())
        for q, n in public_nodes(tree):
            if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            params = [a for a in n.args.args + n.args.kwonlyargs if a.arg not in ("self", "cls")]
            doc = ast.get_docstring(n) or ""
            if params and doc and not FIELD.search(doc):
                plain.append(f"{p.relative_to(ROOT)}::{q}")
    assert plain == []


def test_documented_raises_are_raised():
    """A ``:raises E:`` field must name an exception the function can raise."""
    wrong = []
    for p in package_files():
        if p.parts[-2] == "angular_rank":      # raises through a shared guard helper
            continue
        tree = ast.parse(p.read_text())
        for q, n in public_nodes(tree):
            if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            doc = set(re.findall(r"^\s*:raises (\w+):", ast.get_docstring(n) or "", re.M))
            body = {ast.unparse(x.exc.func if isinstance(x.exc, ast.Call) else x.exc)
                    for x in ast.walk(n) if isinstance(x, ast.Raise) and x.exc is not None}
            if doc - body:
                wrong.append(f"{p.relative_to(ROOT)}::{q}: {sorted(doc - body)}")
    assert wrong == []
