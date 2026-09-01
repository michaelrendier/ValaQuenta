# Engine: The Emerger — Sedenion Bracketing & Firing Order

**Module:** `modules/emerger/` (`maths.py`, `tools.py`)
**Class:** `EmergerModule`
**Version:** 0.1
**Confidence floor:** THEORETICAL
**Notebook:** [notebooks/engines/19_emerger.ipynb](../notebooks/engines/19_emerger.ipynb)
**Claim:** the grouping of imaginary sedenion units into brackets creates
different domains (ℂ / ℍ / 𝕆 / fragment); the domains' prerequisites force a
firing *order* of emergence; σ_RB's tilt-phase picks the entry point into that
order. The ascent-dual of Generational Lineage.

---

## What it is

A **dynamic permutative bracketer** for a Cayley–Dickson algebra. The real
component `e₀` is the **fixed anchor** — the *tilt to the i axis*. It is never
bracketed; every imaginary group is paired against it so the relationship
between a bracket and the real reference stays visible.

A **bracketing** is an ordered partition of the imaginary indices `{1..15}`
into named groups. Each group `G`, with the anchor, spans `span({e₀} ∪ G)`,
classified by closure:

| `|G|` | closed under its own products? | domain |
|---|---|---|
| 1 | yes | **ℂ** |
| 3 | yes | **ℍ** |
| 7 | yes | **𝕆** |
| any | no | **FRAGMENT** — a linear subspace, not a subalgebra; where zero divisors live |

The **firing order** — the order groups are approached — is load-bearing: each
bracket is conditioned on the ones fired before it. It can be **canonical**
(dependency), **σ_RB-phased** (`Σtilt` rotates the entry point into the 12-step
precession, 4 d\* faces : 3 Lambert-W faces, `lcm = 12`), or **any permutation**
(legality reported, not enforced).

## The five canonical brackets

| bracket | groups | emerges | descends from |
|---|---|---|---|
| **{1:15}** | `[{1..15}]` | Re, `N=\|x\|²`, conj, inverse — *grades the algebra* | the CD grading |
| **{2:14}** | `[{8}, rest]` | the pointer `z = x₀ + i·x₈`; `\|z\|`; `\|z\| − Ω_ZS` — *the read head* | {1:15} |
| **{8:8}** | `[{1..7}, {8..15}]` | `\|a\|−\|b\|` (distance from the ZD equator); sheet ±; `J₂` = L vs R | {1:15} |
| **{4:4:4:4}** | four quaternion blocks | four SU(2) phases; σ_RB tilt/axis; **`Σtilt` = net work around the loop** (= 0 ⇔ σ = ½) | {8:8} |
| **{4:8:4}** | gain blocks `{4..7}` / `{1,2,3,8..11}` / `{12..15}` | dominant gain class 0 / 1 / √2 — *multiplicative role* | {1:15} + {4:4:4:4} |

## Mechanism

- **σ_RB.** `ψ[k] = x[k] + i·x[(k+8) mod 16]`; `s[k] = ψ[k]·conj(ψ[k⊕4])`;
  `tilt = Re s` (Scale / Perfect Perturbation), `axis = Im s` (Flow). Oblique-Gear
  T1 ⇒ `s[k⊕4] = conj s[k]` ⇒ **`Σaxis = 0` identically**. `Σtilt = 0 ⇔ σ = ½`.
- **Firing phase.** Rational squash `Σtilt → s = Σtilt/(1+|Σtilt|) ∈ (−1,1) →
  u = (s+1)/2 → step12 = ⌊12u⌋ → entry bracket = step12 mod 5`. `gcd(12,5) = 1`
  so the 12-phase clock cycles all five brackets.
- **ZD tests are exact.** `is_zero_divisor(x)` = rank-deficiency of `Lₓ`
  (Gaussian elimination over `Fraction`). `on_zd_equator(x)` = purely imaginary
  AND norm-balanced across the CD-double boundary (`Re a = Re b = 0`, `|a| = |b|`,
  `a, b ≠ 0`) — the fixed set of the `J_red ↔ J_blue` swap. The full exact locus
  is `box_kite`'s 42 assessors / PSL(2,7); G₂ is the continuous blow-up.

Pure Python 3, `Fraction` throughout, float only at the output boundary.

## Results — run 2026-09-01 (`python3 -m ValaQuenta` → `emerger`)

`verify()` — **14/14 exact self-checks pass**, all derived from the CD table:

```
Sigma_axis == 0 (any input)              OK      e1+e2  is NOT a zero divisor    OK
T1 conj-symmetry holds                   OK      e1+e2  NOT on the ZD equator    OK
e1+e10 IS a zero divisor                 OK      e0 is a unit (not ZD)           OK
e1+e10 ON the ZD equator                 OK      domain_of({1})=C ({1,2,3})=H    OK
                                                 ({1..7})=O  ({1,5,9})=FRAGMENT  OK
n_legal_firing_orders = 4  (of 120 permutations; the canonical order is one)
```

**`emerge('e1+e10')`** (a zero divisor on the equator; `Σtilt = 0` → σ = ½ →
precession step 6/12 → entry bracket #1):

| step | bracket | emergent |
|---|---|---|
| 1 | {2:14} | `z = 0`, `\|z\| − Ω_ZS = −0.56714` |
| 2 | {8:8} | `\|a\|−\|b\| = 0`, **on_zd_equator = True**, **is_zero_divisor = True** |
| 3 | {4:4:4:4} | `Σtilt = 0`, `Σaxis = 0`, σ = ½, T1 holds |
| 4 | {4:8:4} | gain class = unit |
| 5 | {1:15} | Re = 0, `N = 2` |

**σ_RB rotates the order:** a tilted input (`Σtilt = −0.889`) fires
`{4:4:4:4} → {4:8:4} → {1:15} → {2:14} → {8:8}` — a different entry point.

**The permutation space** (`scale_partitions`): the 10 `{1,3,7}`-shapes of 15.
In the contiguous representative, **only the shapes led by one 𝕆 or 𝕆-then-ℂ… are
all-subalgebra**; every shape with an ℍ or 𝕆 group after the first contains a
FRAGMENT. The subalgebra bracketings are rare — most groupings make fragments.

## Confidence

| element | tier | why |
|---|---|---|
| CD algebra, `domain_of`, `is_zero_divisor`, `on_zd_equator`, `Σaxis = 0` | **ESTABLISHED** | exact, from the CD table; matches `box_kite` / `zero_lattice` |
| `Σtilt` = the σ_RB Scale detuning; `Σtilt = 0 ⇔ σ = ½` | **DERIVED** | Oblique-Gear T4 (`h_rb_hat`) |
| `Σtilt` = "net work around the 0→p→q→N loop" | **THEORETICAL** | a reading; the to-and-from frequency difference |
| the {2:14} pointer "carries Ω_ZS" | **THEORETICAL** | `16 − dim G₂ = 2`; `W(1)·e^{W(1)} = 1` lives on that ℂ line |
| the {4:8:4} gain-index assignment | **THEORETICAL** | a reading of the `{4:8:4}` canonical-maths note, not derived here |
| the σ_RB tilt-phase → firing order map | **THEORETICAL** | the 12-step precession is `add_scale_sign`'s "firing order" defect at sedenion scale |

**Open items**

- **A σ_RB phase can select a non-dependency-legal firing order**
  (`phased_is_legal = False` for `e1+e10`). The clock picks the entry phase; the
  engine reports the illegality rather than snapping to the nearest legal order.
- The toy semiprime embedding (`TuringStack/the_emerger.py`) is illustrative only.
- `on_zd_equator` is the sufficient basis-pair condition, not the full
  42-assessor locus.

## Related

- `box_kite` — the exact PSL(2,7) ZD geometry (NOT G₂). `zero_lattice` — 84/42 ZD pairs.
- `angular_rank` — the 16D oscilloscope; `{4,8,4}` as a check. `three_ring_scale` — the `{4:8:4}` grading as a spectral refinement of conformal infinity.
- `add_scale_sign` — `camshaft_defect` = "FIRING ORDER: `u_total − Σ u_parts`" at tier 0; `two_orderings` = chrono vs zeta (Generational Lineage).
- `archimedes_screw` — Ordinal / Zeta-Index / Digits / Spaces (the "Big 4") on `u = ln x`; `δ = ½ ln(q/p)` = a semiprime's entire hidden content.
- `scale` — `rsa_pathway_control` (RSA CRT-decrypt as the process-decomposition control).

## TuringStack — RSA / crypto results this engine feeds

The Emerger is the general form of the sedenion-bracketing done ad hoc across
`TuringStack`:

| TuringStack | what it does | Emerger relation |
|---|---|---|
| `the_emerger.py` | the first-pass numpy prototype of this engine | superseded by `modules/emerger/` |
| `wiki/ZD-locus-equatorial-geodesic-2026-09-01.md` | spinning Telperion sweeps `S¹⁴`; the ZD locus is its balance equator | the `{8:8}` bracket's `on_zd_equator` test |
| `fermat_sedenion_test.py` | do the Fermat coords `a=(p+q)/2, b=(q−p)/2` land on T32 ZD pairs? | a `{8:8}` + equator query on an RSA embedding |
| `hypercomplex_laplacian.py` | `Lₓ` IS the CD Laplacian; ZD pairs are its nodal lines; `dS/dn` across scales | the exact `left_matrix` / `mat_rank` here; the dynamic-lens sweep |
| `udeo_crypto/UDEO_RSA_DEMO.py` | 6 private-key-recovery methods, all scored vs control — **at chance except `d ≡ e (mod 4)`** | the multi-scale probes came back flat = a measurement of the modulus's depth-1 flatness |
| `references/logistic_bifurcation_RSA.png` (v2) | where the factoring *methods* live — **the modulus is NOT a bifurcation** | `N = a² − b²`, depth-1; the erased coordinate is one number |
