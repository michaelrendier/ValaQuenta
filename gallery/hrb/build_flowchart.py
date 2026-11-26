"""
gallery/hrb/build_flowchart.py -- the code flow chart of the h_rb_hat engine, derived from the source by `ast` (no hand-drawn edges).

Nodes: every top-level function of maths.py, oblique_sigma_rb.py and sigma16.py, and the class SigmaRBModule of tools.py.
Edges: a call from one node to another node of the engine, or to engine.constants. Writes svg_flowchart_h_rb_hat.html.

d* faces (all four are needed to chart ln(10) in Universal Native Space):
  d*         = 0.24600          the value the code runs with (Boundary, σ_ζ=½ plane)
  d*_taut    = 0.246307201473  A_π/ln10, the Flow (radial unit)
  d*_RG      = dimension 8; numeric OPEN, no closed form  the Stability (centre r=0)
  d*_ln(10)  = 0.5671432904   d*_taut·ln10 = A_π, the Translator (log bridge)
Full story of d*: Ainulindale/wiki/17_alpha_omega_d_star.md; ~/.clauderc_canonical_maths @RCCM_FOUR_DSTAR; FourthAgePapers/DStarRG
"""
import ast
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.join(HERE, "..", "..", "modules", "h_rb_hat")
FILES = [("maths.py", "maths.py — the scalar operator"), ("oblique_sigma_rb.py", "oblique_sigma_rb.py — the documented sigma_rb map"),
         ("sigma16.py", "sigma16.py — exploratory lifts"), ("tools.py", "tools.py — registry face")]
nodes, calls = {}, []
for fn, _ in FILES:
    tree = ast.parse(open(os.path.join(MOD, fn), encoding="utf-8").read())
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and not n.name.startswith("_"):
            nodes[f"{fn}:{n.name}"] = (fn, n.name, n)
        elif isinstance(n, ast.ClassDef):
            nodes[f"{fn}:{n.name}"] = (fn, n.name, n)
byname = {}
for k, (fn, name, _) in nodes.items():
    byname.setdefault(name, []).append(k)
edges, usesC = set(), set()
for k, (fn, name, node) in nodes.items():
    for c in ast.walk(node):
        if isinstance(c, ast.Call):
            f = c.func
            tgt = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None
            if tgt in byname:
                cand = [x for x in byname[tgt] if x.startswith(fn)] or byname[tgt]
                if cand[0] != k:
                    edges.add((k, cand[0]))
        if isinstance(c, ast.Attribute) and isinstance(c.value, ast.Name) and c.value.id in ("_C", "C"):
            usesC.add((k, c.attr))
# layering: depth = longest path from a node with no callers (calls go left -> right)
callees = {k: [b for a, b in edges if a == k] for k in nodes}
callers = {k: [a for a, b in edges if b == k] for k in nodes}
depth = {}
def d(k, seen=()):
    if k in depth: return depth[k]
    if k in seen: return 0
    depth[k] = 0 if not callers[k] else 1 + max(d(c, seen + (k,)) for c in callers[k])
    return depth[k]
for k in nodes: d(k)
colw, rowh, W0 = 215, 30, 40
cols = {}
for fn, _ in FILES:
    ks = sorted([k for k in nodes if k.startswith(fn)], key=lambda k: (depth[k], k))
    cols[fn] = ks
pos, y = {}, 70
panel = {}
for fn, title in FILES:
    maxd = max((depth[k] for k in cols[fn]), default=0)
    x0 = 30
    rows = {}
    for k in cols[fn]:
        rows.setdefault(depth[k], []).append(k)
    ypanel = y
    yy = y + 34
    for dd in sorted(rows):
        for i, k in enumerate(rows[dd]):
            pos[k] = (x0 + dd * colw, yy + i * rowh)
        yy += 0
    height = max(len(v) for v in rows.values()) * rowh if rows else rowh
    # stack rows of the same depth vertically within the panel; panel height = tallest column
    panel[fn] = (ypanel, height + 50, title)
    y += height + 90
W = 30 + (max(depth.values()) + 1) * colw + 200
H = y + 50
svg = [f'<svg viewBox="0 0 {W} {H}" style="width:100%;font:12px system-ui">',
       '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--mut)"/></marker></defs>']
for fn, (yp, hp, title) in panel.items():
    svg.append(f'<rect x="10" y="{yp}" width="{W-20}" height="{hp}" rx="12" fill="none" stroke="var(--line)"/><text x="24" y="{yp+22}" fill="var(--fg)" font-weight="700" font-size="14">{html.escape(title)}</text>')
for a, b in sorted(edges):
    (xa, ya), (xb, yb) = pos[a], pos[b]
    x1, y1, x2, y2 = xa + 190, ya + 11, xb, yb + 11
    if xb <= xa:  # same-column or back edge
        x1, x2 = xa + 190, xb + 190
        svg.append(f'<path d="M{x1} {y1} C {x1+40} {y1}, {x2+40} {y2}, {x2} {y2}" fill="none" stroke="var(--c2)" stroke-opacity=".55" marker-end="url(#ar)"/>')
    else:
        mx = (x1 + x2) / 2
        svg.append(f'<path d="M{x1} {y1} C {mx} {y1}, {mx} {y2}, {x2} {y2}" fill="none" stroke="var(--mut)" stroke-opacity=".6" marker-end="url(#ar)"/>')
for k, (x, yv) in pos.items():
    fn, name, node = nodes[k]
    cls = isinstance(node, ast.ClassDef)
    colour = {"maths.py": "--c1", "oblique_sigma_rb.py": "--c3", "sigma16.py": "--c4", "tools.py": "--c5"}[fn]
    uses = [a for (kk, a) in usesC if kk == k]
    label = name + (" ★" if uses else "")
    svg.append(f'<g><title>{html.escape(k)}{" uses engine.constants." + ", ".join(sorted(uses)) if uses else ""}</title><rect x="{x}" y="{yv}" width="190" height="22" rx="6" fill="var(--card)" stroke="var(--{colour[2:]})" stroke-width="{2.5 if cls else 1.5}"/><text x="{x+8}" y="{yv+15}" fill="var(--fg)">{html.escape(label)}</text></g>')
svg.append("</svg>")
nodes_n, edges_n = len(nodes), len(edges)
CSS = open(os.path.join(HERE, "build_gallery.py"), encoding="utf-8").read().split('CSS = """')[1].split('"""')[0]
import importlib.util
spec = importlib.util.spec_from_file_location("bg_consts", os.path.join(HERE, "build_gallery.py"))
src = open(os.path.join(HERE, "build_gallery.py"), encoding="utf-8").read()
CONTACT = src.split("CONTACT = (")[1].split(")\nFOOT")[0]
CONTACT = eval("(" + CONTACT + ")")
FOOT = eval("(" + src.split("FOOT = (")[1].split(")\nDSTAR")[0] + ")")
DSTAR = src.split('DSTAR = """')[1].split('"""')[0]
GH = "https://github.com/michaelrendier/ValaQuenta/blob/main/modules/h_rb_hat/"
body = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>h_rb_hat code flow chart</title>
<link rel="icon" type="image/png" href="favicon.png"><style>{CSS}</style></head><body>{CONTACT}
<header><div class="nav"><a href="index.html">← H_RB gallery</a><button onclick="hrbTheme('dark')">dark</button> <button onclick="hrbTheme('light')">light</button></div>
<h1>Code flow chart: the h_rb_hat engine</h1>
<p class="lead">{nodes_n} functions and classes, {edges_n} call edges, read from the source with <code>ast</code> (no hand-drawn edges). An arrow runs from caller to callee; orange curves are calls inside one column. ★ marks a node that reads <code>engine.constants</code> (hover for the names). Blue: <a href="{GH}maths.py">maths.py</a>; green: <a href="{GH}oblique_sigma_rb.py">oblique_sigma_rb.py</a> (the documented sigma_rb map); purple: <a href="{GH}sigma16.py">sigma16.py</a> (exploratory); gold: <a href="{GH}tools.py">tools.py</a>.</p></header>
<main><div class="fig"><span class="imgno">FC1</span>{''.join(svg)}</div>
<p class="note">Reading: in <code>maths.py</code> the scalar chain is geometric_coupling and the two energies → sigma_rb_term → sigma_rb_evaluate, with the six facet functions and the precession/crank/trine equations beside it. In <code>oblique_sigma_rb.py</code> the documented map is sigma_rb_map → tilt_axis; p_red_blue → sigma_self; rot_pair → balance_angle → balanced; run_train closes the gear flow. <code>tools.py</code> exposes the formulary to the registry.</p>
<h2>Sources</h2><ul class="note"><li><a href="{GH}maths.py">maths.py</a>, <a href="{GH}oblique_sigma_rb.py">oblique_sigma_rb.py</a>, <a href="{GH}sigma16.py">sigma16.py</a>, <a href="{GH}tools.py">tools.py</a>; <a href="https://github.com/michaelrendier/ValaQuenta/blob/main/gallery/hrb/build_flowchart.py">gallery/hrb/build_flowchart.py</a> (the generator)</li></ul>{DSTAR}</main>{FOOT}
<script>window.hrbTheme=function(t){{document.documentElement.setAttribute('data-theme',t);}};</script></body></html>"""
open(os.path.join(HERE, "svg_flowchart_h_rb_hat.html"), "w", encoding="utf-8").write(body)
print(nodes_n, "nodes,", edges_n, "edges")
