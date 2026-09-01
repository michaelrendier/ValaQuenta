# Engine: H_NN  Berry-Keating Operator

**Module:** `modules/berry_keating/`  
**Version:** 0.111  
**Confidence floor:** OPEN  
**Notebooks:** [core/07_berry_keating.ipynb](../notebooks/core/07_berry_keating.ipynb)  
**Claim:** d* is a spectral floor read off H=xp, not a fitted constant. d*·ln(10) lands near OMEGA_ZS and the residue is the mass gap.

---

## What it computes

H_NN candidate xp operator. d* gap workbench (gap=0.000707). T coordinate map scaffold. Open Problems 2 & 3.

`d_star_gap_report` and `gap_candidates` are the honest core of this module: they enumerate candidate expressions for d* and report the residual of each, rather than selecting the one that lands closest. The tautological candidate `Omega/ln(10)` reproduces d* to 5 significant figures by construction — it is listed as a candidate precisely so that it is visible as circular, not quietly used as a derivation.

## Results — run 2026-07-28

6/6 equations run argument-free; 0 require parameters; 0 fail.

| Equation | Tier | Run | Result |
|---|---|---|---|
| `T_map` | OPEN | ✓ | {'x': 1.0, 'd_star': 0.246, 'ln_x': 0.0, 'phase': 0.0, 'T_re': 1.0, 'T_im': 0.0, 'T_mod'… |
| `T_map_trajectory` | OPEN | ✓ | {'trajectory': [{'x': 0.1, 'd_star': 0.246, 'ln_x': -2.3025850929940455, 'phase': -0.566… |
| `d_star_gap_report` | OPEN | ✓ | {'d_star_spec': 0.246, 'd_star_taut': 0.24630720147342253, 'ln_10': 2.302585092994046, '… |
| `gap_candidates` | OPEN | ✓ | [{'expression': 'Omega/ln(10)', 'value': 0.24630720147342253, 'x_ln10': 0.56714329040978… |
| `h_nn_eigenvalues` | OPEN | ✓ | {'hbar_nn': 0.1, 'eigenvalues': [0.05, 0.15000000000000002, 0.25, 0.35000000000000003, 0… |
| `xp_spectrum` | OPEN | ✓ | {'x_values': [0.1, 0.2571428571428571, 0.41428571428571426, 0.5714285714285715, 0.728571… |

## Open

- The module's confidence floor is OPEN and stays OPEN. d* = 0.24600 is quoted to 5 significant figures from the BK spectral computation; whether that is exact or an approximation to something else is unsettled.
- Why ln(10) rather than any other base. See derivation_chain `d_star_tower_ln10`, which is also marked OPEN.

---

## The clock is built in — H = xp needs no camshaft (2026-08-31)

`H = xp` generates the dilation flow `x → eᵗx`. **The flow IS the clock** —
there is no external timing signal, the way a Wankel has no camshaft: port
timing is a consequence of geometry. The timing structure is the **4 : 3**: the
four faces of `d*` (Boundary / Stability / Flow / Translator) against the three
of Lambert W (`Ω_ZS`, the rotor faces). `lcm(4,3) = 12` — the phase never
repeats before twelve, so the semiclassical orbit precesses (the "flowers")
instead of closing.

**The EM-side reading — the Cymatic Nodal Line.** `RiemannHypothesisProof`
PAPER.md §6.3.1: `σ_RB` is the hypercomplex Riemann–Silberstein vector, so the
RedBlue field is Maxwell (`i ∂_t F = c ∇×F`, `Re F` = E, `Im F` = cB). `σ = ½`
is the line on which the functional-equation reflection is amplitude-perfect
(`|ξ(s)| = |ξ(1−s)|`), making the field a **pure standing wave** whose nodes are
the zeros — a Chladni figure. The **mass gap `Δ`** is then the width of the
first band above that nodal line: the first stroke of the same engine, the
ignition impulse of recombination (`wiki/bao_mass_gap.md` §"The gap is the first
motion"). Third bearing on `Re(s) = ½`, alongside Courant `Y₁⁰` and the
vanishing Noether current — none closes C1.

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| the spectral coordinate d* = 0.24600 | the H = xp spectral floor | 2 · SCALE | MINGLING | DEFINITIONAL | **FLAGGED** — deficit: is d* = 0.24600 exact, or an approximation to something else? |


Calibration: this verdict agrees with the page's stated status (**OPEN**).
