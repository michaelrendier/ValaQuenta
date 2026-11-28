#!/usr/bin/env python3
"""build_data.py -- bakes ass_data.js for the add_scale_sign gallery from the Python engine (add_scale_sign 0.3), so every page compares its own
JavaScript with the engine's numbers.  Run:  python3 gallery/add_scale_sign/build_data.py   (from the repo root, .venv)"""
import json
import math
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..")))
from ValaQuenta.modules.add_scale_sign import ASS, compose, group_laws_exact

els = [ASS(Fr(a), Fr(s), g) for a in (-2, 0, Fr(3, 2)) for s in (Fr(1, 2), 1, 3) for g in (-1, 1)]
key = lambda e: (e.add, e.scale, e.sign)
idx = {key(e): i for i, e in enumerate(els)}
commute = [[int(key(x @ y) == key(y @ x)) for y in els] for x in els]
closure = [[int(key(x @ y) in idx) for y in els] for x in els]
prod_add = [[str((x @ y).add) for y in els] for x in els]
centre = [i for i, x in enumerate(els) if all(key(x @ y) == key(y @ x) for y in els)]

samples = []
for a in (-2.0, 0.0, 0.5, 3.0):
    for s in (0.25, 1.0, 2.0, 7.5):
        for g in (-1, 1):
            e = ASS(a, s, g)
            sm = e.to_smith()
            samples.append({"a": a, "s": s, "g": g, "u": e.u(), "gamma": e.gamma(), "g_scale": sm["Γ_SCALE"], "g_add": sm["Γ_ADD"],
                            "quadrant": sm["quadrant"], "defect": e.lineage().firing_defect()})

brackets = []
for a in (3.0, -1.5, 0.5):
    for s in (0.5, 2.0, 5.0):
        A, S, G = ASS.ADD(a), ASS.SCALE(s), ASS.SIGN(-1)
        cm = lambda x, y: ~x @ ~y @ x @ y
        brackets.append({"a": a, "s": s, "AS": list(key(cm(A, S))), "AG": list(key(cm(A, G))), "SG": list(key(cm(S, G)))})

words = {
    "ADD(+1) then ADD(−1)": [(1.0, 1.0, 1), (-1.0, 1.0, 1)],
    "SCALE(8), ADD(2), SIGN(−1)/SCALE(½)": [(0.0, 8.0, 1), (2.0, 1.0, 1), (0.0, 0.5, -1)],
    "ADD(2), SCALE(2), ADD(−2), SCALE(½)": [(2.0, 1.0, 1), (0.0, 2.0, 1), (-2.0, 1.0, 1), (0.0, 0.5, 1)],
    "SIGN(−1), SIGN(−1)": [(0.0, 1.0, -1), (0.0, 1.0, -1)],
}
wd = {}
for name, st in words.items():
    T = compose(*[ASS(a, s, g) for a, s, g in st])
    out = {"steps": st, "element": list(key(T))}
    for order in ("chrono", "zeta"):
        w = T.lineage(order)
        out[order] = {"order_steps": [list(key(x)) for x in w.steps], "trajectory": list(w.trajectory(1.0)),
                      "collisions": [[a, b, p] for a, b, p in w.collisions(1.0)], "u_total": w.u_total(),
                      "u_sum_of_steps": w.u_sum_of_steps(), "firing_defect": w.firing_defect(),
                      "would_collide": {c: w.would_collide(ASS.ADD(float(c))) for c in (-1, 0, 1, 2)}}
    wd[name] = out

data = {"grid": {"elements": [[str(e.add), str(e.scale), e.sign] for e in els], "commute": commute, "closure": closure, "prod_add": prod_add,
                 "centre": centre, "commuting_pairs": sum(map(sum, commute)), "closed_pairs": sum(map(sum, closure))},
        "laws": group_laws_exact(), "samples": samples, "brackets": brackets, "words": wd}
out = os.path.join(HERE, "ass_data.js")
open(out, "w", encoding="utf-8").write("window.ASSDATA=" + json.dumps(data, separators=(",", ":")) + ";\n")
print("ass_data.js", os.path.getsize(out), "bytes; commuting pairs", data["grid"]["commuting_pairs"], "of 324; closed", data["grid"]["closed_pairs"], "centre", centre, data["laws"])
