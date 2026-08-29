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

---

## Claim audit — "the spectral residue of the BAO was measured as the mass gap exactly" (2026-08-28)

**Disproven as stated; the weaker form stands.**

- The `residue` returned by `spectral_residue()` is **not measured from any
  decomposition** — line for line it is `BAO_CEILING − BAO_FLOOR`, the same
  `Ω_ζΣ − D*·ln10` subtraction as `GAP`. So `residue_equals_gap` is `True`
  **by construction** (`x == x`), not by measurement. The explicit-formula sum
  over zeros is a genuine convergence demonstration but — as the module
  docstring already says — *"not an input to Δ."* `residue_is_n_independent`
  was a hardcoded literal `True`; it is now actually computed at n ∈ {1, n, 5n}
  (still true, because n never enters the residue).
- **What is real:** `Δ = Ω_ζΣ − D*_spec·ln10 = 0.000707357533`, a
  zero-free-parameter subtraction — though `D*_spec` is carried to 5 sig figs,
  so `Δ` is really `≈ 7.07×10⁻⁴ ± ~2×10⁻⁶`. It is positive (⇒ a gap exists) and
  ≈ 0.4σ of the Planck 2018 BAO precision (⇒ resolvable in principle).
- **The identity `Δ = 1/(1000√2)` is approximate, not exact:**
  `1/(1000√2) = 0.000707106781`, residual `2.51×10⁻⁷` = **0.0354%** (3 sig
  figs). It is *consistent with* `D*`'s carried precision (the `D*` that makes
  it exact is `0.24600010890`, inside the last carried digit) — a consistency
  statement, not a measurement. The `10³` factor is **not derived** from
  framework constants (the open question the page already lists).
- **Undocumented lead (not a derivation):** `Δ ≈ 1/(100·|ρ₁|)` where
  `|ρ₁| = √(¼+γ₁²) = 14.1436 ≈ 10√2` (because `γ₁ = 14.1347 ≈ 10√2`) — agrees
  to 0.05%. This would read the `√2` as the first Riemann zero's height rather
  than only `sin 45°`, and the `1000` as `100·|ρ₁|`. Still a numerical
  coincidence at the ~0.05% level; the module does not use it.

**Bottom line:** `Δ > 0` is solid; `Δ = Ω_ζΣ − D*·ln10 ≈ 7.07×10⁻⁴` is solid
arithmetic at 3 sig figs; `Δ = 1/(1000√2)` and "measured as the residue exactly"
are **not** — the identity is a 3-sig-fig coincidence and the "residue" is the
same subtraction renamed. The generational-lineage FLAG (below) is correct; the
page's **ESTABLISHED** label overstates the identity and should read
ESTABLISHED on `Δ > 0` / THEORETICAL on the closed form.

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| the mass gap Δ = 0.0007073575 = 1/(1000√2) | the residue of the BAO spectral decomposition | 3 · ADD | MINGLING | DEFINITIONAL | **FLAGGED** — deficit: why 10³ in 1/(1000√2)? (the 1/√2 is the σ=½ symmetry; the 10³ is the doubling count / d*_RG — not derived) |


Calibration: this verdict **disagrees with** the page's stated status (**ESTABLISHED**).
