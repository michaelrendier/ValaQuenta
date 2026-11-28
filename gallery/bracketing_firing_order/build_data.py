#!/usr/bin/env python3
"""build_data.py -- bakes bf_data.js for the bracketing_firing_order gallery from the Python engine (0.2), so every page compares its own
JavaScript with the engine's numbers.  Run:  python3 gallery/bracketing_firing_order/build_data.py   (from the repo root, .venv)"""
import json
import os
import random
import sys
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..")))
from ValaQuenta.modules.bracketing_firing_order import maths as bf
from ValaQuenta.modules.h_rb_hat import sigma16

A = (1, 2, 0, 1, 0, 0, 3, 0, 0, 1, 0, 0, 2, 0, 0, 1)
B = (0, 1, 1, 0, 2, 0, 0, 1, 0, 0, 1, 0, 0, 0, -1, 0)
C = (2, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 2)
D4 = (1, 0, -1, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 1, -1)
X = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0)
ints = lambda v: [int(x) for x in v]

rng = random.Random(11)
mul_tests = []
for _ in range(6):
    a = [rng.randint(-3, 3) for _ in range(16)]
    b = [rng.randint(-3, 3) for _ in range(16)]
    mul_tests.append([a, b, ints(bf.sedenion_mul(a, b))])

plans = {}
for n, vecs in ((3, (A, B, C)), (4, (A, B, C, D4))):
    leaves = [bf.Leaf.of(chr(65 + i), v) for i, v in enumerate(vecs)]
    entry = {}
    for mode, make in (("A", bf.plans_bracketing), ("B", bf.plans_firing_order), ("C", bf.plans_firing_of_brackets), ("D", bf.plans_bracketing_of_firing)):
        ps = make(leaves)
        entry[mode] = {"notation": [bf.notation(p) for p in ps], "fire": [bf.fire_sequence(p) for p in ps],
                       "op": [ints(bf.apply_plan(p, X)) for p in ps], "val": [ints(bf.plan_value(p)) for p in ps]}
    plans[str(n)] = entry

L3 = {c: bf.Leaf.of(c, v) for c, v in zip("ABC", (A, B, C))}
plan = bf.parse_plan("((A B | 2 1) C | 2 1)", L3)
evolve = {"plan": bf.notation(plan), "op": [[s[0], ints(s[1])] for s in bf.evolve_operator(plan, X)],
          "val": [[s[0], ints(s[1])] for s in bf.evolve_value(plan)]}

counts = {str(n): {k: str(v) for k, v in bf.mode_counts(n).items()} for n in range(1, 17)}
bell = {str(n): str(bf.bell_number(n)) for n in range(1, 17)}
reach = {str(n): {m: bf.reachable_orders([bf.Leaf(str(i)) for i in range(n)], m) for m in "ABCD"} for n in (3, 4, 5)}

sig = np.array([0.5, 0.1, 0, 0, 0, 0, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0.3])
Cc = sigma16.coupling(sig, 10)
hrb = {"sigma": sig.tolist(), "C": Cc.tolist(), "out": sigma16.mul(Cc, sig).tolist()}

# set membership: Recaman through the engine's own flip test, and some callable words
def recaman(count):
    pos, steps, seen = [0.0], [], [0.0]
    for n in range(1, count):
        cur = pos[-1]
        cand = cur - n
        if cand > 0 and not bf.would_collide(steps, lambda x, n=n: x - n, 0.0):
            steps.append(lambda x, n=n: x - n)
        else:
            steps.append(lambda x, n=n: x + n)
        pos = list(bf.trajectory(steps, 0.0))
    return [int(p) for p in pos]

def make(kind, k):
    return {"add": lambda x: x + k, "mul": lambda x: x * k}[kind]

words = {"+2, −2": [("add", 2), ("add", -2)], "×2, +1, ×½, −1": [("mul", 2), ("add", 1), ("mul", 0.5), ("add", -1)],
         "−x, −x": [("mul", -1), ("mul", -1)], "+3, ×2, −6, +3": [("add", 3), ("mul", 2), ("add", -6), ("add", 3)]}
wd = {}
for k, ws in words.items():
    steps = [make(*w) for w in ws]
    wd[k] = {"steps": ws, "trajectory": list(bf.trajectory(steps, 1.0)), "collisions": [[a, b, p] for a, b, p in bf.collisions(steps, 1.0)],
             "would": {c: bf.would_collide(steps, lambda x, c=c: x + c, 1.0) for c in (-3, -1, 0, 1, 2, 3)}}
jm = {"lineage": ["descend"], "emerger": ["build_up"], "both": ["descend", "build_up"]}
juris = [[o, op, bf.jurisdiction_violation(o, op, {k: set(v) for k, v in jm.items()})["violation"]]
         for o in ("lineage", "emerger", "both", "nowhere") for op in ("descend", "build_up")]
data = {"A": A, "B": B, "C": C, "D": D4, "X": X, "mul_tests": mul_tests, "plans": plans, "evolve": evolve, "counts": counts, "bell": bell,
        "reach": reach, "hrb": hrb, "recaman": recaman(40), "words": wd, "juris_map": jm, "juris": juris}
out = os.path.join(HERE, "bf_data.js")
open(out, "w", encoding="utf-8").write("window.BFDATA=" + json.dumps(data, separators=(",", ":")) + ";\n")
print("bf_data.js", os.path.getsize(out), "bytes; recaman", data["recaman"][:12], "reach", reach)
