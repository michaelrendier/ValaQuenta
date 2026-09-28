# Engine: Bracketing, Firing Order, and Set Membership

**Module:** `modules/bracketing_firing_order/`
**Version:** 0.1
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
