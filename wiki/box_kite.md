# Engine: The Box-Kite Debugger — the ZD Geometry, Made Watchable

**File:** `modules/box_kite/maths.py`
**Class:** `BoxKiteModule`
**Notebook:** `notebooks/engines/15_box_kite.ipynb`
**Ainulindale wiki:** `Ainulindale/wiki/84_the_box_kite_debugger.md`
**Claim:** The sedenion zero-divisor geometry is exactly enumerable, and its object is **PSL(2,7)** (order 168, Aut(Fano) = GL(3,2)) — **not G₂**. Seven box-kites, each an **octahedron**, six Assessors apiece, 42 in all. Chart-level dispersion relation {0,4,4,4,6,6}. The associator is the curvature.

---

## Where the object is, and where it is not

Moreno (1997): the sedenions' norm-one zero divisors are homeomorphic to **G₂**. True — and the wrong place to build. de Marrais (2000), responding directly:

> *"Moreno discovered a homomorphism — a 'blow-up' of an exact correspondence — and the 'blow-ups' in the history of number theory have all entailed the loss of something."*

G₂ is the **continuous shadow**; it forgets which Fano line is which. The exact object is finite: **PSL(2,7) is the finite subgroup of G₂ that preserves the labelling.**

## Everything derives — nothing is asserted

All counts come from the Cayley–Dickson multiplication table in `maths.py`. Agreement with de Marrais and with `ZD_PAIRS=84` / `ZD_CLASSES=42` / `168` is a **check**, not an input. `verify_counts()` reports booleans so it cannot be read past.

```
ASSESSOR   plane span(e_a, e_{b+8}), a,b ∈ 1..7, whose diagonals
           e_a ± e_{b+8} zero-divide.  a == b NEVER works
42         = 49 − 7 aligned planes
84         = 42 × 2 diagonals            ← ZD_PAIRS
168        = 42 × 4 signed unit points   ← |PSL(2,7)|
336        ordered annihilating pairs = 84 × 4
           (each diagonal annihilates exactly 4 others)
STRUT      s = a XOR b ∈ 1..7 — indexes the box-kite
7 × 6 = 42 seven box-kites, six Assessors each
```

Cross-check: de Marrais's published Box-Kite I is (3,10),(2,11),(5,12),(4,13),(7,14),(6,15) → strut 1 here, exact match.

## THE SHAPE IS AN OCTAHEDRON

For every strut the 6 Assessors form a 4-regular graph on 6 vertices with exactly 3 non-edges — and the non-edges are precisely the **reversal pairs** (a,b) ↔ (b,a). That is **K₂,₂,₂**. Built from actual vanishing products (`assessors_adjacent`), verified for all 7 charts.

## The dispersion relation, chart level

```
adjacency:   4,  0,  0,  0, −2, −2
Laplacian:   0,  4,  4,  4,  6,  6      ← ω²(k) on one box-kite
```

One zero mode, a 3-fold degenerate mode at 4, a 2-fold at 6. **The zero mode is e₀'s signature** — exists everywhere, propagates nowhere. It emerges from the graph rather than being inserted, which is the check that ∅_RB really is outside the geometry it generates.

## ∅_RB is not the geometry — checked, not asserted

`e0_is_outside()`: e₀ is not a point of PG(3,2), is in no Assessor, is a vertex of no box-kite, and its associator vanishes against everything (it is the identity, hence central). It **generates the boundary and does not live on it** — the same way d generates ∂ without being a manifold.

## The curvature is the associator

```
[a,b,c] = (ab)c − a(bc)      the curvature analogue
[a,b]   = ab − ba            the torsion analogue
```

**1848 of 4096** basis triples have non-vanishing associator. `associator_field(s)` paints these onto a box-kite's vertices and edges — that is the debug view, and it is what "watch the geometries interact" looks like as numbers.

## THE FINDING: the charts do not touch

The 42-vertex atlas has **84 edges and zero cross-strut edges.** The seven box-kites are mutually disconnected under zero-divisor adjacency — the glued Laplacian has 7 zero modes, one per component.

This is a result, not an instrument failure, and it **changes the shape of the open problem.** A wave cannot propagate between charts via ZD adjacency, so either:

1. the medium genuinely is seven disconnected octahedra and there is no global dispersion relation to find, or
2. the connection is the **PSL(2,7) action permuting the struts** — transition maps are group elements, not edges.

(2) is where to look. The gluing question is no longer "find the edges between charts" but "find the group action that identifies them."

Also worth noting: **84 = ZD_PAIRS is also the atlas edge count.** 42 vertices at degree 4 → 42×4/2 = 84. Same number, second reading.

## Do the charts touch? — yes, in the skeleton (v0.2, 2026-08-05)

Cody: *"i'm pretty sure that those 'surfaces' do actually touch somewhere… they are all from the fixed point anyway… but now we have a clue that 0_RB only points to 'fixed point space'… where the boundary and the geometries are the same thing, right?"*

**Correct**, and it does not contradict the zero-cross-strut-edges finding. They are two structures on one object:

| structure | relation | result |
|---|---|---|
| **adjacency** | zero-divisor products | 7 components, 7 zero modes — disconnected |
| **skeleton** | shared basis indices | every usable index in **6 of 7** charts — almost totally overlapping |

For strut s an Assessor is (a, (a XOR s)+8), valid whenever a ≠ s — so index a sits in every chart *except* s = a. Every chart pair shares exactly **10** skeleton points. The charts touch everywhere in the skeleton and nowhere in the products.

**And exactly two basis elements are in no Assessor: e₀ and e₈.** e₀ is the identity — ∅_RB, the fixed point. e₈ is the Cayley–Dickson doubling generator. Each chart carries one zero mode, and a zero mode is the constant function — **seven copies of one object.** Identify them and the atlas connects, and that identification happens at e₀ and nowhere else.

That is the precise sense in which ∅_RB points to fixed-point space *where the boundary and the geometries are the same thing*: at the fixed point the boundary generator and the geometry's own mode are the same vector. Away from it they separate.

Functions: `index_chart_membership`, `skeleton_overlap`, `fixed_point_gluing`.

## The chart of addresses

The connector to the monad. Its hyperindexing addresses each surface form to a 16-vector (`VAPMIP/monad_sedenion_addresses.pkl`, `book[name]["sedenion"]`); `chart_of(v)` reports exhaustively where that address sits:

```
norm, peak_dim, fixed_point_weight, energy_split (e₀ / e₈ / lower / upper)
chart_energy (all 7), dominant_chart, chart_share
nearest_assessor, d_plus, d_minus, dominant_diagonal
local_curvature (associator defect at the dominant directions)
is_zero_divisor, outside_share
```

`address_census(addresses)` runs it over a whole corpus — descriptive only, counts and distributions, nothing scored against an expectation.

### Census over the monad book (3288 entries)

```
all 42 Assessors occupied
mean fixed-point weight   0.6435    (min 0.0583, max 1.0000)
mean outside share e₀+e₈  0.6537
peak_dim = 0              2751 of 3288  (84%)
dominant chart            strut 2: 30.1%  …  strut 7: 2.2%
mean local curvature      8.37
```

**About two thirds of the average address's energy sits outside the ZD geometry entirely.** Cody's "they are all from the fixed point anyway", measured.

Worth connecting to Phase 23's independent finding that the monad's projections carry ~85% common mode with 2–3% content: this **localises the common mode to e₀ + e₈** — the two basis elements belonging to no Assessor. The part of an address living outside the geometry is exactly the part carrying no discriminating signal.

Descriptive. Not a result about translation.

## The skeleton: PG(3,2)

15 points (the pure imaginaries), 35 lines of 3 (the multiplication triplets), **15** Fano planes. Not 32 — figures circulating with "32 interlocking Fano planes" are wrong.

## Confidence

| Item | Tier |
|---|---|
| All counts (42/84/168/336/7), octahedral structure, chart spectra, PG(3,2) skeleton, associator census, e₀ exclusion | ESTABLISHED — derived and cross-checked |
| Zero cross-strut edges | ESTABLISHED — computed |
| PSL(2,7) action as the transition maps | CONJECTURE — the named next step |
| Global dispersion relation on the ZD surface | OPEN |
