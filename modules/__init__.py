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

Version: 0.150 — Phase 6: box_kite
"""
