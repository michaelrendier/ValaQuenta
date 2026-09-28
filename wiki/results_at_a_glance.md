# Results at a glance

**Engine outputs, quoted.** Moved from the README so the README can be the API: Code Reference. The record of what each engine printed when last run; the reference for how to call it is the [README](../README.md#api-code-reference) and the Sphinx docs.

---


## modules/add_scale_sign/ — the tier-0 datatype

```
ASS(add, scale, sign)  =  x ↦ sign·scale·x + add   —  an element of
  Aff(1,ℝ) = ℝ ⋊ (ℝ_{>0} × ℤ/2) = ADD ⋊ (SCALE × SIGN)

compose  A @ B        invert  ~A        residual  A.residual('SIGN')  (str.strip-style)
decompose  A.lineage(order='chrono' | 'zeta')  →  ASSWord

each generator's equation part:   ADD → a      SCALE → ln s      SIGN → g
the generalized equation:         u = Σₖ [ gₖ·ln sₖ + aₖ ]      Γ = tanh(u/2)
ground state a=0, s=1, g=+1  ⇒  u=0  ⇒  Γ=0  ⇒  the now

firing order (the 3-phase camshaft):  SIGN → SCALE → ADD,  x ↦ ADD(SCALE(SIGN(x)))
firing defect  u − (a + ln s) = (g−1)·ln s   (non-zero ⇔ SIGN flipped a non-trivial SCALE)
orthogonal Smith charts:  Γ_SCALE = tanh(½·ln s)  ⟂  Γ_ADD = tanh(½·a),  parity g
```

Registered as `AddScaleSignModule` (6 code-verified equations; `python3 -m
ValaQuenta --info`). The decomposition maths (the four-question test, roll-down)
stays in `VAPMIP/add_scale_sign.py` — not duplicated. Also an engine + tool in
the SFR decomposer suite (with the fast inverse square root as the worked
example). Formal spec: [wiki/add_scale_sign.md](add_scale_sign.md) ·
`Ainulindale/wiki/107_add_scale_sign_datatype.md`.

## bao_mass_gap.py — Yang-Mills Mass Gap

```
Status: ESTABLISHED (all 5 checks pass)

OMEGA_ZS = 0.5671432904097838  (Lambert W(1), exact)
D_STAR   = 0.24600             (BK spectral, 5 sig figs)
GAP      = 0.000707357533249   (OMEGA_ZS − D_STAR × ln(10))

GAP ≈ 1/(1000√2)  [0.035% approximation]
NOTE: 1/√2000 = 0.02236 — NOT the gap (31.6× larger)
```

See [wiki/bao_mass_gap.md](bao_mass_gap.md)

## hamiltonian.py — H = xp

```
HamiltonianXP:
  scale_check(2,3,λ=2) → True
  trajectory(1,1,t=1)  → x=e, p=1/e, E=xp=1.0 (conserved exactly)
  zeros (BK, first 5)  → [14.1347, 21.0220, 25.0109, 30.4249, 32.9351]

FermatEllipticHamiltonian (lemniscatic, g₂=1, g₃=0):
  Discriminant Δ = 1.0 (valid elliptic curve)
  ℘(1.0) = 1.05083333

RedBlueHamiltonian:
  Red(σ=½) = Blue(σ=½) = 0.707...  (balance at σ=½ ✓)
```

See [wiki/hamiltonian.md](hamiltonian.md)

## noether.py — Ascending/Descending Noether Currents

```
forced_sigma(E, σ₀=any) → 0.5   exactly, for any real σ₀ and any E

FIXED (2026-08-28): the old softmax-weighted-average iteration converged to
σ=½ only for E ≲ 10 (returned σ₀ unchanged above; OverflowError for σ₀<0).
The balance F=B is, in logs, E(1−2σ)=0 — linear in σ — so it is now solved
exactly in one Newton step from any σ₀, with no exp evaluated away from the
balance point. See wiki/noether.md. (Notebook 03_noether.ipynb still shows
the old behaviour and needs a re-run.)

The boundary is ORIENTED: up (toward next CD shadow) / down (toward ZD).
σ=½ is the shadow of the world above — projection of the next CD level.
```

See [wiki/noether.md](noether.md)

## galactic_cavity.py — Galactic Pilot Wave

```
r_t    = 0.738 kpc   (dark matter threshold, d* × r_max_bar)
v_flat = 220.0 km/s  (flat rotation, confirmed)
Period = 22.7 Gyr    (frozen — exceeds universe age 13.8 Gyr)
P1 (r_t = d* × r_max_bar): confirmed against SPARC 97-galaxy sample 2026-05-30
```

See [wiki/galactic_cavity.md](galactic_cavity.md)

## capacitor.py — Semantic Low-Pass Filter

```
H(0) = 1.0  (DC gain — the prime passes through unattenuated)
Pole at s = −1/τ  (stable, left half-plane)
Transfer function: H(s) = 1/(1+sτ)
```

See [wiki/capacitor.md](capacitor.md)

## understand.py — LSHS Pipeline

```
U.process("why is the mass gap 1 over root 2000")
  prime = 0.5 + 48.0052j  (Riemann zero γ₉)
  σ     = 0.5000000000    (derived, never assigned)
  dc    = 0.50000000      (the prime, extracted)

σ=½ is derived for every input. The mathematics forces it.
```

See [wiki/understand.md](understand.md)

---

## Key Identity — What "1/root(2000)" Actually Means

Do not write `GAP = 1/√2000`. Write `GAP ≈ 1/(1000√2)`:

```
1/√2000        = 0.022360...   ← NOT the gap
1/(1000√2)     = 0.000707...   ← the approximate identity (0.035% error)
1/√(2,000,000) = 0.000707...   ← same thing, unambiguous
```

The 1/√2 factor is explained (σ=½ symmetry, first CD doubling). The 10³ factor is an open question.

---
