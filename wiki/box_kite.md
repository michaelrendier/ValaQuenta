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

## The skeleton: PG(3,2)

15 points (the pure imaginaries), 35 lines of 3 (the multiplication triplets), **15** Fano planes. Not 32 — figures circulating with "32 interlocking Fano planes" are wrong.

## Confidence

| Item | Tier |
|---|---|
| All counts (42/84/168/336/7), octahedral structure, chart spectra, PG(3,2) skeleton, associator census, e₀ exclusion | ESTABLISHED — derived and cross-checked |
| Zero cross-strut edges | ESTABLISHED — computed |
| PSL(2,7) action as the transition maps | CONJECTURE — the named next step |
| Global dispersion relation on the ZD surface | OPEN |
