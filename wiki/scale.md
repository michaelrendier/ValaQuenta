# scale — The Scale: Decompositional Analysis, Forwards and Backwards

`modules/scale/` · v0.1 · Status: **ESTABLISHED** (every equation below is
elementary complex analysis, independently verified in this module, not a
new theorem)

SCALE is tier-0 (generational-lineage skill §1, alongside ADD and SIGN).
This module pulls it out of a quantity and names what is left over —
both directions, at three different levels, with three different
answers.

---

## What it computes

| # | question | function |
|---|---|---|
| 1 | one point: exact forward/backward scale extraction | `polar_decompose` / `polar_recompose` |
| 2 | is the raw angle scale-blind under the two-ring fold? | `scale_invariance_under_self_rescale` (pre-fold), then folded directly — **NO** |
| 3 | what actually survives the fold, for every anchor? | `cross_ratio` / `verify_cross_ratio_is_scale_blind` — **YES** |
| 4 | does the fold have a true caustic (vanishing Jacobian)? | `verify_no_caustic` — **NO**, one isolated pole only |
| 5 | can the same discipline decompose a real algorithm? | `ProcessOperator` / `pathway_decompose` |

**Questions 2 and 3 are the same question asked twice, with different
answers, and both are kept on the page** — the rejected candidate is not
deleted once the accepted one is found.

---

## 1. Polar decompose/recompose — exact, always

```python
from ValaQuenta.modules.scale import polar_decompose, polar_recompose, verify_polar_round_trip

r, theta = polar_decompose(3.7 - 1.4j)
polar_recompose(r, theta)          # == 3.7-1.4j, to float precision
verify_polar_round_trip()          # {'max_round_trip_error': 1.16e-10, 'holds': True}
```

`r` is the scale (ordinal, comparable — you can rank two magnitudes).
`theta` is scale-blind under `Z -> lambda*Z` for real `lambda>0`, exactly
— checked directly across five widely different `lambda` (`0.01` to
`1000`), `theta` bit-identical every time.

## 2–3. The two-ring fold's OWN invariant — a rejected candidate, kept

```python
from ValaQuenta.modules.scale import mobius_fold, cross_ratio, verify_cross_ratio_is_scale_blind

# rejected: does arg(Gamma) survive rescaling Z around the ORIGIN?
# measured directly -- it does not.
for lam in (0.5, 1.0, 3.0, 50.0):
    g = mobius_fold(lam * (2.3+1.1j), 1.0)
    print(lam, abs(g), __import__('cmath').phase(g))
# arg(Gamma): 1.054 -> 0.381 -> 0.114 -> 0.007  (NOT constant)

# accepted: the cross-ratio of any four points, folded through the SAME
# map at four DIFFERENT anchors
verify_cross_ratio_is_scale_blind()['holds']    # True, to 1e-9, every anchor
```

**Why the angle fails:** the fold's fixed point is `Z0`, not `0`.
Rescaling `Z` around the origin is a symmetry of `arg(Z)` alone, not of
`Gamma=(Z-Z0)/(Z+Z0)`, so nothing guarantees it survives the fold — and
it measurably doesn't.

**Why the cross-ratio works:** it's the classical Möbius invariant —
preserved by *every* Möbius transformation, by construction, regardless
of which one (which anchor) you pick. Verified here on four wildly
different anchors including one nearly on the fold's own pole
(`Z0=0.01+0.01j`), matching to full numerical precision each time.

## 4. No true caustic

```python
from ValaQuenta.modules.scale import verify_no_caustic
verify_no_caustic()   # {'any_zero': False, 'holds': True}
```

`d(Gamma)/dZ = 2*Z0/(Z+Z0)**2` — checked across six points spanning
`10^-3` to `10^6` in magnitude: never zero, only diverging at `Z=-Z0`.
An optical caustic needs the Jacobian to *vanish*; here it only ever
*diverges*, at one isolated point. Different phenomenon, not conflated.

## 5. Process decomposition — the control case

```python
from ValaQuenta.modules.scale import ProcessOperator, pathway_decompose

# real RSA CRT-decrypt, p=61 q=53 (verified prime, not recalled)
ops = [
    ProcessOperator('m1', lambda cc: pow(cc, dP, p), depends_on=('input',)),
    ProcessOperator('m2', lambda cc: pow(cc, dQ, q), depends_on=('input',)),
    ProcessOperator('h',  lambda m1, m2: (qInv*(m1-m2)) % p, depends_on=('m1','m2')),
    ProcessOperator('m',  lambda h, m2: m2 + h*q, depends_on=('h','m2')),
]
pathway_decompose(c, ops, output_name='m')
# {'real': 65, 'dim': 4, 'order': ['m1','m2','h','m'], ...}
```

`m2` feeds **both** `h` and the final `m` — a genuine fan-out. Resolved
by dependency satisfaction, not assumed left-to-right, so this is
representable at all (a forced linear chain cannot express one node
feeding two downstream consumers without lying about the structure via
closures reaching around it — an earlier draft of this exact code did
that, and was corrected, not patched over).

---

## 6. The master identity — folding IS log-then-bound

```python
from ValaQuenta.modules.scale import fold_is_log_tanh, unfold_is_arctanh_exp, verify_fold_unfold_round_trip

verify_fold_unfold_round_trip()   # {'max_round_trip_error': 2.57e-13, 'holds': True}
```

`Gamma = tanh(½·ln(Z/Z0))`, exactly, for ANY complex `Z`, `Z0` — verified
directly against `mobius_fold()` on genuinely complex, off-axis points, not
just the real-axis special case found first. Folding **is** "take the log
of the ratio to your reference point, then bound it with `tanh`." Unfolding
is the mirror: `Z = Z0·exp(2·arctanh(Gamma))`. `compress_count` (the
WordNet-context module) is the log half of this same move, applied before
any fold; polar decompose (§1 above) is `ln(Z) = ln(r) + iθ`, the same
identity one more level upstream.

## 7. Locally square — automatic, not conditional

```python
from ValaQuenta.modules.scale import verify_locally_square
verify_locally_square(1.7+0.9j, 1+0j)   # equal_magnitude=True, angle_degrees=90.0, holds=True
verify_locally_square(-3+4j, 2-1j)      # same, at a totally different point/anchor
```

At any point, the tangent vectors along increasing `ring1` (constant
`ring2`) and increasing `ring2` (constant `ring1`) are **always** equal in
magnitude and exactly 90° apart — regardless of what `ring1`/`ring2` mean
physically. This is **not** a property that requires the two rings to be
specially related (e.g. harmonic conjugates of some underlying field) — it
is a property of `mobius_fold` being holomorphic in `Z`, inherited
automatically the instant two numbers get used as `Z`'s real/imaginary
parts. A curvilinear "4-sided shape" is a locally-square cell *by
construction*, for any two-ring pair whatsoever.

A **separate, stronger, optional** fact — not claimed here in general,
testable per pair — is whether a *given* `ring1`/`ring2` also happens to be
a genuine harmonic-conjugate pair of some underlying field, the way
velocity-potential/stream-function are in 2D fluid dynamics (`w=φ+iψ`,
governed by the Cauchy-Riemann equations — a coupled PDE system). When that
holds, `Z` isn't just "two numbers folded" — it's a genuine complex
potential over whatever domain the object came from. Whether any specific
pair below has that extra structure is noted per pair, not assumed.

## 8. User-defined rings — the engine takes ANY two relationships

```python
from ValaQuenta.modules.scale import custom_ring_chart

custom_ring_chart(my_object, ring1_fn=lambda o: ..., ring2_fn=lambda o: ...,
                  Z0=complex(1,0), ring1_name='...', ring2_name='...')
```

No built-in special cases — `ring1_fn`/`ring2_fn` are arbitrary callables of
one object. Five pairs were tested directly (2026-08-25), real data, not
speculation:

| ring1 | ring2 | Result | Honest finding |
|---|---|---|---|
| raw count `n` | `compress_count(n)` | `n=1→\|Γ\|=0.79`, `n=1000→\|Γ\|=0.98` | **Same saturation lesson as Phase 31/32**: one unbounded raw axis dominates and drags everything toward the boundary as it grows. Confirms, doesn't discover anew. |
| inertia (`v[0]²`) | Shannon entropy of `\|v_k\|²` | 4 real sentences, `Γ` spread `0.10`–`0.79`, no saturation | Well-conditioned — both axes are naturally bounded (inertia ∈[0,1], entropy ∈[0,4] for 16 dims), genuinely differentiates short vs. long text |
| RSA ciphertext (forward) | RSA plaintext (backward) | 4 messages, `\|Γ\|` `0.25`–`0.44` | Both axes comparable in scale (mod `n=3233`), no saturation; a real forward/backward pair through the same modular function |
| Lagrangian proxy (kinetic−inertia) | distance to `Ω_ZS` (cardioid attractor) | 4 sentences, `Γ` spread across most of the disk | `kinetic` here is a variance-of-`\|v_k\|` **proxy**, not `box_kite`'s own `local_curvature` (a different repo, not imported cross-repo per this project's convention) — labeled as a proxy, not the real thing |
| `J_red` | `J_blue` | **`J_red + J_blue = 1.0000000000` exactly, every time, checked to 10 decimal places** | **Not two independent rings.** `cam_encode` returns a unit vector and RED/BLUE partition all 16 dims with no overlap, so this pair is constrained to the line `ring1+ring2=1` — one degree of freedom (`σ_self`), not two. The genuinely two-independent-ring version would pair `σ_self` against `J_green` (the emergent commutator quantity, `[J_blue,J_red]=J_green` — wiki Phase 3) instead of `J_red` against `J_blue` directly — not built here, a real next step if wanted. |

The last row is the important one: **testing catches a degenerate pairing
that looks like two rings and is actually one.** That's exactly what this
instrument is for.

## Honest scope

Works in complex floats throughout (`cmath`), not `fractions.Fraction` —
an explicit, stated exception to the usual module convention, because the
domain (Möbius transformations, `tanh`, cross-ratio) is inherently
transcendental and `Fraction` has no complex-number support in the
standard library.

"Ring" here (two-ring *families* — RF-engineering slang for concentric
circle families) is not the same object as "ring" in abstract algebra.
Checked, not asserted: Möbius transformations under composition form a
*group* — the group of units of the `2x2` complex matrix ring `M_2(C)`
(matrix multiplication = fold composition). Real, but one level
underneath, and only the multiplicative half is operationally used by
chaining folds — see [[ring_theory]] for the actual ring-theoretic spine
of this project, which lives in a different place (`SedenionFactoralRelativity`)
for a different, factoral reason.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| SCALE pulled out of a quantity, forwards and backwards | polar_decompose / cross_ratio (the two-ring fold) | 0 · SCALE | LAURELIN | DEFINITIONAL | **CLEAN** |


Calibration: this verdict agrees with the page's stated status (**ESTABLISHED**).

## Related

[[ring_theory]] (the sibling "a familiar word already present" page, one
tier down); `SedenionFactoralRelativity/engine/lineage.py` PW13 (`chart_scale_factor`),
PW14 (`pathway_decomposition`), PW15 (`cross_ratio`) — the same results,
proven first in that engine; this module is an independent port, not an
import, per this project's per-repo self-containment convention.
`PtolemyDesktop/Kryptos/Ciphers/{Vigenere,Enigma,RSA}.py` — the real
ciphers this instrument was built against.
