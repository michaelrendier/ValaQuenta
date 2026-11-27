#!/usr/bin/env python3
"""build_data.py -- bakes hg_data.js for the hypergon_constructibility gallery from the Python engines (hypergon_constructibility 0.200, bell_curve 1.2),
so every page compares its own JavaScript with the engine's numbers.  Run:  python3 gallery/hypergon_constructibility/build_data.py   (from the repo root, .venv)"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..")))
from ValaQuenta.modules.hypergon_constructibility import maths as hg
from ValaQuenta.modules.bell_curve import maths as bc

sweep = hg.sedenion_hypergon_sweep()
gap = hg.niemeier_gap_theorem()
fill = hg.moonshine_gap_fill()
ctl = hg.moonshine_fill_control()
tot = hg.totient_constructibility_check(70000)
phi = list(range(70001))
for i in range(2, 70001):
    if phi[i] == i:
        for j in range(i, 70001, i):
            phi[j] -= phi[j] // i
constructible = [n for n in range(3, 70001) if phi[n] & (phi[n] - 1) == 0]
dims = [i * 0.5 for i in range(0, 65)]                       # 0 .. 32 in steps of 1/2
data = {
    "primes16": hg.PRIMES16,
    "rows": sweep["rows"],
    "systems": [{"h": s["h"], "label": s["label"]} for s in gap["root_systems"]],
    "h_values": gap["h_values"], "residues": gap["residues_reached"], "gap": gap["gap"], "proof": gap["proof"],
    "moonshine": hg.MOONSHINE_PRIMES, "by_residue": {str(k): v for k, v in fill["by_residue"].items()},
    "control": {k: ctl[k] for k in ("pool_size", "subsets", "cover_gap", "cover_all_odd", "p_cover_gap", "p_cover_all_odd")},
    "constructible_to_70000": constructible, "totient_mismatches": tot["mismatches"],
    "peak_volume": bc.nball_peak("volume"), "peak_area": bc.nball_peak("area"),
    "nball": {"n": dims, "V": [bc.nball_volume(n) for n in dims], "S": [bc.nsphere_area(n) if n > 0 else None for n in dims]},
    "nball_check": [{"n": n, "V": bc.nball_volume(n), "S": bc.nsphere_area(n)} for n in (0.5, 1, 2, 3, 5, 5.2569464, 16, 24)],
    "gamma_check": [{"x": x, "g": math.gamma(x)} for x in (-3.5, -2.5, -1.5, -0.3, 0.5, 1.5, 3.7, 6.0)],
    "other_rank_gap": {str(r): hg.niemeier_gap_theorem(rank=r)["gap"] for r in (8, 12, 16, 24, 32)},
    "other_rank_count": {str(r): hg.niemeier_gap_theorem(rank=r)["count"] for r in (8, 12, 16, 24, 32)},
}
open(os.path.join(HERE, "hg_data.js"), "w", encoding="utf-8").write("window.HGDATA=" + json.dumps(data, separators=(",", ":")) + ";\n")
print("hg_data.js", os.path.getsize(os.path.join(HERE, "hg_data.js")), "bytes;", len(constructible), "constructible n <= 70000;", data["other_rank_count"])
