#!/usr/bin/env python3
"""
tools/repo_venv.py -- give a repository its own .venv, requirements.txt and INSTALL.md (Clean House step: environments).

Policy (author, 2026-08-15 and 2026-11-26): ValaQuenta/.venv is the root environment and holds every package any engine needs; each other repository
gets only what it needs to run its own code. The system python is broken (numpy 2.x in ~/.local shadows the apt numpy 1.x), so nothing here ever
uses it to import or install anything: it only calls `python3 -m venv`, then the venv's own pip.

    python3 tools/repo_venv.py REPO [REPO ...]         # dry run: list what each repository imports and what it has
    python3 tools/repo_venv.py REPO --apply            # create .venv if missing, write requirements.txt / INSTALL.md if missing, pip install
    python3 tools/repo_venv.py --survey                # one line per repository under ThePlace
    python3 tools/repo_venv.py REPO --refresh          # an existing .venv catches up with the root: new imports installed, ValaQuenta editable, INSTALL.md system block
    python3 tools/repo_venv.py --refresh --all         # every repository that has a .venv (run automatically after an addition to the root, tools/vq_venv_sync.py)

REPO is a directory name under ThePlace (or a path). What it does, in order:
  1. no .venv: `python3 -m venv .venv`; .venv is added to .gitignore.
  2. scans the repository's own .py files (not .venv, Archive, archive, _worktrees, build) for third-party imports, mapping import names to
     distribution names through the ROOT environment (ValaQuenta/.venv). A name the root environment lacks is reported as MISSING: by policy it
     is installed into the root first, then here.
  3. no requirements.txt: writes one (`name>=major.minor  # tested <root version>`); an existing requirements.txt is never overwritten.
  4. a repository that imports ValaQuenta gets `pip install -e <ThePlace>/ValaQuenta` (a source checkout; a PyPI package later).
  5. no INSTALL.md (or install doc): writes one (commands for Linux/macOS and Windows, the broken-system-python warning).
  6. pip installs requirements.txt into the repository's .venv.
"""
import ast
import os
import subprocess
import sys
import warnings

PLACE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOTPY = os.path.join(PLACE, "ValaQuenta", ".venv", "bin", "python")
SKIP = {".venv", "venv", "Archive", "archive", "_worktrees", "build", "__pycache__", ".git", "node_modules", "dist", "lambeq_env", "DataSets", "bins"}
LOCAL_OK = {"ValaQuenta"}


warnings.simplefilter('ignore')
_SIBLINGS = []


def sibling_names():
    """Module names defined anywhere in ThePlace (to 3 levels): sibling code reached through sys.path, not a pip package."""
    if not _SIBLINGS:
        names = set()
        for r in os.listdir(PLACE):
            top = os.path.join(PLACE, r)
            if os.path.isdir(top) and r not in SKIP:
                for dp, dn, fn in os.walk(top):
                    if dp[len(top):].count(os.sep) >= 3:
                        dn[:] = []
                        continue
                    dn[:] = [d for d in dn if d not in SKIP and not d.startswith('.')]
                    names.update(dn)
                    names.update(f[:-3] for f in fn if f.endswith('.py'))
        _SIBLINGS.append(names)
    return _SIBLINGS[0]


SYSTEM_TOOLS = {   # binary -> (regex found in the repository's source, what it is, apt package)
    "blender": (r"\bblender\b|\bbpy\b", "Blender (renders, headless `blender -b -P`)", "blender"),
    "ffmpeg": (r"\bffmpeg\b", "FFmpeg (audio/video)", "ffmpeg"),
    "convert": (r"\bconvert\b.*(png|jpg|svg|-resize|-crop)|ImageMagick|\bmagick\b", "ImageMagick (`convert`, `montage`)", "imagemagick"),
    "rsvg-convert": (r"rsvg-convert", "librsvg (`rsvg-convert`, SVG to PNG)", "librsvg2-bin"),
    "firefox": (r"\bfirefox\b", "Firefox (headless screenshots, viewing the galleries)", "firefox"),
    "espeak": (r"\bespeak\b", "eSpeak (speech)", "espeak"),
    "sox": (r"\bsox\b", "SoX (audio)", "sox"),
    "openscad": (r"\bopenscad\b", "OpenSCAD (3D models)", "openscad"),
    "pdftotext": (r"pdftotext|pdftoppm", "poppler-utils (PDF text and images)", "poppler-utils"),
    "pdflatex": (r"pdflatex|xelatex|latexmk", "TeX Live (papers)", "texlive-latex-extra"),
    "pandoc": (r"\bpandoc\b", "Pandoc", "pandoc"),
    "gcc": (r"\bgcc\b|\bmake\b", "a C compiler (gcc, make) for the C code", "build-essential"),
    "git": (r"\bgit\b", "git", "git"),
    "gh": (r"\bgh (api|run|pr|repo)\b", "GitHub CLI (`gh`)", "gh"),
    "curl": (r"\bcurl\b", "curl", "curl"),
    "jupyter": (r"nbconvert|jupyter|ipykernel", "Jupyter (installed in the .venv by pip; notebooks are executed with nbconvert)", None),
}
SYS_BEGIN, SYS_END = "<!-- system-software:begin -->", "<!-- system-software:end -->"


def system_block(repo):
    """The 'System software' section of INSTALL.md: every non-Python program the repository's own files call, with whether it is installed here."""
    import re
    import shutil
    text = []
    for dp, dn, fn in os.walk(repo):
        dn[:] = [d for d in dn if d not in SKIP and not d.startswith(".venv")]
        for f in fn:
            if f.endswith((".py", ".sh", ".md", ".c", ".h", ".toml", ".yml", ".yaml")) and f not in ("INSTALL.md",):
                try:
                    text.append(open(os.path.join(dp, f), encoding="utf-8", errors="replace").read(200000))
                except OSError:
                    pass
    blob = "\n".join(text)
    rows = []
    for b, (rx, what, apt) in SYSTEM_TOOLS.items():
        if re.search(rx, blob):
            have = shutil.which(b) is not None or b == "jupyter"
            rows.append(f"| {what} | `{b}` | {'installed' if have else '**not installed on the author machine**'} | {('`sudo apt install ' + apt + '`') if apt else 'pip (in the .venv)'} |")
    body = ("| software | command | here | install |\n|---|---|---|---|\n" + "\n".join(rows)) if rows else "None detected."
    return f"{SYS_BEGIN}\n## System software (not Python)\n\nPrograms this repository's own files call, found by scanning its source (`ValaQuenta/tools/repo_venv.py`). Install them with the system package manager; they are not pip packages.\n\n{body}\n{SYS_END}\n"


def write_system_block(repo):
    p = os.path.join(repo, "INSTALL.md")
    block = system_block(repo)
    cur = open(p).read() if os.path.exists(p) else f"# Installing {os.path.basename(os.path.abspath(repo))}\n\nSee the repository README. Use the `.venv`, never the system Python.\n\n"
    if SYS_BEGIN in cur:
        pre, rest = cur.split(SYS_BEGIN, 1)
        post = rest.split(SYS_END, 1)[1] if SYS_END in rest else ""
        new = pre + block + post.lstrip("\n")
    else:
        new = cur.rstrip("\n") + "\n\n" + block
    if new != cur:
        open(p, "w").write(new)
        return True
    return False


def refresh(repo_arg):
    """An existing .venv catches up with the root environment."""
    repo = repo_path(repo_arg)
    name = os.path.basename(os.path.abspath(repo))
    pip = os.path.join(repo, ".venv", "bin", "pip")
    if not os.path.exists(pip):
        return
    third, uses_vq = imports(repo)
    reqs, missing = requirements_text(third, root_dists())
    rp = os.path.join(repo, "requirements.txt")
    cur = open(rp).read() if os.path.exists(rp) else ""
    have = {l.split(">=")[0].split("==")[0].strip().lower() for l in cur.splitlines() if l.strip() and not l.startswith("#")}
    add = [l for l in reqs if l.split(">=")[0].strip().lower() not in have]
    if add:
        open(rp, "a").write(("" if cur.endswith("\n") or not cur else "\n") + "\n".join(add) + "\n")
        subprocess.run([pip, "install", "-q", "-r", rp], capture_output=True)
    if uses_vq:
        subprocess.run([pip, "install", "-q", "-e", os.path.join(PLACE, "ValaQuenta")], capture_output=True)
    changed = write_system_block(repo)
    print(f"{name}: refreshed ({len(add)} requirements added, ValaQuenta editable={uses_vq}, INSTALL.md system block {'updated' if changed else 'current'}; not in root: {missing})")


def repo_path(r):
    return r if os.path.isdir(r) else os.path.join(PLACE, r)


def py_files(repo):
    for dp, dn, fn in os.walk(repo):
        dn[:] = [d for d in dn if d not in SKIP and not d.startswith(".venv")]
        for f in fn:
            if f.endswith(".py"):
                yield os.path.join(dp, f)


def local_names(repo):
    names = set()
    for dp, dn, fn in os.walk(repo):
        dn[:] = [d for d in dn if d not in SKIP and not d.startswith(".venv")]
        names.update(d for d in dn)
        names.update(f[:-3] for f in fn if f.endswith(".py"))
    return names


def imports(repo):
    found, uses_vq = {}, False
    for f in py_files(repo):
        try:
            tree = ast.parse(open(f, encoding="utf-8", errors="replace").read())
        except (SyntaxError, ValueError):
            continue
        for n in ast.walk(tree):
            mods = [a.name for a in n.names] if isinstance(n, ast.Import) else [n.module] if isinstance(n, ast.ImportFrom) and n.module and n.level == 0 else []
            for m in mods:
                top = m.split(".")[0]
                found.setdefault(top, set()).add(os.path.relpath(f, repo))
                uses_vq |= top == "ValaQuenta"
    loc = local_names(repo)
    sib = sibling_names()
    third = {k: v for k, v in found.items() if k not in sys.stdlib_module_names and k not in loc and k not in LOCAL_OK and k != "__future__"}
    third = {k: v for k, v in third.items() if k not in sib or k in root_dists()}
    return third, uses_vq


_RD = []


def root_dists():
    if _RD:
        return _RD[0]
    """import name -> (distribution, version) in the root environment."""
    code = ("import importlib.metadata as m,json;pd=m.packages_distributions()\n"
            "pick=lambda k,v:next((d for d in v if d.lower().replace('-','_')==k.lower().replace('-','_')),v[0])\n"
            "print(json.dumps({k:[pick(k,v),m.version(pick(k,v))] for k,v in pd.items()}))")
    out = subprocess.run([ROOTPY, "-c", code], capture_output=True, text=True)
    import json
    _RD.append(json.loads(out.stdout) if out.returncode == 0 else {})
    return _RD[0]


def requirements_text(third, rd):
    lines, missing = [], []
    for name in sorted(third):
        if name in rd:
            d, v = rd[name]
            mm = ".".join(v.split(".")[:2])
            lines.append(f"{d}>={mm}  # tested {v}")
        else:
            missing.append(name)
    return sorted(set(lines)), missing


INSTALL = """# Installing {name}

{name} runs inside its own virtual environment. **Do not use the system Python**: on the author's machine it has numpy 2.x in `~/.local` shadowing the
apt numpy 1.x, so scientific imports crash. Everything below uses the `.venv`.

Linux / macOS:

```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
{vq}```

Windows (PowerShell):

```powershell
py -3 -m venv .venv
.venv\\Scripts\\pip install -r requirements.txt
{vqw}```

Check: `.venv/bin/python -c "import sys; print(sys.prefix)"` prints a path ending in `.venv`.

`requirements.txt` lists what this repository's own code imports, with the version tested in the root environment (`ValaQuenta/.venv`, which holds every
package any engine needs). If an import is reported missing, install it in `ValaQuenta/.venv` first (`ValaQuenta/tools/vq_venv_sync.py`), then here.
"""


def run(repo_arg, apply):
    repo = repo_path(repo_arg)
    name = os.path.basename(os.path.abspath(repo))
    third, uses_vq = imports(repo)
    rd = root_dists()
    reqs, missing = requirements_text(third, rd)
    has_venv = os.path.exists(os.path.join(repo, ".venv", "bin", "python"))
    has_req = os.path.exists(os.path.join(repo, "requirements.txt"))
    has_inst = any(f.lower().startswith("install") for f in os.listdir(repo))
    print(f"{name}: venv={'yes' if has_venv else 'NO'} requirements={'yes' if has_req else 'NO'} install-doc={'yes' if has_inst else 'NO'} "
          f"uses-ValaQuenta={uses_vq} third-party={len(third)} missing-from-root={missing}")
    if not apply:
        return
    if not has_venv:
        subprocess.run(["python3", "-m", "venv", os.path.join(repo, ".venv")], check=True)
        gi = os.path.join(repo, ".gitignore")
        cur = open(gi).read() if os.path.exists(gi) else ""
        if ".venv" not in cur:
            open(gi, "a").write(("\n" if cur and not cur.endswith("\n") else "") + ".venv/\n")
        print("  created .venv")
    if not has_req:
        open(os.path.join(repo, "requirements.txt"), "w").write(f"# {name}: what this repository's own code imports (tools/repo_venv.py, root environment versions)\n" + "\n".join(reqs) + "\n")
        print(f"  wrote requirements.txt ({len(reqs)} packages)")
    if not has_inst:
        vq = "# this repository imports ValaQuenta (the code root):\n.venv/bin/pip install -e ../ValaQuenta\n" if uses_vq else ""
        vqw = "# this repository imports ValaQuenta (the code root):\n.venv\\Scripts\\pip install -e ..\\ValaQuenta\n" if uses_vq else ""
        open(os.path.join(repo, "INSTALL.md"), "w").write(INSTALL.format(name=name, vq=vq, vqw=vqw))
        print("  wrote INSTALL.md")
    write_system_block(repo) if apply else None
    pip = os.path.join(repo, ".venv", "bin", "pip")
    if not has_venv or not has_req:
        subprocess.run([pip, "install", "-q", "--upgrade", "pip"], check=False)
        r = subprocess.run([pip, "install", "-q", "-r", os.path.join(repo, "requirements.txt")], capture_output=True, text=True)
        print("  pip install -r requirements.txt:", "ok" if r.returncode == 0 else "FAILED\n" + r.stderr[-600:])
    if uses_vq:
        r = subprocess.run([pip, "install", "-q", "-e", os.path.join(PLACE, "ValaQuenta")], capture_output=True, text=True)
        print("  pip install -e ValaQuenta:", "ok" if r.returncode == 0 else "FAILED\n" + r.stderr[-600:])


def main(argv):
    apply = "--apply" in argv
    if "--refresh" in argv:
        rs = [d for d in sorted(os.listdir(PLACE)) if os.path.exists(os.path.join(PLACE, d, ".venv", "bin", "pip"))] if "--all" in argv else [a for a in argv if not a.startswith("--")]
        for r in rs:
            refresh(r)
        return
    repos = [a for a in argv if not a.startswith("--")]
    if "--survey" in argv:
        repos = sorted(d for d in os.listdir(PLACE) if os.path.isdir(os.path.join(PLACE, d, ".git")))
    for r in repos:
        run(r, apply)


if __name__ == "__main__":
    main(sys.argv[1:])
