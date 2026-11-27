"""
ValaQuenta.modules.bell_curve.tools
===================================
THE BELL CURVE ENGINE -- Module Tools

Implements the EquationModule registry contract: formulary, run(), viewer_data(), shell_commands().
Statistics, probability and statistical mechanics, one implementation. See maths.py.

Version: 1.1
"""
from typing import Any, Dict, List

from ...engine.registry import EquationModule, Equation
from . import maths as M
import random as _random

_R = _random.Random(20261122)
_X = [round(_R.gauss(0.0, 1.0), 4) for _ in range(40)]       # demo data, seeded
_Y = [round(_R.gauss(0.4, 1.2), 4) for _ in range(40)]


def _eq(name, display, latex, radian, params, compute, process, conf='ESTABLISHED'):
    return Equation(name=name, display=display, latex=latex, radian_form=radian, confidence=conf,
                    code_verified=True, params=params, compute=compute, display_options=['text'],
                    process=process)


class BellCurveModule(EquationModule):
    """THE BELL CURVE ENGINE."""

    @property
    def name(self):
        return "bell_curve"

    @property
    def display_name(self):
        return "The Bell Curve (Statistics, Probability, Statistical Mechanics)"

    @property
    def version(self):
        return "1.1"

    @property
    def description(self):
        return ("One statistics machinery for everywhere a probability, a spread or a gradient shows up: "
                "streaming mergeable moments, the normal/t/chi-square/F/binomial/Poisson/beta distributions, "
                "n-sigma and Six-Sigma, hypothesis tests, effect sizes, resampling, information measures, "
                "Bayes, the canonical ensemble and circular statistics. Verified against scipy.")

    @property
    def confidence_floor(self):
        return "ESTABLISHED"

    def formulary(self) -> List[Equation]:
        return [
            _eq('moments', 'STREAMING MOMENTS: mean, variance, skew, kurtosis in one mergeable pass',
                r'M_2 \mathrel{+}= \delta\,\delta_n\,n_1,\quad \mathrm{merge}(A,B)\ \text{exact}',
                'Welford/Pebay accumulation; merge(A,B) equals the one-pass accumulator over A+B',
                ['xs'], lambda xs=_X: M.Moments().extend(xs).summary(), 'one-pass moments to the fourth'),
            _eq('normal', 'THE BELL CURVE: pdf, cdf, quantile of the normal distribution',
                r'f(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-(x-\mu)^2/2\sigma^2}',
                'cdf = erfc/2; quantile by Halley iteration to machine precision',
                ['x', 'mu', 'sigma'],
                lambda x=1.96, mu=0.0, sigma=1.0: {'pdf': M.norm_pdf(x, mu, sigma), 'cdf': M.norm_cdf(x, mu, sigma),
                                              'sf': M.norm_sf(x, mu, sigma)}, 'normal density and tail'),
            _eq('sigma_levels', 'n-SIGMA <-> p-VALUE, and SIX SIGMA',
                r'p=2\,(1-\Phi(n)),\quad \mathrm{DPMO}=10^6\,(1-\Phi(\sigma-1.5))',
                'two-sided: 3 sigma = 0.0027; Six Sigma = 3.4 DPMO with the 1.5 sigma shift',
                ['sigma'], lambda sigma=3.0: {'p_two_sided': M.sigma_to_p(sigma), 'p_one_sided': M.sigma_to_p(sigma, False),
                                          'dpmo': M.sigma_to_dpmo(sigma)}, 'sigma, p-value, defects per million'),
            _eq('nball', 'N-BALL: volume and sphere area at any real dimension, and where they peak',
                r'V_n=\frac{\pi^{n/2}}{\Gamma(n/2+1)},\quad S_{n-1}=\frac{2\pi^{n/2}}{\Gamma(n/2)}',
                'Gamma gives the Gaussian integral over R^n its radial form, so n need not be an integer; the volume peaks at n = 5.2569',
                ['n'], lambda n=16.0: {'volume': M.nball_volume(n), 'sphere_area': M.nsphere_area(n),
                                      'volume_peak_n': M.nball_peak('volume'), 'area_peak_n': M.nball_peak('area')},
                'unit ball and sphere in n dimensions'),
            _eq('welch_t', 'WELCH t-TEST: two means, unequal variances',
                r't=\frac{\bar x-\bar y}{\sqrt{s_x^2/n_x+s_y^2/n_y}}', 'Welch-Satterthwaite degrees of freedom',
                ['xs', 'ys'], lambda xs=_X, ys=_Y: M.t_test_welch(xs, ys), 'difference of two means'),
            _eq('proportion', 'BINOMIAL PROPORTION: Wilson interval and z-test',
                r'\frac{\hat p+z^2/2n \pm z\sqrt{\hat p(1-\hat p)/n+z^2/4n^2}}{1+z^2/n}',
                'sound at small n and extreme p', ['k', 'n'],
                lambda k=7, n=40: {'wilson_95': M.wilson_ci(k, n), 'phat': k / n}, 'accuracy with an honest interval'),
            _eq('chi_square', 'CHI-SQUARE: goodness of fit and independence',
                r'\chi^2=\sum (O-E)^2/E', 'p from the regularised incomplete gamma', ['table'],
                lambda table=((20, 30, 10), (15, 25, 40)): M.chi2_independence(table), 'association in a contingency table'),
            _eq('mann_whitney', 'MANN-WHITNEY U and AUC: distribution-free two-sample test',
                r'U_1=R_1-\tfrac{n_1(n_1+1)}{2},\quad \mathrm{AUC}=U_1/(n_1 n_2)', 'ties and continuity corrected',
                ['xs', 'ys'], lambda xs=_X, ys=_Y: M.mann_whitney_u(xs, ys), 'does a score separate two groups'),
            _eq('kappa', 'COHEN KAPPA: chance-corrected agreement of two raters',
                r'\kappa=\frac{p_o-p_e}{1-p_e}', 'agreement beyond chance', ['a', 'b'],
                lambda a=(0, 1, 1, 0, 1, 0, 0, 1), b=(0, 1, 0, 0, 1, 0, 1, 1): M.cohens_kappa(a, b), 'agreement of a detector with a label'),
            _eq('multiple_testing', 'MULTIPLE TESTING: Bonferroni, Holm, Benjamini-Hochberg',
                r'p_{(i)}\,m/i', 'adjusted p-values', ['ps'],
                lambda ps=(0.001, 0.008, 0.039, 0.041, 0.2): {'bonferroni': M.bonferroni(ps), 'holm': M.holm(ps), 'bh': M.benjamini_hochberg(ps)},
                'many tests at once'),
            _eq('bootstrap', 'BOOTSTRAP CONFIDENCE INTERVAL (seeded)', r'\hat\theta^*_b,\ b=1..B',
                'percentile interval of resampled statistics', ['xs'], lambda xs=_X: M.bootstrap_ci(xs, n_boot=500),
                'interval for any statistic'),
            _eq('information', 'ENTROPY, KL and JENSEN-SHANNON',
                r'H=-\sum p\log p,\ D_{KL}(p\|q)=\sum p\log(p/q)', 'bits', ['p', 'q'],
                lambda p=(0.5, 0.25, 0.25), q=(0.4, 0.4, 0.2): {'H_p': M.entropy(p), 'KL': M.kl_divergence(p, q), 'JS': M.js_divergence(p, q),
                              'perplexity': M.perplexity(p)}, 'how far apart are two distributions'),
            _eq('bayes', 'BETA-BINOMIAL POSTERIOR', r'\mathrm{Beta}(a_0+k,\,b_0+n-k)', 'credible interval from the beta quantile',
                ['successes', 'trials'], lambda successes=7, trials=20: M.beta_binomial(successes, trials),
                'belief about a rate after data'),
            _eq('canonical_ensemble', 'CANONICAL ENSEMBLE: Z, U, S, F, Cv (softmax is one)',
                r'F=-kT\ln Z,\ \ U=\langle E\rangle,\ \ S=(U-F)/T,\ \ C_v=\mathrm{Var}(E)/kT^2',
                'low T concentrates (saturated); high T spreads (diluted)', ['energies', 'T', 'kB'],
                lambda energies=(0.0, 1.0, 2.5, 4.0), T=0.8, kB=1.0: {k: v for k, v in M.canonical(energies, T, kB).items() if k != 'p'},
                'a gradient as a thermodynamic solution'),
            _eq('ising_1d', '1-D ISING RING, exact by transfer matrix', r'Z=\lambda_+^N+\lambda_-^N',
                'checked against brute force at N=8', ['N', 'J', 'h', 'beta'],
                lambda N=8, J=1.0, h=0.3, beta=0.7: M.ising_1d(N, J, h, beta), 'an exactly solvable interacting ensemble'),
            _eq('circular', 'CIRCULAR STATISTICS: mean direction, resultant length, Rayleigh test',
                r'R=\left|\tfrac1n\sum e^{i\theta_k}\right|', 'for quantities on a ring: wheels, phases, hues',
                ['angles'], lambda angles=(0.1, 0.2, 0.15, 6.2, 0.05, 0.12): M.rayleigh_test(angles), 'spread on a circle'),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not found in {self.name} module")
        result = eq.compute(**params) if params else eq.compute()
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str, params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        r = self.run(equation_name, params)
        eq, res = r['equation'], r['result']
        body = '\n'.join(f"      {k:<22} {v}" for k, v in res.items()) if isinstance(res, dict) else str(res)
        return {'text': f"  {eq.display}\n  Status: {eq.confidence}  |  Code-verified: {eq.code_verified}\n"
                        f"  {eq.radian_form}\n{body}"}

    def shell_commands(self) -> Dict[str, Any]:
        return {
            'bc_norm_cdf': lambda x, mu=0.0, s=1.0: M.norm_cdf(x, mu, s),
            'bc_norm_ppf': lambda p: M.norm_ppf(p),
            'bc_sigma_p': lambda s: M.sigma_to_p(s),
            'bc_p_sigma': lambda p: M.p_to_sigma(p),
            'bc_t': lambda xs=_X, ys=_Y: M.t_test_welch(xs, ys),
            'bc_moments': lambda xs=_X: M.Moments().extend(xs).summary(),
            'bc_wilson': lambda k, n: M.wilson_ci(k, n),
            'bc_canonical': lambda E, T, kB=1.0: M.canonical(E, T, kB),
            'bc_check': lambda: M.verify_known_values(),
        }

    def on_register(self, registry) -> None:
        pass
