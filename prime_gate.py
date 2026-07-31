"""
PrimeGate — the Boundary-Crossing Alarm

The engine's purpose is the alarm itself, not a test of any dataset:
`BoundaryAlarm` fires once per crossing of a boundary condition, blind to
everything except whether the crossing happened. Same primitive whether the
boundary is "is prime" or "reached sigma=1/2" -- the Holcus FIRING signal
(Ainulindale wiki/44) and pi(x) are the same alarm, run on different streams.

  ALARM  pi(x)             — BoundaryAlarm(is_prime) over the integers.
                              Fires once per prime. Blind to spacing by
                              construction: every alarm event is identical
                              regardless of how far the previous prime was.
  GAP    g_n = p_(n+1)-p_n — the interval between alarms. What the alarm
                              alone does not carry (by design, not oversight).
                              A separate query, only pulled in if spacing
                              matters for the task at hand.

Two spirals built on the ALARM channel, kept distinct on purpose:
  ordinal_spiral  T(n)   = n   * e^{i d* ln n}    address = COUNT
                                                    (matches the P1 hash
                                                    convention in monad.py:
                                                    word -> prime -> pi(p)
                                                    ordinal index -> zero)
  value_spiral    T(p_n) = p_n * e^{i d* ln p_n}   address = MAGNITUDE
These are NOT the same curve. Using the ordinal form discards gap information
by the same design choice as the alarm itself.

d* = 0.24600 (BK spectral floor, ValaQuenta/modules/berry_keating/maths.py
D_STAR_SPEC) -- reproduced locally, matching hamiltonian.py's convention of
self-contained top-level engines.

Aside (kept on record, not the point of this engine): an early attempt to
build a "prime curvature spiral" from cumsum(gap_n) telescopes trivially back
to p_n - p_0, and the corrected version (kappa_n=ln(p_n)) is not a true Euler
spiral. See curvature_spiral / is_true_euler_spiral at the bottom -- a side
investigation that happened while building the alarm, not its purpose.
"""

from math import log, cos, sin
from typing import Callable, Dict, List, Sequence, Tuple

D_STAR = 0.24600


def sieve(limit: int) -> List[int]:
    """Primes up to `limit`, plain Eratosthenes sieve. No dependencies."""
    if limit < 2:
        return []
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i::i] = bytearray(len(is_p[i * i::i]))
    return [i for i, v in enumerate(is_p) if v]


class BoundaryAlarm:
    """
    THE ALARM. Fires once per crossing of `boundary_fn`, blind to everything
    else -- magnitude, spacing, direction of approach. This is the reusable
    primitive: pi(x) is BoundaryAlarm(is_prime) scanned over the integers.
    The Holcus "FIRING" signal (wiki/44, computation reaching sigma=1/2) is
    the same primitive scanned over a semantic sigma-trajectory instead.
    """

    def __init__(self, boundary_fn: Callable[[object], bool]):
        self.boundary_fn = boundary_fn
        self.events: List[Tuple[int, object]] = []

    def scan(self, sequence: Sequence) -> List[Tuple[int, object]]:
        """Feed a whole sequence; record every crossing (index, value), in order."""
        self.events = [(i, v) for i, v in enumerate(sequence) if self.boundary_fn(v)]
        return self.events

    def count_at(self, sequence: Sequence, upto: int) -> int:
        """How many crossings have fired by position `upto`."""
        return sum(1 for v in sequence[:upto] if self.boundary_fn(v))


def sigma_half_alarm(trajectory: Sequence[float], eps: float = 1e-6) -> List[Tuple[int, float]]:
    """
    Demonstrates BoundaryAlarm is not prime-specific: fires when a sigma
    trajectory crosses 1/2 -- the Holcus FIRING signal, wiki/44's halting
    reframe ("does it stop HERE, at this depth"), same alarm primitive.
    """
    alarm = BoundaryAlarm(lambda sigma: abs(sigma - 0.5) < eps)
    return alarm.scan(trajectory)


class PrimeGateEngine:
    """
    The prime instantiation of the alarm, plus the gap channel it
    deliberately leaves out.
    """

    def __init__(self, limit: int = 50000, d_star: float = D_STAR):
        self.limit = limit
        self.d_star = d_star
        self.primes = sieve(limit)
        self._prime_set = set(self.primes)

    # ── The alarm ────────────────────────────────────────────────────────

    def gate_alarm(self, x: float) -> int:
        """
        pi(x): how many primes have fired the alarm by x. Gap-blind.
        Fast path (bisection) for an equivalent, slower definition:
        BoundaryAlarm(is_prime).count_at(range(2, x+1), x-1).
        """
        lo, hi = 0, len(self.primes)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.primes[mid] <= x:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def is_prime(self, v: int) -> bool:
        """The boundary condition the alarm fires on."""
        return v in self._prime_set

    def alarm_events(self) -> List[Tuple[int, int]]:
        """(prime, pi(prime)) -- the exact trigger points, in order."""
        return [(p, n + 1) for n, p in enumerate(self.primes)]

    # ── The channel the alarm leaves out ────────────────────────────────

    def gap_channel(self) -> List[int]:
        """g_n = p_(n+1) - p_n -- the interval the alarm alone does not carry."""
        return [b - a for a, b in zip(self.primes, self.primes[1:])]

    def gap_scaling_fit(self) -> Dict[str, float]:
        """
        Least-squares fit of gap_n against ln(p_n). PNT predicts slope ~ 1,
        intercept small: average gap near p is ~ln(p).
        """
        gaps = self.gap_channel()
        xs = [log(p) for p in self.primes[:-1]]
        n = len(xs)
        mean_x = sum(xs) / n
        mean_y = sum(gaps) / n
        cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, gaps))
        var = sum((x - mean_x) ** 2 for x in xs)
        slope = cov / var
        intercept = mean_y - slope * mean_x
        return {'slope': slope, 'intercept': intercept, 'n_gaps': n,
                'pnt_prediction': 'slope ~ 1.0 (average gap near p ~ ln(p))'}

    # ── Two spirals on the ALARM channel ────────────────────────────────

    def ordinal_spiral(self) -> List[Tuple[float, float]]:
        """T(n) = n * e^{i d* ln n} -- address = count. Gap-blind by design."""
        out = []
        for n in range(1, len(self.primes) + 1):
            phase = self.d_star * log(n)
            out.append((n * cos(phase), n * sin(phase)))
        return out

    def value_spiral(self) -> List[Tuple[float, float]]:
        """T(p_n) = p_n * e^{i d* ln p_n} -- address = magnitude."""
        out = []
        for p in self.primes:
            phase = self.d_star * log(p)
            out.append((p * cos(phase), p * sin(phase)))
        return out

    # ── Aside: not the engine's purpose, kept on record ─────────────────

    def curvature_spiral(self, scale: float = 0.002) -> List[Tuple[float, float]]:
        """
        Side investigation from the same session, not an alarm function.
        Heading from genuine curvature accumulation kappa_n = ln(p_n) (NOT
        raw gap_n -- summing gap_n telescopes trivially back to p_n).
        """
        theta = 0.0
        x = y = 0.0
        out = [(0.0, 0.0)]
        for p in self.primes[:-1]:
            theta += log(p) * scale
            x += cos(theta)
            y += sin(theta)
            out.append((x, y))
        return out

    def is_true_euler_spiral(self) -> Dict[str, object]:
        """
        Side investigation, not an alarm function. FALSIFIED, kept on record:
        ln(p_n) never reverses sign, so curvature_spiral can only tighten
        into one inward spiral -- not a true Euler spiral (clothoid).
        """
        kappa = [log(p) for p in self.primes]
        return {
            'is_clothoid': False,
            'reason': 'ln(p_n) is monotonic and always positive; a clothoid '
                      'requires curvature to cross zero and reverse sign to '
                      'produce two asymptotic eyes (Fresnel integral).',
            'kappa_min': min(kappa),
            'kappa_max': max(kappa),
            'kappa_sign_changes': 0,
            'actual_topology': 'single-point inward spiral (involute-like)',
        }
