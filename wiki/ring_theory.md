# The Ring-Theory Spine — Falls ⟺ the Quotient Has Zero Divisors

**Engine:** `SedenionFactoralRelativity/engine/lineage.py` (relations G1–G6)
**Confidence floor:** ESTABLISHED (G1–G3, G6 KNOWN ring theory; G4–G5 machine-verified)
**Claim:** An element falls if and only if its quotient ring has zero divisors. The same test at ℤ (the Two Trees) and at T₃₂/GF(2) (the SHA-1 nodal line); `gcd` is the integer trace-Laplacian.

> The engine is carried in `SedenionFactoralRelativity`, not in `ValaQuenta`'s
> `modules/`, because ring theory is *factoral*. This page records it here
> because it ties three ValaQuenta engines together — [inversion](inversion.md)
> (J_N), [hamiltonian](hamiltonian.md) (Berry–Keating xp), and
> [noether](noether.md) — under one algebraic statement.

---

## What it computes

The unifying test, read through the quotient ring:

    N prime      ⟺  ℤ/(N) is a field        → SURVIVE (Telperion)
    N composite  ⟺  ℤ/(N) has zero divisors → FALL   (Laurelin)
    N ∈ {0, 1}   ⟺  degenerate quotient     → MINGLING

and the same test one level out in the tower: a constant falls ⟺ it is nilpotent
in T₃₂/GF(2) ⟺ it lies on the zero-divisor locus (the SHA-1 name collision).

The detector is one operation on each side — `gcd(a, N) > 1` on ℤ, the
trace-Laplacian `Δ(w) = w·𝟏` on GF(2). **gcd is the integer trace-Laplacian.**

## Results — run 2026-08-22 (`python3 engine/lineage.py`)

`20/20` relations hold (R1–R8 σ-relations, F1–F6 factoral, G1–G6 ring theory).

| Relation | Tier | Result |
|---|---|---|
| `ring.fall_is_quotient_zd` | 2 | fall ⟺ ℤ/(n) has zero divisors — checked ∀ n ≤ 2000, 0 disagreements |
| `ring.gcd_is_the_detector` | 0 | census units φ(n) + zd + {0} = n, exact |
| `ring.primary_decomposition_is_cepstrum` | 3 | Lasker–Noether = the cepstrum; Ω = Σ exponents; Λ on prime powers |
| `ring.radical_units_split_gf2` | 2 | x² ∈ {0, e₀}; radical vs units 128/128 at dim 8 (exhaustive) |
| `ring.trace_laplacian_is_nilpotency` | 2 | Δ(w)=0 ⟺ w²=0 (exhaustive dim 8, 20 000 random dim 32); SHA-1 IVs null subalgebra |
| `ring.associator_is_ring_defect` | 3 | associator ≡ 0 for ℝ,ℂ,ℍ; ≠ 0 from 𝕆 — the obstruction to being a ring |

## The three orders

| order | ring theory | ValaQuenta connection |
|---|---|---|
| 1 spectrum | zero-divisor set = ∪ associated primes | the Berry–Keating spectrum, [hamiltonian](hamiltonian.md) |
| 2 cepstrum | primary decomposition; von Mangoldt Λ | ψ(x)=x−Σ_ρ xᵖ/ρ back to the zeros |
| 3 bispectrum | the associator — the ring defect | the 168-quantisation; the curvature |

The cepstrum is not an analogy: `log n = Σ aᵢ log pᵢ` turns the product into a
sum, and Λ(n) — nonzero exactly on prime powers — is that reading. This is the
"Riemann-facet fall condition" the factoral repo had been missing, named.

## Connection to the inversion engine

[inversion](inversion.md)'s J_N: (r,θ) → (1/r, θ+π/2) is a torus involution — and
so is J₂, which swaps the R/B octonions across the σ=½ axis. The frontier
direction (provisional): a **Riemann toroidal energy** on the torus S¹×S¹
bifurcates emergently into the Two Trees, J₂ the generator; iterating the
bifurcation gives a **fractal** — the higher-order factoral decomposition, with
ring theory as its skeleton. Circle → ring (cyclotomic ℤ[ζₙ]) → torus → fractal,
each the higher-order generational lineage of the last.

## A refutation, kept

Building the GF(2) relation surfaced that the UDEO white paper's *"𝟏₃₂ is a
global annihilator"* lemma is false (it contradicts its own distance table — the
round constants have Δ = 𝟏 ≠ 0). The correct, machine-verified law is
`Δ(w)=0 ⟺ w²=0`. The theorem stands; the shortcut proof was retracted in
`TuringStack` the same day. Failed predictions stay in the record.

→ Owner's-manual writeup: `Ainulindale/README.md` §20 and
`Ainulindale/wiki/92_ring_theory_spine.md`. Reference: `.clauderc_canonical_maths`
`@RCCM_RING_THEORY_SPINE`.
