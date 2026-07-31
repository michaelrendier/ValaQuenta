# Engine: The Mass Gap — spectral residue of BAO

**Module:** `ValaQuenta/modules/bao_mass_gap` — `maths.py` + `tools.py`
**Registry name:** `bao_mass_gap` **Version:** 0.131 **Equations:** 7
**Notebook:** [notebooks/core/19_bao_mass_gap.ipynb](../notebooks/core/19_bao_mass_gap.ipynb)
**Ainulindale wiki:** [50_bao_mass_gap_engine.md](../../Ainulindale/wiki/50_bao_mass_gap_engine.md)

**Claim:** The mass gap is the residue of the BAO spectral decomposition — the
band between the acoustic ground state and the thermal information ceiling that
no standing wave absorbs.

```
Δ = Ω_ζΣ − D* × ln(10) = 0.0007073575 = 1/(1000√2)
```

Zero free parameters. 7/7 checks pass.

Supersedes the standalone script `ValaQuenta/bao_mass_gap.py`.

---

## Results (run 2026-07-30)

```
OMEGA_ZS = 0.5671432904097838   Lambert W(1) — exact transcendental
D_STAR   = 0.24600              spectral ground state — 5 sig figs
LN10     = 2.302585092994046

floor    D*·ln10    = 0.5664359329   BAO acoustic ground state
ceiling  Ω_ζΣ       = 0.5671432904   thermal information ceiling
residue  Δ          = 0.0007073575   absorbed by no standing wave
closed   1/(1000√2) = 0.0007071068   the Red/Blue symmetry point

7/7 checks pass    free parameters: 0
```

---

## Why it is a residue

The explicit formula decomposes the prime distribution into a ground state plus
one standing wave per non-trivial zero:

```
ψ(x) = x − Σ_ρ x^ρ/ρ − ln(2π) − ½ln(1 − x⁻²)
       ▲   ▲
       │   └── spectral oscillations: one standing wave per γ_n
       └────── de Sitter expansion term: the ground state
```

Read at the BAO scale this is the acoustic spectrum of the CMB:

| Term | Reads as |
|------|----------|
| `x` | de Sitter expansion — the acoustic ground state — Hubble flow |
| `Σ_ρ x^ρ/ρ` | acoustic oscillations — one standing wave per Riemann zero |
| `ln(2π)` | boundary normalisation |
| **residue** | **absorbed by no standing wave — the gap** |

The natural BAO coordinate is `x_BAO = exp(1/Ω_ζΣ) = 5.8312001357` — the scale
at which the information ceiling is exactly one nat. Each zero contributes
amplitude `1/|ρ| = 1/√(¼+γ²)`, strictly decreasing in γ, so `γ₁ = 14.134725`
sets the largest single excitation above the ground state at amplitude
`0.0707035284`.

**The residue is a difference of two constants.** Sum 1 zero or all 20 — the
spectral sum converges, the residue does not move. Spread over n = 1..20 is
exactly 0.0. The notebook demonstrates this directly; the engine asserts it as
`residue_is_n_independent`.

---

## The identity

```
Δ ≈ 1/(1000√2) = 1/√(2×10⁶) = 0.000707106781187
residual  2.508e-07   (0.0354%)
```

`1/√2 = sin(45°) = cos(45°)` — the angle of maximum Red/Blue symmetry at σ=½,
where the forward current equals the backward current. The √2 is the first
Cayley-Dickson doubling.

**Write it `1/(1000√2)` or `1/√(2×10⁶)`.**

| Expression | Value | Ratio to Δ | |
|---|---|---|---|
| `1/sqrt(2000)` | 0.022360679775 | 31.61 | **WRONG — 31.6× too large** |
| `1/(1000*sqrt(2))` | 0.000707106781 | 0.9996 | correct |
| `1/sqrt(2e6)` | 0.000707106781 | 0.9996 | correct |

Misreading this is the single easiest way to misread the whole engine, so the
engine carries `GAP_WRONG_FORM` and the notebook prints all three side by side.

---

## Constants

| Symbol | Value | Role |
|---|---|---|
| `d*_spec` | 0.24600 | the carried spectral value — ACTIVE |
| `d*_taut` | 0.2463072... = Ω_ζΣ/ln(10) | tautological — gap = 0 by construction, reference only |
| `d*_exact` | 0.2460001089... | the D* at which Δ = 1/(1000√2) exactly |

`d*_spec` is carried to 5 decimal places. The identity pins D* to
`0.2460001089`, which is `1.089e-07` from the carried value — inside the last
carried digit. The residual measures D*'s precision, not the identity.

`d*_taut` has zero gap by construction. It is not a result. Do not use it as the
active value.

**Open derivation:** the `1/√2` factor is accounted for — σ=½ symmetry, first
Cayley-Dickson doubling. The `10³` factor is not yet derived from framework
constants. Precise form of the question: *at what algebraic constraint does
`d*_BK × ln(10) + 1/(1000√2) = W(1)` exactly?*

---

## Equations

| Equation | What it does |
|---|---|
| `summary` | one-screen landing view — the headline |
| `gap_value` | Δ = Ω_ζΣ − D*·ln10, two constants and one subtraction |
| `spectral_residue` | the BAO decomposition — why the gap IS a residue |
| `gap_identity` | Δ = 1/(1000√2), the Red/Blue symmetry point |
| `bao_consistency` | Δ against the Planck 2018 acoustic scale |
| `mtheory_compactification` | 11 = 4+7, G₂ holonomy, one vacuum |
| `validate` | all 7 checks |

`spectral_residue` takes one parameter, `n_zeros` (default 20), and supports the
`complex_plane` display mode — the zeros on the critical line, marker area
proportional to `1/|ρ|`.

---

## Checks

| Check | Result |
|---|---|
| `gap_positive` | PASS — ceiling > floor |
| `gap_in_range` | PASS — 5e-4 < Δ < 2e-3 |
| `identity_3sf` | PASS — Δ = 1/(1000√2) to 3 sig figs |
| `identity_in_d_star_precision` | PASS — d*_exact inside D*'s last digit |
| `residue_equals_gap` | PASS — spectral residue reproduces Δ exactly |
| `bao_resolvable` | PASS — Δ/σ_BAO = 0.4002 > 0.1 |
| `dimension_count_exact` | PASS — 11 − 4 == 7 as `Fraction` |

---

## Acoustic scale

Planck 2018: sound horizon at the drag epoch `r_s = 147.09 ± 0.26 Mpc`,
fractional precision 0.177%.

```
Δ/σ_BAO = 0.00070736 / 0.00176763 = 0.400174
```

Above the noise floor — a resolvable feature of the acoustic spectrum.

---

## Compactification

`11 = 4 observable + 7 compact`. The compact 7 carry G₂ holonomy;
`G₂ = Aut(𝕆)`. The 7 directions are the imaginary octonion units `e₁..e₇` —
algebraic, never spatial.

The compactification scale is Δ. Δ is computed, not tuned, so it is not a
modulus. No moduli, no landscape: `10^500 → 1`.

Dimension arithmetic is carried as `Fraction`, so `11 − 4 == 7` is exact rather
than a float comparison.

---

## Usage

```python
from ValaQuenta.modules.bao_mass_gap import maths as bmg

bmg.GAP                    # 0.0007073575332...
bmg.gap_value()            # the subtraction, with ordered derivation steps
bmg.spectral_residue()     # the BAO decomposition
bmg.spectral_residue(50)   # more zeros — residue does not move
bmg.validate()             # all 7 checks
```

Through the registry:

```bash
python3 -m ValaQuenta --info        # bao_mass_gap registers first
python3 -m ValaQuenta --curses      # console: MODULES pane, top entry
```

Every `compute()` returns a `derivation` key — an ordered list of the operations
performed. The console renders that list as the proof chain.

Shell commands: `gap`, `identity`, `residue`, `validate`.
