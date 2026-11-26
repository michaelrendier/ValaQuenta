"""
tools/dstar_block.py -- put the standard "four faces of d*" block into every file that uses d* in any form.

Rule (author, 2026-11-25): d* is the value the code runs with; every file that uses d* in any form carries the full
list of the four values and a pointer to the full story. This tool audits and applies that rule for one engine.

    python3 tools/dstar_block.py ENGINE            # audit: list files that use d* and lack the block
    python3 tools/dstar_block.py ENGINE --apply    # insert the block (.py after the module docstring, .md as a blockquote)
    python3 tools/dstar_block.py --all             # audit every engine

ENGINE is a directory name under modules/ or a top-level file stem (e.g. zero_lattice). .ipynb files are reported, not edited.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(ROOT))
from ValaQuenta.engine import constants as C  # noqa: E402

USES = re.compile(r"D_STAR|d\*|d\^\*|d_star|DSTAR|Ω_ζΣ|Ω_RZ", re.IGNORECASE)
MARK = "d* faces (all four"


def engine_files(name):
    d = os.path.join(ROOT, "modules", name)
    out = []
    if os.path.isdir(d):
        for dp, dn, fn in os.walk(d):
            dn[:] = [x for x in dn if x != "__pycache__"]
            out += [os.path.join(dp, f) for f in fn if f.endswith((".py", ".md", ".ipynb"))]
    for cand in (name + ".py",):
        p = os.path.join(ROOT, cand)
        if os.path.isfile(p):
            out.append(p)
    wiki = os.path.join(ROOT, "wiki", name + ".md")
    tb = [os.path.join(ROOT, "wiki", "toolbox", f) for f in os.listdir(os.path.join(ROOT, "wiki", "toolbox"))
          if f.endswith("_" + name + ".md")]
    if os.path.isfile(wiki):
        out.append(wiki)
    return out + tb


def needs(path):
    t = open(path, encoding="utf-8", errors="ignore").read()
    return bool(USES.search(t)) and MARK not in t


def insert_py(t):
    block = C.dstar_comment_block("# ")
    m = re.match(r'(\s*(?:#[^\n]*\n)*)(\s*[rbRB]?("""|\'\'\').*?\3\s*\n)', t, re.S)
    if m:
        return t[: m.end()] + "\n" + block + "\n" + t[m.end():]
    return block + "\n\n" + t


def insert_md(t):
    quote = "\n".join("> " + ln + "  " for ln in C.dstar_comment_block("").splitlines())
    lines = t.split("\n")
    i = next((k for k, ln in enumerate(lines) if ln.startswith("# ")), -1)
    return "\n".join(lines[: i + 1] + ["", quote, ""] + lines[i + 1:]) if i >= 0 else quote + "\n\n" + t


def run(name, apply):
    hits = []
    for p in engine_files(name):
        if not needs(p):
            continue
        hits.append(os.path.relpath(p, ROOT))
        if apply and p.endswith((".py", ".md")):
            t = open(p, encoding="utf-8").read()
            open(p, "w", encoding="utf-8").write(insert_py(t) if p.endswith(".py") else insert_md(t))
    return hits


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply = "--apply" in sys.argv
    names = (sorted(n for n in os.listdir(os.path.join(ROOT, "modules")) if not n.startswith("__")
                    and os.path.isdir(os.path.join(ROOT, "modules", n))) if "--all" in sys.argv else args)
    for n in names:
        for h in run(n, apply):
            print(("applied " if apply and not h.endswith(".ipynb") else "needs   ") + h)
