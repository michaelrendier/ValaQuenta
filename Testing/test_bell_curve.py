"""Tests for the Bell Curve engine, ValaQuenta.modules.bell_curve (v1.0, 2026-11-22).
Every distribution and test is cross-checked against scipy 1.18 where scipy has it; closed forms are checked exactly."""
import math, os, random, sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ValaQuenta.modules.bell_curve import maths as M
sp = pytest.importorskip('scipy.stats')
import numpy as np
from scipy import special

R = random.Random(7)
X = [R.gauss(3, 2) for _ in range(400)]
Y = [R.gauss(3.4, 2.5) for _ in range(300)]
SK = [R.expovariate(1.0) for _ in range(500)]


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(b))


def test_known_values():
    assert all(M.verify_known_values().values())


def test_moments_match_numpy_scipy():
    m = M.Moments().extend(SK)
    assert close(m.mean, np.mean(SK)) and close(m.var, np.var(SK, ddof=1))
    assert close(m.skew, sp.skew(SK)) and close(m.kurt_excess, sp.kurtosis(SK))


def test_moments_merge_equals_one_pass():
    a, b = M.Moments().extend(SK[:170]), M.Moments().extend(SK[170:])
    o = M.Moments().extend(SK)
    g = a.merge(b)
    for f in ('n', 'mean', 'M2', 'M3', 'M4'):
        assert close(getattr(g, f), getattr(o, f), 1e-9)


@pytest.mark.parametrize('x', [-8.0, -3.1, -0.4, 0.0, 1.96, 5.5])
def test_normal(x):
    assert close(M.norm_cdf(x), sp.norm.cdf(x), 1e-12) and close(M.norm_pdf(x), sp.norm.pdf(x), 1e-12)
    assert close(M.norm_sf(x), sp.norm.sf(x), 1e-12)


@pytest.mark.parametrize('p', [1e-12, 1e-6, 0.001, 0.05, 0.5, 0.9, 0.999999])
def test_norm_ppf(p):
    assert close(M.norm_ppf(p), sp.norm.ppf(p), 1e-10)


@pytest.mark.parametrize('df', [1, 2.5, 5, 30, 200])
def test_student_t(df):
    for x in (-4, -1, 0.3, 2.2):
        assert close(M.t_cdf(x, df), sp.t.cdf(x, df), 1e-10) and close(M.t_pdf(x, df), sp.t.pdf(x, df), 1e-10)
    assert close(M.t_ppf(0.975, df), sp.t.ppf(0.975, df), 1e-8)


@pytest.mark.parametrize('df', [1, 2, 7, 40])
def test_chi2(df):
    for x in (0.1, 1.0, 5.0, 30.0):
        assert close(M.chi2_cdf(x, df), sp.chi2.cdf(x, df), 1e-10) and close(M.chi2_pdf(x, df), sp.chi2.pdf(x, df), 1e-10)
    assert close(M.chi2_ppf(0.95, df), sp.chi2.ppf(0.95, df), 1e-8)


def test_f_beta_gamma_expon():
    assert close(M.f_cdf(2.3, 4, 17), sp.f.cdf(2.3, 4, 17), 1e-10) and close(M.f_ppf(0.95, 4, 17), sp.f.ppf(0.95, 4, 17), 1e-8)
    assert close(M.beta_cdf(0.3, 2.5, 4), sp.beta.cdf(0.3, 2.5, 4), 1e-10)
    assert close(M.beta_ppf(0.9, 2.5, 4), sp.beta.ppf(0.9, 2.5, 4), 1e-8)
    assert close(M.gamma_cdf(3.0, 2.5, 1.5), sp.gamma.cdf(3.0, 2.5, scale=1.5), 1e-10)
    assert close(M.expon_cdf(0.7, 2.0), sp.expon.cdf(0.7, scale=0.5), 1e-12)


def test_discrete():
    for k in (0, 3, 10, 20):
        assert close(M.binom_pmf(k, 20, 0.3), sp.binom.pmf(k, 20, 0.3), 1e-10) and close(M.binom_cdf(k, 20, 0.3), sp.binom.cdf(k, 20, 0.3), 1e-10)
        assert close(M.poisson_pmf(k, 4.2), sp.poisson.pmf(k, 4.2), 1e-10) and close(M.poisson_cdf(k, 4.2), sp.poisson.cdf(k, 4.2), 1e-10)


def test_quantile_matches_numpy():
    for q in (0.05, 0.25, 0.5, 0.9):
        assert close(M.quantile(X, q), np.quantile(X, q), 1e-12)
    assert close(M.mad(X), sp.median_abs_deviation(X, scale='normal'), 1e-12)


def test_sigma_conversions_round_trip():
    for s in (1, 2, 3, 5, 6):
        assert close(M.p_to_sigma(M.sigma_to_p(s)), s, 1e-9)
        assert close(M.dpmo_to_sigma(M.sigma_to_dpmo(s)), s, 1e-8)
    assert abs(M.sigma_to_p(5, False) - 2.866515718791939e-07) < 1e-15


def test_t_tests_match_scipy():
    r = M.t_test_welch(X, Y); s = sp.ttest_ind(X, Y, equal_var=False)
    assert close(r['t'], s.statistic, 1e-9) and close(r['p'], s.pvalue, 1e-8) and close(r['df'], s.df, 1e-9)
    r = M.t_test_one(X, 2.8); s = sp.ttest_1samp(X, 2.8)
    assert close(r['t'], s.statistic, 1e-9) and close(r['p'], s.pvalue, 1e-8)
    r = M.t_test_paired(X[:300], Y); s = sp.ttest_rel(X[:300], Y)
    assert close(r['p'], s.pvalue, 1e-8)


def test_proportion_wilson():
    lo, hi = M.wilson_ci(7, 40); w = sp.binomtest(7, 40).proportion_ci(method='wilson')
    assert close(lo, w.low, 1e-9) and close(hi, w.high, 1e-9)


def test_chi2_tests():
    obs, exp = [18, 22, 31, 29], [25, 25, 25, 25]
    s = sp.chisquare(obs, exp); r = M.chi2_gof(obs, exp)
    assert close(r['chi2'], s.statistic) and close(r['p'], s.pvalue, 1e-9)
    t = [[20, 30, 10], [15, 25, 40]]
    s = sp.chi2_contingency(t, correction=False); r = M.chi2_independence(t)
    assert close(r['chi2'], s.statistic) and close(r['p'], s.pvalue, 1e-9)


def test_mann_whitney_and_auc():
    r = M.mann_whitney_u(X, Y); s = sp.mannwhitneyu(X, Y, method='asymptotic', use_continuity=True)
    assert close(r['U'], s.statistic, 1e-9) and close(r['p'], s.pvalue, 1e-7)
    assert abs(M.roc_auc([2, 3, 4], [1, 2, 2.5]) - sp.mannwhitneyu([2, 3, 4], [1, 2, 2.5]).statistic / 9) < 1e-12


def test_ks_and_jarque_bera():
    r = M.ks_two_sample(X, Y); s = sp.ks_2samp(X, Y, method='asymp')
    assert close(r['D'], s.statistic, 1e-12) and abs(r['p'] - s.pvalue) < 5e-3
    j = M.jarque_bera(SK); s = sp.jarque_bera(SK)
    assert close(j['JB'], s.statistic, 1e-9) and close(j['p'], s.pvalue, 1e-8)


def test_correlation_and_ols():
    xs, ys = X[:300], [x * 0.5 + e for x, e in zip(X[:300], Y)]
    p = M.pearson(xs, ys); s = sp.pearsonr(xs, ys)
    assert close(p['r'], s.statistic) and close(p['p'], s.pvalue, 1e-7)
    q = M.spearman(xs, ys); t = sp.spearmanr(xs, ys)
    assert close(q['r'], t.statistic, 1e-9)
    o = M.ols(xs, ys); l = sp.linregress(xs, ys)
    assert close(o['slope'], l.slope) and close(o['se_slope'], l.stderr, 1e-9) and close(o['r2'], l.rvalue ** 2, 1e-9)


def test_effect_size_kappa_confusion():
    a = [0, 1, 1, 0, 1, 0, 0, 1, 1, 1]; b = [0, 1, 0, 0, 1, 0, 1, 1, 1, 0]
    k = M.cohens_kappa(a, b)
    from sklearn.metrics import cohen_kappa_score, f1_score, matthews_corrcoef
    assert close(k['kappa'], cohen_kappa_score(a, b), 1e-12)
    tp = sum(1 for x, y in zip(a, b) if x == y == 1); fp = sum(1 for x, y in zip(a, b) if x == 0 and y == 1)
    fn = sum(1 for x, y in zip(a, b) if x == 1 and y == 0); tn = sum(1 for x, y in zip(a, b) if x == y == 0)
    c = M.confusion_metrics(tp, fp, fn, tn)
    assert close(c['f1'], f1_score(a, b), 1e-12) and close(c['mcc'], matthews_corrcoef(a, b), 1e-12)


def test_multiple_testing_matches_scipy():
    ps = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.074, 0.205, 0.212, 0.216]
    assert all(close(a, b, 1e-12) for a, b in zip(M.benjamini_hochberg(ps), sp.false_discovery_control(ps)))
    assert all(a >= b for a, b in zip(M.holm(ps), ps)) and all(close(a, min(1, p * 10)) for a, p in zip(M.bonferroni(ps), ps))


def test_resampling_is_seeded_and_sane():
    a = M.bootstrap_ci(X); b = M.bootstrap_ci(X)
    assert a == b and a['ci'][0] < M.mean(X) < a['ci'][1]
    assert M.permutation_test(X, Y)['p'] == M.permutation_test(X, Y)['p']
    assert M.permutation_test(X[:50], [v + 5 for v in X[:50]])['p'] < 0.01


def test_information_measures():
    p, q = [0.5, 0.25, 0.25], [0.4, 0.4, 0.2]
    assert close(M.entropy(p), sp.entropy(p, base=2)) and close(M.kl_divergence(p, q), sp.entropy(p, q, base=2))
    from scipy.spatial.distance import jensenshannon
    assert close(M.js_divergence(p, q), jensenshannon(p, q, base=2) ** 2, 1e-12)
    assert close(M.perplexity([0.25] * 4), 4.0)
    assert close(M.mutual_information([[1, 0], [0, 1]]), 1.0)


def test_bayes():
    post = M.bayes_update([0.5, 0.5], [0.8, 0.2]); assert close(post[0], 0.8)
    r = M.beta_binomial(7, 20); b = sp.beta(1 + 7, 1 + 13)
    assert close(r['credible'][0], b.ppf(0.025), 1e-8) and close(r['mean'], b.mean())


def test_canonical_ensemble_identities():
    E = [0.0, 1.0, 2.5, 4.0]; T = 0.8
    r = M.canonical(E, T, 1.0)
    assert close(sum(r['p']), 1.0, 1e-14)
    assert close(r['S'], -sum(p * math.log(p) for p in r['p']), 1e-12)       # Gibbs entropy
    assert close(r['F'], r['U'] - T * r['S'], 1e-12)
    h = 1e-5; Up = M.canonical(E, T + h, 1.0)['U']; Um = M.canonical(E, T - h, 1.0)['U']
    assert close(r['Cv'], (Up - Um) / (2 * h), 1e-6)                          # Cv = dU/dT
    assert close(M.canonical([0, 1], 1e-3, 1.0)['U'], 0.0, 1e-9)              # T -> 0: ground state


def test_softmax_is_canonical_and_temperature_dilutes():
    x = [1.0, 2.0, 3.0]
    assert all(close(a, b, 1e-12) for a, b in zip(M.softmax(x), special.softmax(x)))
    assert M.softmax(x, 0.1)[2] > 0.99 and abs(M.softmax(x, 1e4)[0] - 1 / 3) < 1e-3


def test_quantum_statistics_and_ising():
    assert abs(M.fermi_dirac(1.0, 1.0, 300.0)) - 0.5 < 1e-12
    assert close(M.bose_einstein(2.0, 0.0, 1.0, 1.0), 1 / math.expm1(2.0))
    assert close(M.ising_1d(10, 0.8, 0.2, 0.9)['Z'], M.ising_1d_bruteforce(10, 0.8, 0.2, 0.9), 1e-9)
    # Maxwell-Boltzmann pdf integrates to 1
    m_, T = 4.65e-26, 300.0; dv = 2.0
    tot = sum(M.maxwell_boltzmann_speed_pdf(v * dv, m_, T) * dv for v in range(1, 1500))
    assert abs(tot - 1.0) < 1e-3
    h = 6.62607015e-34; kB = 1.380649e-23   # Planck at 5800 K peaks near Wien's nu = 5.879e10 * T
    nu = [1e12 * i for i in range(1, 1000)]
    peak = max(nu, key=lambda n: M.planck_spectral_radiance(n, 5800.0))
    assert abs(peak - 5.879e10 * 5800.0) / peak < 0.01


def test_circular_statistics():
    ang = [0.1, 0.2, 0.15, 6.2, 0.05]
    assert abs(M.circ_mean(ang)) < 0.2 and M.circ_R(ang) > 0.99
    assert M.circ_R([0, math.pi]) < 1e-12
    assert close(M.von_mises_pdf(0.0, 0.0, 0.0), 1 / (2 * math.pi)) and close(M.bessel_i0(2.0), special.i0(2.0), 1e-12)
    uni = [2 * math.pi * i / 50 for i in range(50)]
    assert M.rayleigh_test(uni)['p'] > 0.9 and M.rayleigh_test(ang * 6)['p'] < 0.01


def test_registered_module_contract():
    from ValaQuenta.modules.bell_curve import BellCurveModule
    m = BellCurveModule()
    assert m.name == 'bell_curve' and m.version == '1.1' and len(m.formulary()) >= 14
    for e in m.formulary():
        assert e.confidence == 'ESTABLISHED' and e.process
    out = m.run('sigma_levels', {'sigma': 3.0})['result']
    assert close(out['p_two_sided'], 0.0026997960632602, 1e-9)
    assert 'bc_check' in m.shell_commands()


def test_ols_two_points_is_exact_not_a_crash():
    o = M.ols([0.0, 1.0], [1.0, 3.0])
    assert o['slope'] == 2.0 and o['intercept'] == 1.0 and o['n'] == 2 and math.isnan(o['se_slope'])
