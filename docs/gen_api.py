"""Regenerate docs/api/*.rst from the package layout.

Run from anywhere:  python3 docs/gen_api.py
One page per registry module, one for the standalone engines, one for the
engine/ infrastructure. Pages only name modules; autodoc reads the docstrings.
"""
import ast
import json
import pathlib

DOCS = pathlib.Path(__file__).resolve().parent
ROOT = DOCS.parent
API = DOCS / "api"

STANDALONE_SKIP = {"__init__", "__main__", "verify_install"}
ENGINE_MODULES = ["registry", "manifest", "format", "units", "constants"]
AUTO = "   :members:\n   :undoc-members:\n   :show-inheritance:\n"


def title(text, ch="="):
    return f"{text}\n{ch * len(text)}\n\n"


def automodule(name):
    return f".. automodule:: {name}\n{AUTO}\n"


def first_line(path):
    doc = ast.get_docstring(ast.parse(path.read_text())) or ""
    line = doc.strip().split("\n")[0]
    return line.replace("|", "\\|")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def standalone():
    out = title("Standalone engines")
    out += ("Single files, imported by name: ``from ValaQuenta.noether import "
            "NoetherCurrents``.\n\n")
    for p in sorted(ROOT.glob("*.py")):
        if p.stem in STANDALONE_SKIP:
            continue
        out += title(f"``{p.stem}``", "-")
        out += automodule(f"ValaQuenta.{p.stem}")
    write(API / "engines.rst", out)


def infrastructure():
    out = title("Registry and engine infrastructure")
    out += ("The contract every registry module satisfies, the manifest and "
            "plugin-format machinery, and the shared unit and constant tables.\n\n")
    for m in ENGINE_MODULES:
        if (ROOT / "engine" / f"{m}.py").exists():
            out += title(f"``engine.{m}``", "-")
            out += automodule(f"ValaQuenta.engine.{m}")
    write(API / "infrastructure.rst", out)


def modules():
    names = []
    for d in sorted((ROOT / "modules").iterdir()):
        if not (d.is_dir() and (d / "__init__.py").exists()):
            continue
        man = d / "manifest.json"
        display = json.loads(man.read_text())["display"] if man.exists() else d.name
        display = " ".join(display.split())
        out = title(f"``{d.name}``")
        out += f"{display}\n\n"
        out += automodule(f"ValaQuenta.modules.{d.name}")
        for sub in ("maths", "tools"):
            if (d / f"{sub}.py").exists():
                out += title(sub, "-")
                out += automodule(f"ValaQuenta.modules.{d.name}.{sub}")
        for extra in sorted(d.glob("*.py")):
            if extra.stem not in {"__init__", "maths", "tools"}:
                out += title(extra.stem, "-")
                out += automodule(f"ValaQuenta.modules.{d.name}.{extra.stem}")
        write(API / "modules" / f"{d.name}.rst", out)
        names.append((d.name, display))
    return names


def index(names):
    out = title("API Reference")
    out += (".. toctree::\n   :maxdepth: 1\n\n   engines\n   infrastructure\n\n"
            "Registry modules\n----------------\n\n"
            "Each module has ``maths.py`` (the mathematics as plain functions) and, "
            "when registered, ``tools.py`` (the ``EquationModule`` class).\n\n"
            ".. toctree::\n   :maxdepth: 1\n\n")
    for n, _ in names:
        out += f"   modules/{n}\n"
    write(API / "index.rst", out)


if __name__ == "__main__":
    standalone()
    infrastructure()
    index(modules())
    print("wrote", sum(1 for _ in API.rglob("*.rst")), "pages")
