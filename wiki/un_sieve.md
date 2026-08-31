# un_sieve — the recursive un-sieve, Laurelin's own accounting

The **sieve** (`sieve_lineage`) is **Telperion's** book: it watches the
composites *fall* — each dies on the pass of its smallest prime factor,
`generation(n) = π(spf(n))`. What cannot be, struck out in ordinal order.

The **un-sieve** (`un_sieve`, `FactoralDecomposition/engine/lineage.py`) is
**Laurelin's**: from the ground state *"Just Prime Numbers"*, turn primes on
one at a time and watch each composite **arrive** — born the moment its last
needed prime factor is switched on. What IS, assembled.

The two trees counter-rotate. Measured, `N = 10⁵`:

| tree | reading | generation | entropy | range |
|---|---|---|---|---|
| Telperion | **A** extinction, low→high | `rank_asc(spf)` | 2.491 bits | `[0…64]` |
| — | **B** extinction, high→low | `rank_desc(gpf)` | 9.685 bits | `[4459…9591]` |
| Laurelin | **C** birth, low→high | `rank_asc(gpf)` | 9.685 bits | `[0…5132]` |
| — | **D** birth, high→low | `rank_desc(spf)` | 2.491 bits | `[9527…9591]` |

## The mirror

**`D == reverse(A)` exactly** — birth high→low is extinction low→high run
backwards, bit for bit over all 90 407 composites. `H(A) = H(D) = 2.491`; the
reflection preserves entropy. `B == reverse(C)` likewise. Telperion read
upside down **is** Laurelin, when both are keyed on the same prime factor.

## The residual

The one order that is *not* a mirror is **C against A** — birth by *greatest*
prime factor against death by *smallest*. `H(C) − H(A) = +7.19 bits`: the
same information, spread across ~5 000 generations instead of 65. The
histogram difference is a large negative front at the small primes (`p=2:
−49 984`, decaying through `p=13`) then small positive ripples at the
mid-sized primes (`p=47: +593`, `p=61: +591`). Negative spike, positive fine
structure.

## Clocked by zeta

The same reads, run with the ordinal prime rank replaced by zeta-derived
orders — `ln p/√p` (the σ=½ amplitude, peaks at p=7), Riemann–Siegel `θ`, the
sign of the RS `Z`-function, the spiral phase. **`H(C) − H(A) = +7.19355`
bits is invariant to five decimals under every one of them** — it is a
combinatorial invariant of ℕ, not an artefact of counting the primes in
order. Zeta order only moves the *schedule*: an oscillatory clock (`Z`-sign,
spiral phase) smears the compact extinction front across 25–50× more
generations without changing its entropy, and forces you past thousands of
primes that strike nothing before the boundary prime 313 — where the ordinal
order wastes not a single pass.

One thing *does* move the gap: clocking birth by the **real Riemann zeros**
`γ_k` rather than the integers drops `H(C) − H(A)` by ≈ 15 % (`+4.30 → +3.66`
bits, `N = 8 000`). The zeros are a better-matched clock for the construction
than the integers are — Laurelin's book, read on ζ's own timeline, costs
less. See `RiemannHypothesisProof/ADDENDUM_recursive_unsieve_2026-08-30.md`
§B.1–D.1.

## The two boundaries

- **Extinction** completes at the largest prime with `p² ≤ N` — **313** for
  `N = 10⁵` (the "313 Sieve").
- **Birth** completes at the largest prime with `2p ≤ N` — **49 999**.

The sieve finishes killing at `√N` and does not finish birthing until `N/2`.
**60.5 %** of every composite `≤ N` is born after the extinction boundary —
decided by primes that strike nothing.

## The split — extinction is free, existence is not

Telperion's book is cheap: define a number by **what it cannot be** and its
*smallest* prime suffices — bounded, front-loaded, done at `√N` (313), 2.491
bits. Laurelin's book is dear: define it by **what it is** and every prime
factor must be present, so you wait for its *largest* — `+7.19 bits`, not
finished until `N/2` (49 999). Exclusion is free; construction is paid.

## Usage

```python
from engine.lineage import un_sieve
r = un_sieve(100_000)
r['D_equals_reverse_A']          # True
r['H_C_minus_H_A']               # +7.1936
r['extinction_boundary_prime']   # 313
r['birth_boundary_prime']        # 49999
r['residual_fraction']           # 0.6045
```

## See also

- `sieve_lineage`, `sieve_recurrence`, `two_trees` — same engine
- `wiki/prime_gate.md`, `wiki/add_scale_sign.md`
- `RiemannHypothesisProof/ADDENDUM_recursive_unsieve_2026-08-30.md` — the ζ
  reading (ground state "Just Prime Numbers", a Zeta Hamiltonian by Legendre,
  no new maths)
- `Ainulindale/wiki/47_the_two_trees.md`
