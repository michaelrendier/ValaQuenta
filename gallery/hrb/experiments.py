"""
gallery/hrb/experiments.py -- the data behind the Ĥ_RB gallery. Every number is produced by importing the engine and running it
(h_rb_hat.maths, h_rb_hat.sigma16, box_kite via sigma16). Writes data/hrb_data.json and data/hrb_data.js.

    cd <ThePlace> && PYTHONPATH=. ValaQuenta/.venv/bin/python ValaQuenta/gallery/hrb/experiments.py

All results are CALCULATED. The two lifts are definitions (OPEN), see modules/h_rb_hat/sigma16.py.

d* faces (all four are needed to chart ln(10) in Universal Native Space):
  d*         = 0.24600          the value the code runs with (Boundary, σ_ζ=½ plane)
  d*_taut    = 0.246307201473  A_π/ln10, the Flow (radial unit)
  d*_RG      = dimension 8; numeric OPEN, no closed form  the Stability (centre r=0)
  d*_ln(10)  = 0.5671432904   d*_taut·ln10 = A_π, the Translator (log bridge)
Full story of d*: Ainulindale/wiki/17_alpha_omega_d_star.md; ~/.clauderc_canonical_maths @RCCM_FOUR_DSTAR; FourthAgePapers/DStarRG
"""
import json
import os
import time

import numpy as np

from ValaQuenta.engine import constants as C
from ValaQuenta.modules.h_rb_hat import maths as M
from ValaQuenta.modules.h_rb_hat import sigma16 as S

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(20261125)
E = np.eye(16)
D = {"generated": time.strftime("%Y-%m-%d"), "constants": {
    "D_STAR": C.D_STAR, "D_STAR_TAUT": C.D_STAR_TAUT, "D_STAR_LN10": C.D_STAR_LN10, "A_PI": C.A_PI, "ALPHA_FS": C.ALPHA_FS,
    "GAP": float(S.GAP), "GAP_closed_form": float(S.GAP_CLOSED_FORM), "primes": M.PRIMES[:20]}}


def sieve(n):
    s = np.ones(n + 1, bool); s[:2] = False
    for i in range(2, int(n ** .5) + 1):
        if s[i]: s[i * i::i] = False
    return np.flatnonzero(s)


def ab(sigma_riemann, tau, primes):
    lnp = np.log(primes.astype(float)); w = primes.astype(float) ** (-sigma_riemann)
    return (w * np.cos(tau * lnp)).sum(), -(w * np.sin(tau * lnp)).sum()


P20 = np.array(M.PRIMES[:20]); P168 = sieve(1000); P1229 = sieve(10000)

# E1 -- direction atlas: 15 basis directions + every (e_i ± e_j)/√2 + 4000 random directions on S^14
atlas = []
for k in range(1, 16):
    a = E[k]; inv = S.asym_of_unit(a)
    atlas.append({"label": f"e{k}", "kind": "basis", "rank_ad": inv["rank"], "nullity_L": S.zero_divisor_partners(a),
                  "sv_ad": sorted({round(float(x), 5) for x in inv["sv"]}), "sv_L": sorted({round(float(x), 5) for x in S.invariants(S.L(a))["sv"]})})
for i in range(1, 16):
    for j in range(i + 1, 16):
        for sg in (1, -1):
            a = (E[i] + sg * E[j]) / np.sqrt(2); inv = S.asym_of_unit(a)
            atlas.append({"label": f"(e{i}{'+' if sg > 0 else '-'}e{j})/√2", "kind": "pair", "i": i, "j": j, "sign": sg,
                          "rank_ad": inv["rank"], "nullity_L": S.zero_divisor_partners(a),
                          "sv_ad": sorted({round(float(x), 5) for x in inv["sv"]}), "sv_L": sorted({round(float(x), 5) for x in S.invariants(S.L(a))["sv"]})})
D["atlas"] = atlas
rand = []
for _ in range(4000):
    u = rng.normal(size=16); u[0] = 0; u /= np.linalg.norm(u)
    inv = S.asym_of_unit(u)
    rand.append((inv["rank"], S.zero_divisor_partners(u), tuple(sorted({round(float(x), 4) for x in inv["sv"]}))))
cls = {}
for r, n, sv in rand: cls.setdefault((r, n, sv), 0); cls[(r, n, sv)] += 1
D["random_classes"] = [{"rank_ad": k[0], "nullity_L": k[1], "sv_ad": list(k[2]), "count": v} for k, v in sorted(cls.items(), key=lambda x: -x[1])]
D["pair_classes"] = {}
for a in atlas:
    if a["kind"] == "pair":
        key = f"nullity_L={a['nullity_L']} rank_ad={a['rank_ad']}"; D["pair_classes"][key] = D["pair_classes"].get(key, 0) + 1
D["spectra_L"] = {"e1": [[float(z.real), float(z.imag)] for z in S.spectrum_of_L(E[1])],
                  "zd": [[float(z.real), float(z.imag)] for z in S.spectrum_of_L((E[1] + E[10]) / np.sqrt(2))]}

# E2 -- the (σ0, τ) plane: α = Re D, β = Im-part (the balance), with 20 (the code's list), 168 and 1229 primes
sig = np.linspace(-0.5, 3.0, 141); tau = np.linspace(0, 40, 321)
for name, P in (("p20", P20), ("p168", P168)):
    A = np.zeros((len(tau), len(sig))); B = np.zeros_like(A)
    for i, t in enumerate(tau):
        for j, s in enumerate(sig): A[i, j], B[i, j] = ab(s, t, P)
    D[f"plane_{name}"] = {"sigma_riemann": sig.round(4).tolist(), "tau": tau.round(4).tolist(), "alpha": A.round(5).tolist(), "beta": B.round(5).tolist()}

# E3 -- the facet rows (σ0 = 2 GR, 1 YM/NS, 1/2 QM+Riemann, and 0.2463 / 0.5671 as σ0 values), real σ and at τ = 14.1347 (γ1)
fac = []
for lab, s0 in (("GR σ_ζ=2", 2.0), ("YM/NS σ_ζ=1", 1.0), ("QM/Riemann σ_ζ=1/2", 0.5), ("σ_ζ=d* (0.246)", C.D_STAR), ("σ_ζ=A_π", C.A_PI), ("σ_ζ=0", 0.0)):
    for tlab, t in (("τ=0", 0.0), ("τ=γ1=14.1347", 14.134725), ("τ=GAP", float(S.GAP))):
        a, b = ab(s0, t, P20); fac.append({"facet": lab, "sigma_riemann": s0, "tau_label": tlab, "tau": t, "alpha": a, "beta": b,
                                           "modulus": float(np.hypot(a, b)), "asym_fro": float(abs(b) * S.asym_of_unit(E[1])["fro"])})
D["facets"] = fac
D["scalar_facets_from_code"] = {k: M.__dict__[k]()["coupling_sum"] for k in ("facet_general_relativity", "facet_yang_mills", "facet_quantum_mechanics", "facet_navier_stokes", "facet_riemann_zeta") if k in M.__dict__}

# E4 -- the Mass Gap scan: |β| and |asym| against τ on a log grid at σ0 = 1/2, 1/2 ± GAP, and against σ0 near 1/2 at τ = GAP
taus = np.logspace(-8, 1, 181)
D["gap_scan"] = {"tau": taus.tolist()}
for lab, s0 in (("half", 0.5), ("half+gap", 0.5 + S.GAP), ("half-gap", 0.5 - S.GAP)):
    D["gap_scan"][lab] = [ab(s0, t, P20)[1] for t in taus]
c1 = float((P20.astype(float) ** -0.5 * np.log(P20)).sum())
D["gap_scan"]["slope_const_c1"] = c1
D["gap_scan"]["beta_at_tau_GAP"] = ab(0.5, float(S.GAP), P20)[1]
D["gap_scan"]["tau_GAP_times_c1"] = c1 * float(S.GAP)
d_s = np.linspace(0.5 - 5e-3, 0.5 + 5e-3, 201)
D["gap_scan"]["sigma_riemann_near_half"] = d_s.tolist()
D["gap_scan"]["alpha_near_half_tau0"] = [ab(s, 0.0, P20)[0] for s in d_s]
D["gap_scan"]["alpha_near_half_tauGAP"] = [ab(s, float(S.GAP), P20)[0] for s in d_s]
D["gap_scan"]["ratio_1000_sqrt2_gap"] = float(S.GAP * 1000 * np.sqrt(2))

# E5 -- where Ĥ_RB acts as a zero divisor: α = 0 and û a ZD direction. Locate the α = 0 curve in the plane (20 primes)
A20 = np.array(D["plane_p20"]["alpha"]); zeros = []
for i in range(A20.shape[0]):
    for j in range(A20.shape[1] - 1):
        if A20[i, j] == 0 or A20[i, j] * A20[i, j + 1] < 0:
            zeros.append([D["plane_p20"]["sigma_riemann"][j], D["plane_p20"]["tau"][i]])
D["alpha_zero_crossings"] = zeros[:4000]
# nullity of Ĥ_RB = L_C for ZD vs basis directions at a point with α ~ 0
def nullity_at(uhat, a, b):
    cvec = a * E[0] + b * uhat; return S.invariants(S.L(cvec))["nullity"]
zdhat = (E[1] + E[10]) / np.sqrt(2)
D["zero_divisor_action"] = {"alpha=0,zd": nullity_at(zdhat, 0.0, 1.0), "alpha=0,basis": nullity_at(E[1], 0.0, 1.0),
                            "alpha=1,zd": nullity_at(zdhat, 1.0, 1.0), "alpha=1,basis": nullity_at(E[1], 1.0, 1.0)}

# E6 -- Lift A equivariance and the balance of the scalar energies
D["lift_a_spread"] = {f"{s0},{t}": S.lift_a_equivariance(s0, t) for s0, t in ((0.5, 3.0), (1.0, 7.0), (2.0, 14.0))}
bal = []
for x in np.linspace(-3, 3, 61):
    bal.append([float(x), float(M.red_energy(x, 1.0)), float(M.blue_energy(x, 1.0))])
D["energies"] = bal

# E7 -- cycling the sedenion: sweep û through every basis direction at fixed σ (σ0=1/2, τ=3): output of lift A and singular values of lift B
cyc = []
for k in range(1, 16):
    s = S.sigma_rb_vector(0.5, E[k][1:], 3.0); A_ = S.lift_a(s); B_ = S.lift_b(s)
    cyc.append({"k": k, "A_total": A_["total"].round(6).tolist(), "B_sv_asym": sorted({round(float(x), 5) for x in S.invariants(B_["asym"])["sv"]}),
                "B_rank_asym": S.invariants(B_["asym"])["rank"], "B_nullity_HRB": S.invariants(B_["H_RB"])["nullity"]})
D["cycle_basis"] = cyc


# E8 -- scalar-engine panels: partial sums per facet, the σ phase diagram, the balance, the X-9 integrand, the oblique crank
D["partial_sums"] = {lab: np.cumsum(P168.astype(float) ** (-s0)).round(6).tolist() for lab, s0 in (("σ_ζ=2 GR", 2.0), ("σ_ζ=1 YM/NS", 1.0), ("σ_ζ=1/2 QM/Riemann", 0.5), ("σ_ζ=d* (0.246)", C.D_STAR), ("σ_ζ=0.3 forbidden", 0.3))}
D["primes168"] = P168.tolist()
pd = M.sigma_phase_diagram(120)["diagram"]
D["phase_diagram"] = [{"sigma": r["sigma"], "theory": r["theory"], "euler_mag": min(r["euler_mag"], 1e4), "euler_re": r["euler_re"]} for r in pd]
D["balance_scalar"] = [[s, M.sigma_rb_term(2, s, 1.0, 1.0)["balance"], M.sigma_rb_term(5, s, 0.3, 2.0)["balance"]] for s in np.linspace(0, 3, 31)]
D["x9"] = [[s, float(np.exp(-(1 - s) * 2.0) * np.exp(-s * 2.0)), float(np.exp(-(1 - s) * 2.0)), float(np.exp(-s * 2.0))] for s in np.linspace(0, 1, 101)]
D["crank"] = {"theta_deg": float(np.degrees(np.arctan(C.D_STAR))), "theta_taut_deg": float(np.degrees(np.arctan(C.D_STAR_TAUT))), "d_star": C.D_STAR, "d_star_taut": C.D_STAR_TAUT}
D["reflection"] = [[s, float(sum(float(p) ** (-s) for p in P20)), float(sum(float(p) ** (-(1 - s)) for p in P20))] for s in np.linspace(0, 1, 101)]

# E9 -- the TuringStack Chladni / hypercomplex Laplacian data (imported read-only from ../../../TuringStack)
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "TuringStack"))
import hypercomplex_laplacian as HL
tab = np.zeros((32, 32), dtype=np.int64)
for i in range(32):
    for j in range(32): tab[i, j] = HL.t32_mul(1 << i, 1 << j, 32)
def prod_ints(a, b):
    r = 0
    for i in range(32):
        if (a >> i) & 1:
            for j in range(32):
                if (b >> j) & 1: r ^= int(tab[i, j])
    return r
comps = [(1 << i) | (1 << j) for i in range(32) for j in range(i + 1, 32)]
D["chladni_496"] = {"n": len(comps), "popcount": [[bin(prod_ints(a, b)).count("1") for b in comps] for a in comps]}
D["chladni_scales"] = []
for dim in (4, 8, 16, 32):
    ms = (1 << dim) - 1; nil = 0; rows = []
    for w in range(0, 1 << min(dim, 16)):
        pass
    sample = [int(x) & ms for x in rng.integers(1, 1 << 62, 400, dtype=np.int64)] if dim > 16 else list(range(1, 1 << dim))
    nl = [HL.spectral_profile(w, dim)["nullity"] for w in sample[:300]]
    nilfrac = float(np.mean([HL.is_nilpotent(w, dim) for w in sample]))
    D["chladni_scales"].append({"dim": dim, "mean_nullity": float(np.mean(nl)), "nilpotent_fraction": nilfrac, "V_n": float(np.pi ** (dim / 2) / np.exp(np.math.lgamma(dim / 2 + 1))) if hasattr(np, "math") else float(np.pi ** (dim / 2) / __import__("math").gamma(dim / 2 + 1))})
D["sha1"] = [{"name": n, "w": w, "dist": HL.trace_laplacian(w)["spectral_dist"], "bits": [(w >> k) & 1 for k in range(32)]} for n, w in HL.SHA1_IVS + [("K0", 0x5A827999), ("K1", 0x6ED9EBA1), ("K2", 0x8F1BBCDC), ("K3", 0xCA62C1D6)]]
D["multiscale"] = {n: HL.motion_signal(w)["fillings"] for n, w in HL.SHA1_IVS}

# E10 -- the σ_RB[k] = ψ[k]·conj ψ[k⊕4] tilt/axis structure (oblique gear), random ψ in C^16
psi = rng.normal(size=16) + 1j * rng.normal(size=16)
sr = np.array([psi[k] * np.conj(psi[k ^ 4]) for k in range(16)])
D["sigma_rb_tilt_axis"] = {"re": sr.real.round(5).tolist(), "im": sr.imag.round(5).tolist(),
                           "conj_pair_resid": float(max(abs(sr[k ^ 4] - np.conj(sr[k])) for k in range(16))),
                           "sigma_self": float(0.5 + sr.real.sum() / 2 / (abs(psi) ** 2).sum() * 2) if False else float(0.5 + sr.real.sum() / (abs(psi) ** 2).sum())}

# E11 -- census aggregate (docs/HRB_REFERENCE_CENSUS.md source rows)
cen = os.path.join("/tmp/claude-1000/-home-rendier-Projects-ThePlace/9e44fe44-fdda-4cfe-a4db-5e9db4d183f5/scratchpad", "hrb_rows.json")
if os.path.exists(cen):
    rows = [r for r in json.load(open(cen)) if "/build/lib/" not in r[0] and "/docs/_build/" not in r[0]]
    agg = {}
    for p, h, z, s, j in rows:
        repo = p.split("/")[0]; k = "code" if p.endswith((".py", ".c", ".h", ".scad")) else "notebook" if p.endswith(".ipynb") else "html" if p.endswith(".html") else "doc"
        a = agg.setdefault(repo, {"H": 0, "Z": 0, "S": 0, "J": 0, "files": 0, "code": 0, "doc": 0, "notebook": 0, "html": 0}); a["H"] += h; a["Z"] += z; a["S"] += s; a["J"] += j; a["files"] += 1; a[k] += 1
    D["census"] = agg
D["deps"] = {"h_rb_hat": ["clay_millennium", "constants", "derivation_chain", "oblique_gear", "inductive_onset_residual"], "downstream_repos": ["Ainulindale", "VAPMIP", "FourthAgePapers", "GenerationalLineage", "PtolemyDesktop", "RiemannHypothesisProof", "SedenionSpectralRelativity", "TuringStack"]}


# E12 -- the DOCUMENTED sigma_rb map (modules/h_rb_hat/oblique_sigma_rb.py): psi (16) in, sigma_rb (16) out
import math as _m
import random as _r
from ValaQuenta.modules.h_rb_hat import oblique_sigma_rb as O
def _rpsi(seed, scale=1.0):
    r = _r.Random(seed); return [complex(r.gauss(0, scale), r.gauss(0, scale)) for _ in range(16)]
PSI = _rpsi(20260831); tl, ax, srb = O.tilt_axis(PSI)
doc = {"seed": 20260831, "tilt": tl, "axis": ax, "sigma_rb_re": [z.real for z in srb], "sigma_rb_im": [z.imag for z in srb],
       "pair_residual": max(abs(srb[k ^ 4] - srb[k].conjugate()) for k in range(16)), "sigma_self": O.sigma_self(PSI)[0],
       "sigma_self_pred": 0.5 + sum(tl) / sum(O.p_red_blue(PSI))}
mt, ma = sum(tl) / 8, sum(ax) / 8
doc["split_1_7"] = {"tilt_mean": mt, "tilt_struts": [x - mt for x in tl], "axis_mean": ma, "axis_struts": [x - ma for x in ax]}
# pair planes and single components: cycle through the sedenion
single = []; 
for k in range(16):
    psi = [0.0] * 16; psi[k] = 1.0; s = O.sigma_rb_map(psi); single.append({"k": k, "max_sigma_rb": max(abs(z) for z in s), "sigma_self": O.sigma_self(psi)[0]})
pairs = []
for k in O.REP:
    for lab, sg in (("in-phase", 1.0), ("anti-phase", -1.0)):
        psi = [0.0] * 16; psi[k] = 1 / _m.sqrt(2); psi[k ^ 4] = sg / _m.sqrt(2); s = O.sigma_rb_map(psi); tt, aa, _ = O.tilt_axis(psi)
        pairs.append({"pair": f"{k}↔{k ^ 4}", "phase": lab, "nonzero": [i for i, z in enumerate(s) if abs(z) > 1e-12], "tilt_j": tt[O.REP.index(k)], "sigma_self": O.sigma_self(psi)[0]})
doc["single"], doc["pairs"] = single, pairs
# T3 gear rotation
j = O.REP[2]; th = np.linspace(0, 2 * np.pi, 121); d2 = abs(PSI[j]) ** 2 - abs(PSI[j ^ 4]) ** 2
doc["gear"] = {"theta": th.tolist(), "tilt_j": [O.tilt_axis(O.rot_pair(PSI, j, a))[0][2] for a in th], "axis_j": [O.tilt_axis(O.rot_pair(PSI, j, a))[1][2] for a in th],
               "law": [_m.cos(2 * a) * tl[2] + 0.5 * _m.sin(2 * a) * d2 for a in th]}
# T4 sigma_self against 1/2 + sum tilt/energy for 300 random psi
rows = []
for sd in range(300):
    q = _rpsi(1000 + sd); a_, r_, b_ = O.sigma_self(q); tq = O.tilt_axis(q)[0]; rows.append([0.5 + sum(tq) / (r_ + b_), a_])
rows.sort(); doc["sigma_self_law"] = rows
# T6 balance sweep, several seeds
base = _rpsi(7); sweep = []
for lam in np.linspace(0, 1, 21):
    pb = O.balanced(base, float(lam)); tb, ab, _ = O.tilt_axis(pb); sweep.append([float(lam), sum(tb), _m.hypot(*ab), O.sigma_self(pb)[0]])
doc["balance_sweep"] = sweep
# strut-blindness and the onset residual (wiki 123): three strut distributions, several pair energies
Dl = O.onset_residual(); rr = _r.Random(0); dist = []
for tr in range(3):
    tt = [rr.uniform(-0.3, 0.3) for _ in range(8)]; m_ = sum(tt) / 8; tt = [x + Dl - m_ for x in tt]
    dist.append({"spread": float(np.std(tt)), "sigma_self": O.sigma_self(O.embed_tilt(tt, 1.0))[0], "half_plus_delta": 0.5 + Dl})
doc["strut_blind"] = {"delta": Dl, "trials": dist, "by_energy": [[E_, 0.5 + Dl / E_] for E_ in (0.5, 1.0, 2.0, 10.0)]}
# rectifier law
ur = np.random.default_rng(0).normal(size=8); ur -= ur.mean(); ur /= np.linalg.norm(ur); lams = np.logspace(-6, 5, 45); rect = []
for lam in lams:
    tt = Dl + lam * ur; a_ = np.sign(tt) * np.sqrt(np.abs(tt)); b_ = np.sqrt(np.abs(tt)); red = np.sum(np.abs(a_ + b_) ** 2) / 2; blue = np.sum(np.abs(a_ - b_) ** 2) / 2
    rect.append([float(lam), float(red / (red + blue)), float(O.rectifier_sigma_self(list(tt)))])
doc["rectifier"] = rect
# flow: balanced+perturbation (saddle, grows) and generic (converges to balance); |axis| conserved
def _drive(q): return O.tilt_axis(q)[0]
def _step(p, g):
    t0, h = _drive(p), list(p)
    for k in O.REP: h = O.rot_pair(h, k, 0.5 * g * t0[O.REP.index(k)])
    t1, out = _drive(h), list(p)
    for k in O.REP: out = O.rot_pair(out, k, g * t1[O.REP.index(k)])
    return out
flows = {}
for lab, p0 in (("balanced + 1e-9 noise", None), ("generic psi", _rpsi(3))):
    if p0 is None:
        rn = _r.Random(5); p0 = [z + 1e-9 * complex(rn.gauss(0, 1), rn.gauss(0, 1)) for z in O.balanced(_rpsi(7))]
    p = p0; g = 0.0125; tr_, axn, ts = [], [], []
    for n in range(400):
        tq, aq, _ = O.tilt_axis(p); tr_.append(max(abs(x) for x in tq)); axn.append(_m.hypot(*aq)); ts.append(sum(tq)); p = _step(p, g)
    flows[lab] = {"gain": g, "max_abs_tilt": tr_, "axis_norm": axn, "sum_tilt": ts}
doc["flow"] = flows
h = flows["balanced + 1e-9 noise"]["max_abs_tilt"]; doc["lambda"] = (_m.log(h[40]) - _m.log(h[10])) / (30 * 0.0125)
D["doc"] = doc
D["sigma_rb_tilt_axis"] = {"re": tl, "im": ax, "conj_pair_resid": doc["pair_residual"], "sigma_self": doc["sigma_self"]}

json.dump(D, open(os.path.join(OUT, "hrb_data.json"), "w"))
open(os.path.join(OUT, "hrb_data.js"), "w").write("window.HRB=" + json.dumps(D) + ";")
print("wrote", os.path.join(OUT, "hrb_data.json"), os.path.getsize(os.path.join(OUT, "hrb_data.json")) // 1024, "KB")
print("pair classes", D["pair_classes"]); print("random classes", D["random_classes"][:6])
print("zd action", D["zero_divisor_action"]); print("gap", {k: D["gap_scan"][k] for k in ("beta_at_tau_GAP", "tau_GAP_times_c1", "ratio_1000_sqrt2_gap", "slope_const_c1")})
print("scalar facets", D["scalar_facets_from_code"]); print("lift A spread", D["lift_a_spread"])
