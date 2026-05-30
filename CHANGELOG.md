# Changelog — DerivationEngine

Format: `[vX.Y.Z] YYYY-MM-DD — Description`

All changes follow the TDI versioning model. DerivationEngine versions track the
formal derivation state of the SMMIP framework. Code releases (PtolemyHolcus) are
canonical; DerivationEngine records the mathematics that code implements.

---

## [v1.0.0] 2026-05-30 — Repository Established

**Initial formal record of the DerivationEngine.**

### Added
- `README.md` — H_hat_RB Hamiltonian definition, σ-face table, Clay Millennium
  problem projections, TDI crankshaft role, OBD-II / VCDS diagnostic interface
  scope, related repository index
- `TODO.md` — H_hat_RB viewer, Clay Millennium derivation modules (6 open problems),
  TDI engine monitor, OBD-II PID map, VCDS / VAG-COM integration roadmap

### Architecture recorded
The central object is H_hat_RB — the RedBlue Hamiltonian:

```
H_hat_RB = Σ_p  p^{−σ}  ·  [ R̂_p ⊗ ∂̂_∂M  +  ∂̂_∂M† ⊗ B̂_p ]
```

All six open Clay Millennium problems project from this operator at different σ values.
Poincaré (solved 2003, Perelman) validates the geometry.

### Verified at v1.0
- Compression ignition event confirmed 2026-05-27 in PtolemyHolcus v3.0.0
- BAO convergence: OMEGA_ZS = 0.56714 (Lambert W fixed point)
- SELF_EQUATION fixed point: constructive Gödel II result
- Android TDI Seeder: five corpora acquired, phone-side compression ignition confirmed

### Related releases
- PtolemyHolcus v3.0.0 — Tuning the TDI (three systems timed)
- PtolemyHolcus apk-v1.0 — Android TDI Seeder released
- SemanticWordEngine — Hyperwebster layer documented

---

## Versioning

| Target | Version | Description |
|---|---|---|
| v1.x | Formal record | README, TODO, wiki — no executable code |
| v2.x | H_hat_RB viewer | Interactive σ-face display, prime spectrum |
| v3.x | Clay derivations | Formal derivation modules for all six problems |
| v4.x | OBD-II interface | Live TDI diagnostic display |
