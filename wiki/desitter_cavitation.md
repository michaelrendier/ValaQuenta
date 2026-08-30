# Engine: De Sitter Cavitation — No Singularity: the Abrikosov-Vortex Core

**Module:** `modules/desitter_cavitation/`
**Class:** `DeSitterCavitationModule`
**Version:** 0.100
**Confidence floor:** THEORETICAL
**Notebook:** [notebooks/engines/18_desitter_cavitation.ipynb](../notebooks/engines/18_desitter_cavitation.ipynb)
**Fourth Age paper:** [`FourthAgePapers/DeSitterCavitation/`](../../FourthAgePapers/DeSitterCavitation/)
**Claim:** The black-hole interior is a finite, sub-Planckian de Sitter core — not a singularity.

---

## What it computes

**Calculation, not simulation.** Closed-form scalars, ratios and timescales — no
ODE integration, no field solve.

The interior is the Abrikosov vortex core made gravitational: the arithmetic /
spectral condensate goes to zero (a Riemann zero, winding number 1) while
density, pressure and curvature stay finite. A gravastar matching
(Mazur–Mottola 2001) forces the interior de Sitter radius `L_dS = r_s`. Over the
hole's life the core releases **stiff space** (metric, Λ-signed, `p = −ρc²`) and
**stiff matter** (radiative, ceiling `p = ρc²`, Zel'dovich), and at evaporation
it unwraps completely — the **De Sitter Cavitation**.

### HOLCUS prediction (pre-registered)

```
K_core(M) = 24 / L_dS^4 = 24 / r_s^4 = (3/2) · c^8 / (G^4 M^4)          [m^-4]
```

The maximum curvature invariant inside any black hole is the **de Sitter
Kretschmann scalar** at `L_dS = r_s`: finite for every `M > 0`, scaling as
`M^-4`, and **sub-Planckian for every `M > (3/2)^(1/4) m_Pl ≈ 1.107 m_Pl`**. Its
observational shadow is a gravitational-wave ringdown echo at delay
`≈ (2 r_s/c)·ln(r_s/ℓ_Pl)`, of order the interior light-crossing time.

**Falsifier:** a core curvature that either diverges (classical GR singularity)
or pins to the Planck value `K_Pl` independent of `M` (limiting-curvature /
Planck-star). Observationally: no ringdown echoes down to the reflectivity
bound a finite core requires.

---

## Mechanism

| step | statement |
|---|---|
| interior geometry | gravastar match `1 − (r/L)² = 1 − r_s/r` at the shell ⟹ `L_dS = r_s` |
| interior BANG time | `τ = 1/H_dS = L_dS/c = r_s/c = 2GM/c³` — one e-fold; the core cannot rest |
| core curvature | de Sitter `R_abcd R^abcd = 24/L⁴` at `L = r_s` ⟹ the Holcus formula |
| contrast | Schwarzschild interior `K(r) = 48 G²M²/(c⁴ r⁶) → ∞` as `r → 0` — the denied artifact |
| temperatures | `T_dS = ħH_dS/2πk_B = 2·T_H(M)` — both `∝ c³/GM`; the core inherits the hole's scale, doubled |
| two channels | stiff space `p = −ρc²` (Λ-signed) vs stiff matter `p = ρc²` (radiative ceiling) |
| partition (secondary) | `E_space/E_tot = 1 − d* = 0.754`, `E_matter/E_tot = d* = 0.246` |
| unwrapping | horizon recedes below the core as `M` evaporates ⟹ decompression ⟹ cavitation |

---

## Results — run 2026-08-30 (venv)

8/8 equations run; argument-free entries all pass.

### The Holcus check (10 M☉)

```
K_core                 = 3.1518e-17 m^-4
K_core (closed form)   = 3.1518e-17 m^-4      closed_form_matches = True
K_core / K_Planck      = 2.15e-156            (deeply sub-Planckian — smooth core)
Planck crossover       = 1.1067 m_Pl = (3/2)^(1/4) m_Pl
```

### `no_singularity_check` — PASS

| property | result |
|---|---|
| `K_core` finite for every M | ✓ |
| `K_core ∝ M^-4` (rung ratio test) | ✓ (rel err ≤ 1.6e-16) |
| `K_core < K_Planck` for M > crossover | ✓ |
| Schwarzschild `K → ∞` as `r → 0` (the contrast) | ✓ |
| **verdict** | **PASS** |

### Mass-class engineering table

| class | r_s (m) | τ_interior (s) | T_H (K) | t_evap (yr) | K_core (m⁻⁴) | K/K_Pl | QGP? | echo (s) |
|---|---|---|---|---|---|---|---|---|
| kugelblitz / primordial (10¹² kg) | 1.49e-15 | 4.95e-24 | 1.23e11 | 2.67e12 | 4.93e60 | 3.4e-79 | **yes** | 4.56e-22 |
| stellar (10 M☉) | 2.95e4 | 9.85e-5 | 6.17e-9 | 2.10e70 | 3.15e-17 | 2.2e-156 | no | 1.78e-2 |
| intermediate (10⁴ M☉) | 2.95e7 | 9.85e-2 | 6.17e-12 | 2.10e79 | 3.15e-29 | 2.2e-168 | no | 1.92e1 |
| supermassive (10⁹ M☉) | 2.95e12 | 9.85e3 | 6.17e-17 | 2.10e94 | 3.15e-49 | 2.2e-188 | no | 2.15e6 |

QGP (`ρ_core c² ≥ 1 GeV/fm³`) is reached only for `M ≲ 3 M☉` and for
primordial/kugelblitz mass — the `ρ_core ∝ M^-2` scaling makes the small holes
the hot ones. Every class is **sub-Planckian in core curvature by ≥ 78 orders**.

### Secondary (allowed to fail — kept in data)

- `energy_partition` default `1 − d* : d*` = `0.754 : 0.246`.
- `cosmic_cavitation_budget`: `Ω_cav ≈ Ω_BH·(1 − d*) ≈ 7.5e-6` vs `Ω_Λ ≈ 0.685`
  — **falls short by ~5 orders**. The mechanism is directional and cumulative,
  so its signature (if any) is **dark flow**, not a dark-energy magnitude.

---

## Confidence

| equation | tier | note |
|---|---|---|
| `kretschmann_core` | ESTABLISHED | a de Sitter identity; THEORETICAL as "the interior realises it" |
| `no_singularity_check` | THEORETICAL | internal-consistency scorecard, not a proof nature picks this interior |
| `mass_class_table` | ESTABLISHED | all closed form |
| `interior_timescales` | THEORETICAL | bounce/echo coefficients are O(1) and model dependent |
| `stiff_matter_ceiling` | ESTABLISHED | Zel'dovich stiff EoS |
| `energy_partition` | CONJECTURE | the `d*` split is a secondary prediction |
| `cosmic_cavitation_budget` | CONJECTURE | expected FALSIFIED-as-stated |
| `full_desitter_cavitation` | THEORETICAL | the unification |

---

## Open

- **No derivation that nature selects this interior.** The engine checks that
  *if* the interior is the gravastar/Abrikosov core, then `K_core` is the de
  Sitter value — it does not derive the core from a field equation.
- Bounce-time and echo-delay **coefficients** are model dependent (Haggard–Rovelli;
  Cardoso–Pani). Only the scaling (`τ ∝ r_s/c`, `Δt_echo ∝ (r_s/c)·ln`) is firm.
- The `d*` energy split is asserted, not derived. `cosmic_cavitation_budget`
  is expected to fail as a magnitude.
- Labelled-ZD note: the box-kite object is **PSL(2,7)** (order 168, Aut Fano);
  Moreno's G₂ is the blow-up that forgets the labelling — see `box_kite`.

---

*Ainulindale → ValaQuenta → the world. This engine calculates; it does not simulate.*
