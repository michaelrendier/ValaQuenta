# Engine: The Aizawa Attractor (rotation with a radial driver)

**Module:** `modules/aizawa_attractor/` (`maths.py`, `tools.py`, `manifest.json`)
**Class:** `AizawaAttractorModule`
**Version:** 1.0 (2026-11-24)
**Confidence floor:** ESTABLISHED
**Notebook:** [notebooks/engines/28_aizawa_attractor.ipynb](../notebooks/engines/28_aizawa_attractor.ipynb) · **Proof locale:** `engine/proof_locale/aizawa_attractor.json`
**Tests:** `Testing/test_aizawa_attractor.py` (9) · **Toolbox:** [toolbox/45_aizawa_attractor.md](toolbox/45_aizawa_attractor.md)
**Narrative:** `Ainulindale/wiki/145_aizawa_attractor_engine.md`
**External packages:** `numpy`

The Aizawa system,  dx/dt = (z-b)x - dy,  dy/dt = dx + (z-b)y,  dz/dt = c + az - z^3/3 - (x^2+y^2)(1+ez) + f z x^3  (a=.95 b=.7 c=.6 d=3.5 e=.25 f=.1),
read as a rotation with a radial driver.

## The claim, and what checks it

| statement | status | check |
|---|---|---|
| in cylindrical coordinates dr/dt = (z-b) r and dphi/dt = d, exactly | ESTABLISHED, CALCULATED residual 9e-16 | `test_cylindrical_form_is_exact` |
| r never reaches the axis (multiplicative radial law) | ESTABLISHED | `test_radius_never_reaches_the_axis` |
| with f = 0 the 3-D orbit is the 2-D (r, z) flow swept round the axis | ESTABLISHED, CALCULATED 1.7e-8 after 4000 steps | `test_axisymmetric_reduction_for_f_zero` |
| fixed points are on the axis: roots of c + az - z^3/3; eigenvalues (z*-b) +- id and a - z*^2 | ESTABLISHED | `test_fixed_points_...` (finite-difference Jacobian) |
| the orbit is chaotic: largest Lyapunov exponent +0.085 | CALCULATED | `test_orbit_is_bounded_and_chaotic` |
| ln r is bounded, so the long-time mean of z equals b (measured 0.701 vs 0.7) | ESTABLISHED, CALCULATED | `test_long_time_mean_of_z_is_b` |
| RK4 is fourth order | ESTABLISHED | `test_rk4_is_fourth_order` |

## `maths.py`

`STANDARD`, `rhs`, `rk4_step`, `orbit`, `js_layout`, `cylindrical_rates`, `axisymmetric_rhs`, `reduced_orbit`, `fixed_points`, `lyapunov_max`, `bounds`.

## Provenance and honest boundaries

- The browser page that drew the animation Cody saw (the "Holographic Aizawa Attractor" page, copies at `xml12333/HTML_CSS_JS` entry 1137 and on codetap.org) was read, not run; the equations and the slot order (x, z, y) match. Its original author is not established; no licence is shown, so the copy stays local-only. `js_layout` reproduces its buffer layout; the code is independent.
- The original paper reference for the attractor is not verified against a title page this session.
- This engine says nothing about the zeta function. The comparison is in `zeta_uns_path`.
