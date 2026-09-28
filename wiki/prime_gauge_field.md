# Engine: The Prime Gauge Field

**Module:** `modules/prime_gauge_field/` (`maths.py`, `tools.py`)
**Class:** `PrimeGaugeFieldModule`
**Version:** 0.1
**Confidence floor:** THEORETICAL
**Notebook:** [notebooks/engines/20_prime_gauge_field.ipynb](../notebooks/engines/20_prime_gauge_field.ipynb)
**Related paper:** `FourthAgePapers/FastInverse/README.md`
**Claim:** Smith's map `Γ(s)=(s−1)/(s+1)` (the SCALE engine's own global
conformal chart) reduces to *two* candidate local-scale connections, one
provably flat for structural reasons and one that genuinely is not — and
the pre-registered prediction about where the second one goes flat is
*partially* right, checked honestly rather than fitted after the fact.

---

## Origin — the question the Schwarzian check didn't answer

`.claude/scratchpad/2026-09-21_smith_apollonian_uft_probe/` tested whether
`Γ` carries classical gauge curvature and found its Schwarzian derivative
exactly zero. Correct — and narrower than it reads. That test used a
single, fixed, **global** Möbius map. "Gauge" is Weyl's own word (1918):
he tried to unify gravity and electromagnetism by making **scale itself**
a *local*, position-dependent freedom (`Eichinvarianz`) rather than a
fixed global constant, and the curvature of *that* connection was the
first thing ever called gauge curvature — built entirely from the
tier-0 SCALE operator made local. A global transformation was never
going to carry it, by construction. This engine runs the local question.

## The two connections

**`A = grad(log|Γ|)`** — always flat, for *any* holomorphic scalar, by
the Poincaré lemma (`d(df) ≡ 0`). Included explicitly so the contrast is
visible: this generalizes the earlier Schwarzian-zero finding to every
holomorphic map, not something special about `Γ`.

**`A = (Re Γ(s), Im Γ(s))`** — `Γ` read directly as an `ℝ²`-valued
1-form, *not* collapsed into a gradient of one scalar. This one carries
genuine curvature:

    F(s) = ∂A_y/∂x − ∂A_x/∂y = 2·Im(Γ'(s))     (exact, Cauchy-Riemann)

Verified against a finite-difference numeric derivative before being
trusted anywhere downstream — `curvature()` vs `curvature_numeric()`,
max error `~1e-11` over 200 random points.

## The pre-registered prediction, and what actually happened

`FourthAgePapers/FastInverse/README.md` stated, before this engine was
written: the connection's flat locus is the construction's
trivial/vacuum point — where the local scale freedom does no work.

Found, closed form, checked on 2000 random points (`prediction_check()`,
0 mismatches):

| locus | `F(s)` | matches the prediction? |
|---|---|---|
| the real axis (`t=0`) | exactly 0 | **partially** — `Γ` is real-valued here, a defensible "trivial phase" reading |
| `σ=−1` (through `Γ`'s own pole) | exactly 0 | **not predicted** — a genuine new feature |
| everywhere else | nonzero | — |

Reported as a partial match, on purpose — the pole-line locus was not
named in advance and should not be quietly folded into the prediction
now that the computation is in hand.

## Reproduce

```python
from ValaQuenta.modules.prime_gauge_field.maths import report, verify, prediction_check

report(0.5 + 0.1j)     # Gamma, the connection, both curvatures, the zero-locus check
verify()                # the three self-checks in one call
prediction_check(2000)  # the honest sweep against the pre-registration
```

## Related

- `GenerationalLineage/engine/toolsets/scale.py` — `Γ`, `local_scale_factor`, the object this engine is built directly on top of, not reimplemented.
- `Ainulindale/wiki/121_fast_inverse_square_root_of_the_two_trees.md` — the Weyl citation and the Wiener-attack sibling instance.
- `Ainulindale/wiki/122_the_prime_gauge_field.md` — this engine's Ainulindale-side wiki page.
- `.claude/scratchpad/2026-09-21_smith_apollonian_uft_probe/` — the origin experiment.

## Provenance

Moved from the module docstring: a docstring instructs the caller and holds no history; this section is the record.

> Origin: the 2026-09-21 gauge-field experiment
> (`.claude/scratchpad/2026-09-21_smith_apollonian_uft_probe/`) found
> Gamma's Schwarzian derivative exactly zero -- a single, fixed, global
> Mobius map correctly carries no classical gauge curvature. "Gauge" is
> Weyl's own word (1918): he tried to unify gravity and electromagnetism by
> making SCALE a LOCAL freedom rather than a global constant, and it is
> THAT connection's curvature this module tests, not the global map's.
