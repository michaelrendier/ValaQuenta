# Engine: The Zeta Pathway in Universal Native Space

**Module:** `modules/zeta_uns_path/` (`maths.py`, `tools.py`, `manifest.json`)
**Class:** `ZetaUNSPathModule`
**Version:** 1.0 (2026-11-24)
**Confidence floor:** ESTABLISHED (CALCULATED where marked)
**Notebook:** [notebooks/engines/29_zeta_uns_path.ipynb](../notebooks/engines/29_zeta_uns_path.ipynb) · **Proof locale:** `engine/proof_locale/zeta_uns_path.json`
**Tests:** `Testing/test_zeta_uns_path.py` (18; three need `RiemannHypothesisProof/data/zeros_25000_hp.tsv` and skip without it) · **Toolbox:** [toolbox/46_zeta_uns_path.md](toolbox/46_zeta_uns_path.md)
**Narrative:** `Ainulindale/wiki/146_zeta_uns_path_engine.md`
**Pairs with:** `aizawa_attractor` · **Viewer:** `RiemannHypothesisProof/visualizations/javascript/webgl_aizawa_vs_zeta_uns.html`
**External packages:** `numpy`, `scipy` (Lambert W start), `mpmath` (reference values only)

The critical-line path t -> zeta(1/2 + it) = exp(-i theta(t)) Z(t) (Hardy). A rotation at -theta'(t) with a signed radius Z(t) that passes through the axis at every zero.

## Skeleton shared with Aizawa (structural, not a theorem)

| Aizawa | zeta on the critical line | measured |
|---|---|---|
| dphi/dt = d (constant) | angle turns at -theta'(t) = -(1/2) ln(t/2pi) (slowly rising) | identity: residual 1e-10 on the sampled path |
| dr/dt = (z-b) r, so (dr/dt)/r = z - b | (d/dt) ln|Z| = Z'/Z | Z'/Z = sum over zeros of 2t/(t^2-gamma^2) + a smooth part: spread 0.573 -> 0.007 after subtracting the zero sum away from the zeros (25,000 zeros, t in [30, 300]); the remainder is a near-constant 0.75 |
| r > 0 stays > 0: the axis is forbidden | Z changes sign: the path goes through the axis at every zero | sign change at each of the first 30 zeros |
| fixed points on the axis | the zeros are on the axis of the UNS cylinder (height gamma) | by construction |

## Where the primes are

| view | what it shows | measured |
|---|---|---|
| prime spring (Euler path) at height t | partial sums of -ln(1 - p^(-1/2-it)): one step per prime, length ~ p^(-1/2), turned by -t ln p | steps equal p^(-s) to 0.02 for p > 70 |
| resonance heights | t_k = 2 pi k / ln p: where prime p's phasor is back at angle 0 | exact by construction |
| zero spectrum, sum of cos(gamma x) over the zeros | spikes at x = ln p^k (explicit formula, dual side) | with 25,000 zeros: every prime to 47 and the prime powers 4, 8, 9, 25 spike 28x to 750x above the off-grid background; off-grid control median 7e-5 against spike heights 2e-3 to 7e-2 |

## Numbers recorded while building

- Riemann-Siegel with one correction term against mpmath: error 3e-3 at t = 100, 1.5e-4 at t = 500, 1e-4 at t = 2000, 5e-6 at t = 1e4; up to 1.0e-2 near t = 25 (the third zero).
- Sampling by equal steps of theta puts every point on 2 x 16 fixed angles of the flat point: the first browser render showed 32 rigid spokes, a sampling artefact. `sample_by_phase(..., jitter=True)` (golden-ratio offset, order and mean step kept) removes it; tested.
- Mean value of zeta over t is 1.0000 at 100, 1,000, 5,000 and 25,000 zeros; the share of the path with Re zeta < 0 is 17.4%, 20.7%, 22.6%, 24.0% (t-weighted): the sparse side seen from the pole, centred on the negative real axis at every count (`re_negative_share`).
- zeta = S + exp(-2i theta) conj(S) + R (the prime spring plus its mirror; `cardioid_parts`): residual within (t/2pi)^(-1/4) (measured ratio 0.92); no cusp: |Z'| >= 0.62 at the first 1,500 zeros.
- |zeta| = 1 (the equator of the value sphere) is crossed 1.34 times per zero spacing over the first 25,000.

## Honest boundaries

- The Euler product does not converge on the critical line; the prime spring is the partial-sum picture, not a value of zeta.
- `Z_rs` has one correction term; use `Z_exact` (mpmath) for t < 50 when digits matter.
- The analogy with Aizawa is structural. Nothing here is evidence about the Riemann Hypothesis; RH is the statement that every zero lies on the line this path samples.
- Open (asked, not done): the phase-offset reading of the diagonal prime-generating quadratics in UNS space, and whether an orthogonal wave (a Dirichlet L-function character) belongs beside zeta.
