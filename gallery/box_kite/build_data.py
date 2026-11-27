#!/usr/bin/env python3
"""build_data.py -- bakes bk_data.js for the box_kite gallery from the Python engine (box_kite 0.3), so every page compares its own JavaScript
with the engine's numbers.  Run:  python3 gallery/box_kite/build_data.py   (from the repo root, .venv)"""
import json, os, sys
from itertools import permutations
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..")))
from ValaQuenta.modules.box_kite import maths as bk

tab, dim = bk.cd_multiplication_table(4)
table = [[tab[(i, j)][0], tab[(i, j)][1]] for i in range(16) for j in range(16)]
kites = bk.box_kites()
struts = {}
for s in range(1, 8):
    g = bk.box_kite_graph(s)
    struts[str(s)] = {"vertices": [list(v) for v in g["vertices"]], "edges": [list(e) for e in g["edges"]],
                      "non_edges": [list(e) for e in g["non_edges"]], "spectrum": [round(x, 9) for x in bk.chart_spectrum(s)]}
zd = [[d1[0], d1[1], d1[2], d2[0], d2[1], d2[2]] for d1, d2 in bk.zero_divisor_pairs()]
defect = [round(bk.associator_defect(i, j, k), 9) for i in range(16) for j in range(16) for k in range(16)]
census = bk.associator_census()
lines = [list(l) for l in bk.pg32_lines()]
planes = [list(p) for p in bk.fano_planes()]
olines = [list(l) for l in bk._octonion_lines()]
# the Fano permutations, found independently of labelled_automorphisms (lines as sets), and their cycle types
L = {tuple(sorted(l)) for l in olines}
perms = []
for p in permutations(range(1, 8)):
    f = {i + 1: p[i] for i in range(7)}
    if all(tuple(sorted((f[a], f[b], f[c]))) in L for a, b, c in L):
        perms.append([f[i] for i in range(1, 8)])


def cyc(p):
    seen, out = set(), []
    for s in range(1, 8):
        if s in seen:
            continue
        n, x = 0, s
        while x not in seen:
            seen.add(x)
            x = p[x - 1]
            n += 1
        out.append(n)
    return "".join(str(n) for n in sorted(out, reverse=True))


types = {}
for p in perms:
    types[cyc(p)] = types.get(cyc(p), 0) + 1
gg = bk.glued_graph()


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    return o


data = {
    "table": table, "assessors": [list(a) for a in bk.assessors()], "kites": clean(kites),
    "struts": struts, "zd_pairs": zd, "defect": defect, "census": census, "counts": clean(bk.verify_counts()),
    "pg_points": bk.pg32_points(), "pg_lines": lines, "pg_planes": planes, "octonion_lines": olines,
    "aut": clean(bk.labelled_automorphisms()), "split": clean(bk.labelled_group_is_split()), "perms": perms, "cycle_types": types,
    "glued": {"n_vertices": gg["n_vertices"], "n_edges": gg["n_edges"], "cross_strut_edges": gg["cross_strut_edges"],
              "within_strut_edges": gg["within_strut_edges"], "spectrum": [round(x, 6) for x in bk.glued_spectrum()]},
}
out = os.path.join(HERE, "bk_data.js")
open(out, "w", encoding="utf-8").write("window.BKDATA=" + json.dumps(clean(data), separators=(",", ":")) + ";\n")
print("bk_data.js", os.path.getsize(out), "bytes; perms", len(perms), types, "census", census, "counts", data["counts"])
