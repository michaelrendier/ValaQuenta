# Engine: Bracketing, Firing Order, and Set Membership

**Module:** `modules/bracketing_firing_order/`
**Version:** 0.2
**Confidence floor:** ESTABLISHED


**Reference:** every equation with its parameters — [toolbox](toolbox/01_bracketing_firing_order.md) · API — [bracketing_firing_order](https://michaelrendier.github.io/ValaQuenta/api/modules/bracketing_firing_order.html). This page is the record; it holds no API.

---

## Why this engine exists

Two things in this framework used the word "bracket" and looked unrelated:
`add_scale_sign`'s own `[SCALE,ADD]=ADD` (a Lie-bracket-style relation
between three generators) and the sedenion Emerger's "bracket a 16-vector
five ways" (`{1:15}`, `{2:14}`, `{8:8}`, `{4:4:4:4}`, `{4:8:4}`). They
are not two things. Both are instances of one general question — *how
many unordered ways can n things be grouped* — applied to different `n`
(3 generators, 16 sedenion components). This engine is that general
question, built once, domain-independent. `add_scale_sign` and the
Emerger bracket are both **consumers** of it now, not separate
implementations that happen to rhyme.

A second, equally general question sits next to it and is kept
deliberately separate: *how many ways can the same n things be
sequenced* — a permutation, not a partition. `CAMSHAFT = (SIGN, SCALE,
ADD)` (the fixed firing order `add_scale_sign` actually uses) and the
Emerger's firing-order dispersion are both instances of *this* question.
Bracketing answers "how could this be grouped." Firing order answers
"in what order does it fire." Confusing the two loses real structure —
see §2.

A third piece, set membership, was added live (2026-09-27) after tracing
the Recamán sequence's own defining rule exactly: its famous "flip"
between subtracting and adding is decided by testing the candidate value
against the full set of everything visited so far — not a fixed
threshold. That gave the engine's own recorded step sequence (already
named "the Long Path" in `add_scale_sign`'s `record()`) a genuine memory.

---

## 1. Bracketing — unordered groupings

```
bell_number(n)          exact count, Bell triangle, arbitrary precision
set_partitions(items)   exhaustive list, refuses above n=12
bracketing_report(items) count always + list when feasible
```

`bell_number(3) = 5` — the five ways to group `{Add, Scale, Sign}`:
one group of three, three ways to split one-plus-two, or three separate
singletons. `bell_number(16) = 10,480,142,147` — the sedenion's own
arena, ~10.5 billion groupings, of which the Emerger's five named
brackets (`{1:15}` etc.) are a tiny, algebraically-curated subset, not
an exhaustive survey. `set_partitions` refuses to enumerate past `n=12`
rather than silently hang — an honest infeasibility report, matching
this framework's own "guarantee-based" discipline: the exact count is
always available even when the list is not.

## 2. Firing order — sequenced orderings

```
firing_order_count(n)              n!
apply_firing_order(written, order) resequence by a permutation
```

**Firing order can remove written scope order** — the defining example,
verified directly, not asserted: firing order `(3,1,2)` applied to the
written sequence `[Scale, Sign, Add]` gives `[Add, Scale, Sign]` — `ASS`'s
own canonical name, reached purely by resequencing which position fires
when, not by renaming anything. `CAMSHAFT`'s own `(SIGN, SCALE, ADD)` is
one specific member of the `3! = 6`-element space `firing_order_count(3)`
counts exactly.

## 3. Set membership — the Long Path's own memory

Two distinct jobs, both grounded, neither hypothetical:

**(a) Has a firing recurred?** `trajectory()` / `collisions()` /
`would_collide()` generalize `add_scale_sign`'s own `ASSWord` methods
(same names, same behavior, verified identical on the same worked
example) from one repo's extension into a domain-independent tool: any
sequence of callables applied to a starting point, not just `ASS`
elements. This is Recamán's own defining rule, read precisely: the flip
is a set-membership test against the growing history, never a fixed
threshold.

**(b) Did a bracketing use another jurisdiction's maths illegally?**
`jurisdiction_violation(object_name, requested_operation,
jurisdiction_map)` — grounded in `GenerationalLineage/engine/lines.py`'s
own already-named "two jurisdictions" (decomposition/descent vs.
emerger/ascent: "when the descent jurisdiction looks at an object it
names it in descent terms... when the ascent jurisdiction looks at the
same object it names it in ascent terms"). A violation is exactly a
failed membership test: the requested operation is not in the set the
object is actually native to. Deliberately parametrized here, not
hardcoded — `GenerationalLineage`'s own `TOOLSETS` dict is the real
jurisdiction map; this engine stays reusable for any caller's own map.

---

## Results — run 2026-09-27

| Equation | Tier | Result |
|---|---|---|
| `bell_number(3)` | ESTABLISHED | `5` |
| `bell_number(16)` | ESTABLISHED | `10480142147` |
| `set_partitions(3 items)` | ESTABLISHED | 5 partitions, exhaustive, matches Bell(3) exactly |
| `firing_order_count(3)` | ESTABLISHED | `6` |
| `apply_firing_order([Scale,Sign,Add], (3,1,2))` | ESTABLISHED | `[Add, Scale, Sign]` |
| `collisions([+2,-2], x0=1.0)` | ESTABLISHED | `[(0, 2, 1.0)]` — a deliberately-constructed return-to-start, caught |
| `would_collide` (bad vs. ok candidate) | ESTABLISHED | correctly distinguishes both cases |
| `jurisdiction_violation('lineage', 'build_up', ...)` | ESTABLISHED | `True` — `lineage` is decomposition-only, `build_up` is ascent-only |

---

## The four orderings of brackets, on a 16-component vector (version 0.2, 2026-11-27)

The input is a sedenion (16 components, exact `Fraction`) and so is the output; every step in between is a sedenion too. Ĥ_RB works the same way: one 16-component σ_RB in, one 16-component sedenion out (`h_rb_hat/sigma16.py`, lift B is the one-leaf plan x ↦ L_C x). What this engine adds is the structure *between* the input and the output: which operations fire, in which order, grouped how.

| kind | what is chosen | plans over n items | example, n = 3 |
|---|---|---|---|
| **A** bracketing | a grouping of the written sequence | Catalan(n−1) | `((A B) C)`, `(A (B C))` |
| **B** firing order | one flat bracket, any order | n! | `(A B C \| 3 1 2)` |
| **C** firing order of brackets | the written grouping, an order at every bracket | Catalan(n−1)·2ⁿ⁻¹ | `((A B \| 2 1) C \| 2 1)` fires C, B, A |
| **D** bracketing of firing orders | a firing order first, then a grouping of the **fired** sequence | n!·Catalan(n−1) | `((A C) B)`: groups A with C although B sits between them |

D is every ordered binary product of the n items, `(2n−2)!/(n−1)!` of them, so A, B and C are contained in D (tested by value on random 16-vectors). C reaches only the separable permutations as firing orders (6 of 6, **22 of 24**, **90 of 120** for n = 3, 4, 5); D and B reach all n!; A reaches one.

**Two readings of every plan**, kept apart:

| reading | what a bracket is | associative? | what changes the output |
|---|---|---|---|
| operator | the fired children composed as left-multiplication matrices, first fired applied first (`plan_operator`, `apply_plan`) | yes | the firing order only: bracketing at written order gives one output (measured: A → 1 distinct output; B → 24 of 24 for n = 4; C → 22; D → 24) |
| element | the sedenion product of the fired children, folded left to right (`plan_value`) | **no** (252 of the 455 basis triples do not associate) | the bracketing as well: for generic sedenions every plan gives a different output (n = 3: 2, 6, 8, 12 distinct of 2, 6, 8, 12; n = 4: 5, 24, 40, 120 of 5, 24, 40, 120) |

`evolve_operator(plan, x)` returns the input and the vector after every leaf fires; `evolve_value(plan)` returns every product in the order it is computed, labelled by its factors (`(B A)`, `(C (B A))`). The last state is the output; the first is the input.

**Three kinds of "bracketing" at sixteen components, three different counts:** set partitions of the 16 positions, Bell(16) = 10,480,142,147 (tool 1); contiguous blocks (compositions), 2¹⁵ = 32,768, which is what the Emerger's `{4:8:4}` is; and trees, Catalan(15) = 9,694,845 binary groupings (A), up to `(2·16−2)!/15!` = 202,843,204,931,727,360,000 ordered products (D). The Emerger's five named brackets are compositions, a subset of Bell's arena and of the trees' alike.

### Claim table of the clean-house pass (engine 7, `tests/test_bracketing_firing_order.py`, 17 tests; the engine had none)

| claim | outcome | evidence |
|---|---|---|
| Bell(3) = 5, Bell(16) = 10,480,142,147; Bell(12) ≈ 4.2 million (the enumeration ceiling's comment) | HOLDS (Bell(12) = 4,213,597) | `test_bell_and_firing_counts` |
| firing order (3,1,2) on [Scale, Sign, Add] is [Add, Scale, Sign] | HOLDS | same |
| collisions and the flip test; jurisdiction violation | HOLDS | `test_set_membership_and_jurisdiction` |
| `(R I)` and `(R I \| 2 1)` differ in 72 of 256 matrix entries; `L_a = R + I` | HOLDS | two tests |
| written-order binary plans reach 6, 22, 90 orders | HOLDS | `test_firing_orders_reached_by_each_kind` |
| the exact product is the sedenion product | HOLDS, checked against `sigma16`'s independent table | `test_the_exact_product_agrees…` |
| "the Emerger's five named brackets are a tiny curated subset of Bell(16)" | HOLDS-WITH-CHANGE: they are compositions (2¹⁵ of them), so the right arena is 32,768, not 10.5 billion | `test_three_kinds_of_bracketing…` |
| "this module is not yet updated to carry plans" | RESOLVED: ported at 0.2; `GenerationalLineage/engine/bracketing_firing_order.py` gains the same A–D functions | `GenerationalLineage/tests/test_firing_plans.py` |

### Interactive pages (version 0.2)

`gallery/bracketing_firing_order/` (raw Canvas 2D, no libraries, no network; `serve_gallery.sh`, port 8795). Each page recomputes its numbers in the browser and compares them with `bf_data.js`, baked from the Python engine by `build_data.py`; the self-check (8 lines: the product, 217 plans with their outputs, the counts to n = 16 in BigInt, the reachable orders, the evolving vector, the Ĥ_RB leaf, Recamán, set membership) is printed on the page.

| page | shows | does not show |
|---|---|---|
| `canvas2d_evolve.html` | a 16-component input on e₀…e₁₅ and the vector after every step of a plan, tabs A to D, both readings; items from the library (the input, a basis unit, a₁…a₄, Ĥ_RB's coupling C); input and output side by side with the change | a physical evolution; the element reading has no separate input unless an item takes source `x` |
| `canvas2d_allplans.html` | every plan of one kind over 3 or 4 items, each with its output; frames mark plans that agree; item sets where plans collapse (one sedenion repeated, real scalars) | a ranking of plans |
| `canvas2d_tree.html` | one plan as a tree with the numbered firing order; click a bracket to change its order; the kind (A, B, C, D) is named | a geometry of the sedenion |
| `canvas2d_counts.html` | A, B, C, D, Bell(n) and 2ⁿ⁻¹ to n = 16 on a log scale, exact values | which plans matter |
| `canvas2d_membership.html` | Recamán's flip as a membership test, words of callables with collisions and the flip test, the jurisdiction check | why Recamán's sequence behaves as it does (open) |

**Recamán's sequence does revisit numbers** (the rule tests only the down-step against the visited set; an up-step may land on a visited value): among its first 40 terms the page rings three repeats. An expectation of "no revisits" written while building the page was wrong and is corrected there.

---

## Propagation

Module-independence convention (no cross-repo import): the set-membership
tool (§3a) is ported, not imported, into every standalone `ASS`
implementation outside this repo. As of this page: `GenerationalLineage/
engine/add_scale_sign.py`. Exactly two `class ASS` implementations exist
in the whole project (confirmed by exhaustive search) — both carry this
functionality now.

---

## Related

- `modules/add_scale_sign/` — the 3-generator consumer; `CAMSHAFT`,
  `[SCALE,ADD]=ADD`, and the `ASSWord` methods this engine generalizes.
- `modules/emerger/` — the 16-component sedenion bracket consumer.
- `GenerationalLineage/engine/lines.py` — the real "two jurisdictions"
  (`TOOLSETS`, `DECOMPOSITION_LINE`, `EMERGER_LINE`) that §3b's
  `jurisdiction_violation` is grounded in.

## Provenance

Moved from the module docstring: a docstring instructs the caller and holds no history; this section is the record.

> Born 2026-09-27, from a live correction: the `ASS`-engine bracket
> (`[SCALE,ADD]=ADD`) and the Emerger's "bracket a 16-vector five ways"
> looked like two unrelated uses of the word "bracket" -- they are not.
> Cody, directly: "bracketing the add:scale:sign in different ordered
> groupings, bracketing the sedenion into different ordered groupings...and
> bracketing set membership...are all 'bracketing engine functions'...the
> arena." This module is that arena, built once, domain-independent --
> `add_scale_sign` (3 generators) and the sedenion bracket (16 components)
> are both CONSUMERS of it, not separate implementations.

**Update 2026-10-21 — firing plans.** Brackets now carry firing orders: `(R I | 2 1)` fires the second child (the imaginary octonion of the two-octonion sedenion) first, the real octonion second, and a bracket runs as one operation inside its parent in its own order (`((A B | 2 1) C | 2 1)` fires `C B A`). Operator reading (matrix composition) is associative, so only the order changes the result; element reading (the sedenion product) is not, so the bracketing changes it too. Written-order binary plans reach 6, 22, 90 of 3!, 4!, 5! orders. Source and checks: `SedenionSpectralRelativity/firing_plan.py` (15 exact checks), `wiki/Bracketing-and-Firing-Plans.md`, notebook 02 there; standalone port `GenerationalLineage/engine/bracketing_firing_order.py` tool 4 (`wiki/Firing-Plans.md`). This module carries the plans since version 0.2 (below).
