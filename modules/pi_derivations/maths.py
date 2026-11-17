"""
ValaQuenta.modules.pi_derivations.maths
=======================================
THE PI DERIVATION TOOLSET. Every route to π the project meets, each as a function that
computes π from its own inputs WITHOUT reading ``math.pi`` (the constant appears only in the
comparison column). Each route carries a ``circle_in`` label: what, if anything, of a circle
is already present in the route's inputs.

Cody's rule (2026-11-16): a circle causes π to be found, one way or another. The π that DEFINES
a circle is the emergent π: ``cos_zero`` below (π = twice the first positive zero of the cosine
power series; no diameter, circumference or construction). Every other route is kept beside it
and classified, so that "literal π everywhere" can be searched for and each place where the
circle was already in the inputs is on the record.

``circle_in`` values::

    none         no circle, angle or periodic object in the inputs (series, products, integrals of exp)
    orbit        a flow that closes (the circle arrives as the orbit, e.g. x'' = -x)
    constructed  the circle or a polygon in it is drawn first (Archimedes, Monte Carlo)
    dual         the circle group U(1) or its dual (the integers) is the setting (Basel via sin, Parseval)
    path         a closed curve that is NOT a circle (a square) whose winding is counted (Cauchy residue)
    library      a library special function whose own definition is not shown here (Gamma)
    identity     not a derivation: holds for any value of π (e.g. (2/π)·π = 2)

Version: 0.1
"""
import math
from decimal import Decimal, getcontext
from typing import Any, Callable, Dict, List

_REF = math.pi            # comparison only; no route below reads it


def _err(v: float) -> float:
    return abs(v - _REF)


def cos_zero(tol: float = 1e-15) -> float:
    """
    The emergent π: twice the first positive zero of cos, with cos defined only by its power series.

    :param tol: bisection tolerance on the zero
    :type tol: float
    :returns: π as a float
    :rtype: float
    """
    def cos_series(x):
        term, s, k = 1.0, 1.0, 0
        while abs(term) > 1e-18:
            k += 2
            term *= -x * x / ((k - 1) * k)
            s += term
        return s
    lo, hi = 1.0, 2.0                      # cos(1) > 0 > cos(2) by the series itself
    while hi - lo > tol:
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if cos_series(mid) > 0 else (lo, mid)
    return 2 * (lo + hi) / 2


def oscillator_period(dt: float = 1e-4) -> float:
    """
    π from the closing time of the flow x'' = -x, x(0)=1, x'(0)=0 (RK4): half the period.

    :param dt: step
    :type dt: float
    :returns: π as a float
    :rtype: float
    """
    x, v, t = 1.0, 0.0, 0.0

    def f(x, v): return v, -x
    while True:
        k1 = f(x, v); k2 = f(x + dt / 2 * k1[0], v + dt / 2 * k1[1])
        k3 = f(x + dt / 2 * k2[0], v + dt / 2 * k2[1]); k4 = f(x + dt * k3[0], v + dt * k3[1])
        xn = x + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); vn = v + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        if xn <= 0:
            t_zero = t + dt * x / (x - xn)       # linear interpolation of the first zero of x
            return 2 * t_zero
        x, v, t = xn, vn, t + dt


def archimedes(doublings: int = 20) -> float:
    """
    Perimeter of the inscribed regular polygon, starting at the hexagon, sides doubled with square roots only.

    :param doublings: number of side doublings
    :type doublings: int
    :returns: half the perimeter of the unit circle's inscribed polygon (π from below)
    :rtype: float
    """
    # stable form of the side-doubling recurrence: s_{2n} = s / sqrt(2 + sqrt(4 - s^2))
    s, n = 1.0, 6
    for _ in range(doublings):
        s = s / math.sqrt(2 + math.sqrt(4 - s * s)); n *= 2
    return n * s / 2


def gregory_leibniz(terms: int = 2_000_000) -> float:
    """
    π/4 = 1 − 1/3 + 1/5 − …  (the arctangent series at 1), averaged over the last two partial sums.

    :param terms: number of terms
    :type terms: int
    :returns: π as a float
    :rtype: float
    """
    s, prev = 0.0, 0.0
    for k in range(terms):
        prev = s; s += (-1.0) ** k / (2 * k + 1)
    return 4 * (s + prev) / 2


def machin(terms: int = 30) -> float:
    """
    π/4 = 4 arctan(1/5) − arctan(1/239), each arctangent by its own power series.

    :param terms: series terms per arctangent
    :type terms: int
    :returns: π as a float
    :rtype: float
    """
    def at(x):
        return sum((-1) ** k * x ** (2 * k + 1) / (2 * k + 1) for k in range(terms))
    return 4 * (4 * at(1 / 5) - at(1 / 239))


def madhava(terms: int = 30) -> float:
    """
    π = √12 · Σ (−1/3)^k / (2k+1).

    :param terms: number of terms
    :type terms: int
    :returns: π as a float
    :rtype: float
    """
    return math.sqrt(12) * sum((-1 / 3) ** k / (2 * k + 1) for k in range(terms))


def wallis(terms: int = 2_000_000) -> float:
    """
    π/2 = ∏ (2k)²/((2k−1)(2k+1)).

    :param terms: number of factors
    :type terms: int
    :returns: π as a float
    :rtype: float
    """
    p = 1.0
    for k in range(1, terms + 1):
        p *= (2.0 * k) ** 2 / ((2.0 * k - 1) * (2.0 * k + 1))
    return 2 * p


def viete(factors: int = 40) -> float:
    """
    2/π = ∏ cos(π/2^(k+1)) written with nested square roots only: √(1/2)·√(1/2+½√(1/2))·…

    :param factors: number of factors
    :type factors: int
    :returns: π as a float
    :rtype: float
    """
    a, prod = 0.0, 1.0
    for _ in range(factors):
        a = math.sqrt(2 + a); prod *= a / 2
    return 2 / prod


def basel(terms: int = 2_000_000) -> float:
    """
    π = √(6 Σ 1/n²) with the 1/N tail added.

    :param terms: number of terms
    :type terms: int
    :returns: π as a float
    :rtype: float
    """
    s = sum(1.0 / (n * n) for n in range(terms, 0, -1)) + 1.0 / terms - 1.0 / (2 * terms * terms)
    return math.sqrt(6 * s)


def _primes(n: int) -> List[int]:
    sieve = bytearray([1]) * (n + 1); sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(n + 1) if sieve[i]]


def euler_product(limit: int = 2_000_000) -> float:
    """
    π = √(6 ∏_p (1 − p⁻²)⁻¹): Basel through the Euler product over the primes (Telperion side).

    :param limit: largest prime used
    :type limit: int
    :returns: π as a float
    :rtype: float
    """
    prod = 1.0
    for p in _primes(limit):
        prod /= (1 - 1.0 / (p * p))
    return math.sqrt(6 * prod)


def coprime_probability(n: int = 2000) -> float:
    """
    π = √(6/P) where P is the fraction of pairs (a, b) ≤ n with gcd 1.

    :param n: range
    :type n: int
    :returns: π as a float
    :rtype: float
    """
    c = sum(1 for a in range(1, n + 1) for b in range(1, n + 1) if math.gcd(a, b) == 1)
    return math.sqrt(6 * n * n / c)


def gaussian_integral(half_width: float = 9.0, steps: int = 20000) -> float:
    """
    π = (∫ e^{−x²} dx)², trapezoid rule on [−L, L].

    :param half_width: L
    :type half_width: float
    :param steps: number of intervals
    :type steps: int
    :returns: π as a float
    :rtype: float
    """
    h = 2 * half_width / steps
    s = sum(math.exp(-(-half_width + i * h) ** 2) for i in range(1, steps)) + 0.5 * (2 * math.exp(-half_width ** 2))
    return (s * h) ** 2


def gamma_half() -> float:
    """
    π = Γ(½)².

    :returns: π as a float
    :rtype: float
    """
    return math.gamma(0.5) ** 2


def stirling_ratio(n: int = 200000) -> float:
    """
    n! ≈ √(2πn)(n/e)ⁿ: π = ½ (n!/(√n (n/e)ⁿ))² with the 1/(12n) correction removed.

    :param n: n
    :type n: int
    :returns: π as a float
    :rtype: float
    """
    r = math.exp(math.lgamma(n + 1) - 0.5 * math.log(n) - n * (math.log(n) - 1))
    r /= (1 + 1 / (12 * n))
    return r * r / 2


def gauss_legendre(iterations: int = 4) -> float:
    """
    The arithmetic–geometric mean route (Gauss–Legendre): quadratic convergence.

    :param iterations: AGM iterations
    :type iterations: int
    :returns: π as a float
    :rtype: float
    """
    a, b, t, p = 1.0, 1 / math.sqrt(2), 0.25, 1.0
    for _ in range(iterations):
        an = (a + b) / 2; b = math.sqrt(a * b); t -= p * (a - an) ** 2; a = an; p *= 2
    return (a + b) ** 2 / (4 * t)


def ramanujan_1_over_pi(terms: int = 3) -> float:
    """
    Ramanujan (1914): 1/π = (2√2/9801) Σ (4k)!(1103+26390k)/((k!)⁴ 396^{4k}) (modular-form route).

    :param terms: number of terms
    :type terms: int
    :returns: π as a float
    :rtype: float
    """
    s = sum(math.factorial(4 * k) * (1103 + 26390 * k) / (math.factorial(k) ** 4 * 396 ** (4 * k)) for k in range(terms))
    return 1 / (2 * math.sqrt(2) / 9801 * s)


def chudnovsky(digits: int = 60) -> str:
    """
    The Chudnovsky series (14 digits per term), in decimal arithmetic.

    :param digits: digits wanted
    :type digits: int
    :returns: π as a decimal string
    :rtype: str
    """
    getcontext().prec = digits + 10
    C = 426880 * Decimal(10005).sqrt(); M, L, X, K, S = 1, 13591409, 1, 6, Decimal(13591409)
    for q in range(1, digits // 14 + 2):
        M = M * (K ** 3 - 16 * K) // q ** 3; L += 545140134; X *= -262537412640768000; S += Decimal(M * L) / X; K += 12
    return str(+(C / S))[:digits + 1]


def bbp_digit_sum(terms: int = 12) -> float:
    """
    Bailey–Borwein–Plouffe: π = Σ 16⁻ᵏ (4/(8k+1) − 2/(8k+4) − 1/(8k+5) − 1/(8k+6)).

    :param terms: number of terms
    :type terms: int
    :returns: π as a float
    :rtype: float
    """
    return sum(16.0 ** -k * (4 / (8 * k + 1) - 2 / (8 * k + 4) - 1 / (8 * k + 5) - 1 / (8 * k + 6)) for k in range(terms))


def grid_circle_area(n: int = 3000) -> float:
    """
    Monte-Carlo's deterministic twin: count grid points with x² + y² < 1 (the circle is the test), scaled.

    :param n: grid points per axis
    :type n: int
    :returns: π as a float
    :rtype: float
    """
    h = 2.0 / n; cnt = 0
    for i in range(n):
        x = -1 + (i + 0.5) * h
        w = 1 - x * x
        cnt += sum(1 for j in range(n) if (-1 + (j + 0.5) * h) ** 2 < w)
    return cnt * h * h


def residue_square(steps: int = 40000) -> float:
    """
    Im ∮ dz/z around the SQUARE |Re z|,|Im z| = 1 (not a circle): the winding is 2π, so half of it is π.

    :param steps: number of segments on the whole path
    :type steps: int
    :returns: π as a float
    :rtype: float
    """
    corners = [1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j, 1 + 1j]
    per = steps // 4; total = 0j
    for a, b in zip(corners[:-1], corners[1:]):
        for k in range(per):
            z0 = a + (b - a) * k / per; z1 = a + (b - a) * (k + 1) / per
            zm = (z0 + z1) / 2
            total += (z1 - z0) / zm
    return total.imag / 2


def cardioid_area(points: int = 20000) -> float:
    """
    π from the area of the main-cardioid boundary c(μ) = μ/2 − μ²/4, |μ| = 1 (shoelace sum): area = 3π/8.

    :param points: number of boundary samples
    :type points: int
    :returns: π as a float
    :rtype: float
    """
    cs = math.cos; sn = math.sin
    # the unit circle is sampled by the project's own emergent π
    two_pi = 2 * cos_zero()
    pts = []
    for k in range(points):
        a = two_pi * k / points; mu = complex(cs(a), sn(a))
        pts.append(mu / 2 - mu * mu / 4)
    area = 0.5 * sum(pts[k].real * pts[(k + 1) % points].imag - pts[(k + 1) % points].real * pts[k].imag for k in range(points))
    return 8 * area / 3


def smith_arc_length(steps: int = 200000) -> float:
    """
    π from the Smith-chart map Γ = (z−1)/(z+1): the imaginary axis maps onto the unit circle, and
    ∫ dy/(1+y²) over the whole axis is π (arc length of Γ(iy) is 2/(1+y²) dy, a full turn = 2π).

    :param steps: number of intervals in the substitution y = tan(u)-free uniform grid on [−Y, Y]
    :type steps: int
    :returns: π as a float
    :rtype: float
    """
    Y = 2000.0; h = 2 * Y / steps; tot = 0.0
    for i in range(steps):
        y0 = -Y + i * h; y1 = y0 + h; ym = (y0 + y1) / 2
        g0 = (complex(0, y0) - 1) / (complex(0, y0) + 1); g1 = (complex(0, y1) - 1) / (complex(0, y1) + 1)
        tot += abs(g1 - g0)
    return tot / 2 + 2 / Y        # half the turn, plus the arc beyond ±Y (2 arctan tail ≈ 2/Y per side, halved)


def jacobi_conjugate_point(n: int = 400) -> float:
    """
    π from the Lagrangian L = ½ẋ² − ½x²: the discrete stationary-action boundary problem on [0, T] becomes singular
    (a conjugate point: the stationary path stops being unique) first at T = π. Bisection on the sign of the determinant.

    :param n: number of interior grid points
    :type n: int
    :returns: π as a float
    :rtype: float
    """
    import numpy as np

    def det(T):
        h = T / (n + 1)
        A = (np.diag(np.full(n, 2.0)) - np.diag(np.ones(n - 1), 1) - np.diag(np.ones(n - 1), -1)) / h ** 2 - np.eye(n)
        return np.linalg.slogdet(A)[0]
    lo, hi = 2.0, 4.0
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if det(mid) > 0 else (lo, mid)
    return (lo + hi) / 2


def sedenion_exp_period(axis: int = 15) -> float:
    """
    π from inside the sedenion: exp(θ e_axis) built by its power series with the project's own Cayley–Dickson product;
    twice the first positive zero of the real part is π (the circle exists in every imaginary direction).

    :param axis: imaginary axis 1..15
    :type axis: int
    :returns: π as a float
    :rtype: float
    """
    import numpy as np
    from ..tier8_sedenion.maths import cd_mul
    u = np.zeros(16); u[axis] = 1.0

    def re_exp(theta):
        term = np.zeros(16); term[0] = 1.0; tot = term.copy()
        for k in range(1, 40):
            term = cd_mul(term, theta * u) / k
            tot = tot + term
        return tot[0]
    lo, hi = 1.0, 2.0
    for _ in range(45):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if re_exp(mid) > 0 else (lo, mid)
    return (lo + hi)


def ring_eigenvalue(n: int = 2000, circumference: float = 1.0) -> float:
    """
    π from a ring: the lowest non-zero eigenvalue of the periodic second difference on n points around a ring of given
    circumference is (2π/L)²; the matrix is built without π, the eigenvalue is found numerically.

    :param n: points on the ring
    :type n: int
    :param circumference: L
    :type circumference: float
    :returns: π as a float
    :rtype: float
    """
    import numpy as np
    h = circumference / n
    A = 2 * np.eye(n) - np.eye(n, k=1) - np.eye(n, k=-1); A[0, -1] = A[-1, 0] = -1
    lam = np.sort(np.linalg.eigvalsh(A / h ** 2))
    return float(circumference * math.sqrt(lam[1]) / 2)


def u1_normalisation() -> float:
    """
    (2/π)·π = 2: the project's U(1) normalisation. Holds for ANY value of π, so it derives nothing.

    :returns: nan (no value is produced)
    :rtype: float
    """
    return float("nan")


# id -> (function, name, circle_in, what the route needs, tier)
ROUTES: Dict[str, Dict[str, Any]] = {
    "cos_zero":           dict(fn=cos_zero, name="First zero of the cosine power series (π/2)", circle_in="none", tier="ESTABLISHED",
                               needs="the power series of cos, nothing geometric. THE EMERGENT π: it defines the circle's period before any circle is drawn."),
    "oscillator_period":  dict(fn=oscillator_period, name="Closing time of x'' = −x (Hamiltonian / Lagrangian orbit)", circle_in="orbit", tier="ESTABLISHED",
                               needs="a flow; the circle is the orbit it closes on, with no radius given"),
    "archimedes":         dict(fn=archimedes, name="Archimedes: inscribed polygon, sides doubled", circle_in="constructed", tier="ESTABLISHED",
                               needs="a circle drawn first, then polygons inside it"),
    "gregory_leibniz":    dict(fn=gregory_leibniz, name="Gregory–Leibniz: arctan(1) series", circle_in="none", tier="ESTABLISHED", needs="the arctangent power series"),
    "machin":             dict(fn=machin, name="Machin: 4 arctan(1/5) − arctan(1/239)", circle_in="none", tier="ESTABLISHED", needs="the arctangent power series"),
    "madhava":            dict(fn=madhava, name="Madhava: √12 Σ (−1/3)^k/(2k+1)", circle_in="none", tier="ESTABLISHED", needs="the arctangent series at 1/√3"),
    "wallis":             dict(fn=wallis, name="Wallis product", circle_in="none", tier="ESTABLISHED", needs="products of rationals"),
    "viete":              dict(fn=viete, name="Viète: nested square roots", circle_in="constructed", tier="ESTABLISHED", needs="half-angle cosines (polygons) behind the radicals"),
    "basel":              dict(fn=basel, name="Basel: ζ(2) = π²/6", circle_in="dual", tier="ESTABLISHED", needs="the integers as the dual of U(1); sin zeros at the integers"),
    "euler_product":      dict(fn=euler_product, name="Basel through the Euler product over primes (Telperion)", circle_in="dual", tier="ESTABLISHED", needs="primes; the value comes with ζ(2)"),
    "coprime_probability": dict(fn=coprime_probability, name="Probability that two integers are coprime = 6/π²", circle_in="dual", tier="ESTABLISHED", needs="integers only, via ζ(2)"),
    "gaussian_integral":  dict(fn=gaussian_integral, name="(∫e^{−x²}dx)² = π", circle_in="none", tier="ESTABLISHED", needs="a real integral of exp; the usual proof uses polar coordinates, the number does not"),
    "gamma_half":         dict(fn=gamma_half, name="Γ(½)² = π", circle_in="library", tier="ESTABLISHED", needs="the Gamma function"),
    "stirling_ratio":     dict(fn=stirling_ratio, name="Stirling: n! ≈ √(2πn)(n/e)ⁿ", circle_in="none", tier="ESTABLISHED", needs="factorials (the constant comes from Wallis)"),
    "gauss_legendre":     dict(fn=gauss_legendre, name="Gauss–Legendre arithmetic–geometric mean", circle_in="none", tier="ESTABLISHED", needs="square roots and means; the elliptic integral K behind it"),
    "ramanujan":          dict(fn=ramanujan_1_over_pi, name="Ramanujan's 1/π series (modular forms)", circle_in="none", tier="ESTABLISHED", needs="factorials; singular moduli of modular forms behind it"),
    "chudnovsky":         dict(fn=chudnovsky, name="Chudnovsky series (14 digits per term)", circle_in="none", tier="ESTABLISHED", needs="factorials and √10005"),
    "bbp":                dict(fn=bbp_digit_sum, name="Bailey–Borwein–Plouffe (hexadecimal digits)", circle_in="none", tier="ESTABLISHED", needs="rationals"),
    "grid_circle_area":   dict(fn=grid_circle_area, name="Area of the unit disc by counting a grid", circle_in="constructed", tier="ESTABLISHED", needs="the circle as the counting test"),
    "residue_square":     dict(fn=residue_square, name="Cauchy residue: ∮dz/z around a SQUARE", circle_in="path", tier="ESTABLISHED", needs="a closed loop of any shape around 0; no circle"),
    "cardioid_area":      dict(fn=cardioid_area, name="Area of the main cardioid c(μ) = μ/2 − μ²/4 = 3π/8", circle_in="constructed", tier="ESTABLISHED", needs="the unit circle of multipliers, sampled; the cardioid is its image"),
    "smith_arc_length":   dict(fn=smith_arc_length, name="Smith chart: arc length of Γ(iy), the line becomes the circle", circle_in="path", tier="ESTABLISHED", needs="a Möbius map of a straight line; the circle appears as its image"),
    "jacobi_conjugate_point": dict(fn=jacobi_conjugate_point, name="Lagrangian: first conjugate point of L = ½ẋ² − ½x² at T = π", circle_in="orbit", tier="ESTABLISHED", needs="the action's second variation; no circle, no angle"),
    "sedenion_exp_period": dict(fn=sedenion_exp_period, name="exp(θ·e₁₅) in the sedenion, first return to −1", circle_in="none", tier="ESTABLISHED", needs="the Cayley–Dickson product and the exponential series; a circle in every imaginary direction"),
    "ring_eigenvalue":    dict(fn=ring_eigenvalue, name="Lowest eigenvalue of the periodic second difference on a ring", circle_in="constructed", tier="ESTABLISHED", needs="periodic boundary conditions (the ring), no angle"),
    "u1_normalisation":   dict(fn=u1_normalisation, name="(2/π)·π = 2 (the project's U(1) normalisation)", circle_in="identity", tier="OPEN", needs="nothing: an identity for any value of π, not a derivation"),
}


def derive(name: str, **kw) -> Dict[str, Any]:
    """
    Run one route and report value, error against ``math.pi`` and the circle classification.

    :param name: a key of ``ROUTES``
    :type name: str
    :param kw: parameters passed to the route
    :returns: dict with value, error, circle_in, needs, tier
    :rtype: dict
    """
    r = ROUTES[name]
    v = r["fn"](**kw)
    if isinstance(v, str):
        err = abs(Decimal(v) - Decimal("3.14159265358979323846264338327950288419716939937510582097494459"[:len(v)]))
        err = float(err)
    else:
        err = _err(v) if v == v else float("nan")
    return {"id": name, "name": r["name"], "value": v, "error": err, "circle_in": r["circle_in"], "needs": r["needs"], "tier": r["tier"]}


def all_routes() -> List[Dict[str, Any]]:
    """
    Run every route with its default parameters.

    :returns: one result dict per route, in registry order
    :rtype: list
    """
    return [derive(k) for k in ROUTES]


def circle_audit() -> Dict[str, Any]:
    """
    Group the routes by what of the circle their inputs already contain.

    :returns: dict of circle_in label -> list of route ids
    :rtype: dict
    """
    out: Dict[str, List[str]] = {}
    for k, r in ROUTES.items():
        out.setdefault(r["circle_in"], []).append(k)
    return out


def emergent_pi() -> Dict[str, Any]:
    """
    The emergent π (cos_zero) with its disclosure: what it was computed from.

    :returns: dict with value, error and the inputs statement
    :rtype: dict
    """
    d = derive("cos_zero")
    d["inputs"] = "the power series cos x = Σ (−1)^k x^{2k}/(2k)! and bisection; no diameter, circumference, angle or polygon"
    return d


def verify() -> Dict[str, Any]:
    """
    Self-checks: every route that claims a value lands within its stated tolerance; the identity route is flagged.

    :returns: dict of check name -> measured value or bool
    :rtype: dict
    """
    tol = {"cos_zero": 1e-13, "oscillator_period": 1e-6, "archimedes": 1e-9, "gregory_leibniz": 1e-5, "machin": 1e-13, "madhava": 1e-13,
           "wallis": 1e-5, "viete": 1e-12, "basel": 1e-6, "euler_product": 1e-6, "coprime_probability": 5e-3, "gaussian_integral": 1e-9,
           "gamma_half": 1e-12, "stirling_ratio": 1e-8, "gauss_legendre": 1e-12, "ramanujan": 1e-12, "bbp": 1e-12,
           "grid_circle_area": 1e-3, "residue_square": 1e-3, "cardioid_area": 1e-6,
           "smith_arc_length": 1e-4, "jacobi_conjugate_point": 1e-3, "sedenion_exp_period": 1e-12, "ring_eigenvalue": 1e-5}
    out: Dict[str, Any] = {}
    for k, t in tol.items():
        out[f"{k}: error ≤ {t:g}"] = derive(k)["error"] <= t
    chud = derive("chudnovsky")
    out["chudnovsky: 60 digits"] = chud["error"] < 1e-55
    out["u1_normalisation is an identity (value nan)"] = math.isnan(ROUTES["u1_normalisation"]["fn"]())
    return out
