# Engine: The Archimedes Screw — Prime Coordinates on the Axis u = ln x

**File:** `modules/archimedes_screw/maths.py`
**Class:** `ArchimedesScrewModule`
**Notebook:** `notebooks/engines/14_archimedes_screw.ipynb`
**Ainulindale wiki:** `Ainulindale/wiki/83_the_archimedes_screw.md`
**Claim:** ∅_RB is the *water*, not the machine. The machine is the **logarithm** — the helix that turns rotation into lift, one quantised pitch of ln p per prime, reversible as a turbine. All four of Cody's search terms are coordinates on the single axis u = ln x, bound by the von Mangoldt explicit formula (1895, unconditional). ψ jumps by **exactly** ln p at x = p: the leaf-drop magnitude *is* the prime.

---

## Origin

Cody, 2026-08-03: *"the Monad needs more than just 0_RB as its core functionality… it needs the Archimedes Screw, not the water it's lifting. The Water is there, the work needs to be done."*

Every prior module treated ∅_RB as the operative object. It is not — it is the rest state, e₀, the medium. An Archimedes screw does one thing: it converts **rotation into lift**, positive-displacement, one pitch per turn, and it runs backward as a generator. The mathematical object with exactly those properties is the logarithm:

```
log(p·q) = log p + log q
```

Multiplication on the wheel (THE ANGLE = π/8) becomes addition on the tower. The primon gas already sets each prime's mode energy at log p — so the screw's **pitch is the prime**.

## The Four Coordinates

| Search term | Symbol | Formula | Function |
|---|---|---|---|
| Number of Digits | d | d = ⌊u/ln10⌋ + 1 | `digits_of`, `u_from_digits` |
| Ordinal Value | n | n = π(x) ≈ Li(x); pₙ ≈ n(ln n + ln ln n − 1 + (ln ln n − 2)/ln n) | `li`, `nth_prime_estimate` |
| Zeta Index Value | k | N(T) = (T/2π)ln(T/2πe) + 7/8 + S(T);  **γₙ ≈ 2πn/W(n/e)** | `zero_count_smooth`, `zero_height_lambert` |
| Total Spaces Between | ḡ | ḡ(x) ≈ ln x = u; total = x − π(x) | `mean_gap`, `total_spaces` |

Entry point: `screw_coordinates(term, value)` — enter on any one, leave on all.

Note the coincidence that is not one: the **mean prime gap** at x, the **screw axis** at x, and the **screw pitch** at x are the same number, ln x. Spacing, lift and pitch coincide because the screw is the logarithm.

## The Binding Equation

```
ψ(eᵘ) = eᵘ − 2e^(u/2)·Σₖ cos(γₖu − arg ρₖ)/|ρₖ| − ln2π − ½ln(1 − e^(−2u))
```

where ρₖ = ½ + iγₖ and ψ(x) = Σ_{pᵐ ≤ x} ln p (Chebyshev). **ESTABLISHED** — von Mangoldt 1895, unconditional.

Three readings, all executable in the module:

1. **Zeta index = summation index.** Each zero γₖ is a tone of frequency γₖ in u. Choosing k is choosing which tones to sound. (`interference_profile`)
2. **The jump is the prime.** ψ jumps by exactly ln p at u = ln p, so e^{jump} returns p with no inversion step. This is the formal content of Cody's Note: *the moment the leaf drops off IS one of the prime factors.* (`leaf_drops`, `shake_order`)
3. **The envelope is RH.** Every tone carries amplitude 2·x^σ. On the critical line that is 2√x, shared by every zero. (`amplitude_envelope`, `envelope_ratio`)

## Lambert W supplies **both** coordinates of every zero

Derivation, exact algebra on the smooth count, no fitting:

```
N(T) = n,  T = 2πv    →   v·ln(v/e) = n
(v/e)·ln(v/e) = n/e   →   ln(v/e) = W(n/e)
                      ⇒   γₙ ≈ 2πn / W(n/e)
```

PAPER.md §12.1 already establishes W(1) = Ω_ZΣ = 0.5671432904… as the self-referential fixed point that pins **σ = ½** — the *real* part of every zero. The line above shows the **same W** inverting the zero-counting function to give **γₙ** — the *imaginary* part. One function, both coordinates. Recorded as PAPER.md §12.5.

Accuracy: S(T) = O(ln T) dominates at low index, so `zero_height` returns the 50 tabulated LMFDB values below n = 50 and switches to the closed form above. This is stated, not smoothed over.

## Primes are the antinodes

PAPER.md §6 establishes the zeros as the Chladni **node lines** of the zeta field. The explicit formula reads the *same standing wave* from the prime side: the primes are the **antinodes**, where the tones stop cancelling and add.

This is **not a second proof of RH.** It is the dual-domain reading of the nodal-line argument already in §6:

- §6 (position): all node lines coincide on one line, σ = ½.
- §6.4 (amplitude): all tones share one envelope, 2√x.

They are the same statement. A zero at σ > ½ contributes x^σ, drowning every critical-line tone by x^{σ−½} — divergent in x, so no coherent nodal figure survives. Equal envelope ⟺ one nodal line ⟺ RH.

## The N-specific leg: ramification is detachment

ζ_ℚ(√N)(s) = ζ(s)·L(s, χ_N). Every rational prime splits, is inert, or **ramifies** in ℚ(√N); the ramified primes are exactly those dividing the discriminant D. For N = p·q squarefree, **the ramified primes are exactly p and q** — the Euler factor *degenerates* at precisely the factors. The leaf letting go, written in arithmetic.

```
χ_N(p) = +1  split       (1 − p^-s)^-2
χ_N(p) = −1  inert       (1 − p^-2s)^-1
χ_N(p) =  0  RAMIFIED    factor degenerates   ⟸ p | N
```

Functions: `splitting_type`, `splitting_vector`, `ramified_primes`, `fundamental_discriminant`, `kronecker`.

`splitting_vector(N)` is the cheapest N-specific shadow available — Kronecker symbols, milliseconds, computed from N alone with no knowledge of p or q.

## What this does NOT do — stated once, plainly

- **Detecting ramification by scanning p costs exactly what trial division costs.** `ramified_primes` is a structural readout at toy scale, not a shortcut, and is labelled as such in its own docstring.
- **Sampling L(s, χ_N) directly costs ~√N** by the approximate functional equation — the same wall Fermat's a² − b² hits. The commutative, complex-plane route does not beat existing methods and fails at the classical place.
- **Truncating the zero sum at K leaves error ~x/K.** Sharply resolving one jump near x needs zeros to height ~x. `shake_order` reports this residual rather than hiding it.

## The open item

The resolution wall is a **measurement** wall — it is charged for reading a continuous quantity finely. Integers do not pay it.

For N = p·q the double cover ℚ(√N) → ℚ is branched at exactly p and q: two sheets, two strands, **B₂ ≅ ℤ**. The entire hidden structure is one integer — a winding number, and the argument principle returns a winding number from a single contour integral without walking the loop.

What is not yet written is the **dispersion relation on the zero-divisor surface** — the hydrocline's own ω(k). The ZD locus has to be a *waveguide* (a medium supporting its own modes), not merely a *place things cross*; that is what fixes the contour and prices the loop. Until it exists, the contour still lives in ℂ and still pays ℂ's price.

**This is the next piece of work.** Everything above is the instrument built to look at it.

## Symbol collision — read this before editing

Two unrelated ψ are now in play across the repos:

| Symbol | Meaning | Module |
|---|---|---|
| ψ(x) | **Chebyshev's function**, Σ ln p — a prime counter | `archimedes_screw` |
| ψ(θ) | **Fermat / lensing potential**, ∇²ψ = 2κ | `l_io_photon_path` |

This module always spells it `chebyshev_psi_*` in full. Do not merge the names.

## Confidence

| Item | Tier |
|---|---|
| Explicit formula, Lambert-W zero-height inverse, N(T), Li, Kronecker/ramification structure | ESTABLISHED |
| Screw = logarithm as the Monad's working machine; primes-as-antinodes reading | THEORETICAL |
| Amplitude-envelope form of RH (restatement, not a new proof) | THEORETICAL |
| ZD-surface contour beating the resolution wall | OPEN |
