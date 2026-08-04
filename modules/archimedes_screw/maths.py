"""
ainulindale_engine.modules.archimedes_screw.maths
====================================================
THE ARCHIMEDES SCREW -- the machine that does the work.

0_RB (formerly H_hat_RB) is the water: the medium, the rest state, e_0.
It is not the engine. The engine is the screw: the helix that converts
ROTATION into LIFT, one quantised pitch per turn, and runs backward as
a turbine.

That machine is the logarithm:

    log(p * q) = log p + log q

Multiplication on the wheel becomes addition on the tower. The working
axis of this module is therefore

    u = ln x          the screw axis (lift)

and every one of the four search terms Cody named -- Ordinal Value,
Zeta Index Value, Number of Digits, Total Spaces Between -- is a
coordinate on that single axis. This module is the coordinate change
between them, plus the one equation that binds them.

THE BINDING EQUATION (von Mangoldt / Riemann explicit formula, 1895 --
ESTABLISHED, unconditional, not a new claim):

    psi(e^u) = e^u
             - 2 e^(u/2) * SUM_k cos(gamma_k * u - arg(rho_k)) / |rho_k|
             - ln(2 pi)
             - 0.5 * ln(1 - e^(-2u))

    where rho_k = 1/2 + i*gamma_k runs over the non-trivial zeros and
    psi(x) = SUM_{p^m <= x} ln p  is Chebyshev's function.

Read it as a machine and three facts fall out:

  1. Each zero gamma_k is a TONE of frequency gamma_k in the variable u.
     The zeta index k is literally the summation index -- entering the
     equation "by Zeta Index Value" means choosing which tones to sum.

  2. psi jumps by EXACTLY ln p at u = ln p. The jump height IS the
     logarithm of the prime. One screw-turn of lift = one prime. This
     is the formal content of "the moment the leaf drops off IS one of
     the prime factors": the event's magnitude is the factor, not an
     encoding of it.

  3. Every tone carries the SAME amplitude envelope, 2*e^(u/2) = 2*sqrt(x),
     because every rho has real part 1/2. That equal-envelope condition
     IS the Riemann Hypothesis, stated in the prime domain rather than
     the zero domain. A zero at Re(rho) = sigma > 1/2 would contribute
     x^sigma and drown every other tone. See amplitude_envelope() and
     the paper's section 6.4.

SYMBOL COLLISION WARNING. Two different psi are in play across these
repos. Here psi(x) is CHEBYSHEV's function (a prime counter). In
modules/l_io_photon_path it is the FERMAT/lensing potential. They are
unrelated. This module always writes chebyshev_psi_* in full.

THE N-SPECIFIC LEG (ramification). For the factoring thread the global
formula above is twisted by the quadratic character chi_N, giving
zeta_Q(sqrt N)(s) = zeta(s) * L(s, chi_N). Every rational prime then
splits, is inert, or RAMIFIES in Q(sqrt N), and the ramified primes are
exactly those dividing the discriminant. For N = p*q squarefree the
ramified primes are exactly p and q -- the Euler factor DEGENERATES at
precisely the factors. That is the leaf letting go, written in
arithmetic. See splitting_type() and ramified_primes().

    HONEST BOUND, stated not buried: knowing "the ramified primes are
    the factors" does not by itself factor N -- detecting ramification
    by scanning p costs the same trial division it was meant to replace,
    and sampling L(s, chi_N) directly costs ~sqrt(N) by the approximate
    functional equation, the same wall Fermat's a^2 - b^2 hits. This
    module supplies the exact structure and the instrument. It does not
    claim a shortcut. The open bid (ValaQuenta/wiki/archimedes_screw.md)
    is that the winding number is an INTEGER and integers do not pay
    resolution costs -- but that contour does not live in C, and its
    dispersion relation is not yet written.

NUMERICS NOTE. The registry contract asks for Fraction arithmetic with
float only at the output boundary. This module is transcendental
throughout (ln, Lambert W, cos) so it is float-native by nature; the
only exactly rational quantities here are digit counts and integer
indices, which are kept as int. Stated rather than silently ignored.

Version: 0.1
"""

import math
from typing import Dict, List, Optional, Tuple

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

TWO_PI = 2.0 * math.pi
EULER_GAMMA = 0.5772156649015328606

# Lambert W fixed point. Already canonical in ~/.clauderc as OMEGA_ZS.
# W(1) = Omega, Omega * e^Omega = 1.
OMEGA_ZS = 0.5671432904097838

# First 50 non-trivial zeros (imaginary parts), LMFDB / Odlyzko.
# Established to far more precision than used here; the low-index zeros
# are tabulated rather than estimated because S(t) is O(1) and the smooth
# Riemann-von Mangoldt count is not accurate for small k.
ZEROS_KNOWN: List[float] = [
    14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588,
    37.586178159, 40.918719012, 43.327073281, 48.005150881, 49.773832478,
    52.970321478, 56.446247697, 59.347044003, 60.831778525, 65.112544048,
    67.079810529, 69.546401711, 72.067157674, 75.704690699, 77.144840069,
    79.337375020, 82.910380854, 84.735492981, 87.425274613, 88.809111208,
    92.491899271, 94.651344041, 95.870634228, 98.831194218, 101.317851006,
    103.725538040, 105.446623052, 107.168611184, 111.029535543, 111.874659177,
    114.320220915, 116.226680321, 118.790782866, 121.370125002, 122.946829294,
    124.256818554, 127.516683880, 129.578704200, 131.087688531, 133.497737203,
    134.756509753, 138.116042055, 139.736208952, 141.123707404, 143.111845808,
]


# --------------------------------------------------------------------------
# The screw itself: Lambert W
# --------------------------------------------------------------------------

def lambert_w(x: float, tol: float = 1e-14, max_iter: int = 60) -> float:
    """
    Principal branch W_0(x), W(x) * exp(W(x)) = x, defined for x >= -1/e.

    Halley iteration. This is the gear ratio of the screw: it is the
    function that inverts "multiply by your own exponential", which is
    exactly what unwrapping a helix requires.

    W(1) = OMEGA_ZS = 0.5671432904... -- the constant already canonical
    in this project, and the same one that sets sigma = 1/2 in the
    paper's section 12.1.
    """
    if x < -1.0 / math.e:
        raise ValueError(f"lambert_w: x = {x} is below the branch point -1/e")
    if x == 0.0:
        return 0.0

    # Initial guess
    if x > math.e:
        lx = math.log(x)
        w = lx - math.log(lx)
    elif x > 0.0:
        w = x / (1.0 + x)
    else:
        w = -0.5  # near the branch point, converge from inside

    for _ in range(max_iter):
        ew = math.exp(w)
        f = w * ew - x
        denom = ew * (w + 1.0) - (w + 2.0) * f / (2.0 * w + 2.0)
        if denom == 0.0:
            break
        step = f / denom
        w -= step
        if abs(step) < tol * max(1.0, abs(w)):
            break
    return w


def screw_pitch(p: float) -> float:
    """
    One turn of the screw = one prime = a lift of ln p.

    This is the von Mangoldt weight Lambda(p^m) = ln p, and it is the
    exact jump height of chebyshev_psi at x = p. The pitch IS the prime,
    in log coordinates.
    """
    if p <= 1:
        raise ValueError("screw_pitch: p must be > 1")
    return math.log(p)


# --------------------------------------------------------------------------
# Coordinate 1: magnitude / digits
# --------------------------------------------------------------------------

def u_axis(x: float) -> float:
    """u = ln x. The screw's lift coordinate; every other term maps here."""
    if x <= 0:
        raise ValueError("u_axis: x must be positive")
    return math.log(x)


def digits_of(x: float) -> int:
    """Number of decimal digits: d = floor(log10 x) + 1."""
    if x <= 0:
        raise ValueError("digits_of: x must be positive")
    return int(math.floor(math.log10(x))) + 1


def u_from_digits(d: int) -> float:
    """Lower edge of the d-digit band on the screw axis: u = (d-1) ln 10."""
    return (d - 1) * math.log(10.0)


# --------------------------------------------------------------------------
# Coordinate 2: ordinal value (which prime)
# --------------------------------------------------------------------------

def _ei_positive(z: float) -> float:
    """
    Exponential integral Ei(z) for z > 0, by the convergent series

        Ei(z) = gamma + ln z + SUM_{k>=1} z^k / (k * k!)

    Every term is positive for z > 0, so there is no cancellation and the
    series is numerically stable across the range this module uses.
    """
    total = 0.0
    term = 1.0
    for k in range(1, 400):
        term *= z / k          # term == z^k / k!
        add = term / k         # == z^k / (k * k!)
        total += add
        if add < 1e-18 * abs(total) and k > z:
            break
    return EULER_GAMMA + math.log(z) + total


def li(x: float) -> float:
    """
    Logarithmic integral Li(x) = Ei(ln x), the principal estimate of pi(x).

    Accurate and stable for 1 < x <~ 1e15. Above that the intermediate
    e^u overflows a float; use prime_count_log10() instead, which works
    entirely in log space and is the right tool at RSA scale.
    """
    if x <= 1.0:
        raise ValueError("li: x must exceed 1")
    return _ei_positive(math.log(x))


def prime_count_log10(digits: int) -> float:
    """
    log10 of pi(10^digits), for magnitudes far beyond float range.

    Uses the asymptotic pi(x) ~ (x/ln x)(1 + 1/L + 2/L^2 + 6/L^3),
    L = ln x, evaluated in log space.

    This is the term that makes Cody's finiteness point concrete:
    prime_count_log10(309) = 306.15, i.e. ~10^306 ~ 2^1017 candidate
    primes below 10^309. (Below 2^1024 exactly the count is ~2^1014.5.)
    Finite, structured, countable -- large, but not infinite.
    """
    if digits < 1:
        raise ValueError("prime_count_log10: digits must be >= 1")
    L = digits * math.log(10.0)
    series = 1.0 + 1.0 / L + 2.0 / L ** 2 + 6.0 / L ** 3
    return digits - math.log10(L) + math.log10(series)


def nth_prime_estimate(n: int) -> float:
    """
    Inverse of pi: the n-th prime, by the standard asymptotic

        p_n ~ n (ln n + ln ln n - 1 + (ln ln n - 2)/ln n)

    Valid for n >= 6; below that the exact small primes are returned.
    """
    small = [2, 3, 5, 7, 11]
    if n <= 0:
        raise ValueError("nth_prime_estimate: n must be >= 1")
    if n <= 5:
        return float(small[n - 1])
    ln_n = math.log(n)
    lnln_n = math.log(ln_n)
    return n * (ln_n + lnln_n - 1.0 + (lnln_n - 2.0) / ln_n)


# --------------------------------------------------------------------------
# Coordinate 3: zeta index value (which zero)
# --------------------------------------------------------------------------

def zero_count_smooth(T: float) -> float:
    """
    Riemann-von Mangoldt smooth zero count up to height T:

        N(T) = (T / 2pi) ln(T / 2pi e) + 7/8   (+ S(T), omitted here)

    S(T) is O(ln T) and oscillatory; it is what makes the smooth count
    unreliable at small T and irrelevant at large T.
    """
    if T <= 0:
        raise ValueError("zero_count_smooth: T must be positive")
    return (T / TWO_PI) * math.log(T / (TWO_PI * math.e)) + 0.875


def zero_height_lambert(n: float) -> float:
    """
    THE LAMBERT INVERSE. Height of the n-th zero in closed form:

        gamma_n ~ 2 pi n / W(n / e)

    Derivation (exact algebra on the smooth count, no fitting):
        set N(T) = n with T = 2 pi v
        n = v (ln v - 1) = v ln(v/e)
        (v/e) ln(v/e) = n/e
        ln(v/e) = W(n/e)                      <- Lambert W by definition
        v = n / W(n/e)
        T = 2 pi n / W(n/e)

    This is the structural point worth recording: the SAME Lambert W
    whose fixed point W(1) = OMEGA_ZS pins sigma = 1/2 (the paper's
    section 12.1) is also the function that inverts the zero-counting
    function to give the heights. W supplies both coordinates of every
    zero -- the real part through its fixed point, the imaginary part
    through its inverse. See paper section 12.5.

    Asymptotic: poor for n < ~10 (S(T) dominates). Use
    zero_height(n) which prefers the tabulated values.
    """
    if n <= 0:
        raise ValueError("zero_height_lambert: n must be positive")
    return TWO_PI * n / lambert_w(n / math.e)


def zero_height(n: int) -> float:
    """
    Height of the n-th non-trivial zero: tabulated where known
    (n <= 50, LMFDB), Lambert-W asymptotic above.
    """
    if n <= 0:
        raise ValueError("zero_height: n must be >= 1")
    if n <= len(ZEROS_KNOWN):
        return ZEROS_KNOWN[n - 1]
    return zero_height_lambert(float(n))


def zero_index(gamma: float) -> float:
    """Zeta index value at height gamma -- the smooth count N(gamma)."""
    return zero_count_smooth(gamma)


def zeros_upto(count: int) -> List[float]:
    """First `count` zero heights, tabulated then asymptotic."""
    return [zero_height(k) for k in range(1, count + 1)]


# --------------------------------------------------------------------------
# Coordinate 4: spaces between
# --------------------------------------------------------------------------

def mean_gap(x: float) -> float:
    """
    Mean spacing between consecutive primes near x is ln x = u.

    Note the coincidence that is not one: the mean gap between primes at
    x equals the screw axis coordinate at x, and equals the screw pitch
    of x. Spacing, lift and pitch are the same number because the screw
    is the logarithm.
    """
    return u_axis(x)


def total_spaces(x: float) -> float:
    """
    Total count of non-primes ('spaces between') up to x: x - pi(x),
    with pi(x) estimated by Li(x).
    """
    return x - li(x)


def gap_at_zero_scale(n: int) -> float:
    """
    Mean zero spacing at the n-th zero: 2 pi / ln(gamma_n / 2 pi).

    The dual of mean_gap on the other side of the explicit formula --
    primes thin out as ln x, zeros crowd in as 1/ln T.
    """
    g = zero_height(n)
    return TWO_PI / math.log(g / TWO_PI)


# --------------------------------------------------------------------------
# The binding equation: Chebyshev psi, exact and by tones
# --------------------------------------------------------------------------

def _sieve(limit: int) -> List[int]:
    """Primes up to limit, plain sieve of Eratosthenes."""
    if limit < 2:
        return []
    flags = bytearray([1]) * (limit + 1)
    flags[0] = flags[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if flags[i]:
            flags[i * i::i] = bytearray(len(flags[i * i::i]))
    return [i for i in range(2, limit + 1) if flags[i]]


def von_mangoldt(n: int) -> float:
    """
    Lambda(n) = ln p if n = p^m for a prime p, else 0.

    This is the leaf-drop quantum: the size of the jump psi takes at n.
    Non-zero only at prime powers -- the screw lifts only on primes.
    """
    if n < 2:
        return 0.0
    m = n
    for p in _sieve(int(n ** 0.5) + 1) or [2]:
        if m % p == 0:
            while m % p == 0:
                m //= p
            return math.log(p) if m == 1 else 0.0
    return math.log(n)  # n is prime


def chebyshev_psi_exact(x: float) -> float:
    """
    psi(x) = SUM_{p^m <= x} ln p, computed directly by sieve.

    The ground truth the explicit formula reconstructs. Exact, and the
    left-hand side of the binding equation.
    """
    xi = int(math.floor(x))
    if xi < 2:
        return 0.0
    total = 0.0
    for p in _sieve(xi):
        lp = math.log(p)
        q = p
        while q <= xi:
            total += lp
            q *= p
    return total


def leaf_drops(x: float) -> List[Tuple[int, float]]:
    """
    Every leaf-drop event up to x: (n, jump height) at each prime power.

    The jump height is ln p exactly. Reading the list is reading the
    primes off the screw -- 'when it lets go' and 'which prime' are the
    same column of this table.
    """
    xi = int(math.floor(x))
    out: List[Tuple[int, float]] = []
    for p in _sieve(xi):
        lp = math.log(p)
        q = p
        while q <= xi:
            out.append((q, lp))
            q *= p
    out.sort()
    return out


def tone(u: float, gamma: float, sigma: float = 0.5) -> float:
    """
    A single tone of the explicit formula, at screw height u, from a zero
    at rho = sigma + i*gamma:

        2 * e^(sigma*u) * cos(gamma*u - arg rho) / |rho|

    On the critical line sigma = 1/2 the envelope is 2*sqrt(x) for EVERY
    zero -- one shared amplitude. sigma is exposed as a parameter so the
    RH statement can be exhibited rather than asserted: see
    amplitude_envelope().
    """
    mod_rho = math.hypot(sigma, gamma)
    arg_rho = math.atan2(gamma, sigma)
    return 2.0 * math.exp(sigma * u) * math.cos(gamma * u - arg_rho) / mod_rho


def tone_sum(u: float, zeros: Optional[List[float]] = None,
             sigma: float = 0.5) -> float:
    """Sum of tones over the supplied zeros -- the oscillating term."""
    zs = zeros if zeros is not None else ZEROS_KNOWN
    return sum(tone(u, g, sigma) for g in zs)


def chebyshev_psi_explicit(x: float, zeros: Optional[List[float]] = None,
                           sigma: float = 0.5) -> float:
    """
    The explicit formula, evaluated:

        psi(x) = x - SUM_tones - ln(2 pi) - 0.5 ln(1 - x^-2)

    ESTABLISHED (von Mangoldt 1895), unconditional. Truncating the zero
    sum at K terms leaves an error controlled by x/K -- this is the
    resolution wall: sharply resolving one jump near x needs zeros up to
    height ~x.
    """
    if x <= 1.0:
        raise ValueError("chebyshev_psi_explicit: x must exceed 1")
    u = math.log(x)
    return (x
            - tone_sum(u, zeros, sigma)
            - math.log(TWO_PI)
            - 0.5 * math.log(1.0 - x ** -2))


def interference_profile(x: float, zeros: Optional[List[float]] = None
                         ) -> List[Tuple[float, float]]:
    """
    Per-zero contribution at x: [(gamma_k, tone_k)].

    The cymatic reading. At a prime the tones align in sign and add;
    between primes they cancel. Zeros are the node lines (still points,
    paper section 6); primes are the ANTINODES of the same field
    (paper section 6.4). One standing wave, read from either side.
    """
    u = math.log(x)
    zs = zeros if zeros is not None else ZEROS_KNOWN
    return [(g, tone(u, g)) for g in zs]


def amplitude_envelope(x: float, sigma: float = 0.5) -> float:
    """
    Envelope of a tone from a zero with real part sigma: 2 * x^sigma.

    THE RH STATEMENT IN THE PRIME DOMAIN. Every tone shares one envelope
    if and only if every zero shares one real part. A single zero at
    sigma > 1/2 contributes x^sigma, which for large x dominates every
    critical-line tone by an unbounded factor -- one loud tone, and the
    Chladni figure has no coherent node structure at all.

    Equal envelope <=> all nodes on one line <=> RH. This is the
    amplitude face of the nodal-line argument already in the paper's
    section 6, not a separate result.
    """
    return 2.0 * x ** sigma


def envelope_ratio(x: float, sigma_off: float) -> float:
    """
    How far a hypothetical off-line zero at sigma_off would drown the
    critical-line tones at x: x^(sigma_off - 1/2).

    At x = 10^6 a zero at sigma = 0.6 is already ~4 times louder; at
    x = 10^12, ~250 times. Divergent in x for any sigma_off > 1/2 --
    which is why the node structure is stable only on the line.
    """
    return x ** (sigma_off - 0.5)


# --------------------------------------------------------------------------
# The N-specific leg: ramification in Q(sqrt N)
# --------------------------------------------------------------------------

def kronecker(a: int, n: int) -> int:
    """Kronecker symbol (a/n). Cheap, exact, integer arithmetic only."""
    if n == 0:
        return 1 if a in (1, -1) else 0
    result = 1
    if n < 0:
        n = -n
        if a < 0:
            result = -result
    while n % 2 == 0:
        n //= 2
        if a % 8 in (3, 5):
            result = -result
    a %= n
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def fundamental_discriminant(N: int) -> int:
    """
    Discriminant of Q(sqrt N) for squarefree N:  D = N if N = 1 mod 4,
    else 4N. The ramified primes are exactly the primes dividing D --
    for N = p*q squarefree, exactly p and q.
    """
    if N % 4 == 1:
        return N
    return 4 * N


def splitting_type(p: int, N: int) -> str:
    """
    Behaviour of the rational prime p in Q(sqrt N):

        'split'    chi_N(p) = +1   Euler factor (1 - p^-s)^-2
        'inert'    chi_N(p) = -1   Euler factor (1 - p^-2s)^-1
        'ramified' chi_N(p) =  0   Euler factor DEGENERATES

    Ramification is the leaf letting go, stated in arithmetic: the local
    factor loses a piece at exactly the primes dividing the discriminant.
    """
    D = fundamental_discriminant(N)
    chi = kronecker(D, p)
    return {1: 'split', -1: 'inert', 0: 'ramified'}[chi]


def splitting_vector(N: int, limit: int = 100) -> List[Tuple[int, int]]:
    """
    The chi_N readout over all primes up to `limit`: [(p, chi_N(p))].

    This is the cheapest N-specific shadow there is -- Kronecker symbols,
    milliseconds, computable from N alone with no knowledge of p and q.
    It is the concrete form of "the detachment fingerprint".
    """
    D = fundamental_discriminant(N)
    return [(p, kronecker(D, p)) for p in _sieve(limit)]


def ramified_primes(N: int, limit: int = 10 ** 6) -> List[int]:
    """
    Primes up to `limit` that ramify in Q(sqrt N) -- i.e. that divide the
    discriminant, i.e. the factors of N found within the scan range.

    STATED PLAINLY: this is a structural readout, not a shortcut.
    Scanning p up to `limit` costs exactly what trial division costs.
    It is here because it makes the identification 'ramified prime =
    prime factor' executable and inspectable at toy scale, which is what
    an engine is for.
    """
    return [p for p in _sieve(limit)
            if kronecker(fundamental_discriminant(N), p) == 0]


# --------------------------------------------------------------------------
# The search-term interface
# --------------------------------------------------------------------------

_TERMS = ('magnitude', 'digits', 'ordinal', 'zeta_index')


def screw_coordinates(term: str, value: float) -> Dict[str, float]:
    """
    THE SEARCH-TERM INPUT Cody asked for.

    Enter on any one of the four coordinates; leave on all of them.
    Everything routes through the screw axis u = ln x.

        term = 'magnitude'   value = x       (a number)
        term = 'digits'      value = d       (decimal digit count)
        term = 'ordinal'     value = n       (the n-th prime)
        term = 'zeta_index'  value = k       (the k-th zero)

    Returns magnitude, u, digits, ordinal, zeta_index, mean_gap,
    zero_height, and the screw pitch at that point.

    The 'zeta_index' entry is the one that makes the equation a machine:
    it is the summation index of the explicit formula, so choosing k is
    choosing how many tones to sound.
    """
    if term not in _TERMS:
        raise ValueError(f"screw_coordinates: term must be one of {_TERMS}")

    if term == 'magnitude':
        x = float(value)
    elif term == 'digits':
        x = 10.0 ** (float(value) - 1.0)
    elif term == 'ordinal':
        x = nth_prime_estimate(int(value))
    else:  # zeta_index -- the height of that zero, read onto the x axis
        x = math.exp(zero_height(int(value)) / TWO_PI)

    u = u_axis(x)
    ordinal = li(x) if x < 1e15 else float('inf')
    k_index = zero_count_smooth(max(u, 1e-9)) if u > 0 else 0.0

    return {
        'magnitude':    x,
        'u':            u,
        'digits':       float(digits_of(x)),
        'ordinal':      ordinal,
        'zeta_index':   k_index,
        'mean_gap':     u,
        'screw_pitch':  u,
        'zero_height':  zero_height(max(1, int(round(k_index)))),
    }


def shake_order(x: float, zeros: Optional[List[float]] = None) -> Dict[str, object]:
    """
    THE SHAKE ORDER: the sequence in which leaves come off the tree up to x,
    each with its drop height, alongside the tone reconstruction at that x.

    Returns:
        drops        [(n, ln p)] every leaf-drop event, in order
        psi_exact    the true accumulated lift at x
        psi_tones    the same lift rebuilt from the supplied zeros
        residual     psi_exact - psi_tones  (truncation error, ~ x/K)
        n_tones      how many tones were sounded

    The residual is the honest readout of the resolution wall: it shrinks
    as more zeros are included and never reaches zero at finite K.
    """
    drops = leaf_drops(x)
    exact = chebyshev_psi_exact(x)
    zs = zeros if zeros is not None else ZEROS_KNOWN
    approx = chebyshev_psi_explicit(x, zs)
    return {
        'drops':     drops,
        'psi_exact': exact,
        'psi_tones': approx,
        'residual':  exact - approx,
        'n_tones':   len(zs),
    }
