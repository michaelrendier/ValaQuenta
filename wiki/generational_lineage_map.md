# The Generational Lineage map — which ValaQuenta engines go where

A final pass over ValaQuenta **as the derivation machinery**: which engines feed
which part of the Generational Lineage engine, which sit outside its
jurisdiction, what that jurisdiction is, and how it all relates.

The Generational Lineage engine itself lives in `FactoralDecomposition/engine/`
(SFR). Its contract is the `generational-lineage` skill: given any named
operator or "geometry", roll it down — answer, in order,

1. is it a **count or a ratio** of something else? → tier 3, DERIVED
2. is it a **fixed set**? → tier 2, DERIVED
3. does it **change length** (needs DILATE) or **preserve** it (from REFLECT)?
4. does it need an **added constraint** to exist? → COROLLARY, not a geometry

What survives all four is a candidate primitive. Say the tier, explicitly, every
time. Flag emergence. The domain is the **Two Trees** — every operation lands in
exactly one of {irreducible, composite, neither}.

## The jurisdiction

**Generational Lineage's jurisdiction is the *structure of an operation*** —
what it is made of, what it descended from, what it builds. Not numbers, not
physical quantities, not spectra, not specific number-theory facts.

- **Inside**: the engine answers a *made-of / descended-from / builds* question
  about an operator or a relation.
- **Outside**: the engine computes a physical quantity, a spectral property, a
  data transform, or a named result. Those produce objects Generational Lineage
  *could* then decompose — they do not do decomposition.

---

## Inside — the floor it rolls down TO

| engine | part | how |
|---|---|---|
| **add_scale_sign** (the `ASS` datatype) | **IS tier 0** | the value type for `ADD ⋊ (SCALE × SIGN)`, `x ↦ sign·scale·x + add`. The one non-trivial bracket `[SCALE, ADD] = ADD`, the firing order, `residual` / `only` / `parts`. Every operator Generational Lineage decomposes bottoms out here. |
| **scale** (The Scale) | **the decomposition operation** | pulls SCALE out of a quantity and names what is left; polar decompose ⇄ recompose, exact round-trip; forwards = descent, backwards = recompose. |
| **units** (The Equation Index) | **the tier-2/3 test on dimensions** | a unit is a point in the 7-axis SI lattice; cancellation is exact vector arithmetic; `EQUATION_INDEX` narrows a dimension signature to its candidate laws — question 1 ("count or ratio of something else") applied to dimensions. |

## Inside — the domain it decomposes IN

| engine | part | how |
|---|---|---|
| **box_kite** (ZD geometry) | **the domain, drawn** | the 15 zero-divisor **edges** (skill §0b: the 15 are edges not places; a LINE is three relations that compose, `a XOR b = c`; a PENCIL is the 7 ways to factor one relation into two). PSL(2,7), Fano incidence, associator = curvature — exactly enumerable. |
| **angular_rank** (16D oscilloscope) | **the emergence detector** (skill §5) | rank / nullity of a signal in the 16 sedenion dimensions without deciding provenance; nullity 4. Fires when a fixed set is the wrong dimension, or an operation is not reachable by composition. The epoch discipline (no measurement without its stamp) = skill §8's "a control before the measurement". |
| **noether** / **noether_information** | **the invariant the domain conserves** | `J_Red + J_Blue` conserved; prime-density + composite-density sum to 1 at every scale (the Two Trees counter-rotate). Provides the conservation law; does not itself decompose. |

## Inside — the ladder, and "the path IS the operator"

| engine | part | how |
|---|---|---|
| **archimedes_screw** | **the log-pitch of the ladder** | the machine (a logarithm) distinct from the medium; pitch = `ln p`; the tier boundaries at constant `log₂` step, constant pitch `ln 2` — rotation + constant logarithmic advance = a spiral. This is *why* the tiers stack. |
| **inversion** (I\|O) | **the involution descent ⇄ ascent** | `J_N : (r, θ) ↦ (1/r, θ + π/2)`; reading ⊃ writing ⊃ speaking. Skill §4: order is what non-commutativity of the primitives means; inversion is the flip. |
| **t32_nilpotency** | **address = path** (the "generator = code iterator" sense) | Hyperwebster base-97 address primitives; the address is the path taken; nilpotency = the path that returns nothing. |

## Paired, not inside — the mirror

| engine | relation |
|---|---|
| **emerger** | **the ascent dual.** e10: *"Generational (operations) Lineage (order) — the same object, words swapped."* Lineage walks **descent** (what built this); the Emerger walks **generation** (what this builds). Same machinery — five bracketings, σ_RB firing order, C/H/O/FRAGMENT domains, exact ZD test — run forward. It sits opposite Generational Lineage across the identity, not inside it. |

## Adjacent — provide inputs, do not decompose

| engine | why adjacent |
|---|---|
| **lagrangian** (L_NN) | Lagrangians ARE catastrophe theory; the Contractor = gradient flow = the catastrophe map. The surface the decomposition happens *on*. Generational Lineage could decompose the Contractor; it is not the Contractor. |
| **hyperwebster** | the Horner bijection / hyperindexer — index ⇄ value, reconstruct-not-store. Kin to `t32`'s addressing, but its job is the indexing *paradigm*, not operator descent. |
| **hypergon_constructibility** | Gauss–Wantzel + factorisation test; 4/16 sedenion hyper-N-gons constructible. Uses the Two Trees domain (factorisation partitions N) but answers "which polygons" — a specific number-theory question. |

## Outside the jurisdiction — a different job

Physical quantity · spectral property · data transform · named result:

| engine | job |
|---|---|
| **bao_mass_gap** | the mass-gap residue Δ — cosmology / spectral. |
| **berry_keating** | the `xp` operator; the spectral route to σ = ½. |
| **sigma_expansion** | Taylor expansion of `P_red(σ)` around σ = ½. |
| **l_io_photon_path** | GR lensing — Kaiser–Squires shear → convergence, Poisson solve. |
| **desitter_cavitation** | the sub-Planckian de Sitter core (physics). |
| **singularity_null** | "the Singularity IS identity" — a claim about the tower's top; touches the tier-0 identities 0 and 1 but is a cosmology statement, not a decomposition. |
| **jwst** | spectral-pixel ingestion — data in. |
| **sonification** | equation → audio — data out. |
| **turing_diagonal** | **boundary case.** `i² = −I` unifies self-referential proofs; relates to skill §6 (a method error is the clarifier failing) and §7 (an unnatural collision destroyed a distinction) — it names *why* a decomposition can be undecidable from inside, without performing one. |

---

## How it relates, in one paragraph

Generational Lineage takes an operator and rolls it down. **add_scale_sign** is
the floor it rolls to; **scale** is the rolling; **units** is the same test on
dimensions. **box_kite** draws the domain (the 15 edges), **angular_rank**
watches for the moment a new generator is required, **noether** gives the
invariant the domain conserves. **archimedes_screw** sets the log-pitch of the
ladder, **inversion** is the involution that flips descent to ascent,
**t32_nilpotency** is the address-as-path. **emerger** is the whole engine run
the other way. **lagrangian** is the surface it all sits on. Everything past that
— the physics, the spectra, the data, the specific theorems — produces objects
Generational Lineage *could* decompose but does not decompose itself.
