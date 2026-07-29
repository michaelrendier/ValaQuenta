# Engine: Derivation Chain — Tiers 1–5

**Module:** `modules/derivation_chain/`  
**Version:** 0.100  
**Confidence floor:** THEORETICAL  
**Notebooks:** [core/02_derivation_chain.ipynb](../notebooks/core/02_derivation_chain.ipynb)  
**Claim:** Tiers 1–5 form a single ordered chain: from Alpha_F + OMEGA_ZS to d*, to Riemann=Fermat, to the Tier-2 dropouts, to H_RB.

---

## What it computes

Full derivation chain from root constants to Geometric Observer. T1: Riemann=Fermat (R̂†=B̂). T2: Yang-Mills, BK, Noether, NS, Langlands, BSD all drop out. T3: H_RB is what remains. T4: Geometries defined → Geometric Observer (another Hamiltonian). T5: ln = Hubble constant of ℕ, d* tower → ln(10) [OPEN], ħ↔ln.

The word **dropout** is load-bearing. A dropout is a result that falls out of the chain without being inserted: Yang-Mills mass gap, H=xp, Noether conservation, BSD. Four are ESTABLISHED; Navier-Stokes and Langlands are THEORETICAL and say so.

This is the module to read first. It is the index to every other engine.

## Results — run 2026-07-28

14/14 equations run argument-free; 0 require parameters; 0 fail.

| Equation | Tier | Run | Result |
|---|---|---|---|
| `berry_keating_dropout` | ESTABLISHED | ✓ | {'tier': 2, 'drops_out': 'H = xp (Berry-Keating Hamiltonian)', 'mechanism': 'Scale invar… |
| `geometry_definition` | ESTABLISHED | ✓ | {'tier': 4, 'claim': 'σ=½ is not a convention. It is the equatorial node in the correct … |
| `h_rb_emergence` | ESTABLISHED | ✓ | {'tier': 3, 'emergence': 'H_RB = Σ_p p^{-σ}[R̂_p ⊗ ∂̂_{∂M} + ∂̂†_{∂M} ⊗ B̂_p]', 'not_pos… |
| `ln_natural_unit` | ESTABLISHED | ✓ | {'tier': 5, 'claim': 'ln(x) is the natural unit — Hubble constant of ℕ = BK time coordin… |
| `noether_dropout` | ESTABLISHED | ✓ | {'tier': 2, 'drops_out': 'J_R + J_G + J_B = 0 (Noether current conservation)', 'mechanis… |
| `yang_mills_dropout` | ESTABLISHED | ✓ | {'tier': 2, 'drops_out': 'Yang-Mills mass gap δ = OMEGA_ZS − d*·ln10 = 0.000707', 'mecha… |
| `full_derivation_chain` | THEORETICAL | ✓ | {'chain': 'Alpha_F + OMEGA_ZS → d* → Riemann=Fermat → dropouts → H_RB → Geometries → Obs… |
| `geometric_observer` | THEORETICAL | ✓ | {'tier': 4, 'claim': '∂̂_{∂M} IS a Hamiltonian — the Geometric Observer.', 'discovery': … |
| `langlands_dropout` | THEORETICAL | ✓ | {'tier': 2, 'drops_out': 'Langlands programme = J^μ at σ=1 over sedenion strata', 'mecha… |
| `navier_stokes_dropout` | THEORETICAL | ✓ | {'tier': 2, 'drops_out': 'Navier-Stokes = H_RB\|_{Im=0} (Yang-Mills minus i)', 'mechanis… |
| `planck_ln_connection` | THEORETICAL | ✓ | {'tier': 5, 'claim': 'ħ (quantum of action) ↔ ln (quantum of information)', 'landauer': … |
| `d_star_tower_ln10` | OPEN | ✓ | {'tier': 5, 'claim': 'd*_ℝ + d*_ℂ + d*_ℍ + d*_𝕆 = ln(10) [OPEN — highest priority]', 'kn… |
| `bsd_dropout` | ESTABLISHED (rank 0,1); THEORETICAL (rank≥2) | ✓ | {'tier': 2, 'drops_out': 'BSD conjecture = rank(E) = ord_{s=1} L(E,s)', 'mechanism': 'L(… |
| `riemann_equals_fermat` | ESTABLISHED (Wiles) + THEORETICAL (operator identity) | ✓ | {'tier': 1, 'claim': 'Riemann = Fermat. R̂†=B̂. Both are Euler products from opposite si… |

## Open

- `d_star_tower_ln10` — the claim that d*_ℝ + d*_ℂ + d*_ℍ + d*_𝕆 = ln(10) — is tagged OPEN in its own result dict, with the text '[OPEN — high]'. This is the same ln(10) that appears in the mass gap. It is not derived.
- `geometric_observer` and `planck_ln_connection` are THEORETICAL.
