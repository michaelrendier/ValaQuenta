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

## When the leaf falls — the composite side (v0.2, 2026-08-05)

ψ counts **only prime powers**, so a composite contributes nothing to it. As first built this engine could name every prime and say nothing about any child; composites live in the complement, x − π(x), the fourth search term.

**Two events, and they are not the same:**

| event | occurs at | meaning |
|---|---|---|
| discovery | `lpf(N)` | first strike — you learn N is composite, cofactor comes free |
| **fall** | **`gpf(N)`** | the sieve is finished with N — nothing remains open |

Cody's case: 14 = 2·7 is struck at 2 but **stays on the tree**; it drops at 7. The leaf hangs while any factor is unresolved, so the fall is at gpf.

This is not a stylistic choice of ordering. **Smoothness is defined by the greatest prime factor** (N is y-smooth ⟺ gpf(N) ≤ y), and smooth relations are the engine of GNFS, the quadratic sieve, CFRAC and index calculus. The tree's own criterion is the one the field already runs on.

### The fall-time distribution already existed

Native to this axis, because the Dickman coordinate is a **ratio of screw lifts**:

```
u = ln N / ln(gpf N)
u·ρ′(u) = −ρ(u−1),   ρ(u) = 1 on [0,1]
Ψ(x, x^(1/u)) ~ x·ρ(u)
```

`dickman_rho` marches ρ(u) = (1/u)∫_{u−1}^{u}ρ(t)dt on a fixed grid; verified against published values to ~10⁻⁷ at u = 1…5. **A balanced semiprime sits at u = 2 exactly** — exponent 1/u = ½. The ½ again, this time through smoothness.

### The harvest is closed-form

```
leaves falling at step p       =  Ψ(X/p, p)          `harvest`
two-parent leaves at step p    =  π(min(p, X/p))     `semiprime_harvest`
```

`harvest_curve` counts the same thing directly off a `gpf_table` sieve; the two agree exactly at every p tested (X = 10⁵, p ∈ {2,3,5,7,97,997}). Disagreement is a bug, not a discovery.

### Why balanced RSA is hard, in these terms

On the screw the family identity is **exact**: ln p₁ + ln p₂ = ln N. So a semiprime is one public constraint plus one free number:

```
ln p₁ = ½ln N − δ,   ln p₂ = ½ln N + δ,   δ = ½ln(p₂/p₁)
```

**δ is the entire hidden content.** The two falls are separated by exactly 2δ. Unbalanced ⟹ far apart, and the early event hands you everything. Balanced ⟹ δ → 0 and **both falls collapse onto ½ln N**. There is no early event to catch. Not "the search space is large" — **the two observables coincide.**

### Cost, stated

`lpf`/`gpf` are trial division, O(√n). `harvest_curve`/`psi_smooth` are O(X log log X) time, O(X) memory. Tracking the fall is cheap; reaching it for a 2048-bit modulus still means sieving to 2¹⁰²⁴. Naming the event correctly does not move that wall.

## The negative space — μ, Mertens, and the three motions (v0.3, 2026-08-05)

Cody, 2026-08-05: *"that is working on the bulk rather than the negative space."*

ψ counts what **accumulates**. It had no counterpart for what is **excluded** — and the sieve is an exclusion process: you never test primality positively, you remove multiples and keep the residue. Fermat carves the forbidden zone; what survives *is* prime.

The two motions are reciprocal Euler products:

```
GROWTH      ζ(s)   = Σ n⁻ˢ      = ∏ (1 − p⁻ˢ)⁻¹
EXTINCTION  1/ζ(s) = Σ μ(n)n⁻ˢ  = ∏ (1 − p⁻ˢ)
```

Same product, inverted exponent. **μ is the negative-space operator** — the Dirichlet inverse of 1, Σ_{d|n} μ(d) = [n=1] — and the sieve is literally μ in action (Legendre: π(x) − π(√x) + 1 = Σ_d μ(d)⌊x/d⌋).

The negative space has its own counting function, ψ's mirror:

```
ψ(x) = Σ_{pᵐ≤x} ln p     the BULK       ψ(x) ~ x
M(x) = Σ_{n≤x} μ(n)      the MERTENS    RH ⟺ M(x) = O(x^{½+ε})
```

**The same ½, on the exclusion side.** Verified against known values: M(10) = −1, M(100) = 1, M(1000) = 2, M(10000) = −23.

### Three motions, not two

This resolves the lpf/gpf tangle — they are not two definitions of one event but two events of opposite polarity:

| motion | agent | event | at |
|---|---|---|---|
| **grown** | ζ orders the primes | the leaf is placed at ln N | — |
| **extinct** | μ excludes | struck, removed — *without naming* | **lpf** |
| **identified** | the N-shape names | the factors are resolved | **gpf** |

Between extinction and identification the leaf is **dead but unnamed**, an interval of length ln(gpf/lpf) = **2δ**. For balanced RSA δ → 0 and all three observables coincide at ½ln N.

A prime is the degenerate case: grown, extinct and identified at the same instant. It is its own leaf.

Functions: `mobius`, `mertens`, `mertens_envelope`, `sieve_extinction`.

## The projection ledger — what "the domain" actually is

`domain_ladder(modulus_bits)`. Cody, 2026-08-05: *"is that everything from 2 through the RSA modulus? or is that only using the prime numbers that have enough digits?"* — **neither.**

```
RSA-2048                                    log₂(count)
all integers 2 … N                             2048
all integers 2 … √N          trial range       1024
all PRIMES ≤ √N              only these test   1014.53
primes with exactly 1024 bits                  1013.53
GNFS pathway actually walked                    112

√N bound saves      1024 bits   (free — Fermat: p ≤ q ⟹ p ≤ √N)
primes-only saves      9.47 bits
size restriction       1.00 bit
GNFS saves further   901.53 bits
```

**THE ONE-BIT FACT.** Restricting to primes "with enough digits" prunes by a factor of exactly **2**, not by orders of magnitude. Primes are top-heavy: density 1/ln x barely moves across an octave (at 2¹⁰²⁴, ln x differs by 0.1% between x/2 and x), so

```
π(x) − π(x/2) ≈ x/(2 ln x) ≈ ½ π(x)
```

Half of all primes below any bound live in the top octave. The size restriction discards the other half and nothing else. Verified: the saving is 1.0028 at 1024 bits, 1.0014 at 2048, 1.0007 at 4096 — tightening to exactly 1 as the modulus grows.

This joins the other cheap algebraic constraints, all worth single digits: mod 4 ≈ 1 bit, mod 16 = 3 bits, size = 1 bit.

**The only row that is a target.** Everything above 2¹¹² is naive-domain accounting that was beaten in the 1990s. A new method must clear **2¹¹²**, not 2¹⁰²⁴.

## The slot correspondence — read this before editing

*(Revised 2026-08-04. Previously read "two unrelated ψ, do not merge" — true, but it undersold the situation.)*

**They are different objects. Itemise them.**

| | ψ_Cheb(x) — here | ψ_Fermat(θ) — `l_io_photon_path` |
|---|---|---|
| domain | ℝ⁺, 1-D | 2D field |
| regularity | monotone **step** function | smooth scalar field |
| source | discrete Λ(n) on prime powers | continuous density κ |
| above source | ψ′ = Σ Λ(n)δ(x−n) — **one** integration | ∇²ψ = 2κ — **two** |

You cannot Poisson-solve a staircase; you cannot read a prime off a smooth field.

**But they are one slot apart in the same equation.**

```
lensing:   L_(I|O)  =  L   −  ψ_Fermat
primes:    ψ_Cheb   =  x   −  Σ_ρ x^ρ/ρ    (− ln2π − ½ln(1−x⁻²))

    ψ_Cheb      ↔  L_(I|O)     the actual, bent path
    x           ↔  L           the clean geodesic
    Σ_ρ x^ρ/ρ   ↔  ψ_Fermat    the potential — the bend
```

Chebyshev ψ is the counterpart of **L_(I|O)**, not of the Fermat potential. The object that corresponds to ψ_Fermat is the **zero sum**, which had no name in these repos until this revision — it lived inline inside `chebyshev_psi_explicit`, which is exactly why the collision read as an accident. Now `zero_sum()`.

Consequently the main term x **is** L — "the path of least primes", the phrase the 2026-07-31 primer carries without a formula, now `clean_path_L()`. And the prime side already had an L_(I|O); it was being called ψ.

`l_io_decomposition(x)` returns all three slots by role name (`L`, `psi_bend`, `trivial`, `L_IO`), identity `L_IO = L − psi_bend + trivial` held by construction. Fourth dictionary column in `Ainulindale/wiki/83` §9.3 and the primer §4.

`chebyshev_psi_*` keeps its name — it is standard and expected. What changed is that the object it was hiding now has one too.

## Confidence

| Item | Tier |
|---|---|
| Explicit formula, Lambert-W zero-height inverse, N(T), Li, Kronecker/ramification structure | ESTABLISHED |
| Screw = logarithm as the Monad's working machine; primes-as-antinodes reading | THEORETICAL |
| Amplitude-envelope form of RH (restatement, not a new proof) | THEORETICAL |
| ZD-surface contour beating the resolution wall | OPEN |
