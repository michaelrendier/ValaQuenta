"""
ainulindale_engine.modules
===========================
Equation modules. Each subdirectory is a self-contained module
implementing the EquationModule registry contract.

Current modules (Phase 1):
    inversion   — (I|O) map, gradient flow, phi attractor

Current modules (Phase 2):
    lagrangian         — L_NN, all four terms, running coupling
    noether            — Emmy Noether conserved currents, violation diagnostics
    noether_information — Information current, entropic arrow, blockchain ledger
    spherical          — Y_lm harmonics, Courant theorem, Tesla/Schumann, J_N mode ID

Current modules (Phase 3 — Second Age):
    berry_keating      — H_NN candidate, d* gap (OP-3 RESOLVED: T_transform = Wiles 1995)
    h_rb_hat           — Σ_RB: RedBlue Summed Integral
                         The inductive boundary sum. R̂ and B̂ over all primes.
                         Facets: GR, Yang-Mills, QM, NS (lacks i), Noether, Fermat.
                         SIGMA_RB engine: stroke, oblique crank (d*), trine.
    clay_millennium    — All 7 Clay Millennium Problems derived from Σ_RB
                         RH, Yang-Mills, NS, P/NP, Hodge, BSD, Poincaré (SOLVED).

Planned modules:
    sonification       — Equation-derived audio (radian -> pitch)
    hyperwebster       — HyperWebster hypergalley, monad
    jwst               — JWST spectral pixel module

Current modules (Phase 4):
    sigma_expansion    — Closed-form Taylor expansion of P_red(sigma) around
                         sigma=1/2 (c1, c3 derived, not fitted). Raw
                         |J_red|^2+|J_blue|^2 is NOT constant across sigma —
                         minimum at 1/2, not flat quantum-style conservation.

Current modules (Phase 5):
    archimedes_screw   — The machine, distinct from the medium it lifts.
                         0_RB is the water; the screw is the logarithm.
                         Four search terms (Ordinal, Zeta Index, Digits,
                         Spaces Between) as four coordinates on one axis
                         u = ln x, bound by the von Mangoldt explicit
                         formula. psi jumps by exactly ln p at x = p —
                         the leaf-drop magnitude IS the prime. Lambert-W
                         inverse of the zero count (same W whose fixed
                         point W(1)=Ω_ZS pins σ=½). RH as the shared
                         amplitude envelope 2√x. Ramification leg:
                         the Euler factor degenerates at exactly the
                         factors of N in ℚ(√N).

                         v0.2 (2026-08-05) adds the composite side: the
                         leaf falls at gpf(N) not lpf(N) (14 falls at 7),
                         Dickman ρ as the fall-time distribution in
                         u = lnN/ln(gpf N), the harvest Ψ(X/p,p) in closed
                         form, and δ = ½ln(q/p) — a semiprime's entire
                         hidden content, collapsing to 0 for balanced RSA.

    box_kite           — The Box-Kite Debugger. The ZD geometry made
                         visible and exactly enumerable. The object is
                         PSL(2,7) (order 168, Aut Fano), NOT G₂ — Moreno's
                         G₂ is the blow-up that forgets the labelling.
                         42 Assessors, 84 diagonals, 168 unit points, 336
                         annihilating pairs, 7 box-kites of 6 — all derived
                         from the CD table. Each chart is an OCTAHEDRON
                         with Laplacian spectrum {0,4,4,4,6,6}; the zero
                         mode is e₀'s signature. Associator = curvature.

    angular_rank       — The 16D Oscilloscope. Angular content and subspace
                         occupancy, measured on a FROZEN EPOCH. Answers
                         "does this signal carry direction?" (scalar
                         address 0.0000, char encoder 0.0002, phonetic
                         face 0.402 — Phase 27.2) and "did this come from
                         outside?" (energy in ker(L_a), which the internal
                         channel cannot reach) with ONE measurement. Every
                         entry point refuses a live sequence: measuring a
                         span the measured process is growing is
                         iterate-while-modify and drifts silently.
                         Mutation is dated by bearing(), not forbidden.
                         Isotropic null for kernel occupancy is exactly
                         4/16 — report the EXCESS, never the raw fraction.

    scale              — THE SCALE. Decompositional analysis, forwards
                         and backwards — SCALE (tier-0, alongside ADD and
                         SIGN) pulled out of a quantity and named as its
                         own object. polar_decompose/recompose: the exact
                         forward/backward pair for one point (r=scale,
                         theta=scale-blind under self-rescaling, verified
                         round-trip). The two-ring Mobius fold's OWN
                         scale-blind object is a harder, different
                         question: the raw angle does NOT survive the
                         fold (tested, rejected, kept in the record); the
                         cross-ratio of any four points IS exactly
                         invariant under every anchor. pathway_decompose
                         applies the same discipline to a real algorithm
                         (RSA CRT-decrypt as the control case — a genuine
                         dependency fan-out, not a forced linear chain).

    units              — UNITS. Dimensional exponent vectors as a fourth
                         domain for this project's factoral-decomposition
                         discipline (numbers: factor_lineage; processes:
                         pathway_decompose; now units: the 7 SI base
                         dimensions as leaves). Every named compound (N, J,
                         W, Pa, C, V, ohm, F, Wb, T, H) has an exact,
                         computable lineage back to the 7 leaves;
                         cancellation (mol/L * L -> mol) is exact vector
                         arithmetic. A unit carries no numeric content and
                         does no work itself -- a geometry -- but it
                         determines which permutations of content are
                         legal. EQUATION_INDEX: a dimension signature
                         narrows the candidate physical laws, the same
                         move context_vector makes for a word narrowing to
                         its candidate synsets -- units as "word
                         possibilities" for equations.

    desitter_cavitation
                       — NO SINGULARITY. Calculation, not simulation. The
                         black-hole interior is a finite, sub-Planckian de
                         Sitter core — the Abrikosov vortex core made
                         gravitational: the condensate goes to zero (a
                         Riemann zero, winding 1) while density, pressure
                         and curvature stay finite. HOLCUS: the maximum
                         curvature is the de Sitter Kretschmann scalar at
                         L_dS = r_s, K_core(M) = (3/2) c^8 / (G^4 M^4) —
                         M^-4, sub-Planckian for every M > (3/2)^(1/4)
                         m_Pl, with a ringdown-echo delay ~ r_s/c as its
                         observational shadow. The core releases stiff
                         space (Lambda-signed) and stiff matter
                         (radiative) over the hole's life and unwraps at
                         evaporation — the De Sitter Cavitation. Falsifier:
                         a divergent core curvature, or one pinned to
                         K_Planck independent of M. Engine for
                         FourthAgePapers/DeSitterCavitation. confidence
                         floor THEORETICAL.


    emerger            — THE EMERGER. Sedenion Bracketing & Firing Order. A
                         dynamic permutative bracketer over the imaginary
                         part of a Cayley-Dickson algebra; e_0 (real) is the
                         fixed anchor -- the tilt to the i axis -- never
                         bracketed. A bracketing is an ordered partition of
                         {1..15}; each group + anchor spans span({e_0} u G),
                         classified C / H / O / FRAGMENT by closure (the
                         fragment is where zero divisors live). Five
                         canonical brackets: {1:15} grades the algebra;
                         {2:14} is the (e_0,e_8) pointer plane carrying
                         Omega_ZS; {8:8} is the CD double (J_red/J_blue, the
                         ZD equator, J_2 = L vs R); {4:4:4:4} is four SU(2)
                         phases + sigma_RB tilt/axis (Sigma_tilt = net work,
                         = 0 iff sigma=1/2); {4:8:4} is the gain spectrum
                         0/1/sqrt2. The FIRING ORDER is load-bearing: each
                         bracket is conditioned on the ones before it.
                         Canonical (dependency), sigma_RB-phased (Sigma_tilt
                         rotates the entry point into the 12-step precession,
                         4 d* faces : 3 Lambert-W faces), or any permutation
                         (legality reported -- FINDING: some sigma_RB phases
                         select a non-dependency-legal order). ZD tests are
                         exact (rank-deficiency of L_x; equator = purely
                         imaginary + norm-balanced across the CD-double
                         boundary). Exact ZD geometry is box_kite's PSL(2,7);
                         G_2 is the continuous blow-up. The ascent-dual of
                         Generational Lineage: descent = what built this
                         (writing); ascent = what emerges, in what order
                         (reading -- spectroscopy, factoral decomposition).
                         confidence floor THEORETICAL.

Current modules (Phase 12):
    prime_gauge_field  — The Weyl-shaped local-scale connection built
                         directly from Gamma(s)=(s-1)/(s+1), the SCALE
                         engine's own global conformal map. Two candidate
                         connections: A=grad(log|Gamma|), provably flat
                         for ANY holomorphic scalar (Poincare lemma) --
                         generalizes the earlier Schwarzian-derivative-
                         zero finding to any such map, not special to
                         Gamma; and A=(Re Gamma, Im Gamma) read directly
                         as an R^2-valued 1-form, NOT a gradient -- this
                         one carries real curvature, closed form
                         F(s)=2*Im(dGamma/ds), verified against finite
                         differences. The pre-registered prediction
                         (FastInverse paper) -- that the flat locus is the
                         construction's trivial/vacuum point -- partially
                         confirmed: F=0 exactly on the real axis (Gamma
                         real-valued, a defensible "trivial phase" locus)
                         AND on sigma=-1 (Gamma's own pole line, NOT
                         predicted, reported honestly as new rather than
                         folded into the prediction after the fact).
                         confidence floor THEORETICAL.

    oblique_gear       — The Oblique Gear, tested across scale. Does the
                         black-hole crank angle theta_crank = arctan(d*)
                         (h_rb_hat's Witches Hat half-angle) equal the
                         galaxy Stokes-drift rotation curve's own tangent
                         angle at its transition radius r=r_t, making the
                         two `arctan` usages the same fact twice? Computed
                         directly: REFUTED as stated -- 13.82 deg (crank)
                         vs 17.66 deg (galaxy tangent at r_t), a real
                         ~3.84 deg gap. The shared-d*, shared-arctan-family
                         kinship survives; the stronger same-mechanism
                         claim, in this formulation, does not. Confidence
                         floor OPEN.

    spectral_primes    — Spectral Representation of the Primes. The
                         theta(t)-rotation spiral split into spin (major
                         loop, theta'(t), non-resonant) and wobble (minor
                         loop, resonant at the primes -- classical von
                         Mangoldt/Weil, demonstrated via psi(x)
                         reconstruction from the same zero set). Primes
                         are not an artifact of wobbling -- they are its
                         genuine spectral content. Separately tests
                         whether the real-axis tilt (oblique gearing's
                         Omega proportional to sin(tilt)) IS the wobble by
                         minimum-information identification: REFUTED AS
                         TESTED, correlation ~0.037, methodological gap
                         (pointwise vs interval sampling) named and left
                         open. Also: the crossing of the Real Tilt and the
                         central t-Axis is an isolated, simple zero,
                         pinned at sigma=0.500000 to machine precision
                         across every zero tested -- moves up the t-axis,
                         never sideways in sigma. Confidence floor OPEN.

    bracketing_firing_order — The Bracketing Engine, the Firing Order
                         Engine, and Set Membership. THREE domain-
                         independent tools, not one thing tied to
                         add_scale_sign: BRACKETING (exact Bell-number
                         count of unordered groupings, always; exhaustive
                         list only when n<=12), FIRING ORDER (n!
                         sequencings; applying one is a literal
                         permutation -- verified: (3,1,2) applied to
                         [Scale,Sign,Add] gives [Add,Scale,Sign], ASS's
                         own canonical name reached by resequencing), and
                         SET MEMBERSHIP (trajectory/collision detection,
                         generalizing Recaman's own defining rule to any
                         sequence of callables; plus jurisdiction_violation,
                         grounded in GenerationalLineage's decomposition/
                         emerger "two jurisdictions", parametrized not
                         hardcoded). add_scale_sign (3 generators) and the
                         sedenion Emerger bracket (16 components) are both
                         CONSUMERS of this, not separate implementations.
                         Confidence floor ESTABLISHED.

Version: 0.159 — Phase 15: bracketing_firing_order (Bracketing, Firing Order, and Set Membership)
"""
