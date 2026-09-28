# add_scale_sign — ADD / SCALE / SIGN: the tier-0 floor, and the roll-down

`VAPMIP/add_scale_sign.py` (the decomposition maths — four-question test,
roll-down) · **`ValaQuenta/modules/add_scale_sign/` (the DATATYPE — `ASS`,
`ASSWord`, `AddScaleSignModule`)** · `SedenionFactoralRelativity/engine/lineage.py`
(`root_irreducible`, `ROOT_OF`, `AFF1`) · `VAPMIP/engines/e10_generational_lineage.py`
(`r_add_scale_sign_floor`, `decompose_operation`) · v0.1 · Status:
**ESTABLISHED** (the group structure is elementary; the {0, 1, √2} spectrum
and the one-bit sign structure are measured at run time, not asserted)

The `generational-lineage` skill §1 names three irreducibles and stops there.
This page is the reference the skill did not carry: **what the three are, how
they fit together as a group, and how to roll any named operation all the way
down to the one it rests on.**


**Reference:** every equation with its parameters — [toolbox](toolbox/02_add_scale_sign.md) · API — [add_scale_sign](https://michaelrendier.github.io/ValaQuenta/api/modules/add_scale_sign.html). This page is the record; it holds no API.

---

## 1. The three

| irreducible | identity | content | gain | axis | group factor |
|---|---|---|---|---|---|
| **ADD**   | `0`          | the flow · the fold **count** · order-dependent | 0 | `{+, −}` | `ℝ` (translations) |
| **SCALE** | `1`          | the **size** · the gain · ≅ ADD in the log chart | 1 | `{×, ÷}` | `ℝ_{>0}` (dilations) |
| **SIGN**  | even parity  | the **direction** · one bit, nothing between · det ±1 | — | one bit | `ℤ/2` (the flip) |

`0` and `1` are free because they are the identities of the first two — which
is why neither can be prime, why they are tier 0, and why they sit off both
Two Trees (the Mingling). `+1` is SIGN's identity; the three identities
`(0, 1, +1)` are the three "does nothing" elements.

---

## 2. The group: Aff(1, ℝ) = ADD ⋊ (SCALE × SIGN)

    Aff(1, ℝ) = ℝ ⋊ (ℝ_{>0} × ℤ/2) = ADD ⋊ (SCALE × SIGN)
              = (fold COUNT) ⋊ (fold SIZE × fold DIRECTION)

The product is **semidirect, not direct**. SCALE and SIGN reparametrise ADD:
dilate-then-translate ≠ translate-then-dilate, and the difference is a
translation. Written as a bracket, the **only non-trivial one** is

    [SCALE, ADD] = ADD

SIGN and SCALE commute; SIGN and ADD commute up to the flip. So "order
matters" in this floor is entirely a statement about **ADD** — which is why
ADD wants a positional encoding and SCALE/SIGN want a multiplicative one
(skill §4).

- **ADD alone** is affine: no fixed point.
- **SCALE alone** is linear: fixes `0`.
- **Together** they are every 1-D similarity transform.
- **SCALE ≅ ADD** as abstract groups, via `log` / `exp` — the log chart is
  where a SCALE problem becomes an ADD problem (gcd = one division = the LCA;
  `radical_distance` = `log a + log b − 2·log gcd(a,b)`).

---

## 3. What it computes

| # | question | function | result |
|---|---|---|---|
| 1 | classify a spec against the four-question test (skill §3) | `classify(OpSpec(...))` | tier, `IS` (if it is one of the three), `root`, tree |
| 2 | classify a bare **name**, no flags | `describe(name)` | same, using the known-spec table; roll-down root wins over flag inference |
| 3 | roll a named operation down to its tier-0 root | `root_of(name)` / `SFR.root_irreducible(name)` | `'ADD'` \| `'SCALE'` \| `'SIGN'` \| `None` |
| 4 | verify the floor is exactly these three | `e10 … r_add_scale_sign_floor` | HOLDS — spectrum `{0, 1, √2}`, sign is one bit |

`None` from `root_of` on a **known** operation is a table gap (fill it); on an
**unknown** operation it is the skill-§5 emergence signal — the domain is
incomplete, and that is a bigger claim than a new name.

---

## 4. The roll-down

`decompose()` (SFR) places an operation on a tier and names its immediate
parent. `root_irreducible()` finishes the walk — past REFLECT / DILATE, past
every fixed set and every count — to the one tier-0 irreducible underneath.

**REFLECT is SIGN + a fixed axis.** So:

- anything whose content is a reflection, a parity, or a **fixed set of** a
  reflection → roots on **SIGN**
  (reflect, rotate, vector, boundary, origin, fulcrum, anchor, balance, ideal,
  radical, zero-divisor, basin, chirality, factorial, factoral, leverage,
  associator, orbit-curvature)
- anything that **changes a length** → roots on **SCALE**
  (dilate, contract, quotient, bifurcation, spiral, tuning, unit, self-similar,
  fractal, lyapunov, gcd)
- only the **raw flow / count** → roots on **ADD**
  (derivative, pathway, primary-decomposition, orbit-trap)

### Results (from code, 2026-08-27)

```
operation        tier   IS      ROOT    status
translation        0    ADD     ADD     IRREDUCIBLE
multiplication     0    SCALE   SCALE   IRREDUCIBLE
dilate             1    SCALE   SCALE   DERIVED
reflect            1    SIGN    SIGN    DERIVED
origin             2    —       SIGN    DERIVED
pathway            2    —       ADD     DERIVED
factorial          3    —       SIGN    DERIVED
leverage           3    —       SIGN    COROLLARY
associator         3    —       SIGN    DERIVED
the number 1      −1    —       —       IRREDUCIBLE (Mingling)
```

`e10 … r_add_scale_sign_floor` → **HOLDS** (9/9 relations in the engine):
the sedenion zero-divisor gain spectrum is exactly `{0, 1, √2}` — two free
(the identities), one irrational price — and every non-commuting unit pair
disagrees by a **pure sign flip**, so SIGN carries one bit with nothing
between.

---

## 5. Folds, not steps — and the recent decomposition paths

The affine triple reads as **fold count / fold size / fold direction**, not
step. Mountain-fold vs valley-fold is SIGN. Origami is a partitioning
algorithm; the Two Trees domain is the factoring map; **folding = partitioning
= factoring**, all the way up and down the tower.

- **primes** — SIGN recursed over the ordered pathway of prior primes. Each
  sieve rung is SIGN (the divisibility bit) over SCALE-generated multiples,
  marched by ADD, mex-selected; recursion depth `π(√n)`. A prime's definition
  — "for all `q < p`: `q ∤ p`" — references every prior prime. Not a constant
  number, a **constant hierarchical pathway**.

- **the Sieve IS the generational lineage** (measured 2026-08-27; `e10` R10–R12,
  `SFR sieve_lineage` / `sieve_recurrence`). Composite `n` is first struck on
  the pass of prime `spf(n)`, and **`generation(n) = π(spf(n))`** exactly — the
  ordered prime list *is* the decompositional order (the ordinal values). The
  sieve is one deterministic forward sweep of `π(√N)` passes — no iteration to
  a fixed point, no backtracking — which is why the factoral lineage is
  **stable**: one pass per prime, not a convergence.
  - **Fibonacci under factoring waves.** Legendre's count obeys
    `φ(x, a) = φ(x, a−1) − φ(x/pₐ, a−1)` — Fibonacci's linear two-term shape,
    except the second term's argument is **SCALE-shifted by a prime** (a
    factoring wave) instead of index-shifted by 1. Fibonacci is the degenerate
    "`pₐ` acts as a `+1` shift" case.
  - **Closed form = ADD ∘ SIGN ∘ SCALE**: `φ(x, a) = Σ_{d | Pₐ} μ(d)·⌊x/d⌋` —
    a superposition of signed division waves (32 `+`, 32 `−` at `a = 6`).
  - **Ordering.** The final prime set and the disjoint first-mark partition are
    order-invariant. `generation = π(spf)` holds **only** for the ordinal
    (ascending-prime) order, which also minimises the generation entropy
    (`2.56` bits vs `3.69` for a Riemann-ζ weight order `ln p/√p`, `5.07` for
    greatest-prime-first) — pass 0 alone strikes every even, `55%` of all
    composites in one wave. The ordinal order is the canonical,
    maximum-compression decomposition order.
- **factorial** — the **multiplicative integral**: `n! = ∏_{k=1}^n k`. Its
  un-integral is the ratio of consecutive terms, `n!/(n−1)! = n`, exactly, no
  `+C`. After `log`: `ln(n!) = Σ ln k`, and `ln(n!) − ln((n−1)!) = ln n`
  exactly — a cleaner inverse pair than `d/dx` vs `∫` (which loses the
  constant). In lineage terms factorial = the order of the coordinate
  reflection group = SIGN-compositions counted → tier 3.
- **e** — quantization, not growth. `e` is the base that makes `ln` a
  step-counter: one `e`-multiply advances `ln` by exactly 1. `d/dx eˣ = eˣ` is
  the **fixed point** of differentiation (step = state), not a rate.
  `e = Σ 1/k!` — a sum over discrete arrangements.
- **Flattening Syndrome** — viewing the SCALE spiral (`u = ln x`, the
  Archimedes-screw pitch axis) through a lossy flat circle. The discarded
  axial coordinate re-manifests as apparent retrocausality / false cyclicity /
  degeneracy. `u = ln x` is the anti-flattening coordinate; recurrence stops
  being paradoxical once you carry it. See [scale.md](scale.md),
  `archimedes_screw.md`, and `project_flattening_syndrome` (memory).

---

## 6. Where it is wired

| repo | entry point | what it adds |
|---|---|---|
| VAPMIP | `add_scale_sign.py` | the shared primitive: `classify`, `describe`, `root_of`, `AFF1`, `FINDINGS` |
| VAPMIP | `engines/e10_generational_lineage.py` | `r_add_scale_sign_floor` (R9) + `decompose_operation()`; **`r_sieve_is_lineage` (R10), `r_sieve_two_term_recurrence` (R11), `r_sieve_ordering` (R12)** + `sieve_lineage(N, order)` |
| SFR | `engine/lineage.py` | `root_irreducible()`, `ROOT_OF`, `AFF1`; `decompose()` now returns `root`; **`sieve_lineage(N, order)`, `sieve_recurrence(x, a)`** |
| SFR | `engine/bio.py` | **STUB** — the biological factoral tower (`TOWER_LEVELS`: knot 𝕊/16 → molecule T₃₂ → DNA T₆₄ → protein T₁₂₈ → genome T₂₅₆); `molecular_decomposition`, `dna_decomposition` (`plan_only=True` returns the path; structural only, no medical inference) |
| SFR | `engine/__init__.py` | re-exports all of the above |

The existing SFR `decompose(operation)` (the §3 four-question test, 40-entry
`TIERS` table) is unchanged except for the added `root` key. `e10`'s eight
σ-anatomy relations are unchanged; R9 is additive.

---

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| the tier-0 floor ADD ⋊ (SCALE × SIGN) | classify / roll any op down to its root | 0 · SIGN | TELPERION | DEFINITIONAL | **CLEAN** |


Calibration: this verdict agrees with the page's stated status (**ESTABLISHED**).

---

## The datatype — `ValaQuenta/modules/add_scale_sign/` (2026-08-28)

**Formal specification:** `Ainulindale/wiki/107_add_scale_sign_datatype.md`
(canonical) · SFR-side: `SedenionFactoralRelativity/wiki/ADD-SCALE-SIGN-Datatype.md`.

A Python value type for elements of `Aff(1,ℝ)`: `x ↦ sign·scale·x + add`.
Like `str` carries `split`/`strip`/`replace`, `ASS` carries its own
manipulation surface. **No redundant maths** — the four-question test and
roll-down stay in `VAPMIP/add_scale_sign.py`; this is the value type.

| | |
|---|---|
| construct | `ASS(add, scale, sign)` · `ASS.ADD(a)` `ASS.SCALE(s)` `ASS.SIGN(g)` · `ASS.GROUND` |
| forward | `a @ b` (compose) · `.then(b)` · `.__call__(x)` (apply) |
| backward | `~a` (invert) — reverses **and** inverts the record |
| **residual** (the `str.strip` analogue) | `.residual('SIGN')` — strip one generator, keep the rest · `.only('SCALE')` · `.parts()` |
| decompose | `.lineage(order='chrono' \| 'zeta')` → an `ASSWord` |
| record keeping | `.steps` (application order) · `.record()` (immutable `(a,s,g)` log) — Paper's Hands / the Long Path |

**Each generator's equation part** — its contribution to the generalized word:

    ADD    x ↦ x + a     Δ = a            free
    SCALE  x ↦ s·x        Δ = ln s         the work
    SIGN   x ↦ g·x        Δ = g ∈ {−1,+1}  free

    u  =  Σₖ [ gₖ·ln sₖ + aₖ ]          Γ  =  tanh(u/2)
    ground state a=0, s=1, g=+1  ⇒  u=0  ⇒  Γ=0  ⇒  the now

**Firing order — the three-phase camshaft.** `CAMSHAFT = (SIGN, SCALE, ADD)`,
SIGN innermost: `x ↦ ADD(SCALE(SIGN(x)))`. The one non-trivial bracket is
`[SCALE, ADD] = ADD`. **Firing defect** `u_total − Σ u_generators = (g−1)·ln s`
— zero iff `g=+1` or `s=1`, else `−2·ln s`; non-zero ⇔ SIGN flipped a
non-trivial SCALE ⇔ "defined twice" (the same shape as the Bell
composed-rotation defect).

**Two generational-lineage orderings** of a recorded word: `chrono` (when each
step fired) vs `zeta` (by spectral weight `|uₖ|` ↓). Their departure is this
datatype's `ψ(x) − x`.

**Orthogonal Smith charts** (`.to_smith()`), in the maths language it was built
on: `Γ_SCALE = tanh(½·ln s)` ⟂ `Γ_ADD = tanh(½·a)`, parity `g` picks the sheet.

**Worked example — the fast inverse square root.** `1/√x = exp(−½·ln x)` is
the `ASS` word `SIGN(−1) ∘ SCALE(½)` on `ln x`. Quake III's `0x5f3759df`
computes exactly that in the IEEE-754 exponent field: `>>1` = SCALE by ½ as a
**shift** (multiply skipped), `MAGIC − …` = ADD, sign bit untouched = SIGN.
Mantissa linearity = "good enough"; one Newton step = the residual.
(`SedenionFactoralRelativity/engine/add_scale_sign.py` `fisr_word`.)

Registered as `AddScaleSignModule` (6 code-verified equations; `python3 -m
ValaQuenta --info`); also an **engine + tool** in the SFR decomposer suite
(`engine/add_scale_sign.py`, `report_add_scale_sign()`). Scratchpad:
`.claude/scratchpad/2026-08-28_add-scale-sign-datatype/`.

## SIGN and the direction of the Noether currents (2026-09-28)

*Question (Cody):* is SIGN the only part of ADD:SCALE:SIGN that matters to the
direction of the Noether-current conversation, `J_red` versus `J_blue`?

**Answer: no. SIGN is necessary, not sufficient.** It supplies the orientation
(one bit, nothing between). The *size*, the *side of ½ you stand on*, and the
*order things fire in* belong to the other two generators — and the "up/down"
of the currents is a fact about the Cayley–Dickson tower, of which the tier-0
sign bit is at most the trace.

Provenance: everything in the tables below is a **CALCULATION** against the live
code (`GenerationalLineage/engine/add_scale_sign.py` and the `forced_sigma`
forms of `ValaQuenta/noether.py`); script and log:
`ContextPlease/claude/scratchpad/2026-09-28_sign_noether_direction/sign_noether_direction.py` / `.log`. The **readings** are marked as such.

### 1. What SIGN does supply

The two currents are reflections of each other. `noether.py` defines
`backward = −forward`, and the `forced_sigma` forms `F(σ) = e^(−σE)`,
`B(σ) = e^(−(1−σ)E)` swap under `σ ↔ 1−σ` (an involution — order 2 — which is
what a sign-type act is).

### 2. The exact identity: the direction is `sign · scale · offset`

    ln F − ln B  =  E·(1 − 2σ)  =  ASS(add=0, scale=2E, sign=−1) applied to (σ − ½)

Checked over E ∈ {0.5, 2, 10} × σ ∈ {0, ¼, ½, ¾, 1}: maximum difference **0**.

| E | σ | ln F − ln B | direction | F + B |
|---:|---:|---:|:---:|---:|
| 2 | 0.00 | +2.0000 | + | 1.13534 |
| 2 | 0.25 | +1.0000 | + | 0.82966 |
| 2 | 0.50 |  0.0000 | 0 | 0.73576 |
| 2 | 0.75 | −1.0000 | − | 0.82966 |
| 2 | 1.00 | −2.0000 | − | 1.13534 |

*Reading* (an interpretation of an exact identity, not a further test): the
three generators each take a different job.

| generator | role in the identity | decides |
|---|---|---|
| **SCALE** `2E` | the gain | **how strongly** one current beats the other |
| **ADD**-offset `σ − ½` | where you stand relative to balance | **which side** of ½ — the sign of the offset |
| **SIGN** `g = −1` | the orientation convention | which current is called "red" |

Because SCALE > 0 always, the net direction is the **product of two signs**:
SIGN's `g` and the sign of the ADD offset. So the direction is not SIGN alone —
it is SIGN acting on where ADD has put you.

### 3. SIGN acts on ADD; it does not act on SCALE

Composed elements `(add, scale, sign)`, with `ADD(3)`, `SCALE(2)`, `SIGN(−1)`:

| pair | X∘Y | Y∘X | commute? |
|---|---|---|:---:|
| SIGN, SCALE | (0, 2, −1) | (0, 2, −1) | **yes** |
| SIGN, ADD   | (−3, 1, −1) | (+3, 1, −1) | no — the offset is reflected |
| SCALE, ADD  | (6, 2, +1) | (3, 2, +1) | no — the offset is dilated |

Group commutators: `[ADD(3), SIGN(−1)] = (−6, 1, +1)` and `[ADD(3), SCALE(2)] =
(−1.5, 1, +1)` — both **pure translations**; `[SCALE(2), SIGN(−1)] = identity`.
The reflection `σ ↦ 1−σ` about ½ is exactly SIGN acting on the offset
`x = σ − ½` (`x ↦ −x`). Order matters *only through ADD* (§2, `[SCALE, ADD] = ADD`),
and SIGN is entangled with ADD in the same way.

### 4. SIGN's effect on the fold is gated by SCALE

`u = g·ln s + a`, so flipping SIGN changes `u` by `(g−1)·ln s = −2 ln s`:

| scale | add | u (g=+1) | u (g=−1) | Δu | −2 ln s |
|---:|---:|---:|---:|---:|---:|
| 1.0 | 0 | 0.00000 | 0.00000 | **0** | 0 |
| 1.0 | 2 | 2.00000 | 2.00000 | **0** | 0 |
| 2.0 | 0 | 0.69315 | −0.69315 | −1.38629 | −1.38629 |
| 0.5 | 1 | 0.30685 | 1.69315 | +1.38629 | +1.38629 |
| 10  | 0 | 2.30259 | −2.30259 | −4.60517 | −4.60517 |

At `s = 1` a sign flip does nothing to the fold (the firing defect of §5 above
is zero). SIGN only matters where SCALE is non-trivial.

### 5. What SIGN cannot say (readings, not tested here)

- **Up/down is a tower fact.** `Ainulindale/wiki/61` corrected "forward/backward"
  to **up/down in the Cayley–Dickson tower** (away from / toward the
  zero-divisors). The tower's losses — commutativity, associativity, then zero
  divisors (`r_lineage_is_order_of_operations`) — are order-of-operations
  properties of *higher* tiers. The tier-0 SIGN bit can encode an orientation;
  it cannot say *which level* the orientation is at.
- **Red/blue is more than one bit.** `sigma.not_a_scalar` (lineage): two states
  with identical `σ_self` differ in `σ_RB`, which carries 8 components (tilt and
  axis). Reducing the balance to a red-or-blue flag discards that.

### 6. Two cautions to keep with this

1. **`backward = −forward` is a definition, not a derivation.** "SIGN is all
   that matters" is true of that class *by construction*. What is derived is
   that the two forms meet at σ = ½ (`forced_sigma`).
2. **`F + B` is not conserved in σ** (E = 2: minimum 0.73576 at σ = ½, maximum
   1.13534 at the ends). Three different conservation statements circulate and
   should be named each time: `toolsets/noether.py` checks
   `J_red + J_blue = const` (only on synthetic readings); `wiki/noether.md`
   states `J_up + J_down + J_3 = E`; `sigma_expansion` finds the raw
   `|J_red|² + |J_blue|²` has a minimum at ½. The `F`, `B` above are
   `forced_sigma`'s model, **not** `sigma_expansion`'s Dirichlet-projected
   currents — the two were not compared numerically.

## See also

- [scale.md](scale.md) — SCALE pulled out of a quantity, both directions, three levels
- [ring_theory.md](ring_theory.md) — `…/lineage.py` (SFR): the factoral decomposition engine
- [telperion.md](telperion.md) — the BLUE tree; irreducible = what cannot be decomposed
- [units.md](units.md) — the same discipline on dimensional exponent vectors
- `generational-lineage` skill §§0–3 — the Two Trees domain and the four-question test
