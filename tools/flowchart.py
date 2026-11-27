#!/usr/bin/env python3
"""tools/flowchart.py -- the code flow chart of one ValaQuenta engine (or all), derived from the source by ``ast``.

The chart is drawn in the ISO 5807:1985 symbol set by ``tools/flowlib.py`` (the same drawer as the Monad / Harness charts in
VAPMIP/docs/flowcharts). Nothing is hand-drawn: every title is a name that exists in the code, and every arrow is a call found in the source.

    python3 tools/flowchart.py ENGINE            # one engine -> docs/flowcharts/ENGINE_flow.svg (+ .png via rsvg-convert)
    python3 tools/flowchart.py --all             # every engine under modules/ and every top-level engine file, then index.html
    python3 tools/flowchart.py --check           # fail if a chart is missing or older than its source

Symbols: oval = the registry class (entry/exit); rectangle = a public function of the engine; double-barred rectangle = a function
of another engine or of ``engine.constants`` that this engine calls; parallelogram = a registry call surface (``formulary``, ``run``,
``viewer_data``); cylinder = a data file the code opens. Lanes = the source files of the engine, left to right in call order.
"""
from __future__ import annotations

import ast
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flowlib import Chart  # noqa: E402

OUT = os.path.join(ROOT, "docs", "flowcharts")
DATA_RE = re.compile(r"""['"]([\w./-]+\.(?:json|bin|npy|npz|csv|txt|fits|ptorrent|pkl|db))['"]""")
MAX_NODES = 60


def engines():
    """Return ``{name: [source files]}`` for every package under modules/ and every top-level engine file."""
    out = {}
    mods = os.path.join(ROOT, "modules")
    for d in sorted(os.listdir(mods)):
        p = os.path.join(mods, d)
        if os.path.isdir(p) and not d.startswith("_"):
            fs = sorted(f for f in os.listdir(p) if f.endswith(".py") and f != "__init__.py")
            if fs:
                out[d] = [os.path.join(p, f) for f in fs]
    skip = {"__init__", "__main__"}
    for f in sorted(os.listdir(ROOT)):
        if f.endswith(".py") and f[:-3] not in skip and f[:-3] not in out and f[:-3] not in ("verify_install", "understand"):
            out[f[:-3]] = [os.path.join(ROOT, f)]
    return out


def first_line(node) -> str:
    """First sentence of a docstring, trimmed to what fits under a title."""
    doc = ast.get_docstring(node) or ""
    line = next((l.strip() for l in doc.splitlines() if l.strip() and not set(l.strip()) <= set("=-~`")), "")
    line = re.sub(r":\w+:`~?([^`]*)`", r"\1", line)
    line = re.sub(r"[`\\]", "", line)
    return (line[:62] + "…") if len(line) > 63 else line


def parse(name, files):
    """Return nodes (key -> dict), edges and external callees for one engine."""
    nodes, imports = {}, {}
    for f in files:
        tree = ast.parse(open(f, encoding="utf-8").read())
        fn = os.path.basename(f)
        for n in tree.body:
            if isinstance(n, ast.ImportFrom) and n.module is not None or isinstance(n, ast.ImportFrom):
                mod = ("." * n.level) + (n.module or "")
                for a in n.names:
                    imports[a.asname or a.name] = mod
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and not n.name.startswith("_"):
                nodes[f"{fn}:{n.name}"] = dict(file=fn, name=n.name, ast=n, cls=isinstance(n, ast.ClassDef))
    byname = {}
    for k, v in nodes.items():
        byname.setdefault(v["name"], []).append(k)
    edges, external, data = set(), {}, {}
    for k, v in nodes.items():
        for c in ast.walk(v["ast"]):
            if isinstance(c, ast.Call):
                t = c.func
                tgt = t.id if isinstance(t, ast.Name) else t.attr if isinstance(t, ast.Attribute) else None
                if tgt in byname:
                    cand = [x for x in byname[tgt] if x.startswith(v["file"] + ":")] or byname[tgt]
                    if cand[0] != k:
                        edges.add((k, cand[0]))
                elif isinstance(t, ast.Name) and t.id in imports and not imports[t.id].startswith(("typing", "math", "cmath", "fractions")) and not imports[t.id].endswith("engine.registry"):
                    external.setdefault(t.id, imports[t.id])
                    edges.add((k, "ext:" + t.id))
            if isinstance(c, ast.Name) and isinstance(c.ctx, ast.Load) and c.id in byname and v["cls"]:
                cand = [x for x in byname[c.id] if x.startswith(v["file"] + ":")] or byname[c.id]
                if cand[0] != k:
                    edges.add((k, cand[0]))
            if isinstance(c, ast.Constant) and isinstance(c.value, str):
                m = DATA_RE.fullmatch("'" + c.value + "'") if "/" not in c.value[:1] else None
                if m and len(c.value) < 80:
                    data.setdefault(c.value, set()).add(k)
    return nodes, edges, external, data


def build(name, files) -> Chart | None:
    """Lay the derived graph out as a Chart (lanes = files; rows = call depth)."""
    nodes, edges, external, data = parse(name, files)
    if not nodes:
        return None
    if len(nodes) > MAX_NODES:                            # keep the picture legible: the most-connected nodes first
        deg = {k: 0 for k in nodes}
        for a, b in edges:
            deg[a] = deg.get(a, 0) + 1
            if b in deg:
                deg[b] += 1
        keep = set(sorted(nodes, key=lambda k: (-deg[k], k))[:MAX_NODES])
        nodes = {k: v for k, v in nodes.items() if k in keep}
        edges = {(a, b) for a, b in edges if a in keep and (b in keep or b.startswith("ext:"))}
    callers = {k: [a for a, b in edges if b == k] for k in list(nodes) + ["ext:" + e for e in external]}
    has_cls = any(v["cls"] for v in nodes.values())
    depth = {}

    def d(k, seen=()):
        if k in depth:
            return depth[k]
        if k in seen:
            return 0
        cs = [c for c in callers.get(k, []) if c in nodes or c.startswith("ext:")]
        depth[k] = (0 if (k.startswith("ext:") or not has_cls or nodes[k]["cls"]) else 1) if not cs else 1 + max(d(c, seen + (k,)) for c in cs)
        return depth[k]

    for k in nodes:
        d(k)
    maxd = max(depth[k] for k in nodes)
    names = {0: "entry: registry class" if has_cls else "entry points"}
    lanes = [(names.get(k, f"level {k}"), "called by the level to its left" if k else "start of every call path") for k in range(maxd + 1)]
    ext_lane = len(lanes)
    if external:
        lanes.append(("other engines", "called from this engine"))
    if data:
        lanes.append(("stored data", "files the code opens"))
    lane_of = {"stored data": len(lanes) - 1}
    ch = Chart(f"{name}: code flow", f"derived from the source by ast · {len(nodes)} public names · arrows = calls (or references) found in the code · tools/flowchart.py",
               lanes, lane_w=300, row_h=84, top=104)
    ids = {}
    perlane = {}
    for k in sorted(nodes, key=lambda k: (depth[k], nodes[k]["file"] != "tools.py", nodes[k]["name"])):
        ln = depth[k]
        r = perlane.get(ln, 0); perlane[ln] = r + 1
        ids[k] = f"n{len(ids)}"
        stem = nodes[k]["file"][:-3]
        doc = first_line(nodes[k]["ast"])
        ch.node(ids[k], ln, r + 1, "term" if nodes[k]["cls"] else "proc", nodes[k]["name"], f"{stem} · {doc}" if doc else stem)
    er = 0
    for ename, mod in sorted(external.items()):
        ids["ext:" + ename] = f"x{er}"
        ch.node(ids["ext:" + ename], ext_lane, er + 1, "pre", ename, mod.replace("...", "ValaQuenta.").replace("..", "ValaQuenta.modules.").lstrip("."))
        er += 1
    if data:
        dl = lane_of["stored data"]
        for i, (dn, users) in enumerate(sorted(data.items())):
            ch.node(f"d{i}", dl, i + 1, "data", os.path.basename(dn), "read by " + ", ".join(sorted({nodes[u]["name"] for u in users if u in nodes}))[:60])
            for u in users:
                if u in ids:
                    ch.edge(ids[u], f"d{i}", "", "sidein", bend=(i % 4) * 4)
    for a, b in sorted(edges):
        if a in ids and b in ids:
            same = ch.nodes[ids[a]]["lane"] == ch.nodes[ids[b]]["lane"]
            gap = abs(ch.nodes[ids[a]]["row"] - ch.nodes[ids[b]]["row"])
            bend = (sum(map(ord, a + b)) % 5) * 4
            ch.edge(ids[a], ids[b], "", ("loopl" if gap > 1 else "auto") if same else "sidein", bend=bend)
    return ch


def write(name, ch: Chart) -> str:
    os.makedirs(OUT, exist_ok=True)
    svg = os.path.join(OUT, f"{name}_flow.svg")
    with open(svg, "w", encoding="utf-8") as fh:
        fh.write(ch.svg())
    subprocess.run(["rsvg-convert", "-o", svg[:-4] + ".png", svg], check=False)
    return svg


def index(done: dict) -> None:
    """Write docs/flowcharts/index.html listing every chart (same page style as VAPMIP/docs/flowcharts)."""
    rows = "\n".join(
        f'<section class="fig" id="{n}"><span class="imgno">{i}</span><h2><code>{n}</code></h2>'
        f'<p>{c} public names · <a href="{n}_flow.svg" target="_blank">SVG</a> · <a href="{n}_flow.png" target="_blank">PNG</a> · '
        f'<a href="../../wiki/{n}.md">wiki</a></p>'
        f'<div class="wrap"><img src="{n}_flow.svg" alt="Code flow chart of the {n} engine" loading="lazy"></div></section>'
        for i, (n, c) in enumerate(sorted(done.items()), 1))
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ValaQuenta Code Flow</title>
<style>
:root{{--bg:#f5f3ec;--fg:#16202c;--mut:#3a4656;--card:#fbfaf6;--line:#d6d1c3;--acc:#1f5fa8;--badge:#ffd34d;--badge-fg:#000}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#10151c;--fg:#e8edf3;--mut:#b9c3d0;--card:#18202a;--line:#33404f;--acc:#8ec0ff}}}}
*{{box-sizing:border-box}}html,body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif}}
header,main,footer{{max-width:1500px;margin:0 auto;padding:0 16px}}header{{padding-top:22px}}
h1{{margin:.1em 0 .2em;font-size:1.7rem}}p.lead{{color:var(--mut);max-width:75ch}}
.fig{{position:relative;background:var(--card);border:1px solid var(--line);border-radius:12px;margin:0 0 22px;padding:12px}}
.imgno{{position:absolute;top:10px;left:10px;background:var(--badge);color:var(--badge-fg);font-weight:800;border-radius:8px;padding:2px 10px}}
.fig h2{{margin:.1em 0 .1em 64px;font-size:1.15rem}}.fig p{{margin:.1em 0 .8em 64px;color:var(--mut);font-size:.95rem}}
.wrap{{overflow:auto;max-height:80vh;border:1px solid var(--line);border-radius:8px;background:#fbfaf6}}.wrap img{{display:block;height:auto;min-width:980px;width:100%}}
a{{color:var(--acc)}}code{{font-family:ui-monospace,monospace}}footer{{padding-bottom:40px;color:var(--mut);font-size:.92rem}}
</style></head><body><header><h1>ValaQuenta: code flow of every engine</h1>
<p class="lead">One chart per engine, derived from the source by <code>ast</code> (<code>tools/flowchart.py</code>); nothing is hand-drawn. Every title is a name that exists in the code and every arrow is a call found in it. Lanes are the engine's source files, left to right; the last lanes are other engines and stored data. A picture shows the machinery; it is not evidence that the mathematics is right.</p></header>
<main>{rows}</main>
<footer><p><b>How to read them.</b> ISO 5807:1985 symbols: oval = the registry class, rectangle = a public function, double-barred rectangle = a function of another engine, cylinder = a data file. Drawn with <code>tools/flowlib.py</code>; same style as the Monad and Harness charts in VAPMIP. Python conventions follow <a href="https://peps.python.org/pep-0008/">PEP 8</a>, <a href="https://peps.python.org/pep-0257/">PEP 257</a> and the <a href="https://docs.python.org/3/">Python documentation</a>.</p></footer>
</body></html>"""
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(html)


def main(argv):
    allE = engines()
    if argv and argv[0] == "--check":
        bad = [n for n, fs in allE.items() if not os.path.exists(os.path.join(OUT, f"{n}_flow.svg"))
               or os.path.getmtime(os.path.join(OUT, f"{n}_flow.svg")) < max(os.path.getmtime(f) for f in fs)]
        print("stale or missing:", ", ".join(bad) or "none")
        return 1 if bad else 0
    names = list(allE) if argv and argv[0] == "--all" else argv
    done = {}
    for n in names:
        ch = build(n, allE[n])
        if ch:
            write(n, ch)
            done[n] = len(ch.nodes)
            print(f"{n}: {len(ch.nodes)} nodes")
    if argv and argv[0] == "--all":
        index(done)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
