# Engine: Fixed Point

**File:** `fixed_point.py`  
**Class:** `FixedPoint`  
**Claim:** The Cayley-Dickson tower has two fixed points — The Unit (V(0)=1) and T_256 — and the gap between them is the mass gap.

---

## What it computes

```
Fixed Point Engine — The Boundary
```

## Results — run 2026-07-28

Paper: 'The Zero Tree', FourthAgePapers.

The two fixed points and the measured gap between them:

```
FP_trivial:  The Unit  dim=1    V=1.000000     n_imag=0
FP_maximal:  T_256     dim=256  V=1.1195e-152  n_imag=255
GAP between them: 7.073575e-04
```

The angular quantum halves at every CD doubling: 180° at ℂ, 90° at ℍ, 45° at 𝕆, 22.5° at 𝕊 (first ZD), down to 1.40625° at T_256. Below that spacing the 256 basis elements are indistinguishable and collapse back to 1 — The Unit. All roots become 1.

The N-ball volume V(n) peaks at n*=5.2569 and then falls away: V(0)=1 exactly, V(5)=5.263789 at peak differentiation, V(16)=0.235331 at the sedenion level, V(256)=1.1195e-152 where the volume is all boundary.


## The Null Operator

`e₀ = 1` is the multiplicative **identity** of the algebra — The Null Operator.
It never participates in zero-divisor crossings and it is the reference axis of
the Cayley-Dickson tower.

This matters when reading results from this engine: where a computation returns
the identity, or `V(0)=1`, or an unchanged value, **that is the answer, not a
missing one**. NULL-as-identity is the operative convention — nothing × nothing
= p; the prime IS a singularity in factor space. An engine reporting e₀ has not
failed to produce a result.

## Constants

| Name | Value |
|---|---|
| `CD_MAX` | 8 |
| `D_STAR` | 0.246 |
| `GAP` | 0.000707357533248576 |
| `N_STAR` | 5.25694640446261 |
| `OMEGA_ZS` | 0.5671432904097838 |
| `SIGMA_HALF` | 0.5 |
| `UNIT_VOLUME` | 1.0 |

## Entry points

`angular_quantum_sequence()`, `bang_as_evaporation()`, `gravastar_shell()`, `inside_out_horizon()`, `roots_of_unity_collapse()`, `run_all()`, `transformer_profile()`, `two_fixed_points()`, `v_nball()`, `v_nball_peak()`, `virtual_particle_regime()`

## Open

- The Bang-as-gravastar-evaporation reading in section [7] is an interpretation of the geometry, not a derivation from it.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| the two fixed points of the iteration map; V(0)=1 | solve ker(M − I) | 2 · SIGN | MINGLING | DEFINITIONAL | **CLEAN** |


Calibration: this verdict agrees with the page's stated status (**ESTABLISHED**).
