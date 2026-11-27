"""
ValaQuenta.modules.bell_curve.maths
===================================
THE BELL CURVE ENGINE -- one statistics, probability and statistical-mechanics
machinery, for everywhere a probability, a spread or a gradient shows up.

Version: 1.2   (2026-11-27; 1.2: nball_volume, nsphere_area, nball_peak; 1.1: ols handles n = 2)

STATUS: ESTABLISHED. Every function here is textbook mathematics (references at
each section). The engine's own claim is only that it is ONE implementation,
verified against scipy 1.18 where scipy has the function (Testing/test_bell_curve.py),
exact where a closed form exists, and stdlib-only (math, random) so any module,
the Monad's pipelines included, can import it with no dependency.

SECTIONS::

  1  Moments          Welford/Pebay streaming mean, variance, skew, kurtosis; exact merge
  2  Descriptive      quantiles (type 7), MAD, IQR, z-scores, histogram, KDE, covariance
  3  Special functions  regularised incomplete gamma and beta, log-binomial, n-ball volume and sphere area (Gamma at half-integers)
  4  Distributions    normal, Student t, chi-square, F, binomial, Poisson, exponential,
                      uniform, gamma, beta: pdf/pmf, cdf, ppf
  5  Sigma            n-sigma <-> p-value, Six-Sigma DPMO, Cp/Cpk
  6  Inference        z/t/Welch/paired tests, proportion tests, chi-square, Mann-Whitney,
                      Kolmogorov-Smirnov, Jarque-Bera, correlation, regression, CIs
  7  Effect, agreement, classification   Cohen d, Hedges g, kappa, F1, MCC, ROC AUC
  8  Multiple testing  Bonferroni, Holm, Benjamini-Hochberg
  9  Resampling       seeded bootstrap and permutation
 10  Information      entropy, cross-entropy, KL, Jensen-Shannon, mutual information, perplexity
 11  Bayes            update, beta-binomial posterior and credible interval
 12  Statistical mechanics  canonical ensemble (Z, U, S, F, Cv), Boltzmann, softmax as a
                      canonical ensemble, Fermi-Dirac, Bose-Einstein, Maxwell-Boltzmann,
                      Planck, two-level, harmonic oscillator, 1-D Ising (transfer matrix)
 13  Circular statistics  mean direction, resultant length, von Mises, Rayleigh test
                      (for quantities that live on a ring, which is every wheel in this project)

References: Welford 1962; Pebay 2008 (SAND2008-6212); Chan, Golub, LeVeque 1983;
Press et al. Numerical Recipes 3e ch. 6 (gamma, beta); Wichura 1988 AS241 / Abramowitz & Stegun
26.2.23 (normal quantile start); Hyndman & Fan 1996 (quantile type 7); Welch 1947;
Mann & Whitney 1947; Kolmogorov 1933, Smirnov 1948; Jarque & Bera 1987; Cohen 1960, 1988;
Hedges 1981; Holm 1979; Benjamini & Hochberg 1995; Shannon 1948; Kullback & Leibler 1951;
Lin 1991; Gibbs 1902; Kramers & Wannier 1941; Mardia & Jupp 2000; Zar 1999 (Rayleigh).
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

SQRT2 = math.sqrt(2.0)
LN2 = math.log(2.0)
K_B = 1.380649e-23          # J/K, exact since the 2019 SI redefinition
H_PLANCK = 6.62607015e-34   # J s, exact
C_LIGHT = 299792458.0       # m/s, exact


# ═══════════════════════════ 1  MOMENTS ═══════════════════════════════════
@dataclass
class Moments:
    """Streaming central moments to the fourth, one pass, mergeable (Welford, Pebay).

    `add` one value; `merge` two accumulators exactly (the result equals the one-pass
    accumulator over the concatenated data up to rounding). This is the object a gradient
    that "gets more or less diluted, or saturated" is accumulated in."""
    n: int = 0
    mean: float = 0.0
    M2: float = 0.0
    M3: float = 0.0
    M4: float = 0.0

    def add(self, x: float) -> "Moments":
        """Add one value to the accumulator (Welford/Pebay update of the first four moments).

        :param x: the new value
        :returns: self, so calls can be chained
        """
        n1 = self.n
        self.n += 1
        n = self.n
        d = x - self.mean
        dn = d / n
        dn2 = dn * dn
        t1 = d * dn * n1
        self.mean += dn
        self.M4 += t1 * dn2 * (n * n - 3 * n + 3) + 6 * dn2 * self.M2 - 4 * dn * self.M3
        self.M3 += t1 * dn * (n - 2) - 3 * dn * self.M2
        self.M2 += t1
        return self

    def extend(self, xs: Iterable[float]) -> "Moments":
        """Add every value of an iterable, one at a time.

        :param xs: the values to add
        :returns: self
        """
        for x in xs:
            self.add(x)
        return self

    def merge(self, o: "Moments") -> "Moments":
        """Combine two accumulators exactly (Pebay 2008); neither input is changed.

        :param o: the other accumulator
        :returns: a new Moments equal to the accumulator over both data sets
        """
        if o.n == 0:
            return Moments(self.n, self.mean, self.M2, self.M3, self.M4)
        if self.n == 0:
            return Moments(o.n, o.mean, o.M2, o.M3, o.M4)
        na, nb = self.n, o.n
        n = na + nb
        d = o.mean - self.mean
        mean = self.mean + d * nb / n
        M2 = self.M2 + o.M2 + d * d * na * nb / n
        M3 = (self.M3 + o.M3 + d ** 3 * na * nb * (na - nb) / n ** 2
              + 3 * d * (na * o.M2 - nb * self.M2) / n)
        M4 = (self.M4 + o.M4 + d ** 4 * na * nb * (na * na - na * nb + nb * nb) / n ** 3
              + 6 * d * d * (na * na * o.M2 + nb * nb * self.M2) / n ** 2
              + 4 * d * (na * o.M3 - nb * self.M3) / n)
        return Moments(n, mean, M2, M3, M4)

    @property
    def var_pop(self) -> float:
        """Population variance (divides by n).

        :returns: M2 / n, or nan when n = 0
        """
        return self.M2 / self.n if self.n else float('nan')

    @property
    def var(self) -> float:
        """Sample variance (n-1)."""
        return self.M2 / (self.n - 1) if self.n > 1 else float('nan')

    @property
    def std(self) -> float:
        """Sample standard deviation (divides by n - 1).

        :returns: the square root of var, or nan when n < 2
        """
        return math.sqrt(self.var) if self.n > 1 else float('nan')

    @property
    def sem(self) -> float:
        """Standard error of the mean.

        :returns: std / sqrt(n), or nan when n < 2
        """
        return self.std / math.sqrt(self.n) if self.n > 1 else float('nan')

    @property
    def skew(self) -> float:
        """Population skewness g1."""
        if self.n < 2 or self.M2 == 0:
            return float('nan')
        return math.sqrt(self.n) * self.M3 / self.M2 ** 1.5

    @property
    def kurt_excess(self) -> float:
        """Population excess kurtosis g2 (normal = 0)."""
        if self.n < 2 or self.M2 == 0:
            return float('nan')
        return self.n * self.M4 / (self.M2 * self.M2) - 3.0

    def summary(self) -> Dict[str, float]:
        """The headline numbers of the accumulator in one dict.

        :returns: dict with n, mean, std, sem, skew, kurt_excess
        """
        return {'n': self.n, 'mean': self.mean, 'std': self.std, 'sem': self.sem,
                'skew': self.skew, 'kurt_excess': self.kurt_excess}


def mean(xs: Sequence[float]) -> float:
    """Arithmetic mean, summed with math.fsum so rounding does not accumulate.

    :param xs: the sample, a sequence of numbers
    :returns: the mean, float
    """
    return math.fsum(xs) / len(xs)


def variance(xs: Sequence[float], ddof: int = 1) -> float:
    """Variance by the streaming accumulator.

    :param xs: the sample, a sequence of numbers
    :param ddof: delta degrees of freedom: 1 for the sample variance, 0 for the population variance
    :returns: the variance, float
    """
    return Moments().extend(xs).M2 / (len(xs) - ddof)


def stdev(xs: Sequence[float], ddof: int = 1) -> float:
    """Standard deviation, the square root of variance.

    :param xs: the sample, a sequence of numbers
    :param ddof: delta degrees of freedom (1 = sample, 0 = population)
    :returns: the standard deviation, float
    """
    return math.sqrt(variance(xs, ddof))


# ═══════════════════════════ 2  DESCRIPTIVE ═══════════════════════════════
def quantile(xs: Sequence[float], q: float) -> float:
    """Hyndman-Fan type 7 (the numpy / R default): linear interpolation between order statistics.

    :param xs: the sample, a sequence of numbers
    :param q: probability in [0, 1]
    :returns: the q-quantile, or nan for an empty sample
    """
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return float('nan')
    h = (n - 1) * q
    lo = int(math.floor(h))
    hi = min(lo + 1, n - 1)
    return s[lo] + (h - lo) * (s[hi] - s[lo])


def median(xs: Sequence[float]) -> float:
    """Median, the 0.5 quantile (type 7).

    :param xs: the sample, a sequence of numbers
    :returns: the median, float
    """
    return quantile(xs, 0.5)


def iqr(xs: Sequence[float]) -> float:
    """Interquartile range, the 0.75 quantile minus the 0.25 quantile.

    :param xs: the sample, a sequence of numbers
    :returns: the IQR, float
    """
    return quantile(xs, 0.75) - quantile(xs, 0.25)


def mad(xs: Sequence[float], scale_normal: bool = True) -> float:
    """Median absolute deviation; x1.4826 makes it a consistent estimator of sigma for normal data.

    :param xs: the sample, a sequence of numbers
    :param scale_normal: multiply by 1.4826 so the value estimates sigma for normal data
    :returns: the median absolute deviation, float
    """
    m = median(xs)
    d = median([abs(x - m) for x in xs])
    return d * 1.482602218505602 if scale_normal else d


def zscores(xs: Sequence[float], robust: bool = False) -> List[float]:
    """Standardise a sample to (x - centre) / spread; a zero spread gives 0 for every value.

    :param xs: the sample, a sequence of numbers
    :param robust: use the median and MAD instead of the mean and standard deviation
    :returns: list of z-scores, same length as xs
    """
    if robust:
        m, s = median(xs), mad(xs)
    else:
        m, s = mean(xs), stdev(xs)
    return [(x - m) / s if s else 0.0 for x in xs]


def covariance(xs: Sequence[float], ys: Sequence[float], ddof: int = 1) -> float:
    """Covariance of two equal-length samples.

    :param xs: the sample, a sequence of numbers
    :param ys: the second sample, a sequence of numbers
    :param ddof: delta degrees of freedom (1 = sample)
    :returns: the covariance, float
    """
    mx, my = mean(xs), mean(ys)
    return math.fsum((a - mx) * (b - my) for a, b in zip(xs, ys)) / (len(xs) - ddof)


def histogram(xs: Sequence[float], bins: Optional[int] = None, lo: Optional[float] = None,
              hi: Optional[float] = None) -> Tuple[List[float], List[int]]:
    """(edges, counts). Default bin count from Freedman-Diaconis.

    :param xs: the sample, a sequence of numbers
    :param bins: number of bins; None chooses by the Freedman-Diaconis rule, at most 200
    :param lo: lower edge; None means min(xs)
    :param hi: upper edge; None means max(xs)
    :returns: (edges, counts): bins + 1 edges and bins integer counts
    """
    lo = min(xs) if lo is None else lo
    hi = max(xs) if hi is None else hi
    if bins is None:
        h = 2 * iqr(xs) / len(xs) ** (1 / 3) if len(xs) > 3 else 0
        bins = max(1, int(math.ceil((hi - lo) / h))) if h > 0 else 10
        bins = min(bins, 200)
    w = (hi - lo) / bins or 1.0
    edges = [lo + i * w for i in range(bins + 1)]
    counts = [0] * bins
    for x in xs:
        if lo <= x <= hi:
            counts[min(bins - 1, int((x - lo) / w))] += 1
    return edges, counts


def kde(xs: Sequence[float], at: Sequence[float], bw: Optional[float] = None) -> List[float]:
    """Gaussian kernel density estimate at the points `at`; Silverman's rule-of-thumb bandwidth.

    :param xs: the sample, a sequence of numbers
    :param at: points at which to evaluate the density
    :param bw: bandwidth; None uses Silverman's rule
    :returns: list of density values, one per point in at
    """
    n = len(xs)
    if bw is None:
        s = min(stdev(xs), iqr(xs) / 1.34) or stdev(xs) or 1.0
        bw = 0.9 * s * n ** (-0.2)
    c = 1.0 / (n * bw * math.sqrt(2 * math.pi))
    return [c * math.fsum(math.exp(-0.5 * ((a - x) / bw) ** 2) for x in xs) for a in at]


# ═══════════════════════════ 3  SPECIAL FUNCTIONS ═════════════════════════
_EPS = 3e-16
_TINY = 1e-300


def gammainc_p(a: float, x: float) -> float:
    """Regularised lower incomplete gamma P(a, x) (series for x < a+1, continued fraction above).

    :param a: shape, a > 0
    :param x: upper limit of the integral
    :returns: P(a, x) in [0, 1]
    """
    if x <= 0:
        return 0.0
    if x < a + 1.0:
        ap, s, d = a, 1.0 / a, 1.0 / a
        for _ in range(10000):
            ap += 1.0
            d *= x / ap
            s += d
            if abs(d) < abs(s) * _EPS:
                break
        return s * math.exp(-x + a * math.log(x) - math.lgamma(a))
    b = x + 1.0 - a
    c = 1.0 / _TINY
    d = 1.0 / b
    h = d
    for i in range(1, 10000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        d = _TINY if abs(d) < _TINY else d
        c = b + an / c
        c = _TINY if abs(c) < _TINY else c
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < _EPS:
            break
    return 1.0 - math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def _betacf(a: float, b: float, x: float) -> float:
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    d = _TINY if abs(d) < _TINY else d
    d = 1.0 / d
    h = d
    for m in range(1, 10000):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = _TINY if abs(d) < _TINY else d
        c = 1.0 + aa / c
        c = _TINY if abs(c) < _TINY else c
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = _TINY if abs(d) < _TINY else d
        c = 1.0 + aa / c
        c = _TINY if abs(c) < _TINY else c
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < _EPS:
            break
    return h


def betainc(a: float, b: float, x: float) -> float:
    """Regularised incomplete beta I_x(a, b).

    :param a: first shape, a > 0
    :param b: second shape, b > 0
    :param x: upper limit, in [0, 1]
    :returns: I_x(a, b) in [0, 1]
    """
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def log_comb(n: int, k: int) -> float:
    """Natural log of the binomial coefficient C(n, k), by log-gamma so large n does not overflow.

    :param n: number of items
    :param k: number chosen
    :returns: ln C(n, k), float
    """
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def nball_volume(n: float) -> float:
    """
    Volume of the unit ball in n dimensions, pi^(n/2) / Gamma(n/2 + 1), for any real n >= 0.

    The Gamma function is what lets n be non-integer: the n-dimensional Gaussian integral gives (sqrt(pi))^n = (S/2) Gamma(n/2), where S is the
    area of the unit sphere, so Gamma(n/2) is the radial bookkeeping of a sphere. n = 1 gives 2 (a segment), n = 2 gives pi (the circle's disc),
    n = 3 gives 4 pi/3. The volume peaks near n = 5.2569 and then falls towards 0 (nball_peak).

    :param n: dimension, a real number >= 0
    :returns: the volume of the unit ball, float
    """
    return math.exp(0.5 * n * math.log(math.pi) - math.lgamma(0.5 * n + 1.0))


def nsphere_area(n: float) -> float:
    """
    Area of the unit sphere in R^n (the (n-1)-sphere), 2 pi^(n/2) / Gamma(n/2); equal to n times the ball volume.

    n = 2 gives 2 pi, the circumference of the unit circle. The area peaks near n = 7.2569, two dimensions after the volume.

    :param n: dimension, a real number > 0
    :returns: the area of the unit sphere, float
    """
    return 2.0 * math.exp(0.5 * n * math.log(math.pi) - math.lgamma(0.5 * n))


def nball_peak(which: str = 'volume') -> float:
    """
    The real dimension at which the unit-ball volume (or sphere area) is largest: where d/dn ln V = (1/2) ln pi - (1/2) digamma(n/2 + 1) = 0.

    Found by bisection on a central difference of the log, so the engine stays stdlib-only. The volume peaks at n = 5.2569464..., the area at
    n = 7.2569464... (the volume's peak plus 2).

    :param which: 'volume' or 'area'
    :returns: the dimension of the maximum, float
    """
    f = nball_volume if which == 'volume' else nsphere_area
    lo, hi, h = (1.0, 12.0, 1e-5)
    g = lambda n: math.log(f(n + h)) - math.log(f(n - h))
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if g(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _invert(cdf: Callable[[float], float], p: float, lo: float, hi: float, tol: float = 1e-14) -> float:
    """Monotone-cdf inverse by bracket expansion then bisection polished with secant steps."""
    while cdf(lo) > p:
        lo = lo * 2 if lo < 0 else lo - 1.0
    while cdf(hi) < p:
        hi = hi * 2 if hi > 0 else hi + 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if cdf(mid) < p:
            lo = mid
        else:
            hi = mid
        if hi - lo <= tol * max(1.0, abs(mid)):
            break
    return 0.5 * (lo + hi)


# ═══════════════════════════ 4  DISTRIBUTIONS ═════════════════════════════
# normal
def norm_pdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """Normal probability density.

    :param x: the point
    :param mu: mean
    :param sigma: standard deviation
    :returns: density at x, float
    """
    z = (x - mu) / sigma
    return math.exp(-0.5 * z * z) / (sigma * math.sqrt(2 * math.pi))


def norm_cdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """Normal cumulative distribution, by the complementary error function.

    :param x: the point
    :param mu: mean
    :param sigma: standard deviation
    :returns: P(X <= x), float
    """
    return 0.5 * math.erfc(-(x - mu) / (sigma * SQRT2))


def norm_sf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """Survival function 1 - cdf, accurate far into the tail.

    :param x: the point
    :param mu: mean
    :param sigma: standard deviation
    :returns: P(X > x), float
    """
    return 0.5 * math.erfc((x - mu) / (sigma * SQRT2))


def norm_ppf(p: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """Normal quantile: Abramowitz-Stegun 26.2.23 start, then Halley on erfc to machine precision.

    :param p: probability in [0, 1]
    :param mu: mean
    :param sigma: standard deviation
    :returns: the quantile x with cdf(x) = p; raises ValueError outside [0, 1]
    """
    if not 0.0 < p < 1.0:
        if p == 0.0:
            return -math.inf
        if p == 1.0:
            return math.inf
        raise ValueError('p must be in [0, 1]')
    q = p if p < 0.5 else 1.0 - p
    t = math.sqrt(-2.0 * math.log(q))
    x = -(t - (2.515517 + 0.802853 * t + 0.010328 * t * t) /
          (1.0 + 1.432788 * t + 0.189269 * t * t + 0.001308 * t ** 3))
    for _ in range(4):
        e = 0.5 * math.erfc(-x / SQRT2) - q
        u = e * math.sqrt(2 * math.pi) * math.exp(0.5 * x * x)
        x = x - u / (1.0 + 0.5 * x * u)
    return mu + sigma * (x if p < 0.5 else -x)


# Student t
def t_cdf(x: float, df: float) -> float:
    """Student t cumulative distribution, through the incomplete beta function.

    :param x: the point
    :param df: degrees of freedom (math.inf gives the normal)
    :returns: P(T <= x), float
    """
    if math.isinf(df):
        return norm_cdf(x)
    ib = betainc(df / 2.0, 0.5, df / (df + x * x))
    return 1.0 - 0.5 * ib if x > 0 else 0.5 * ib


def t_pdf(x: float, df: float) -> float:
    """Student t probability density.

    :param x: the point
    :param df: degrees of freedom
    :returns: density at x, float
    """
    return math.exp(math.lgamma((df + 1) / 2) - math.lgamma(df / 2)) / math.sqrt(df * math.pi) \
        * (1 + x * x / df) ** (-(df + 1) / 2)


def t_ppf(p: float, df: float) -> float:
    """Student t quantile, by inverting the cdf.

    :param p: probability in (0, 1)
    :param df: degrees of freedom
    :returns: the quantile, float
    """
    if math.isinf(df):
        return norm_ppf(p)
    return _invert(lambda x: t_cdf(x, df), p, -10.0, 10.0)


# chi-square
def chi2_cdf(x: float, df: float) -> float:
    """Chi-square cumulative distribution, through the incomplete gamma function.

    :param x: the point
    :param df: degrees of freedom
    :returns: P(X <= x), float
    """
    return gammainc_p(df / 2.0, x / 2.0)


def chi2_sf(x: float, df: float) -> float:
    """Chi-square survival function, 1 - cdf.

    :param x: the point
    :param df: degrees of freedom
    :returns: P(X > x), float
    """
    return 1.0 - chi2_cdf(x, df)


def chi2_pdf(x: float, df: float) -> float:
    """Chi-square probability density.

    :param x: the point
    :param df: degrees of freedom
    :returns: density at x, 0 for x <= 0
    """
    if x <= 0:
        return 0.0
    return math.exp((df / 2 - 1) * math.log(x) - x / 2 - (df / 2) * LN2 - math.lgamma(df / 2))


def chi2_ppf(p: float, df: float) -> float:
    """Chi-square quantile, by inverting the cdf.

    :param p: probability in (0, 1)
    :param df: degrees of freedom
    :returns: the quantile, float
    """
    return _invert(lambda x: chi2_cdf(x, df), p, 0.0, max(10.0, 3 * df))


# F
def f_cdf(x: float, d1: float, d2: float) -> float:
    """F-distribution cumulative distribution, through the incomplete beta function.

    :param x: the point
    :param d1: numerator degrees of freedom
    :param d2: denominator degrees of freedom
    :returns: P(F <= x), float
    """
    if x <= 0:
        return 0.0
    return betainc(d1 / 2.0, d2 / 2.0, d1 * x / (d1 * x + d2))


def f_ppf(p: float, d1: float, d2: float) -> float:
    """F-distribution quantile, by inverting the cdf.

    :param p: probability in (0, 1)
    :param d1: numerator degrees of freedom
    :param d2: denominator degrees of freedom
    :returns: the quantile, float
    """
    return _invert(lambda x: f_cdf(x, d1, d2), p, 0.0, 10.0)


# gamma, beta, exponential, uniform
def gamma_cdf(x: float, shape: float, scale: float = 1.0) -> float:
    """Gamma cumulative distribution.

    :param x: the point
    :param shape: shape parameter
    :param scale: scale parameter
    :returns: P(X <= x), float
    """
    return gammainc_p(shape, x / scale)


def beta_pdf(x: float, a: float, b: float) -> float:
    """Beta probability density.

    :param x: the point, in (0, 1)
    :param a: first shape
    :param b: second shape
    :returns: density at x, 0 outside (0, 1)
    """
    if not 0 < x < 1:
        return 0.0
    return math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + (a - 1) * math.log(x)
                    + (b - 1) * math.log1p(-x))


def beta_cdf(x: float, a: float, b: float) -> float:
    """Beta cumulative distribution, the regularised incomplete beta.

    :param x: the point, in [0, 1]
    :param a: first shape
    :param b: second shape
    :returns: P(X <= x), float
    """
    return betainc(a, b, x)


def beta_ppf(p: float, a: float, b: float) -> float:
    """Beta quantile, by inverting the cdf.

    :param p: probability in (0, 1)
    :param a: first shape
    :param b: second shape
    :returns: the quantile, float in [0, 1]
    """
    return _invert(lambda x: betainc(a, b, x), p, 0.0, 1.0)


def expon_pdf(x: float, rate: float = 1.0) -> float:
    """Exponential probability density.

    :param x: the point
    :param rate: rate lambda
    :returns: density at x, 0 for x < 0
    """
    return rate * math.exp(-rate * x) if x >= 0 else 0.0


def expon_cdf(x: float, rate: float = 1.0) -> float:
    """Exponential cumulative distribution.

    :param x: the point
    :param rate: rate lambda
    :returns: P(X <= x), float
    """
    return -math.expm1(-rate * x) if x >= 0 else 0.0


def uniform_cdf(x: float, a: float = 0.0, b: float = 1.0) -> float:
    """Uniform cumulative distribution on [a, b].

    :param x: the point
    :param a: lower end
    :param b: upper end
    :returns: P(X <= x), float
    """
    return 0.0 if x <= a else 1.0 if x >= b else (x - a) / (b - a)


# discrete
def binom_pmf(k: int, n: int, p: float) -> float:
    """Binomial probability mass, computed in logs.

    :param k: number of successes
    :param n: number of trials
    :param p: success probability
    :returns: P(K = k), float
    """
    if k < 0 or k > n:
        return 0.0
    if p in (0.0, 1.0):
        return 1.0 if k == (0 if p == 0.0 else n) else 0.0
    return math.exp(log_comb(n, k) + k * math.log(p) + (n - k) * math.log1p(-p))


def binom_cdf(k: int, n: int, p: float) -> float:
    """Binomial cumulative distribution, through the incomplete beta.

    :param k: number of successes
    :param n: number of trials
    :param p: success probability
    :returns: P(K <= k), float
    """
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    return betainc(n - k, k + 1, 1.0 - p)


def poisson_pmf(k: int, lam: float) -> float:
    """Poisson probability mass.

    :param k: count
    :param lam: mean
    :returns: P(K = k), float
    """
    return math.exp(k * math.log(lam) - lam - math.lgamma(k + 1)) if k >= 0 and lam > 0 else (1.0 if k == 0 else 0.0)


def poisson_cdf(k: int, lam: float) -> float:
    """Poisson cumulative distribution, through the incomplete gamma.

    :param k: count
    :param lam: mean
    :returns: P(K <= k), float
    """
    return 1.0 - gammainc_p(k + 1.0, lam) if k >= 0 else 0.0


# ═══════════════════════════ 5  SIGMA ═════════════════════════════════════
def p_to_sigma(p: float, two_sided: bool = True) -> float:
    """The n-sigma a p-value corresponds to (two-sided: 3 sigma <-> p = 0.0027).

    :param p: the p-value
    :param two_sided: treat p as two-sided
    :returns: n, the number of sigmas, float
    """
    return -norm_ppf(p / 2.0 if two_sided else p)       # tail probability used directly: no 1-p cancellation


def sigma_to_p(sigma: float, two_sided: bool = True) -> float:
    """The p-value of an n-sigma result.

    :param sigma: the number of sigmas
    :param two_sided: two-sided p (3 sigma gives 0.0027)
    :returns: the p-value, float
    """
    return (2.0 if two_sided else 1.0) * norm_sf(sigma)


def sigma_to_dpmo(sigma_level: float, shift: float = 1.5) -> float:
    """Six-Sigma convention: defects per million opportunities at a short-term sigma level with the
    customary 1.5-sigma long-term shift (6 sigma -> 3.4 DPMO).

    :param sigma_level: short-term sigma level
    :param shift: long-term shift in sigmas
    :returns: defects per million opportunities, float
    """
    return 1e6 * norm_sf(sigma_level - shift)


def dpmo_to_sigma(dpmo: float, shift: float = 1.5) -> float:
    """Inverse of sigma_to_dpmo: the sigma level that gives a defect rate.

    :param dpmo: defects per million opportunities
    :param shift: long-term shift in sigmas
    :returns: the short-term sigma level, float
    """
    return -norm_ppf(dpmo / 1e6) + shift


def cp_cpk(mu: float, sigma: float, lsl: float, usl: float) -> Tuple[float, float]:
    """Process capability indices Cp (spread against the tolerance) and Cpk (also the centring).

    :param mu: process mean
    :param sigma: process standard deviation
    :param lsl: lower specification limit
    :param usl: upper specification limit
    :returns: (Cp, Cpk)
    """
    cp = (usl - lsl) / (6 * sigma)
    return cp, min(usl - mu, mu - lsl) / (3 * sigma)


# ═══════════════════════════ 6  INFERENCE ═════════════════════════════════
def _t_two_sided_p(t: float, df: float) -> float:
    return 2.0 * (1.0 - t_cdf(abs(t), df))


def t_test_one(xs: Sequence[float], mu0: float = 0.0, conf: float = 0.95) -> Dict[str, float]:
    """One-sample t test of the mean against mu0.

    :param xs: the sample, a sequence of numbers
    :param mu0: the hypothesised mean
    :param conf: confidence level of the interval (0.95 = 95%)
    :returns: dict with t, df, p (two-sided), mean, ci, d
    """
    m = Moments().extend(xs)
    t = (m.mean - mu0) / m.sem
    df = m.n - 1
    h = t_ppf(0.5 + conf / 2, df) * m.sem
    return {'t': t, 'df': df, 'p': _t_two_sided_p(t, df), 'mean': m.mean, 'ci': (m.mean - h, m.mean + h),
            'd': (m.mean - mu0) / m.std}


def t_test_welch(xs: Sequence[float], ys: Sequence[float], conf: float = 0.95) -> Dict[str, float]:
    """Welch's two-sample t test, unequal variances (Welch 1947).

    :param xs: the sample, a sequence of numbers
    :param ys: the second sample, a sequence of numbers
    :param conf: confidence level of the interval (0.95 = 95%)
    :returns: dict with t, df, p (two-sided), diff, ci, d
    """
    a, b = Moments().extend(xs), Moments().extend(ys)
    va, vb = a.var / a.n, b.var / b.n
    se = math.sqrt(va + vb)
    t = (a.mean - b.mean) / se
    df = (va + vb) ** 2 / (va * va / (a.n - 1) + vb * vb / (b.n - 1))
    h = t_ppf(0.5 + conf / 2, df) * se
    diff = a.mean - b.mean
    return {'t': t, 'df': df, 'p': _t_two_sided_p(t, df), 'diff': diff, 'ci': (diff - h, diff + h),
            'd': cohens_d(xs, ys)}


def t_test_paired(xs: Sequence[float], ys: Sequence[float], conf: float = 0.95) -> Dict[str, float]:
    """Paired t test: a one-sample test of the pairwise differences against zero.

    :param xs: first measurements
    :param ys: second measurements, paired with xs
    :param conf: confidence level of the interval (0.95 = 95%)
    :returns: dict as for t_test_one
    """
    return t_test_one([a - b for a, b in zip(xs, ys)], 0.0, conf)


def z_test_prop(k: int, n: int, p0: float) -> Dict[str, float]:
    """z test of a proportion against p0.

    :param k: successes
    :param n: trials
    :param p0: the hypothesised proportion
    :returns: dict with z, p (two-sided), phat
    """
    z = (k / n - p0) / math.sqrt(p0 * (1 - p0) / n)
    return {'z': z, 'p': 2 * norm_sf(abs(z)), 'phat': k / n}


def wilson_ci(k: int, n: int, conf: float = 0.95) -> Tuple[float, float]:
    """Wilson score interval for a binomial proportion (Wilson 1927); sound at small n and extreme p.

    :param k: successes
    :param n: trials
    :param conf: confidence level of the interval (0.95 = 95%)
    :returns: (lower, upper)
    """
    z = norm_ppf(0.5 + conf / 2)
    ph = k / n
    den = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / den
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


def chi2_gof(observed: Sequence[float], expected: Sequence[float]) -> Dict[str, float]:
    """Chi-square goodness of fit.

    :param observed: observed counts
    :param expected: expected counts, same length
    :returns: dict with chi2, df, p
    """
    stat = math.fsum((o - e) ** 2 / e for o, e in zip(observed, expected))
    df = len(observed) - 1
    return {'chi2': stat, 'df': df, 'p': chi2_sf(stat, df)}


def chi2_independence(table: Sequence[Sequence[float]]) -> Dict[str, float]:
    """Chi-square test of independence on a contingency table, with Cramer's V.

    :param table: rows of observed counts
    :returns: dict with chi2, df, p, cramers_v
    """
    r, c = len(table), len(table[0])
    rs = [sum(row) for row in table]
    cs = [sum(table[i][j] for i in range(r)) for j in range(c)]
    n = sum(rs)
    stat = math.fsum((table[i][j] - rs[i] * cs[j] / n) ** 2 / (rs[i] * cs[j] / n)
                     for i in range(r) for j in range(c))
    df = (r - 1) * (c - 1)
    v = math.sqrt(stat / (n * min(r - 1, c - 1))) if min(r, c) > 1 else float('nan')
    return {'chi2': stat, 'df': df, 'p': chi2_sf(stat, df), 'cramers_v': v}


def _ranks(xs: Sequence[float]) -> Tuple[List[float], List[int]]:
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    ties: List[int] = []
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2.0 + 1.0
        ties.append(j - i + 1)
        i = j + 1
    return r, ties


def mann_whitney_u(xs: Sequence[float], ys: Sequence[float]) -> Dict[str, float]:
    """Mann-Whitney U, normal approximation with tie and continuity correction; also the AUC.

    :param xs: the sample, a sequence of numbers
    :param ys: the second sample, a sequence of numbers
    :returns: dict with U, z, p (two-sided), auc
    """
    n1, n2 = len(xs), len(ys)
    r, ties = _ranks(list(xs) + list(ys))
    u1 = sum(r[:n1]) - n1 * (n1 + 1) / 2.0
    n = n1 + n2
    tie = sum(t ** 3 - t for t in ties)
    sd = math.sqrt(n1 * n2 / 12.0 * ((n + 1) - tie / (n * (n - 1)))) if n > 1 else float('nan')
    mu = n1 * n2 / 2.0
    z = (abs(u1 - mu) - 0.5) / sd if sd else 0.0
    return {'U': u1, 'z': z, 'p': min(1.0, 2 * norm_sf(z)), 'auc': u1 / (n1 * n2)}


def ks_two_sample(xs: Sequence[float], ys: Sequence[float]) -> Dict[str, float]:
    """Two-sample Kolmogorov-Smirnov, asymptotic p (Kolmogorov series).

    :param xs: the sample, a sequence of numbers
    :param ys: the second sample, a sequence of numbers
    :returns: dict with D and p
    """
    a, b = sorted(xs), sorted(ys)
    i = j = 0
    d = 0.0
    na, nb = len(a), len(b)
    while i < na and j < nb:
        x = min(a[i], b[j])
        while i < na and a[i] <= x:
            i += 1
        while j < nb and b[j] <= x:
            j += 1
        d = max(d, abs(i / na - j / nb))
    en = math.sqrt(na * nb / (na + nb))
    lam = (en + 0.12 + 0.11 / en) * d
    p = 2.0 * math.fsum((-1) ** (k - 1) * math.exp(-2.0 * k * k * lam * lam) for k in range(1, 101))
    return {'D': d, 'p': min(1.0, max(0.0, p))}


def jarque_bera(xs: Sequence[float]) -> Dict[str, float]:
    """Jarque-Bera test of normality from skewness and excess kurtosis (Jarque and Bera 1987).

    :param xs: the sample, a sequence of numbers
    :returns: dict with JB, p, skew, kurt_excess
    """
    m = Moments().extend(xs)
    jb = m.n / 6.0 * (m.skew ** 2 + m.kurt_excess ** 2 / 4.0)
    return {'JB': jb, 'p': chi2_sf(jb, 2), 'skew': m.skew, 'kurt_excess': m.kurt_excess}


def pearson(xs: Sequence[float], ys: Sequence[float], conf: float = 0.95) -> Dict[str, float]:
    """Pearson correlation with a t-test p-value and a Fisher-z confidence interval.

    :param xs: the sample, a sequence of numbers
    :param ys: the second sample, a sequence of numbers
    :param conf: confidence level of the interval (0.95 = 95%)
    :returns: dict with r, p, ci, n
    """
    n = len(xs)
    r = covariance(xs, ys) / (stdev(xs) * stdev(ys))
    r = max(-1.0, min(1.0, r))
    if n > 2 and abs(r) < 1:
        t = r * math.sqrt((n - 2) / (1 - r * r))
        p = _t_two_sided_p(t, n - 2)
    else:
        p = 0.0
    if n > 3 and abs(r) < 1:
        z, se = math.atanh(r), 1 / math.sqrt(n - 3)
        h = norm_ppf(0.5 + conf / 2) * se
        ci = (math.tanh(z - h), math.tanh(z + h))
    else:
        ci = (r, r)
    return {'r': r, 'p': p, 'ci': ci, 'n': n}


def spearman(xs: Sequence[float], ys: Sequence[float]) -> Dict[str, float]:
    """Spearman rank correlation: Pearson on the ranks, ties averaged.

    :param xs: the sample, a sequence of numbers
    :param ys: the second sample, a sequence of numbers
    :returns: dict as for pearson
    """
    return pearson(_ranks(xs)[0], _ranks(ys)[0])


def ols(xs: Sequence[float], ys: Sequence[float], conf: float = 0.95) -> Dict[str, float]:
    """Simple linear regression y = a + b x with standard errors, p, r^2 and a CI on the slope.

    :param xs: the sample, a sequence of numbers
    :param ys: the second sample, a sequence of numbers
    :param conf: confidence level of the interval (0.95 = 95%)
    :returns: dict with slope, intercept, r2, se_slope, p_slope, ci_slope, n
    """
    n = len(xs)
    mx, my = mean(xs), mean(ys)
    sxx = math.fsum((x - mx) ** 2 for x in xs)
    sxy = math.fsum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx
    a = my - b * mx
    sse = math.fsum((y - a - b * x) ** 2 for x, y in zip(xs, ys))
    sst = math.fsum((y - my) ** 2 for y in ys)
    if n < 3:                                   # two points fit exactly: slope and intercept, no error estimate
        return {'slope': b, 'intercept': a, 'r2': 1.0 if n == 2 else float('nan'), 'se_slope': float('nan'),
                'p_slope': float('nan'), 'ci_slope': (float('nan'), float('nan')), 'n': n}
    s2 = sse / (n - 2)
    seb = math.sqrt(s2 / sxx)
    t = b / seb if seb else float('inf')
    h = t_ppf(0.5 + conf / 2, n - 2) * seb
    return {'slope': b, 'intercept': a, 'r2': 1 - sse / sst if sst else 1.0, 'se_slope': seb,
            'p_slope': _t_two_sided_p(t, n - 2), 'ci_slope': (b - h, b + h), 'n': n}


# ═══════════════════════════ 7  EFFECT / AGREEMENT / CLASSIFICATION ═══════
def cohens_d(xs: Sequence[float], ys: Sequence[float]) -> float:
    """Cohen's d: the difference of means over the pooled standard deviation (Cohen 1988).

    :param xs: the sample, a sequence of numbers
    :param ys: the second sample, a sequence of numbers
    :returns: d, float (nan when the pooled deviation is 0)
    """
    a, b = Moments().extend(xs), Moments().extend(ys)
    sp = math.sqrt(((a.n - 1) * a.var + (b.n - 1) * b.var) / (a.n + b.n - 2))
    return (a.mean - b.mean) / sp if sp else float('nan')


def hedges_g(xs: Sequence[float], ys: Sequence[float]) -> float:
    """Hedges' g: Cohen's d with the small-sample correction (Hedges 1981).

    :param xs: the sample, a sequence of numbers
    :param ys: the second sample, a sequence of numbers
    :returns: g, float
    """
    df = len(xs) + len(ys) - 2
    return cohens_d(xs, ys) * (1 - 3.0 / (4 * df - 1))


def cohens_kappa(a: Sequence, b: Sequence) -> Dict[str, float]:
    """Chance-corrected agreement between two raters (Cohen 1960) with Fleiss-style standard error.

    :param a: labels from the first rater
    :param b: labels from the second rater, same length
    :returns: dict with kappa, po, pe, se
    """
    n = len(a)
    cats = sorted(set(a) | set(b))
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pe = sum((sum(1 for x in a if x == c) / n) * (sum(1 for y in b if y == c) / n) for c in cats)
    k = (po - pe) / (1 - pe) if pe < 1 else 1.0
    se = math.sqrt(po * (1 - po) / (n * (1 - pe) ** 2)) if pe < 1 else 0.0
    return {'kappa': k, 'po': po, 'pe': pe, 'se': se}


def confusion_metrics(tp: int, fp: int, fn: int, tn: int) -> Dict[str, float]:
    """Classification metrics from a confusion matrix.

    :param tp: true positives
    :param fp: false positives
    :param fn: false negatives
    :param tn: true negatives
    :returns: dict with precision, recall, f1, accuracy, mcc
    """
    prec = tp / (tp + fp) if tp + fp else float('nan')
    rec = tp / (tp + fn) if tp + fn else float('nan')
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else float('nan')
    den = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    return {'precision': prec, 'recall': rec, 'f1': f1, 'accuracy': (tp + tn) / (tp + fp + fn + tn),
            'mcc': (tp * tn - fp * fn) / den if den else float('nan')}


def roc_auc(scores_pos: Sequence[float], scores_neg: Sequence[float]) -> float:
    """Area under the ROC curve, equal to the Mann-Whitney AUC.

    :param scores_pos: scores of the positive cases
    :param scores_neg: scores of the negative cases
    :returns: AUC in [0, 1]
    """
    return mann_whitney_u(scores_pos, scores_neg)['auc']


# ═══════════════════════════ 8  MULTIPLE TESTING ══════════════════════════
def bonferroni(ps: Sequence[float]) -> List[float]:
    """Bonferroni adjustment: each p multiplied by the number of tests, capped at 1.

    :param ps: raw p-values
    :returns: adjusted p-values, same order
    """
    m = len(ps)
    return [min(1.0, p * m) for p in ps]


def holm(ps: Sequence[float]) -> List[float]:
    """Holm step-down adjustment (Holm 1979), uniformly better than Bonferroni.

    :param ps: raw p-values
    :returns: adjusted p-values, same order
    """
    m = len(ps)
    order = sorted(range(m), key=lambda i: ps[i])
    out = [0.0] * m
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (m - rank) * ps[i]))
        out[i] = run
    return out


def benjamini_hochberg(ps: Sequence[float]) -> List[float]:
    """Benjamini-Hochberg false-discovery-rate adjustment (1995).

    :param ps: raw p-values
    :returns: adjusted p-values (q-values), same order
    """
    m = len(ps)
    order = sorted(range(m), key=lambda i: ps[i], reverse=True)
    out = [0.0] * m
    run = 1.0
    for k, i in enumerate(order):
        rank = m - k
        run = min(run, ps[i] * m / rank)
        out[i] = run
    return out


# ═══════════════════════════ 9  RESAMPLING ════════════════════════════════
def bootstrap_ci(xs: Sequence[float], stat: Callable[[Sequence[float]], float] = mean,
                 n_boot: int = 2000, conf: float = 0.95, seed: int = 20261122) -> Dict[str, float]:
    """Percentile bootstrap confidence interval for any statistic, with a seeded generator so a rerun gives the same answer.

    :param xs: the sample, a sequence of numbers
    :param stat: function of a sample that returns a number
    :param n_boot: number of resamples
    :param conf: confidence level of the interval (0.95 = 95%)
    :param seed: seed of the random generator
    :returns: dict with stat, ci, se
    """
    rng = random.Random(seed)
    n = len(xs)
    vals = [stat([xs[rng.randrange(n)] for _ in range(n)]) for _ in range(n_boot)]
    a = (1 - conf) / 2
    return {'stat': stat(xs), 'ci': (quantile(vals, a), quantile(vals, 1 - a)), 'se': stdev(vals)}


def permutation_test(xs: Sequence[float], ys: Sequence[float],
                     stat: Callable[[Sequence[float], Sequence[float]], float] = lambda a, b: mean(a) - mean(b),
                     n_perm: int = 5000, seed: int = 20261122) -> Dict[str, float]:
    """Two-sample permutation test, two-sided, seeded.

    :param xs: the sample, a sequence of numbers
    :param ys: the second sample, a sequence of numbers
    :param stat: function of two samples; default is the difference of means
    :param n_perm: number of shuffles
    :param seed: seed of the random generator
    :returns: dict with observed and p = (hits + 1) / (n_perm + 1)
    """
    rng = random.Random(seed)
    obs = stat(xs, ys)
    pool = list(xs) + list(ys)
    n1 = len(xs)
    hits = 0
    for _ in range(n_perm):
        rng.shuffle(pool)
        if abs(stat(pool[:n1], pool[n1:])) >= abs(obs) - 1e-12:
            hits += 1
    return {'observed': obs, 'p': (hits + 1) / (n_perm + 1)}


# ═══════════════════════════ 10  INFORMATION ══════════════════════════════
def entropy(p: Sequence[float], base: float = 2.0) -> float:
    """Shannon entropy of a distribution (Shannon 1948); the input is normalised first.

    :param p: the probabilities, a sequence (normalised inside where stated)
    :param base: logarithm base (2 gives bits)
    :returns: entropy, float
    """
    s = math.fsum(p)
    return -math.fsum((x / s) * math.log(x / s, base) for x in p if x > 0)


def cross_entropy(p: Sequence[float], q: Sequence[float], base: float = 2.0) -> float:
    """Cross-entropy H(p, q).

    :param p: the true distribution
    :param q: the model distribution
    :param base: logarithm base
    :returns: cross-entropy, float
    """
    return -math.fsum(a * math.log(b, base) for a, b in zip(p, q) if a > 0)


def kl_divergence(p: Sequence[float], q: Sequence[float], base: float = 2.0) -> float:
    """Kullback-Leibler divergence D(p || q) (1951); raises ZeroDivisionError if q is 0 where p is not.

    :param p: the true distribution
    :param q: the model distribution
    :param base: logarithm base
    :returns: divergence, float
    """
    return math.fsum(a * math.log(a / b, base) for a, b in zip(p, q) if a > 0)


def js_divergence(p: Sequence[float], q: Sequence[float], base: float = 2.0) -> float:
    """Jensen-Shannon divergence (Lin 1991): the symmetric, bounded relative of KL.

    :param p: first distribution
    :param q: second distribution
    :param base: logarithm base
    :returns: divergence, float
    """
    m = [(a + b) / 2 for a, b in zip(p, q)]
    return 0.5 * kl_divergence(p, m, base) + 0.5 * kl_divergence(q, m, base)


def mutual_information(joint: Sequence[Sequence[float]], base: float = 2.0) -> float:
    """Mutual information of a joint table of counts or probabilities.

    :param joint: rows of joint counts or probabilities
    :param base: logarithm base
    :returns: I(X; Y), float
    """
    n = math.fsum(math.fsum(r) for r in joint)
    px = [math.fsum(r) / n for r in joint]
    py = [math.fsum(joint[i][j] for i in range(len(joint))) / n for j in range(len(joint[0]))]
    return math.fsum((joint[i][j] / n) * math.log((joint[i][j] / n) / (px[i] * py[j]), base)
                     for i in range(len(joint)) for j in range(len(joint[0])) if joint[i][j] > 0)


def perplexity(p: Sequence[float]) -> float:
    """Perplexity 2^H of a distribution: the effective number of equally likely outcomes.

    :param p: the probabilities, a sequence (normalised inside where stated)
    :returns: perplexity, float
    """
    return 2.0 ** entropy(p, 2.0)


# ═══════════════════════════ 11  BAYES ════════════════════════════════════
def bayes_update(prior: Sequence[float], likelihood: Sequence[float]) -> List[float]:
    """Bayes' rule on a discrete hypothesis set: posterior proportional to prior times likelihood.

    :param prior: prior probabilities
    :param likelihood: likelihood of the data under each hypothesis
    :returns: normalised posterior, list
    """
    post = [a * b for a, b in zip(prior, likelihood)]
    s = math.fsum(post)
    return [x / s for x in post]


def beta_binomial(successes: int, trials: int, a0: float = 1.0, b0: float = 1.0,
                  conf: float = 0.95) -> Dict[str, float]:
    """Beta-binomial posterior for a proportion, with an equal-tailed credible interval.

    :param successes: observed successes
    :param trials: observed trials
    :param a0: prior alpha
    :param b0: prior beta
    :param conf: credible mass
    :returns: dict with a, b, mean, credible
    """
    a, b = a0 + successes, b0 + trials - successes
    lo, hi = beta_ppf((1 - conf) / 2, a, b), beta_ppf(1 - (1 - conf) / 2, a, b)
    return {'a': a, 'b': b, 'mean': a / (a + b), 'credible': (lo, hi)}


# ═══════════════════════════ 12  STATISTICAL MECHANICS ════════════════════
def boltzmann_probs(energies: Sequence[float], beta: float,
                    degeneracy: Optional[Sequence[float]] = None) -> List[float]:
    """p_i = g_i exp(-beta E_i) / Z, computed with the minimum subtracted (no overflow).

    :param energies: energy levels
    :param beta: inverse temperature 1/(kB T), in the inverse of the energy unit
    :param degeneracy: g_i for each level; None means 1 each
    :returns: probabilities, list, summing to 1
    """
    g = degeneracy or [1.0] * len(energies)
    e0 = min(energies)
    w = [gi * math.exp(-beta * (e - e0)) for gi, e in zip(g, energies)]
    z = math.fsum(w)
    return [x / z for x in w]


def canonical(energies: Sequence[float], T: float, kB: float = K_B,
              degeneracy: Optional[Sequence[float]] = None) -> Dict[str, float]:
    """Canonical ensemble of a finite level system: Z, U, S, F, Cv (Gibbs 1902).
    F = -kT ln Z; U = <E>; S = (U - F)/T = -k sum p ln p; Cv = Var(E)/(k T^2).

    :param energies: energy levels
    :param T: temperature in kelvin
    :param kB: Boltzmann constant in the energy unit per kelvin
    :param degeneracy: g_i for each level; None means 1 each
    :returns: dict with Z, lnZ, U, F, S, Cv, p
    """
    beta = 1.0 / (kB * T)
    g = degeneracy or [1.0] * len(energies)
    e0 = min(energies)
    w = [gi * math.exp(-beta * (e - e0)) for gi, e in zip(g, energies)]
    zr = math.fsum(w)
    p = [x / zr for x in w]
    U = math.fsum(pi * e for pi, e in zip(p, energies))
    var = math.fsum(pi * (e - U) ** 2 for pi, e in zip(p, energies))
    lnZ = math.log(zr) - beta * e0
    F = -kB * T * lnZ
    return {'Z': math.exp(lnZ) if lnZ < 700 else math.inf, 'lnZ': lnZ, 'U': U, 'F': F, 'S': (U - F) / T,
            'Cv': var / (kB * T * T), 'p': p}


def softmax(xs: Sequence[float], temperature: float = 1.0) -> List[float]:
    """softmax IS the canonical ensemble with E = -x, kT = temperature: low T concentrates on the
    largest (saturated), high T spreads towards uniform (diluted).

    :param xs: scores
    :param temperature: temperature; 1 is the usual softmax
    :returns: probabilities, list, summing to 1
    """
    return boltzmann_probs([-x for x in xs], 1.0 / temperature)


def fermi_dirac(E: float, mu: float, T: float, kB: float = K_B) -> float:
    """Fermi-Dirac occupation of a level.

    :param E: level energy
    :param mu: chemical potential
    :param T: temperature in kelvin
    :param kB: Boltzmann constant
    :returns: occupation in [0, 1]
    """
    x = (E - mu) / (kB * T)
    return 1.0 / (math.exp(x) + 1.0) if x < 700 else 0.0


def bose_einstein(E: float, mu: float, T: float, kB: float = K_B) -> float:
    """Bose-Einstein occupation of a level (needs E > mu).

    :param E: level energy
    :param mu: chemical potential
    :param T: temperature in kelvin
    :param kB: Boltzmann constant
    :returns: mean occupation, float
    """
    x = (E - mu) / (kB * T)
    return 1.0 / math.expm1(x)


def maxwell_boltzmann_speed_pdf(v: float, m: float, T: float, kB: float = K_B) -> float:
    """Maxwell-Boltzmann probability density of the speed of a gas particle.

    :param v: speed in m/s
    :param m: particle mass in kg
    :param T: temperature in kelvin
    :param kB: Boltzmann constant
    :returns: density per m/s, float
    """
    a = m / (2 * math.pi * kB * T)
    return 4 * math.pi * a ** 1.5 * v * v * math.exp(-m * v * v / (2 * kB * T))


def planck_spectral_radiance(nu: float, T: float) -> float:
    """Planck's law: black-body spectral radiance per unit frequency.

    :param nu: frequency in Hz
    :param T: temperature in kelvin
    :returns: radiance in W sr^-1 m^-2 Hz^-1
    """
    return 2 * H_PLANCK * nu ** 3 / C_LIGHT ** 2 / math.expm1(H_PLANCK * nu / (K_B * T))


def two_level(eps: float, T: float, kB: float = K_B) -> Dict[str, float]:
    """Canonical ensemble of a two-level system with levels 0 and eps.

    :param eps: level spacing
    :param T: temperature in kelvin
    :param kB: Boltzmann constant
    :returns: dict as for canonical
    """
    return canonical([0.0, eps], T, kB)


def harmonic_oscillator(omega: float, T: float, hbar: float = H_PLANCK / (2 * math.pi),
                        kB: float = K_B, levels: int = 400) -> Dict[str, float]:
    """Canonical ensemble of a quantum harmonic oscillator, levels hbar omega (n + 1/2), truncated.

    :param omega: angular frequency in rad/s
    :param T: temperature in kelvin
    :param hbar: reduced Planck constant
    :param kB: Boltzmann constant
    :param levels: number of levels kept
    :returns: dict as for canonical
    """
    return canonical([hbar * omega * (n + 0.5) for n in range(levels)], T, kB)


def ising_1d(N: int, J: float, h: float, beta: float) -> Dict[str, float]:
    """1-D Ising ring, exact by transfer matrix (Kramers-Wannier 1941): Z = l+^N + l-^N.

    :param N: number of spins on the ring
    :param J: coupling
    :param h: external field
    :param beta: inverse temperature
    :returns: dict with Z, lambda_plus, lambda_minus, free_energy_per_spin
    """
    bJ, bh = beta * J, beta * h
    a = math.exp(bJ) * math.cosh(bh)
    disc = math.sqrt(math.exp(2 * bJ) * math.sinh(bh) ** 2 + math.exp(-2 * bJ))
    lp, lm = a + disc, a - disc
    Z = lp ** N + lm ** N
    return {'Z': Z, 'lambda_plus': lp, 'lambda_minus': lm, 'free_energy_per_spin': -math.log(Z) / (beta * N)}


def ising_1d_bruteforce(N: int, J: float, h: float, beta: float) -> float:
    """The same partition function as ising_1d by summing all 2^N configurations; the check, and only practical for small N.

    :param N: number of spins on the ring
    :param J: coupling
    :param h: external field
    :param beta: inverse temperature
    :returns: Z, float
    """
    Z = 0.0
    for conf in range(1 << N):
        s = [1 if (conf >> i) & 1 else -1 for i in range(N)]
        e = -J * sum(s[i] * s[(i + 1) % N] for i in range(N)) - h * sum(s)
        Z += math.exp(-beta * e)
    return Z


# ═══════════════════════════ 13  CIRCULAR ═════════════════════════════════
def circ_mean(angles: Sequence[float], weights: Optional[Sequence[float]] = None) -> float:
    """Mean direction of angles on a circle.

    :param angles: angles in radians
    :param weights: weight of each angle; None means equal
    :returns: mean direction in (-pi, pi]
    """
    w = weights or [1.0] * len(angles)
    return math.atan2(math.fsum(wi * math.sin(a) for wi, a in zip(w, angles)),
                      math.fsum(wi * math.cos(a) for wi, a in zip(w, angles)))


def circ_R(angles: Sequence[float], weights: Optional[Sequence[float]] = None) -> float:
    """Mean resultant length in [0,1]: 1 = all one direction, 0 = uniformly spread.

    :param angles: angles in radians
    :param weights: weight of each angle; None means equal
    :returns: R in [0, 1]
    """
    w = weights or [1.0] * len(angles)
    s = math.fsum(w)
    return math.hypot(math.fsum(wi * math.sin(a) for wi, a in zip(w, angles)),
                      math.fsum(wi * math.cos(a) for wi, a in zip(w, angles))) / s


def circ_var(angles: Sequence[float]) -> float:
    """Circular variance, 1 - R.

    :param angles: angles in radians
    :returns: variance in [0, 1]
    """
    return 1.0 - circ_R(angles)


def circ_std(angles: Sequence[float]) -> float:
    """Circular standard deviation sqrt(-2 ln R); infinite when R = 0.

    :param angles: angles in radians
    :returns: standard deviation in radians
    """
    R = circ_R(angles)
    return math.sqrt(-2.0 * math.log(R)) if R > 0 else math.inf


def bessel_i0(x: float) -> float:
    """Modified Bessel function of the first kind, order 0, by its power series.

    :param x: the argument
    :returns: I0(x), float
    """
    s, t = 1.0, 1.0
    for k in range(1, 500):
        t *= (x / (2 * k)) ** 2
        s += t
        if t < s * 1e-17:
            break
    return s


def von_mises_pdf(theta: float, mu: float, kappa: float) -> float:
    """Von Mises density, the circular analogue of the normal.

    :param theta: the angle in radians
    :param mu: mean direction
    :param kappa: concentration (0 is uniform)
    :returns: density at theta, float
    """
    return math.exp(kappa * math.cos(theta - mu)) / (2 * math.pi * bessel_i0(kappa))


def rayleigh_test(angles: Sequence[float]) -> Dict[str, float]:
    """Rayleigh test of uniformity on the circle (Zar 1999 approximation).

    :param angles: angles in radians
    :returns: dict with R, Z, p, mean_direction
    """
    n = len(angles)
    R = circ_R(angles)
    Rn = n * R
    p = math.exp(math.sqrt(1 + 4 * n + 4 * (n * n - Rn * Rn)) - (1 + 2 * n))
    return {'R': R, 'Z': Rn * Rn / n, 'p': min(1.0, p), 'mean_direction': circ_mean(angles)}


# ═══════════════════════════ SELF-CHECK ═══════════════════════════════════
def verify_known_values() -> Dict[str, bool]:
    """Spot-checks against exact or tabulated values; the full cross-check against scipy is
    Testing/test_bell_curve.py."""
    return {
        'norm_cdf(1.96)': abs(norm_cdf(1.96) - 0.9750021048517795) < 1e-12,
        'norm_ppf(0.975)': abs(norm_ppf(0.975) - 1.959963984540054) < 1e-12,
        'three_sigma_p': abs(sigma_to_p(3.0) - 0.002699796063260207) < 1e-14,
        'six_sigma_dpmo': abs(sigma_to_dpmo(6.0) - 3.3976731247300535) < 1e-9,
        'chi2_crit_1df_95': abs(chi2_ppf(0.95, 1) - 3.841458820694124) < 1e-9,
        't_crit_10df_975': abs(t_ppf(0.975, 10) - 2.2281388519649385) < 1e-9,
        'ising_matches_bruteforce': abs(ising_1d(8, 1.0, 0.3, 0.7)['Z'] - ising_1d_bruteforce(8, 1.0, 0.3, 0.7)) < 1e-8,
        'softmax_is_canonical': abs(softmax([1, 2, 3], 1.0)[2] - 0.6652409557748219) < 1e-12,
    }
