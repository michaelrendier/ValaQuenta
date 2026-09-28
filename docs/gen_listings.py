"""Regenerate docs/listings.rst: short mechanisms shown as complete code.

Each listing is extracted from the source by name (docstrings removed, every
statement otherwise byte-for-byte), assembled into ONE self-contained unit, and
then executed cold in an empty namespace. The REPL output shown under each
listing is what that execution printed. tests/test_listings.py re-runs the same
extraction, so a listing that stops running fails the test suite.

Run:  python3 docs/gen_listings.py
"""
import ast
import io
import contextlib
import json
import pathlib
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(__file__).resolve().parent / "listings.rst"

LISTINGS = [
    dict(
        key="horner", module="hyperwebster",
        title="Text to address: the Horner bijection",
        file="modules/hyperwebster/maths.py",
        names=("US_KEYBOARD_CHARS", "VOCAB_BASE", "_CHAR_TO_IDX", "_IDX_TO_CHAR", "char_to_idx",
               "idx_to_char", "horner_encode", "horner_decode"),
        header="from typing import Dict\n",
        prose=("A word is an integer. Each character is an index into a 97-character "
               "keyboard map, and the text is read as a numeral in base 97. The map is "
               "one-to-one, so the address decodes back to the text exactly."),
        example='n = horner_encode("prime")\nprint(n)\nprint(horner_decode(n, 5))',
    ),
    dict(
        key="p1", module="udeo_crypto",
        title="Word to Riemann-zero index: the P1 hash",
        file="modules/udeo_crypto/maths.py",
        span=("_P1_PRIME_CAP", "p1_zero_index"),
        header="from typing import List\n",
        prose=("A word is hashed by Horner's rule in base 95, the hash is taken to the next prime "
               "p ≤ 65536, and π(p) is the index of a Riemann zero. Everything is integer "
               "arithmetic."),
        example='print(p1_horner_hash("prime"))\nprint(p1_zero_index("prime"))',
    ),
    dict(
        key="channel", module="translator_common",
        title="Token to sixteen prime channels",
        file="modules/translator_common/maths.py",
        names=("PRIME_CHANNELS", "channel_signature"),
        header="import math\nfrom typing import List\n",
        prose=("The Dirichlet-weighted cosine projection of a token's character codes onto the "
               "sixteen prime channels. Deterministic, with no parameters."),
        example='print([round(x, 4) for x in channel_signature("dog")[:4]])',
    ),
    dict(
        key="collisions", module="bracketing_firing_order",
        title="A process that remembers where it has been",
        file="modules/bracketing_firing_order/maths.py",
        names=("trajectory", "visited_positions", "collisions"),
        header="from typing import Callable, Dict, List, Sequence, Tuple\n",
        prose=("The set-membership test behind Recamán's rule, for any sequence of steps: "
               "record every position the process reaches and report each revisit."),
        example=("steps = [lambda x: x + 1, lambda x: x - 1, lambda x: x + 1]\n"
                 "print(trajectory(steps))\nprint(collisions(steps))"),
    ),
    dict(
        key="sigma", module="noether",
        title="Solving the balance in one step",
        file="noether.py",
        method=("NoetherCurrents", "forced_sigma"),
        header="",
        prose=("The forward and backward currents balance where E·(1 − 2σ) = 0. That is linear in "
               "σ, so one Newton step reaches ½ from any real starting σ₀. The method is shown "
               "inside its class; it uses nothing else from the class."),
        example=("print(NoetherCurrents().forced_sigma(1000.0, sigma_0=-3.0))\n"
                 "print(NoetherCurrents().forced_sigma(0.5, sigma_0=7.0))"),
    ),
]


def strip_doc(node):
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        b = node.body
        if b and isinstance(b[0], ast.Expr) and isinstance(getattr(b[0], "value", None), ast.Constant) \
                and isinstance(b[0].value.value, str):
            node.body = b[1:] or [ast.Pass()]
    return node


def node_name(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        return n.name
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name):
        return n.targets[0].id
    if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
        return n.target.id
    return None


def segment(src, node):
    """Source of a top-level node with its docstrings removed, statements verbatim."""
    lines = src.split("\n")
    text = "\n".join(lines[node.lineno - 1:node.end_lineno])
    # remove docstrings textually: locate them via the AST of the segment
    seg = textwrap.dedent(text)
    tree = ast.parse(seg)
    cut = []
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.Module)):
            b = n.body
            if b and isinstance(b[0], ast.Expr) and isinstance(getattr(b[0], "value", None), ast.Constant) \
                    and isinstance(b[0].value.value, str):
                cut.append((b[0].lineno, b[0].end_lineno, len(n.body) == 1))
    sl = seg.split("\n")
    for a, b, only in sorted(cut, reverse=True):
        indent = len(sl[a - 1]) - len(sl[a - 1].lstrip())
        sl[a - 1:b] = ([" " * indent + "pass"] if only else [])
    return "\n".join(sl)


def build(spec):
    src = (ROOT / spec["file"]).read_text()
    tree = ast.parse(src)
    body = tree.body
    parts = []
    if "method" in spec:
        cls, meth = spec["method"]
        c = next(n for n in body if isinstance(n, ast.ClassDef) and n.name == cls)
        m = next(n for n in c.body if isinstance(n, ast.FunctionDef) and n.name == meth)
        parts.append(f"class {cls}:\n" + textwrap.indent(segment(src, m).rstrip("\n"), "    "))
        # the method's needs from the module's imports
        used = {x.id for x in ast.walk(m) if isinstance(x, ast.Name)}
        for n in body:
            if isinstance(n, ast.ImportFrom) or isinstance(n, ast.Import):
                names = {(a.asname or a.name.split(".")[0]) for a in n.names}
                if names & used:
                    parts.insert(0, ast.get_source_segment(src, n))
    else:
        if "span" in spec:
            a, z = spec["span"]
            idx = {node_name(n): i for i, n in enumerate(body) if node_name(n)}
            chosen = body[idx[a]: idx[z] + 1]
        else:
            chosen = [n for n in body if node_name(n) in spec["names"]]
        for extra in spec.get("extra", ()):
            chosen.append(next(n for n in body if node_name(n) == extra))
        for n in chosen:
            parts.append((segment(src, n).rstrip("\n"), isinstance(n, (ast.FunctionDef, ast.ClassDef))))
    if "method" in spec:
        parts = [(p, True) for p in parts]
    body_txt = ""
    for i, (txt, is_def) in enumerate(parts):
        if i:
            body_txt += "\n\n" if (is_def or prev_def) else "\n"
        body_txt += txt
        prev_def = is_def
    return spec["header"] + ("\n\n" if spec["header"] else "") + body_txt + "\n"


def run_cold(code, example):
    """Exec the listing in an empty namespace, then each example statement in turn.
    Returns the REPL transcript: '>>> stmt' followed by what that statement printed."""
    ns = {"__name__": "__listing__"}
    exec(compile(code, "<listing>", "exec"), ns)
    lines = []
    for node in ast.parse(example).body:
        stmt = ast.get_source_segment(example, node)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(compile(ast.Module([node], []), "<example>", "exec"), ns)
        lines.append(">>> " + stmt.replace("\n", "\n... "))
        if buf.getvalue():
            lines.append(buf.getvalue().rstrip("\n"))
    return "\n".join(lines)


def main():
    doc = ["Listings\n========\n\n",
           "Short mechanisms shown as complete code. Each listing is one self-contained "
           "unit: it is extracted from the named file by ``docs/gen_listings.py`` (docstrings "
           "removed, every statement otherwise verbatim), and the output shown is what it "
           "printed when executed cold in an empty namespace. A listing that stops running "
           "fails ``tests/test_listings.py``.\n\n"
           "Everything else is described by name and location in the :doc:`api/index`.\n\n"]
    for i, spec in enumerate(LISTINGS, 1):
        code = build(spec)
        out = run_cold(code, spec["example"])
        nlines = len(code.rstrip("\n").split("\n"))
        doc.append(f"Listing {i} — {spec['title']}\n" + "-" * (len(f"Listing {i} — {spec['title']}")) + "\n\n")
        doc.append(spec["prose"] + "\n\n")
        obj = ", ".join(spec.get("names", ()) + spec.get("extra", ())) or (
            f"{spec['method'][0]}.{spec['method'][1]}" if "method" in spec else "{} … {}".format(*spec["span"]))
        doc.append(f"*Source:* ``{spec['file']}`` (``{obj}``). *Extracted*, docstrings removed; "
                   f"{nlines} lines. Module: :mod:`ValaQuenta.modules.{spec['module']}.maths`.\n\n"
                   if "modules" in spec["file"] else
                   f"*Source:* ``{spec['file']}`` (``{obj}``). *Extracted*, docstrings removed; "
                   f"{nlines} lines. Module: :mod:`ValaQuenta.{spec['module']}`.\n\n")
        doc.append(".. code-block:: python\n\n" + textwrap.indent(code.rstrip("\n"), "   ") + "\n\n")
        doc.append("Run cold:\n\n.. code-block:: pycon\n\n" + textwrap.indent(out, "   ") + "\n\n")
    OUT.write_text("".join(doc))
    print("wrote", OUT.name, len(LISTINGS), "listings")


if __name__ == "__main__":
    main()
