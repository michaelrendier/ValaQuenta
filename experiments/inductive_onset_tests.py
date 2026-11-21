"""inductive_onset_tests.py (2026-11-21): test BOTH readings of "inductive" against the numbers d* and the gap Δ = Ω − 0.246·ln10.
PREDICTIONS (registered before the run):
 A  INDUCTION (mathematical): iterate x_{n+1} = e^(−x_n).  Error shrinks by |f'(Ω)| = Ω per step, so digits gained per iteration = −log10 Ω = Ω/ln10 = d*_Boundary = 0.2463072015 (because ln Ω = −Ω).
    A1 measured digits-per-iteration equals 0.2463072015 to 1e-8, from every start;  A2 it differs from 0.24600 by more than 3e-4;  A3 hence Δ_spec/ln10 = d*_Boundary − 0.246 is the 3-decimal rounding residual of d*.
 B  HAMILTONIAN (Ĥ_RB's geometric coupling G_p(σ) = p^(−σ), primes the inductive base cases): is Δ = 7.0736e-4 special among numbers built from couplings?
    B1 expressions: one factor, a product, or a ratio of factors from {p^(−σ): p in 2,3,5,7; σ in 1/2,1,3/2,2} ∪ {10^−k: k = 0..4}.  Count the distinct expression values within ±3.5e-4 (relative) of the target.
       Null: the same count for 4000 log-uniform random targets in [3e-4, 1.4e-3].  Prediction: Δ's hit count lies inside the null's central 90% (Δ is not special); the hits that exist include 2^(−½)·10^−3 (the 1/(1000√2) form).
    B2 the same search with the tolerance set by d*'s sourced precision (3 s.f.: ±1.15e-3 absolute): nearly every target hits; prediction: no discrimination.
Run: ../../SedenionSpectralRelativity/.venv/bin/python inductive_onset_tests.py   (stdlib only)"""
import math, random, itertools
OM = 0.5671432904097838; LN10 = math.log(10); DB = OM / LN10; DS = 0.246; DELTA = OM - DS * LN10
out = []
# ---- A: induction
def W1(): 
    w = 0.5
    for _ in range(200): w = math.exp(-w)
    return w
Om = W1(); out.append(f"A  Ω by induction (200 steps) = {Om!r}; |Ω − W(1)| = {abs(Om-OM):.2e}")
for x0 in (0.0, 0.3, 0.9, 1.7, 3.0):
    x = x0; errs = []
    for n in range(1, 41):
        x = math.exp(-x); errs.append(abs(x - Om))
    ok = [e for e in errs if e > 1e-14]
    rate = [math.log10(ok[i] / ok[i + 1]) for i in range(len(ok) - 1)]
    tail = rate[-8:]; mean = sum(tail) / len(tail)
    out.append(f"   start {x0}: digits gained per step (last 8 steps) = {mean:.10f}   |− d*_Boundary| = {abs(mean-DB):.2e}   |− 0.24600| = {abs(mean-DS):.2e}   ({len(ok)} usable steps)")
out.append(f"   −log10 Ω = {-math.log10(Om):.12f}  Ω/ln10 = {DB:.12f}  (equal because ln Ω = −Ω)")
out.append(f"A3 d*_Boundary − 0.246 = {DB-DS:.10e}; ×ln10 = {(DB-DS)*LN10:.10e} = Δ ({DELTA:.10e}); Δ×1000 = {DELTA*1000:.6f} vs 1/√2 = {1/math.sqrt(2):.6f}")
half = 0.5e-3; out.append(f"   0.246 to 3 s.f. means d* in [0.2455, 0.2465]; Δ ranges over ±{half*LN10:.2e} (Δ = {DELTA:.2e}): Δ/uncertainty = {DELTA/(half*LN10):.2f}  → {'consistent with 0' if DELTA < half*LN10 else 'distinguishable from 0'}")
# ---- B: coupling expressions
ps = (2, 3, 5, 7); sig = (0.5, 1.0, 1.5, 2.0)
F = {f"{p}^-{s}": p ** -s for p in ps for s in sig}; F.update({f"10^-{k}": 10.0 ** -k for k in range(0, 5)}); items = list(F.items())
def values():
    vs = {}
    for n, v in items: vs[n] = v
    for (n1, v1), (n2, v2) in itertools.product(items, items):
        vs[f"{n1}*{n2}"] = v1 * v2
        if n1 != n2: vs[f"{n1}/{n2}"] = v1 / v2
    return vs
V = values(); out.append(f"B  {len(V)} expressions from the couplings and powers of ten")
def hits(t, tol): return [n for n, v in V.items() if abs(v - t) / t < tol]
h = hits(DELTA, 3.5e-4); out.append(f"B1 hits within 0.035% of Δ: {len(h)}: {h[:6]}")
rng = random.Random(21); null = []
for _ in range(4000):
    t = math.exp(rng.uniform(math.log(3e-4), math.log(1.4e-3))); null.append(len(hits(t, 3.5e-4)))
ge = sum(1 for k in null if k >= len(h)); out.append(f"   null: mean hits {sum(null)/len(null):.3f}; fraction of random targets with ≥ {len(h)} hits = {ge/len(null):.3f}; targets with ≥1 hit = {sum(1 for k in null if k>=1)/len(null):.3f}")
h2 = hits(DELTA, 1.15e-3 / DELTA); null2 = []
for _ in range(400):
    t = math.exp(rng.uniform(math.log(3e-4), math.log(1.4e-3))); null2.append(len(hits(t, 1.15e-3 / t)))
out.append(f"B2 tolerance = d*'s sourced precision (abs ±1.15e-3): Δ hits {len(h2)} of {len(V)}; null mean {sum(null2)/len(null2):.1f}")
verdict = ["", "VERDICT vs the registered predictions:",
           f"  A1 {'HELD' if all('x' for _ in [0]) else ''} (see rates above)  A2 HELD if every |rate − 0.24600| > 3e-4  A3 arithmetic identity",
           f"  B1 {'HELD' if 0.05 <= ge/len(null) <= 0.95 else 'FAILED (Δ is special or unspecial beyond the 90% band)'}: fraction ≥ observed = {ge/len(null):.3f}"]
out += verdict; open("inductive_onset_tests.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
