# Engine: Pi Derivations (the Pi Derivation Toolset)

**Module:** `modules/pi_derivations/` (`maths.py`, `tools.py`, `manifest.json`)
**Class:** `PiDerivationsModule`
**Version:** 0.1 (2026-11-16)
**Confidence floor:** ESTABLISHED (status label `ESTABLISHED:CALCULATED`)
**Notebook:** [notebooks/engines/23_pi_derivations.ipynb](../notebooks/engines/23_pi_derivations.ipynb) · **Proof locale:** `engine/proof_locale/pi_derivations.json` · **Ainulindale:** `wiki/138_the_pi_derivation_toolset.md`
**Tests:** `tests/test_pi_derivations.py` (6)
Kept beside the 0_RB toolset (`modules/h_rb_hat`).

## API

`ROUTES`
: dict id → {fn, name, circle_in, tier, needs}; 26 routes.

`derive(name, **kw)`
: :param name: key of `ROUTES`. :returns: dict id, name, value, error (against `math.pi`, comparison only), circle_in, needs, tier.

`all_routes()`
: every route with default parameters.

`circle_audit()`
: routes grouped by `circle_in`.

`emergent_pi()`
: `cos_zero` with its disclosure of inputs.

`verify()`
: every route within tolerance; `u1_normalisation` returns no value.

Route functions: `cos_zero`, `oscillator_period`, `archimedes`, `gregory_leibniz`, `machin`, `madhava`, `wallis`, `viete`, `basel`, `euler_product`, `coprime_probability`, `gaussian_integral`, `gamma_half`, `stirling_ratio`, `gauss_legendre`, `ramanujan_1_over_pi`, `chudnovsky`, `bbp_digit_sum`, `grid_circle_area`, `residue_square`, `cardioid_area`, `smith_arc_length`, `jacobi_conjugate_point`, `sedenion_exp_period`, `ring_eigenvalue`, `u1_normalisation`.

## `circle_in`
`none` (series, products, exp integrals) · `orbit` (a flow that closes) · `constructed` (circle or polygon drawn first) · `dual` (U(1) or its dual, the integers) · `path` (a closed curve that is not a circle) · `library` (Γ) · `identity` (holds for any π).

## Measured (executed in notebook 23)
All 25 value routes within tolerance (errors 0 … 9.5e-4 for the coprime probability, which converges slowly). **Emergent π** `cos_zero` 8.9e-16. Orbit: `oscillator_period` 3.2e-13, `jacobi_conjugate_point` 8.0e-6 (first conjugate point of the Lagrangian at T = π). Path: `residue_square` 3.3e-9 (∮dz/z round a square), `smith_arc_length`. `sedenion_exp_period` 1.8e-14 (exp(θ·e₁₅) by the project's own Cayley–Dickson product). `chudnovsky` 60 digits exact. **`u1_normalisation`: (2/π)·π = 2 holds for any π; the route returns no value and is classed `identity`.**
Rule: the route bodies never read `math.pi` (a test greps the source).
