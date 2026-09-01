# d_star_rg — The d* Renormalization Group

**Status:** THEORETICAL — protocol only. Engine `engine/d_star_rg.py` not yet
built. Full spec: `FourthAgePapers/DStarRG/README.md` + `construction.json`.

Engineering structure, **no claim**. `d*_RG` is a **given** — "The Stability,"
one of the four canonical faces of `d*` (`wiki/constants.md`,
`Ainulindale/wiki/17`).

---

## What it is

`d*_RG` is the **fixed point of a renormalization group**, obtained by
iterating — not by a closed form (which is OPEN).

- **as a value:** ≈ 0.24631, self-consistent with the Translator face
  (`d*_RG · ln10 → Ω_ZS = 0.56714`).
- **as a dimension:** **8** — the persistent octonion. The flow converges
  dimensionally to the 8-DOF gain-1 core (`persist ≡ 8` at d = 8,16,32,64;
  `void = (d−8)/2`; `8/d → 0`). Dimensional, not fractional.

## The RG = the Cayley–Dickson tower

| Wilson RG step | CD tower |
|---|---|
| block transform | CD-double `d → 2d` (`_smul` recursion) |
| relevant vs irrelevant | persistent (gain 1: `e₀`, `e_{d/2}`, Boundary Lever) vs void `(2d−8)/2` |
| integrate out irrelevant | project onto the 8-core, **carry phase** (never `|z|²`) |
| rescale | ÷ `d*_taut = Ω_ZS/ln(10)` |
| iterate to fixed point | until `|Δd*| < ε` → `d*_RG` |

The flow is a **σ=½ saddle** — `wiki/telperion.md` / *The Oblique Gear* give a
positive Lyapunov exponent λ ≈ 6 off balance. The iteration must approach on
the **stable manifold**: balance `Σ tilt → 0` every pass (Oblique-Gear T6
construction) or it diverges.

## Renormalization is built in

The void is **projected** — an exact resummation, phase carried — never
**subtracted**. No counterterm, no discarded infinity; the nat budget balances
at every pass. This is the standing **No Renormalization** rule stated as an
engineering constraint: the engine renormalizes by construction; the operator
never adds a second, hand-applied one.

## Windows of order ARE renormalization

The periodic windows in a chaotic bifurcation diagram are Feigenbaum
renormalization fixed points — each a rescaled copy of the whole cascade under
`R[f](x) = α f(f(x/α))`. `d*_RG` is the CD-tower analogue: the largest bubble
of order in the tower's chaos, the one every smaller window is a rescaling of.
Bubbles of order rise buoyantly through the chaotic medium; each has a **wake**
— a return path carrying the disorder it displaced back down (the Noether
Information current). See `FourthAgePapers/` — *Hyper-Bifurcation*.

## Protocol (summary)

```
INPUT  seed x₀ ∈ CD algebra (default 𝕆, d₀=8); max dim D=256; tol ε=1e-9
STEP   a DOUBLE  b CLASSIFY (persistent 8-core / void)  c BALANCE (Σtilt→0)
       d PROJECT (carry phase; assert Σnats_in = Σnats_out)  e RESCALE (÷d*_taut)
       f RECORD d*_k
LOOP   until |d*_k − d*_{k-1}| < ε  →  d*_RG := lim d*_k
CHECKS |persistent|=8 · d*_RG·ln10→Ω_ZS · approach-exponent = Oblique-Gear λ
       · semigroup · SHA-256(history) reproducible
```

## See also

- `wiki/constants.md`, `wiki/fixed_point.md`, `wiki/berry_keating.md`,
  `wiki/telperion.md`, `wiki/ring_theory.md`, `wiki/three_ring_scale.md`
- `Ainulindale/wiki/17_alpha_omega_d_star.md`
- `FourthAgePapers/DStarRG/`, `FourthAgePapers/BoundaryLever/`
