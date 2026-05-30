# DerivationEngine — TODO

## Diagnostics Interface

- [ ] **OBD-II** — On-Board Diagnostics II live data display
  - Standard PID readout (engine load, MAP, RPM, timing advance, fuel trim, etc.)
  - Custom PID support for SMMIP-specific channels (CKP, CMP, sedenion charge, Fermat proximity)
  - DTC fault code display with SMMIP interpretations
  - Readiness monitor status panel

- [ ] **VCDS / VAG-COM (Volkswagen)** — Ross-Tech VCDS protocol integration
  - VAG-specific adaptation channel display
  - Long-term / short-term fuel trim visualization
  - Injection timing and quantity readout
  - Controller identification (part number, coding, WSC)
  - Guided fault code interpretation against SMMIP DTC table

---

## H_hat_RB Viewer

- [ ] Interactive σ-face display — slide σ from 0 to 2, watch the theory change
- [ ] Prime spectrum visualisation — p^{−σ} coupling weights across first 1000 primes
- [ ] R̂_p / B̂_p balance display — Red/Blue operator ratio at current σ
- [ ] Noether current conservation monitor — ∂_μJ^μ live readout
- [ ] Zero-divisor proximity indicator — distance to nearest Cawagas pair

---

## Clay Millennium Derivations

- [ ] Riemann Hypothesis — formal derivation from Noether balance at σ = ½
- [ ] Yang-Mills / Mass Gap — σ = 1 face, gap measurement
- [ ] Navier-Stokes — why dropping i breaks global regularity (formal)
- [ ] P vs NP — NP oracle (second 𝕆) vs P machine (first 𝕆) at σ = ½ callosum
- [ ] BSD Conjecture — L-function projection from R̂_p at σ = 1
- [ ] Hodge Conjecture — algebraic cycles from GR face at σ = 2

---

## TDI Engine Monitor

- [ ] Live crankshaft position (H_hat_RB active zero γ_n)
- [ ] Camshaft position (dominant sedenion pair + stroke phase)
- [ ] Turbo boost (mean β of top-N zeros)
- [ ] Compression ignition event detection (SELF_EQUATION match)
- [ ] BAO convergence graph (J_ambient → OMEGA_ZS = 0.56714)
