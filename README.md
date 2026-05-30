# DerivationEngine

**Heavy mathematics derivation viewer for the SMMIP framework.**

*Formal derivation engine for H_hat_RB, Clay Millennium problems, and the TDI architecture.*

---

> *The crankshaft provides the compression cycle. Without the crankshaft, the camshaft has nothing to resist against and the ECU has nothing to inject into. The DerivationEngine is the formal record of the crankshaft's geometry.*

---

## What This Is

The DerivationEngine is the viewer and formal record for the mathematical derivations underlying the [PtolemyHolcus](https://github.com/michaelrendier/PtolemyHolcus) TDI engine. Where PtolemyHolcus is running code, the DerivationEngine is the mathematics that the code implements.

The central object is **H_hat_RB** — the RedBlue Hamiltonian:

```
H_hat_RB = Σ_p  p^{−σ}  ·  [ R̂_p ⊗ ∂̂_∂M  +  ∂̂_∂M† ⊗ B̂_p ]
```

All six open Clay Millennium problems project from this single operator at different values of σ.

---

## The H_hat_RB Hamiltonian

| Component | Formal object | Role |
|---|---|---|
| `p` | Primes | Irreducible distinctions — inductive base cases |
| `σ` | Re(s) | Coupling exponent — selects the physical theory |
| `R̂_p` | Berry-Keating xp | Red operator — what IS |
| `B̂_p` | Weierstrass ½p²+℘(x) | Blue operator — what CANNOT BE |
| `G_p(σ)` | p^{−σ} | Geometric coupling — Euler/Dirichlet coefficient |

**Foundation:** The existence of a distinction. H_hat_RB is not defined on the boundary. It IS the boundary.

**Self-adjoint structure:** R̂_p† = B̂_p. The functional equation ξ(s) = ξ(1−s) as operator identity. Truth preserved across representations.

**σ-face table:**

| σ | Physical theory |
|---|---|
| σ = 2 | General Relativity |
| σ = 1 | Yang-Mills / Standard Model |
| σ = ½ | Quantum Mechanics / Riemann zeros |
| σ = 1, Im = 0 | Navier-Stokes (lacks i — this is why NS always breaks) |
| σ < ½ | Fermat forbidden zone |

---

## Clay Millennium Problems

All six open Clay problems project from H_hat_RB. Poincaré (solved 2003, Perelman) validates the geometry.

| Problem | σ value | H_hat_RB projection |
|---|---|---|
| Riemann Hypothesis | σ = ½ | Non-trivial zeros lie on Re(s) = ½ by Noether conservation |
| Yang-Mills / Mass Gap | σ = 1 | Mass gap = distance from Yang-Mills face to σ = ½ boundary |
| Navier-Stokes | σ = 1, Im = 0 | NS breaks because it drops i — loses the σ = ½ boundary |
| P vs NP | σ varies | NP oracle (second 𝕆, mind) vs P machine (first 𝕆, hands) at σ = ½ callosum |
| BSD Conjecture | σ = 1 | L-function of elliptic curve projects from R̂_p at σ = 1 |
| Hodge Conjecture | σ = 2 | Algebraic cycles project from GR face at σ = 2 |

The derivation modules live in `Ainulindale/ValaQuenta/modules/`.

---

## The TDI Crankshaft Role

In the TDI architecture, H_hat_RB is the **crankshaft**:

- The crankshaft converts linear piston motion into rotational output
- H_hat_RB converts prime-indexed distinctions into conserved current flow
- Without the crankshaft, the pistons (Sedenion) move but produce no torque
- Without the crankshaft, the ECU (Monad) has no compression cycle to inject into

The zero-divisor events in the Sedenion (TDC moments) are the piston reaching top dead centre. H_hat_RB at σ = ½ is the compression ratio that makes self-ignition possible.

---

## OBDII and VCDS

The DerivationEngine will expose an OBD-II compatible diagnostic interface:
- Standard PID readout mapped to SMMIP channels
- VCDS / VAG-COM (Volkswagen) protocol integration
- Custom PIDs for SMMIP-specific measurements

See [TODO.md](TODO.md) for the implementation roadmap.

---

## Related Repositories

| Repository | Role |
|---|---|
| [PtolemyHolcus](https://github.com/michaelrendier/PtolemyHolcus) | Engine implementation — the code this formalises |
| [Ainulindalë](https://github.com/michaelrendier/Ainulindale) | Full conjecture — Third Age document |
| [SemanticWordEngine](https://github.com/michaelrendier/SemanticWordEngine) | Hyperwebster address layer |
| [UniversalSynth](https://github.com/michaelrendier/UniversalSynth) | Sonification of the derivation output |
