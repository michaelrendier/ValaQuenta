# SPDX-License-Identifier: GPL-3.0-only
"""Bridge to the project's own structure.  Every function states which part is ESTABLISHED arithmetic and which reading is INTERPRETATION.
Nothing here claims that Einstein's equations are contained in or derived from the Null Operator."""
from __future__ import annotations
from fractions import Fraction as Fr
import math
import sympy as sp
from . import minkowski as Mk


def prime_boost(p: int) -> dict:
    """A boost whose Doppler factor is the integer p.  ESTABLISHED arithmetic: beta = (p^2 - 1)/(p^2 + 1), gamma = (p^2 + 1)/(2p),
    gamma beta = (p^2 - 1)/(2p), rapidity ln p; (p^2 - 1, 2p, p^2 + 1) is a Pythagorean triple (the boost is rational).

    :param p: the integer Doppler factor
    :returns: dict of beta, gamma, gamma_beta, rapidity, the Pythagorean triple and its check
    """
    p = int(p); beta = Fr(p * p - 1, p * p + 1); g = Fr(p * p + 1, 2 * p); gb = Fr(p * p - 1, 2 * p)
    a, b, c = p * p - 1, 2 * p, p * p + 1
    return {"p": p, "beta": beta, "gamma": g, "gamma_beta": gb, "rapidity": math.log(p), "triple": (a, b, c), "triple_ok": a * a + b * b == c * c,
            "doppler_factor_check": float(math.sqrt((1 + float(beta)) / (1 - float(beta)))) - p}


def compose_prime_boosts(p: int, q: int) -> dict:
    """Composing the boosts with Doppler factors p and q is the boost with Doppler factor pq: the group of boosts along a line with rational
    Doppler factor is the multiplicative group of positive rationals.  Velocity addition computed exactly with Fractions.

    :param p: first integer Doppler factor
    :param q: second prime
    :returns: dict with the summed velocity, the velocity of boost pq and whether they are equal
    """
    b1 = Fr(p * p - 1, p * p + 1); b2 = Fr(q * q - 1, q * q + 1); s = (b1 + b2) / (1 + b1 * b2); pq = p * q
    return {"beta_sum": s, "beta_of_pq": Fr(pq * pq - 1, pq * pq + 1), "equal": s == Fr(pq * pq - 1, pq * pq + 1)}


def boost_factorisation(k: Fr) -> dict:
    """A rational Doppler factor k = a/b has a unique factorisation into prime boosts (and their inverses): the exponent vector over the primes.
    Rapidity = sum_p e_p ln p.  ESTABLISHED (unique factorisation); the reading that Lorentz composition along a line IS prime factorisation is
    INTERPRETATION.

    :param k: rational Doppler factor
    :returns: dict with the prime exponents and the rapidity both ways
    """
    k = Fr(k); num = sp.factorint(k.numerator); den = sp.factorint(k.denominator); ev = {}
    for p, e in num.items(): ev[p] = ev.get(p, 0) + e
    for p, e in den.items(): ev[p] = ev.get(p, 0) - e
    rap = sum(e * math.log(p) for p, e in ev.items())
    return {"doppler_factor": k, "exponents": dict(sorted(ev.items())), "rapidity": rap, "rapidity_direct": math.log(float(k)), "residual": abs(rap - math.log(float(k)))}
