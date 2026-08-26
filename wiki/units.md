# units — Units as the Equation Index

`modules/units/` · v0.1 · Status: **ESTABLISHED** (elementary dimensional
analysis — Buckingham Pi theorem territory — independently verified in this
module, not a new theorem)

UNITS is a fourth domain for this project's own factoral-decomposition
discipline: numbers ([[ring_theory]]'s side, factor_lineage), processes
([[scale]] §5's pathway_decompose), and now physical units — the 7 SI base
dimensions as the irreducible leaves.

---

## What it computes

| # | question | function |
|---|---|---|
| 1 | combine units by multiplying/dividing quantities | `unit_mul` / `unit_div` / `unit_pow` |
| 2 | does a named compound's lineage recombine to its own declared vector? | `unit_lineage_decompose` / `verify_lineage_table` — **yes**, all 11 named units |
| 3 | does cancellation actually cancel (the chemistry case)? | `verify_cancellation` — `mol/L * L == mol`, exactly |
| 4 | what does a dimension signature narrow the possibilities to? | `equation_index_lookup` / `EQUATION_INDEX` |

## 1–3. The exponent-vector arithmetic

```python
from ValaQuenta.modules.units import unit_vector, unit_mul, unit_div, SI_BASE

MOL    = unit_vector((0,0,0,0,0,1,0), name='mol')
LITER  = unit_vector((0,3,0,0,0,0,0), name='L')
conc   = unit_div(MOL, LITER)          # mol/L -> (0,-3,0,0,0,1,0)
back   = unit_mul(conc, LITER)         # cancels back to mol EXACTLY
back['exponents'] == MOL['exponents']  # True
```

`SI_BASE = ('kg','m','s','A','K','mol','cd')` — fixed order, 7 leaves.
Multiplying quantities adds exponent vectors; dividing subtracts;
cancellation is a component landing on zero — no special-casing.

## Named compounds — an exact, traced lineage

```python
from ValaQuenta.modules.units import LINEAGE_TABLE, verify_lineage_table
verify_lineage_table()['holds']   # True — N, J, W, Pa, C, V, Ω, F, Wb, T, H all match
```

Each entry's `lineage` is `(parent, power)` pairs, not bare names — Tesla is
`Wb¹·m⁻²`, not `Wb+m`:

```python
'T': {'exponents': (1,0,-2,-1,0,0,0), 'lineage': (('Wb', 1), ('m', -2))}
```

**Caught while building this, not hidden:** the first draft stored bare
parent names and always *added* their vectors — running it failed all six
named units immediately, because several of them (Tesla included) are
built by *dividing*, not multiplying, and by a *square*, not a first power.
Fixed by carrying the signed power explicitly. The Tesla trace, six
generations deep, recombines exactly:

```
T <- Wb <- V <- W <- J <- N <- {kg, m, s}  (with signed exponents at every step)
```

## 4. The equation index — units as "word possibilities"

```python
from ValaQuenta.modules.units import equation_index_lookup
equation_index_lookup((1,2,-2,0,0,0,0))
# ['kinetic energy: E = (1/2)*m*v^2', 'gravitational PE: E = m*g*h',
#  'work: W = F*d', 'spring PE: E = (1/2)*k*x^2', 'heat: Q = m*c*dT']
```

Exact structural parallel to `box_kite`'s `context_vector`: a word's
context vector narrows it to candidate WordNet senses; a quantity's
dimension signature narrows it to candidate physical laws. Neither
guarantees which one is meant — both cut a large space down to a short,
checkable list. `EQUATION_INDEX` currently covers the common mechanical
and electromagnetic compounds (16 signatures); it's a real, extensible
lookup, not exhaustive — the space of physical laws isn't finite the way
`SI_BASE`'s 7 leaves are.

## Units are a geometry, not content

Same finding as [[scale]] and `SedenionFactoralRelativity`'s `0_RB`/`σ_RB`
work, a fourth instance: a unit vector carries no numeric content and does
no computation on its own — but it is exactly what decides which
recombinations of content are dimensionally legal. `7.2 J + 3.1 kg` is
illegal (mismatched vectors); `7.2 J / 3.1 s` is legal and lands on power
automatically, without being told to.

## Honest scope

Plain `int`/`float` exponents (matching the sibling `SedenionFactoralRelativity`
port, not `fractions.Fraction`) — this module's convention, not a claim
that fractional/root exponents can't be represented (they can, `unit_pow`
takes any real `n`).

## Related

[[scale]] (the sibling tier-0 irreducible, SCALE, that unit composition is
built from); `SedenionFactoralRelativity/wiki/Units-and-the-Equation-Index.md`,
`Ainulindale/wiki/97_units_as_the_equation_index.md` (same day, sibling
pages); `PtolemyDesktop/Archimedes/UnitVector.py` (the original, independent
string-list-based design this module's arithmetic supersedes for
cancellation, while its "label is the string" idea remains a real,
unimplemented next step: reverse-lookup `LINEAGE_TABLE` after arithmetic so
a computed vector re-adopts its name automatically).
