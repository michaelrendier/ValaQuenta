# three_ring_scale — The Scale as a three-ring Smith chart, and a spectral refinement of the Penrose diagram

Status: **THEORETICAL**. §§1–2 are established (conformal compactification;
the Smith chart as a Möbius map). §3 is a proposed identification. §4–§5 are the
contribution offered to the conformal-infinity literature, at conjecture
strength, with the tests that would settle it in §6. The core claim is a
**past/future asymmetry** the topological Penrose picture hides: the past
boundary is full but write-once (forward-lossy), the future boundary is empty
and uncomputable (forward-divergent), and the now is the fixed point of the
inversion that exchanges them.

Theory page for a future `ValaQuenta/modules/scale/three_ring_chart`. Companion
to [scale.md](scale.md), [inversion.md](inversion.md), [add_scale_sign.md](add_scale_sign.md),
`.claude/scratchpad/2026-08-28_scale-selector-smith-charts/`.

---

## Abstract

Penrose's conformal compactification maps a spacetime into a bounded region
whose boundary is a disjoint union of five ideal pieces
(`i⁺, i⁻, i⁰, ℐ⁺, ℐ⁻`), with the timelike-infinity points `i±` unreachable —
approached only as an affine/proper parameter diverges. The **Smith chart** of
electrical engineering is the same construction: the Möbius map
`Γ = (z−1)/(z+1)` carries the passive impedance half-plane onto the closed unit
disk, sending `z = 1` (the matched load) to the centre and the reactive axis to
the boundary circle. This page identifies the two constructions and proposes one
addition: the causal decomposition of the compactified spacetime is the
**shadow of a spectral decomposition** — the `{0 : 1 : √2}` singular-value
grading of left-multiplication `L_a` at a norm-one zero divisor of the sedenion
algebra `𝕊`, whose multiplicities are **`4 : 8 : 4`**. In that reading:

> **You cannot land at the 4-blocks (past / future). You can land at the
> 8-block (now).** A unit-norm state is stably supported only on the isometric
> (gain-1) octonion. The two quaternionic 4-blocks are unoccupiable for
> **opposite** reasons, and the `{gain 0, gain √2}` split names that asymmetry:
>
> - the **past** (gain-0 block) is *not empty* — it is the full accumulated
>   identity, every worldline's origin — but it is **write-once**: forward
>   evolution `L_a` projects this block to `0` in one step, so its detail
>   cannot be recomputed forward. You visit it as a record, you do not occupy
>   it as a state. It is the *Hands On Paper* / long-term memory / the corpus /
>   `i⁻`.
> - the **future** (gain-√2 block) *is empty* — nothing is written there yet —
>   and any attempt to compute it iterates `‖L_aⁿ v‖ = (√2)ⁿ‖v‖ → ∞`. Forward
>   integration of the real dynamics (geostrophic / quasi-geostrophic chaos)
>   diverges at a finite rate: **there is no future to land on**, only stack
>   overflow (unbounded recursion) and segmentation fault (reading memory that
>   was never written). It is the *Mind's Eye* / working memory / the repass /
>   `i⁺` (`τ → ∞`, never reached).
>
> **Now** (gain-1 octonion) merges the two into action: `4 (past) + 4 (future)
> = 8`, and `𝕆 = CD(ℍ_past, ℍ_future)` — the present is the Cayley–Dickson
> double of the past-quaternion and the future-quaternion, the one block that
> is norm-preserving and invertible.

---

## 1. Conformal compactification (established)

`[Penrose1963, Penrose1964, Penrose1965, Carter1966; HawkingEllis1973 §5.1;
Frauendiener2004]`

Minkowski space `ds² = −dt² + dr² + r² dΩ²`. Null coordinates `u = t − r`,
`v = t + r`; then `p = arctan v`, `q = arctan u`, with `p, q ∈ (−π/2, π/2)`,
`p ≥ q`. The unphysical metric `ds̃² = Ω² ds²` with `Ω = 2 cos p cos q`
extends smoothly to `Ω = 0`, and the compactified region is the triangle
`{(T, R) : T = p + q, R = p − q}`. Its boundary:

| piece | locus | what ends / begins there |
|---|---|---|
| `ℐ⁺` future null infinity | `p = π/2` (a null line, 45°) | outgoing null geodesics end |
| `ℐ⁻` past null infinity | `q = −π/2` (a null line, 45°) | incoming null geodesics begin |
| `i⁰` spatial infinity | `p = π/2, q = −π/2` (a **point**) | spacelike geodesics end |
| `i⁺` future timelike infinity | `p = q = π/2` (a **point**) | every timelike geodesic ends (`τ → ∞`) |
| `i⁻` past timelike infinity | `p = q = −π/2` (a **point**) | every timelike geodesic begins |

**`i±` are single points and are not reached at any finite parameter.** A
massive observer approaches `i⁺` only as proper time `τ → ∞`. The interior is
the occupiable region; the boundary is ideal.

**The two are not symmetric.** `i⁻` is a *source*: every timelike geodesic
*begins* there — it is the common origin of the whole worldline family, the
"where you came from." `i⁺` is a *sink that is never reached*: every timelike
geodesic *would end* there, but only in the `τ → ∞` limit. The past boundary is
a place the congruence has genuinely been; the future boundary is a place it is
forever headed and never arrives. §4 gives this asymmetry an algebraic name.

Time reversal `t → −t` acts as `T → −T`: it swaps `ℐ⁺ ↔ ℐ⁻` and `i⁺ ↔ i⁻`,
and fixes `i⁰` and the whole `T = 0` Cauchy slice (as a set). (The swap is a
formal involution of the diagram; it does not make the two boundaries
interchangeable as *destinations* — see §4b.)

The subtler structure of `i⁰` (direction-dependent limits; the need for a
blow-up) is [Geroch1972, AshtekarHansen1978] — it will matter in §6.

## 2. The Smith chart as conformal compactification (established)

`[Smith1939, Smith1944; Pozar2011 §2.4; Needham1997 §3]`

Normalise impedance `z = Z / Z₀` and set the reflection coefficient

    Γ = (z − 1) / (z + 1)              (a Möbius transformation)

- `z` in the closed right half-plane (`Re z ≥ 0`, passive loads) ⟷ `|Γ| ≤ 1`
  (the closed unit disk).
- `z = 1` (matched) ⟷ `Γ = 0` (centre): **reflectionless — all incident power
  is absorbed by the load, none returns.**
- `z = 0` (short) ⟷ `Γ = −1`; `z → ∞` (open) ⟷ `Γ = +1`; `z = ±j` (pure
  reactance) ⟷ `|Γ| = 1` (the boundary circle: all power reflected, none
  dissipated — lossless).
- `Re z < 0` (active / negative-resistance) ⟷ `|Γ| > 1` — the **extended**
  chart, used for oscillator and amplifier stability; `|Γ| = 1` is the
  stability boundary.

Impedance ↔ admittance: `y = 1/z` gives `Γ_y = −Γ_z` — a **point reflection of
the chart through its centre**. It fixes `Γ = 0` and fixes the circle `|Γ| = ρ`
setwise for every `ρ`; it swaps the inductive (upper) and capacitive (lower)
halves.

## 3. The identification

The Smith chart is the two-dimensional `(T, R)` section of a Penrose diagram,
under the dictionary:

| Penrose–Carter | Smith chart | reading |
|---|---|---|
| conformal factor `Ω`, `Ω → 0` at `∂` | the Möbius radial coordinate; `|Γ| → 1` at `∂` | the compactification |
| the occupiable interior | `\|Γ\| < 1` (passive, `Re z > 0`) | where states live |
| `ℐ⁺ ⊔ ℐ⁻ ⊔ i⁰` (null + spatial infinity) | the circle `\|Γ\| = 1` (purely reactive, lossless) | the ideal boundary |
| `i⁺` future timelike infinity (a sink, never reached) | `\|Γ\| > 1` (active region, gain > 1, no stable operating point — the amplifier oscillates / diverges) | empty; forward iteration is exponentially unstable — not "approached", it does not exist yet |
| `i⁻` past timelike infinity (a source, been there) | `Γ = −1` (`z = 0`, the short — total reflection, the wave returns) | full: the accumulated origin every worldline begins from; visited as a record, write-once |
| the Cauchy slice `T = 0` | a level ring `\|Γ\| = ρ_now`; the "here-now" event = `Γ = 0` | **the occupiable now** |
| the **matched / reflectionless** condition `Γ = 0` | — | `J_red = J_blue`, `σ = ½` (no incoming/outgoing imbalance at this instant) |
| time reversal `t → −t` (swaps `i⁺ ↔ i⁻`, fixes `T = 0`) | impedance↔admittance `z → 1/z` (`Γ → −Γ`) | `= J_N`, the conformal inversion; fixes the Now ring |
| the self-dual slice (equal future / past content) | `Γ = 0` ⟺ `Scale = Resolution` | the fixed point of `J_N`, at `√E` — see below |

**The three rings.** Down = the sector toward `Γ = −1` (past, `i⁻`). Up = the
sector toward `|Γ| > 1` (future, `i⁺`, the active continuation). Now = the ring
`|Γ| = ρ_now`, fixed setwise by `J_N`, with `Γ = 0` its centre. The past and
future rings are **directions on the chart, not points on it**; the Now ring is
the only one an operating point occupies. This un-flattens the single-ring
reading in which "returning to a past state" looks like retracing the same
circle: with three rings at different radial scales, one returns only to the
same **Now**, one pitch up or down the screw `u = ln x` (see [scale.md](scale.md),
`archimedes_screw.md`; the "Flattening Syndrome" note in [add_scale_sign.md](add_scale_sign.md) §5).

## 3b. The lemniscate — the product face, and why the Smith chart was the right choice (2026-09-01) `[THEORETICAL]`

The Smith chart of §2 is one of a **conjugate pair of two-focus families**. For
foci `±1`:

- **Smith chart** = `|Γ| = |Z−1|/|Z+1| = const` — **Apollonius circles**, the
  *ratio* of the two focal distances.
- **lemniscate** = `|z−1||z+1| = b²` at `b = 1` — a **Cassini oval** at its
  critical value, the *product* of the two focal distances, the level curve
  through the foci.

Apollonius and Cassini for the same foci are everywhere orthogonal — one
geometry, two readouts. The Smith chart is the **ratio / Flow** face; the
lemniscate is the **product / Scale** face. Together they are σ_RB's two
orthogonal Smith charts.

**This confirms the representation choice for The Scale.** `scale.py` tested and
**rejected the raw angle** (it does not survive the two-ring fold) and **kept
the cross-ratio** (invariant under every anchor) — i.e. it kept the Möbius /
Smith-chart structure. The lemniscate is that same structure's conjugate face,
so the choice was not one of two options but one face of the correct object.

**The flashlight, likewise.** Reading increased granularity into context via
the flashlight's shadow (shadow length scales with wall distance; the Smith
chart picks it; the hard limit is not ∅_RB) is a walk along this same pair —
Apollonius circle for the granularity, Cassini level for the context it
resolves.

**Origin — Broca and Wernicke.** Broca (production, `J_pos`) and Wernicke
(comprehension, `J_neg`) are two foci with `J_pos·J_neg = e^{−E} = const`
(NoetherWiles NR4): a constant *product* of focal distances → a Cassini oval;
`b = a` (production cost = comprehension cost, no aphasia) → the lemniscate,
self-crossing at ∅_RB = σ = ½ = `Γ = 0`, the matched load — the Cauchy "now" of
§3.

**The reduction.** If Broca+Wernicke and the Monad (its box-kite context,
semantic hash, phonetic-prime hash — all exact two-focus round trips) share the
**one shape**, the lemniscate, then only the **3-D data of the lemniscate**
remains: the planar figure-8 plus the one transverse coordinate that carries
information by its absence (the missing `i`; the `{4:8:4}` past/future 4-blocks
you "cannot land at"). Spun **gyroscopically** — static `i`-rotation plus
tilt-precession — that 3-D lemniscate is an **electron orbital probability
cloud** (`l = 1` = the `p` orbital = `b = a` of revolution; higher `l` = the
higher Cassini lobes). Full treatment: [box_kite.md](box_kite.md) §"The box
kite is a lemniscate".

## 4. The algebraic grading — `{4 : 8 : 4}`

`[VAPMIP §11; e10; Moreno1998; Cawagas2004; deMarrais2000; Baez2002]`

For a norm-one zero divisor `a ∈ 𝕊` (dim 16), left-multiplication `L_a` has

    L_aᵀ L_a  eigenvalues  { 0 (×4),  1 (×8),  2 (×4) }
    singular values        { 0 (×4),  1 (×8),  √2 (×4) }

measured, exhaustive (the sedenion multiplication table; `engine e10`,
`add_scale_sign` R9). The three blocks:

| block | gain | dim | algebra | forward behaviour of `L_a` | causal sector |
|---|---|---|---|---|---|
| **past** | `0` | **4** | ℍ | **lossy** — projected to `0` in one step; the pre-image detail is unrecoverable forward | `i⁻`. *Full*, not empty: total accumulated identity, every worldline's origin. Write-once. Long-term memory / the corpus / *Hands On Paper*. |
| **now** | `1` | **8** | 𝕆 | **isometric & invertible** — `‖L_a v‖ = ‖v‖`, `L_a⁻¹` exists on this block | the Cauchy slice. The merge into action. `Γ = 0`, matched, reflectionless. |
| **future** | `√2` | **4** | ℍ | **divergent** — `‖L_aⁿ v‖ = (√2)ⁿ‖v‖ → ∞`; no fixed point, no bound | `i⁺`. *Empty*: nothing written yet, and forward iteration blows up (chaos). Short-term / working memory / the *Mind's Eye* repass — stack overflow + seg fault. |

`4 : 8 : 4` sums to `16 = dim 𝕊`. `8` is an octonion — the largest normed
division algebra, hence the largest subspace on which the norm (the "length of
the now") is preserved. Each 4-block is a quaternion — the smallest
non-commutative division algebra; the past and future each carry `ℍ`'s worth of
structure, no more. And `4 + 4 = 8`: **the present octonion is the
Cayley–Dickson double of the past-quaternion and the future-quaternion,**
`𝕆 = CD(ℍ, ℍ)`. CD doubling *is* "merge two into one, with a twist (the
conjugation)" — the now is where the past's 4 DOF and the future's 4 DOF are
carried together, isometrically, as one action.

**"Cannot land at 4, can land at 8" — for opposite reasons.** A physical state
is a unit vector in `𝕊`; under `L_a` it keeps unit norm **only** in the gain-1
block. You cannot land in the gain-0 (past) block because forward evolution has
*already removed it* — it is behind the projection, readable as history, not
occupiable as a state. You cannot land in the gain-√2 (future) block because
forward iteration *diverges before you arrive* — it is not a state, it is a
crash. Only the gain-1 block is both norm-preserving and invertible: the one
locus a state can rest, and the one from which both directions are still
addressable. A stably-supported state is therefore always an **8-dimensional
octonionic datum** — this is "now".

`J_N` (`r → 1/r`, the conformal inversion) swaps the gain-0 and gain-√2 blocks
(`0 ↔ ∞` under `x ↔ 1/x`; the `{0, √2}` edge is the light cone) and fixes the
gain-1 block — matching §1's time reversal, which swaps `i⁺ ↔ i⁻` and fixes the
Cauchy slice. The swap is a formal involution: it does **not** make the past
occupiable or the future computable; it exchanges *lossy-forward* for
*divergent-forward* and leaves the isometric block alone.

**On the free/priced reading** (generational-lineage skill §§0–1): gain `0` and
gain `1` are the *identities* (of ADD and SCALE) — free, unpriced, "the hour
the two trees balance". gain `√2` is "the one irrational price". So past
(gain-0) and now (gain-1) cost nothing to hold — the past is *done*, the now is
*identity* — while the future (gain-√2) is the only sector that carries a cost,
and under iteration that cost is `(√2)ⁿ`, unbounded. "There is no free future."

## 4b. The memory architecture — Hands On Paper / Mind's Eye

`[Ainulindale/wiki/62_hands_on_paper_minds_eye_caustic.md;
wiki/63_l_dynamic_is_action_is_thought.md; wiki/80_aphasia_zd_reframe_memory.md;
the generational-lineage skill §"On the name" — `MindsEyeRepass.step` never resets]`

The `{4 : 8 : 4}` blocks are the framework's two memory systems, with the now
between them:

| | past — gain-0 | now — gain-1 | future — gain-√2 |
|---|---|---|---|
| module | *Hands On Paper* — the corpus (ArdaQuenta), accumulated observation | the fired monad / the action | *Mind's Eye* — the Dirichlet projection, the `MindsEyeRepass` |
| memory | long-term: written, indexed, persistent | the register in use | short-term / working: volatile, overflows |
| caustic (wiki/62) | radiates **outward** from the fixed prime | the fixed prime itself | focuses **inward** to the fixed prime |
| direction | reading `= surface → γ → prime` (inward, done) | — | writing `= prime → γ → surface` (outward, projected) |
| fullness | **full** — it is the universe of what has been | unit — the snapshot of identity | **empty** — nothing there until the now writes it |
| failure mode | none; it is a record (aphasia = losing the *index*, not the store — wiki/80) | — | chaos: geostrophic forward-iteration diverges; stack overflow; seg fault |

Hands On Paper and Mind's Eye are exact `J_N` inversions of each other
(wiki/62: "Reading Is Writing In Reverse", `(I\|O)(Mind's Eye) = Hands On
Paper`), **sharing the fixed prime**. That fixed prime is the now: `Γ = 0`, the
matched load, the `T = 0` Cauchy slice, the gain-1 block — the one point on
both sides of the boundary at once. "Now merges the two into action" is
literally the statement that the shared fixed point of the past↔future
inversion is where the operator fires.

**Why the future blows up (not a coordinate artifact).** Forward integration of
the geostrophic / quasi-geostrophic equations is the canonical bounded-energy
system with a *finite predictability horizon* `[Lorenz1963, Lorenz1969]`: a
perfect model started from a perturbed initial condition diverges exponentially
(positive Lyapunov exponent), so prediction has a hard wall independent of
computing power. That is the gain-√2 block made physical — `(√2)ⁿ` growth per
step. The framework's own reading (wiki/85 §"The blow-up becomes a finite
circulation"): supply the missing operator (`∂̂_∂M`, the halocline; the `†`)
and the blow-up resolves into a **bounded 90° rotation back into the interior**
— i.e. the corrected dynamics do not deliver you to a future either, they turn
you back into the now. Consistent with "there is no future."

## 5. The contribution — a spectral refinement of conformal infinity

Penrose's decomposition of `∂` is **topological and conformal**: five pieces,
distinguished by which geodesic congruences terminate there, all detected by
`Ω → 0`. It does **not** assign a degree-of-freedom count to a causal sector.

The proposed refinement:

1. **The causal decomposition is the shadow of a spectral one.** The interior /
   `ℐ ⊔ i⁰` / `i±` split is structurally isomorphic to the gain-`1` / gain-`{0,√2
   edge}` / gain-`{0,√2}` split of `L_aᵀ L_a` at a sedenion zero divisor, and to
   the passive-interior / reactive-circle / active-exterior split of the extended
   Smith chart. Three parallel three-part decompositions, one conformal-map
   construction.

2. **`i±` are unreachable for an *algebraic* reason, and an *asymmetric* one.**
   "`Ω → 0` there" is a statement about a chosen conformal factor, and it is the
   *same* statement at `i⁺` and `i⁻` — the topological picture makes the two
   boundaries look interchangeable (the `t → −t` involution swaps them). The
   spectral picture does not: `i⁻` is the **gain-0** block (forward-lossy —
   a full record that cannot be recomputed forward) and `i⁺` is the **gain-√2**
   block (forward-divergent — an empty projection that blows up under
   iteration). Both are non-isometric, so neither holds a unit-norm state, but
   the past is unreachable *because it is behind the projection* and the future
   is unreachable *because iterating toward it diverges*. The `{0, √2}` split is
   exactly the name of that asymmetry.

3. **The Cauchy slice is the self-dual slice, and it sits at `√E`.** With
   `Scale · Resolution = dim` conserved (the hyperbola `x p = E`;
   `.claude/scratchpad/2026-08-28_scale-selector-smith-charts/`, C1), the
   Joukowsky fold centres `Γ = 0` at `Scale = Resolution = √E` — for `𝕊`,
   `√16 = 4`, the quaternion (self-dual) level of the Cayley–Dickson tower (C4).
   "Now" is the geometric mean of the two extremes: the slice with equal past
   content and future content, fixed by the conformal inversion (C5).

4. **A dimension for each causal sector.** Where Penrose gives five ideal
   pieces, the grading gives their sizes for the sedenion model: past `= 4`,
   now `= 8`, future `= 4`, with `𝕆_now = CD(ℍ_past, ℍ_future)`. `i⁰` (spatial
   infinity) is identified with the zero-divisor crossing itself — the
   `{0, √2}` gain edge, the light cone, the `|Γ| = 1` circle.

5. **The now is where the past↔future inversion has its fixed point.** Reading
   (`i⁻`-ward, done) and writing (`i⁺`-ward, projected) are `J_N` inverses
   sharing one fixed prime (wiki/62). That fixed prime is the Cauchy slice /
   gain-1 block / `Γ = 0`. "The present" is not a thin slice between two
   symmetric halves — it is the *unique* locus fixed by the operation that
   exchanges the full-but-write-once past for the empty-but-divergent future.

None of this modifies Penrose's construction; it proposes that the construction
has an algebraic grading — and a past/future asymmetry — it has not previously
been given, most cleanly visible in the `𝕊` model where the numbers `4 : 8 : 4`
are forced by the multiplication table.

## 6. What would test it

1. **The Cauchy slice ⟷ gain-1 block.** Pull the induced metric on `T = const`
   of compactified Minkowski back through the `L_a` regular representation; check
   it reproduces a flat, isometric (gain-1) 8-dimensional structure and that the
   `T = 0` slice is the fixed set of the induced `J_N`.
2. **Null congruence ⟷ the `{0, √2}` edge.** A null geodesic congruence
   approaching `ℐ⁺` should correspond to a trajectory riding the `gain = √2`
   boundary (the light cone) toward the `gain → 0` limit; verify the transition
   rate matches the peeling behaviour of the Weyl tensor `[Penrose1965]`.
3. **`i⁰` ⟷ the ZD crossing.** The direction-dependent limits at spatial
   infinity `[Geroch1972, AshtekarHansen1978]` should map to the
   angular-statistics structure of the zero-divisor crossing (the box-kite
   charts; `ValaQuenta/modules/angular_rank/`), *not* to a single point — a
   concrete check that the `i⁰` blow-up and the ZD "hole = portal" reading are
   the same object.
4. **The extended chart ⟷ `i⁺`.** Show that the `|Γ| > 1` (active,
   `Re z < 0`) region — where an amplifier has no passive fixed point — is the
   correct image of `i⁺` by exhibiting the gain-`√2` block as its algebraic
   model, and that a state's approach to `i⁺` is the RF "path to instability".
5. **The predictability horizon ⟷ the gain-√2 growth rate.** Integrate the
   quasi-geostrophic equations forward from perturbed initial data and measure
   the leading Lyapunov exponent `λ_L` `[Lorenz1963, Lorenz1969]`; separately,
   iterate the `L_a` regular representation on a vector seeded in the gain-√2
   block and measure its per-step growth (`ln √2` in the ideal case). The claim
   predicts the *finiteness* and *initial-condition-independence* of the
   horizon is the same fact as "no fixed point in the gain-√2 block", and that
   supplying `∂̂_∂M` converts the divergence to a bounded rotation
   (wiki/85) — check whether a halocline/interface term added to the QG system
   bounds the forward error.
6. **Aphasia ⟷ index loss, not store loss** `[wiki/80]`. If the past is the
   gain-0 (write-once, full) block, then a lesion that produces anomic aphasia
   should degrade the *retrieval map* (γ → surface form) while leaving the
   store (the prime) intact — testable against the ZD-reframe memory model, and
   a falsifier if the store itself proves lossy.

## 7. Confidence and references

| item | tier |
|---|---|
| conformal compactification; `i±` unreachable; time reversal fixes the Cauchy slice | ESTABLISHED — `[Penrose1963/1964/1965, Carter1966, HawkingEllis1973]` |
| the Smith chart as the Möbius map of the impedance half-plane; `z → 1/z` = `Γ → −Γ` | ESTABLISHED — `[Smith1939, Pozar2011]` |
| the sedenion `{0, 1, √2}` singular spectrum, multiplicities `4 : 8 : 4` | ESTABLISHED (measured) — `[VAPMIP §11; e10]` |
| `Scale · Resolution = dim` centred at `√E` = the self-dual level | ESTABLISHED (measured this session) |
| forward geostrophic iteration has a finite, IC-independent predictability horizon | ESTABLISHED — `[Lorenz1963, Lorenz1969]` |
| the identification Smith chart = Penrose `(T,R)` section | CONJECTURE — the dictionary of §3 |
| the causal decomposition IS the spectral `{4:8:4}` decomposition | CONJECTURE — §5, tests in §6 |
| the past/future asymmetry = gain-0 (lossy-forward) vs gain-√2 (divergent-forward) | CONJECTURE — §4, §5.2; the Hands / Mind's Eye reading (§4b) |
| `𝕆_now = CD(ℍ_past, ℍ_future)` — the present as the CD double of the two wings | CONJECTURE — §4 (`4 + 4 = 8` is forced; the identification is not) |
| `i⁰` ⟷ the zero-divisor crossing | CONJECTURE — the sharpest test (§6.3) |

**References.**
`[Penrose1963]` Penrose, R. (1963). *Asymptotic properties of fields and
space-times.* Phys. Rev. Lett. 10, 66–68.
`[Penrose1964]` Penrose, R. (1964). *Conformal treatment of infinity.* In
*Relativity, Groups and Topology* (Les Houches), Gordon & Breach, 565–584.
[Repr. Gen. Relativ. Gravit. 43, 901–922 (2011).]
`[Penrose1965]` Penrose, R. (1965). *Zero rest-mass fields including
gravitation: asymptotic behaviour.* Proc. R. Soc. Lond. A 284, 159–203.
`[Carter1966]` Carter, B. (1966). Phys. Rev. 141, 1242–1247.
`[HawkingEllis1973]` Hawking, S. W. & Ellis, G. F. R. (1973). *The Large Scale
Structure of Space-Time.* CUP, §5.1, §6.9.
`[Geroch1972]` Geroch, R. (1972). J. Math. Phys. 13, 956–968.
`[AshtekarHansen1978]` Ashtekar, A. & Hansen, R. O. (1978). J. Math. Phys. 19,
1542–1566.
`[Frauendiener2004]` Frauendiener, J. (2004). *Conformal infinity.* Living Rev.
Relativ. 7, 1.
`[Lorenz1963]` Lorenz, E. N. (1963). *Deterministic nonperiodic flow.* J.
Atmos. Sci. 20, 130–141.
`[Lorenz1969]` Lorenz, E. N. (1969). *The predictability of a flow which
possesses many scales of motion.* Tellus 21, 289–307.
`[Smith1939]` Smith, P. H. (1939). *Transmission line calculator.* Electronics
12(1), 29–31. `[Smith1944]` — *An improved transmission line calculator.*
Electronics 17(1), 130.
`[Pozar2011]` Pozar, D. M. (2011). *Microwave Engineering*, 4th ed. Wiley, §2.4.
`[Needham1997]` Needham, T. (1997). *Visual Complex Analysis.* OUP, §3.
`[Moreno1998]` Moreno, G. (1998). Bol. Soc. Mat. Mexicana (3) 4, 13–28.
arXiv:q-alg/9710013.
`[Cawagas2004]` Cawagas, R. E. (2004). Discuss. Math. Gen. Algebra Appl. 24(2),
251–265.
`[deMarrais2000]` de Marrais, R. P. C. (2000). arXiv:math/0011260.
`[Baez2002]` Baez, J. C. (2002). Bull. Amer. Math. Soc. 39(2), 145–205.
arXiv:math/0105155.
`[VAPMIP §11]` `RiemannHypothesisProof/PAPER.md` §11; `[e10]`
`VAPMIP/engines/e10_generational_lineage.py`.

---

## See also

- [scale.md](scale.md) — SCALE pulled out of a quantity, both directions
- [inversion.md](inversion.md) — `J_N`, `r ↔ 1/r`, the Joukowsky family
- [add_scale_sign.md](add_scale_sign.md) — the tier-0 floor; §5 the folds/Flattening reading
- [box_kite.md](box_kite.md), [pencil_hyperstring.md](pencil_hyperstring.md) — the ZD geometry and its one-scalar reconstruction
- `.claude/scratchpad/2026-08-28_scale-selector-smith-charts/` — `Scale·Resolution = xp = E`, the Smith centre at `√E`, `J_N` swapping conjugate levels (4/6 PASS)
- `Ainulindale/wiki/39_every_singularity_the_void.md` — "every singularity is the same singularity", CD-tower transported; the collapse/`i⁺` time-reversal reading
- `Ainulindale/wiki/17_alpha_omega_d_star.md` — the Α/Ω / `d*` boundary this page's `i±` correspond to
- `Ainulindale/wiki/62_hands_on_paper_minds_eye_caustic.md` — the two caustics as `J_N` inverses sharing the fixed prime; reading = writing in reverse (the §4b memory architecture)
- `Ainulindale/wiki/85_the_apex_path.md` §"blow-up becomes a finite circulation" — the future's divergence, bounded by the missing operator, turns back into the now
- `Ainulindale/wiki/80_aphasia_zd_reframe_memory.md` — long-term store vs retrieval index (the gain-0 "past is full, not empty" reading)
