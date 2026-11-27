# Engine: The Bell Curve (statistics, probability, statistical mechanics)

**Module:** `modules/bell_curve/` (`maths.py`, `tools.py`, `manifest.json`)
**Class:** `BellCurveModule`
**Version:** 1.1 (2026-11-22; 1.1: `ols` handles n = 2)
**Confidence floor:** ESTABLISHED
**Notebook:** [notebooks/engines/27_bell_curve.ipynb](../notebooks/engines/27_bell_curve.ipynb) · **Proof locale:** `engine/proof_locale/bell_curve.json`
**Tests:** `Testing/test_bell_curve.py` (46, cross-checked against scipy 1.18) · **Toolbox:** [toolbox/44_bell_curve.md](toolbox/44_bell_curve.md)
**Narrative:** `Ainulindale/wiki/144_bell_curve_statistics_engine.md`
**External packages:** none to run (stdlib `math`, `random`); `scipy`, `numpy`, `scikit-learn` for the tests only

One implementation of statistics for every place a probability, a spread or a gradient appears.

## `maths.py`

| section | functions / classes |
|---|---|
| 1 Moments | `Moments` (`add`, `extend`, `merge`, `mean`, `var`, `std`, `sem`, `skew`, `kurt_excess`, `summary`), `mean`, `variance`, `stdev` |
| 2 Descriptive | `quantile` (type 7), `median`, `iqr`, `mad`, `zscores`, `covariance`, `histogram`, `kde` |
| 3 Special functions | `gammainc_p`, `betainc`, `log_comb` |
| 4 Distributions | normal `norm_pdf/cdf/sf/ppf`; `t_pdf/cdf/ppf`; `chi2_pdf/cdf/sf/ppf`; `f_cdf/ppf`; `gamma_cdf`; `beta_pdf/cdf/ppf`; `expon_pdf/cdf`; `uniform_cdf`; `binom_pmf/cdf`; `poisson_pmf/cdf` |
| 5 Sigma | `p_to_sigma`, `sigma_to_p`, `sigma_to_dpmo`, `dpmo_to_sigma`, `cp_cpk` |
| 6 Inference | `t_test_one`, `t_test_welch`, `t_test_paired`, `z_test_prop`, `wilson_ci`, `chi2_gof`, `chi2_independence`, `mann_whitney_u`, `ks_two_sample`, `jarque_bera`, `pearson`, `spearman`, `ols` |
| 7 Effect, agreement, classification | `cohens_d`, `hedges_g`, `cohens_kappa`, `confusion_metrics`, `roc_auc` |
| 8 Multiple testing | `bonferroni`, `holm`, `benjamini_hochberg` |
| 9 Resampling | `bootstrap_ci`, `permutation_test` (both seeded) |
| 10 Information | `entropy`, `cross_entropy`, `kl_divergence`, `js_divergence`, `mutual_information`, `perplexity` |
| 11 Bayes | `bayes_update`, `beta_binomial` |
| 12 Statistical mechanics | `boltzmann_probs`, `canonical` (Z, U, S, F, Cv), `softmax`, `fermi_dirac`, `bose_einstein`, `maxwell_boltzmann_speed_pdf`, `planck_spectral_radiance`, `two_level`, `harmonic_oscillator`, `ising_1d`, `ising_1d_bruteforce` |
| 13 Circular | `circ_mean`, `circ_R`, `circ_var`, `circ_std`, `bessel_i0`, `von_mises_pdf`, `rayleigh_test` |

Constants: `K_B`, `H_PLANCK`, `C_LIGHT` (exact SI values). `verify_known_values()` runs eight tabulated spot checks.

## `tools.py`

`BellCurveModule` with 15 formulary entries (`moments`, `normal`, `sigma_levels`, `welch_t`, `proportion`, `chi_square`, `mann_whitney`, `kappa`, `multiple_testing`, `bootstrap`, `information`, `bayes`, `canonical_ensemble`, `ising_1d`, `circular`) and shell commands `bc_*`.

## Confidence

| claim | tier | check |
|---|---|---|
| every distribution matches scipy to 1e-8 … 1e-12 | ESTABLISHED | `Testing/test_bell_curve.py` |
| Moments.merge equals the one-pass accumulator | ESTABLISHED | merge test |
| canonical ensemble: S = Gibbs entropy, F = U − TS, Cv = dU/dT | ESTABLISHED | identity tests |
| softmax is the canonical ensemble | ESTABLISHED | equals `scipy.special.softmax` |
| Ising 1-D transfer matrix equals brute force (N = 8, 10) | ESTABLISHED | exact |

## Findings recorded while building

- `p_to_sigma` first computed `norm_ppf(1 − p/2)`; at 6 sigma it returned 5.99999999 (cancellation in the tail). It now uses `−norm_ppf(p/2)` with the small tail probability directly. Found by the round-trip test.

## Not in v1.0

Multivariate tests, ARMA and time series, MCMC, generalised linear models, exact small-sample tests (Fisher, Wilcoxon exact).

---

## The n-ball (version 1.2, 2026-11-27)

Gamma appears in this engine (see the code for where). It is also the bookkeeping of a hypersphere: the Gaussian integral of e^(−|x|²) over n dimensions is (√π)^n = (S/2)·Γ(n/2), so the unit ball has volume V(n) = π^(n/2)/Γ(n/2 + 1) and the unit sphere area S(n) = 2π^(n/2)/Γ(n/2) = n·V(n) for every real n. At n = 2 these are π and 2π, the circle. V peaks at n = 5.2569464 and S at n = 7.2569464 (`bell_curve.nball_peak`, which is the `n* ≈ 5.257` of the Ainulindale texts; its identification with the BAO freeze point is THEORETICAL, not computed). Machinery: `ValaQuenta/modules/bell_curve/maths.py` (`nball_volume`, `nsphere_area`, `nball_peak`); pictures: `gallery/hypergon_constructibility/canvas2d_nball.html` (the curves, the poles of Γ at 0, −1, −2, …) and `canvas2d_frame3d.html` (the curve in the frame n, V, S).

The poles of Γ at the non-positive integers are where ∫ t^(z−1) e^(−t) dt stops converging; the function is continued past them by Γ(z) = Γ(z+1)/z, and the residue at −k is (−1)^k/k!. They are part of the function and are drawn on the n-ball page.
