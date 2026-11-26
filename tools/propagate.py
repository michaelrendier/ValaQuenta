"""
tools/propagate.py -- ValaQuenta is the code root: a change made here is carried to every place the code is used.

    python3 tools/propagate.py ENGINE [ENGINE ...]          # dry run: list downstream files that use the engine and are out of date
    python3 tools/propagate.py ENGINE --apply               # carry the standard d* block into those files (working tree only)
    python3 tools/propagate.py --changed [--apply]          # engines touched by the last ValaQuenta commit (used by the post-commit hook)

What "uses an engine" means: a file outside ValaQuenta that imports it (`ValaQuenta.modules.X`, `modules/X`, `modules.X.maths|tools`),
or a top-level ValaQuenta engine file (`ValaQuenta.zero_lattice`, ...). What "out of date" means today: the file uses d* in any form and
lacks the four-faces block (tools/dstar_block.py); symbol/name drift is reported, not rewritten (it needs reading, engine by engine).

Safety: only .py and .md files are edited, only in the working tree, never committed or pushed from here; a file with
uncommitted changes is skipped and reported; every action is appended to PROPAGATION_LEDGER.md in the ValaQuenta root.
Skipped: _worktrees, archive/Archive, virtualenvs, Build, ContextPlease (it archives, it does not run the code).
"""
import datetime
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACE = os.path.dirname(ROOT)
sys.path.insert(0, ROOT)
import dstar_block as DB  # noqa: E402  (tools/dstar_block.py)

SKIP_DIRS = {"_worktrees", "archive", "Archive", "Build", "ContextPlease", "lambeq_env", "__pycache__", ".git",
             "node_modules", ".venv", "venv", "ValaQuenta", "DataSets", "bins", "Pictures", "Music", "zips-11-21-26"}
EXTS = (".py", ".md")
LEDGER = os.path.join(ROOT, "PROPAGATION_LEDGER.md")


def pattern(engine):
    e = re.escape(engine)
    return re.compile(r"ValaQuenta[./]modules[./]%s\b|modules[./]%s[./](?:maths|tools)\b|ValaQuenta[./]%s\b" % (e, e, e))


def downstream_files():
    for repo in sorted(os.listdir(PLACE)):
        top = os.path.join(PLACE, repo)
        if repo in SKIP_DIRS or not os.path.isdir(top):
            continue
        for dp, dn, fn in os.walk(top):
            dn[:] = [d for d in dn if d not in SKIP_DIRS and not d.startswith(".venv")]
            for f in fn:
                if f.endswith(EXTS):
                    yield os.path.join(dp, f)


def dirty(path):
    """True if the file has uncommitted changes in its own git repo (or is untracked)."""
    d = os.path.dirname(path)
    r = subprocess.run(["git", "-C", d, "status", "--porcelain", "--", path], capture_output=True, text=True)
    return r.returncode == 0 and bool(r.stdout.strip())


def in_repo(path):
    r = subprocess.run(["git", "-C", os.path.dirname(path), "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True)
    return r.returncode == 0


def scan(engine):
    pat = pattern(engine)
    out = []
    for p in downstream_files():
        try:
            t = open(p, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if pat.search(t):
            out.append((p, bool(DB.USES.search(t)), DB.MARK in t))
    return out


def log(lines):
    new = not os.path.exists(LEDGER)
    with open(LEDGER, "a", encoding="utf-8") as f:
        if new:
            f.write("# Propagation ledger\n\nEvery downstream file ValaQuenta's tools changed or skipped. Working tree only; nothing committed from here.\n\n")
        f.write("\n".join(lines) + "\n")


def run(engines, apply):
    stamp = datetime.date.today().isoformat()
    ledger = []
    for eng in engines:
        rows = scan(eng)
        todo = [r for r in rows if r[1] and not r[2]]
        print(f"[{eng}] {len(rows)} downstream files use it; {len(todo)} use d* without the four-faces block")
        for p, uses, has in todo:
            rel = os.path.relpath(p, PLACE)
            if not apply:
                print("   needs   " + rel)
                continue
            if not in_repo(p) or dirty(p):
                print("   SKIPPED (uncommitted changes or not in a repo) " + rel)
                ledger.append(f"- {stamp} `{eng}` SKIPPED {rel} (uncommitted changes)")
                continue
            t = open(p, encoding="utf-8").read()
            open(p, "w", encoding="utf-8").write(DB.insert_py(t) if p.endswith(".py") else DB.insert_md(t))
            print("   applied " + rel)
            ledger.append(f"- {stamp} `{eng}` d*-block applied to {rel}")
    if apply and ledger:
        log(ledger)


def changed_engines():
    r = subprocess.run(["git", "-C", ROOT, "diff", "--name-only", "HEAD~1", "HEAD"], capture_output=True, text=True)
    names = set()
    for ln in r.stdout.splitlines():
        m = re.match(r"modules/([^/]+)/", ln) or re.match(r"([A-Za-z_]+)\.py$", ln)
        if m:
            names.add(m.group(1))
    return sorted(names)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    engines = changed_engines() if "--changed" in sys.argv else args
    run(engines, "--apply" in sys.argv)
