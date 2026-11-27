"""
ValaQuenta.modules.h_rb_hat.sigma16
===================================
The 16-dimensional σ_RB input and its 16-dimensional output: a rigorous, definition-first test bench.

Nothing here is assumed to be the author's final mapping of σ_RB (the record has two uses of the symbol, see
wiki/DISAMBIGUATION_NOTES.md). This module states two precise lifts of the scalar Ĥ_RB of ``maths.py`` to the Emmy Noether
sedenion 𝕊_EN, runs them, and reports exactly what falls out.

The input is one sedenion  σ_RB = σ_ζ·e₀ + σ_RB₁e₁ + … + σ_RB₁₅e₁₅  (the real scalar plus the 15 imaginary components).
Write u = (σ_RB₁…σ_RB₁₅), τ = |u|, û = u/τ (a point of S¹⁴, û² = −1). The sedenions are power-associative, so

    p^(−σ_RB) := exp(−σ_RB ln p) = p^(−σ_ζ) · ( cos(τ ln p) − û sin(τ ln p) )          [exact]

which is the Dirichlet term p^(−(σ_ζ + iτ)) with the imaginary unit i replaced by the unit û.

LIFT A — scalar energies (the lift ``maths.sigma_rb_term`` already implies).
    Σ_RB(σ_RB; x, p) = Σ_p p^(−σ_RB) · [E_red(x,p) + E_blue(x,p)]   ∈ 𝕊
    The energies are real, so each term lies in the plane span(e₀, û). The output is a 2-plane and the direction û is
    a gauge: A depends on (σ_ζ, τ) only. (`lift_a_equivariance` checks this.)

LIFT B — operators on 𝕊 (the reading used in TuringStack/udeo_crypto/RSA_DEMO.py, method 2).
    C(σ_RB) = Σ_p p^(−σ_RB)            ∈ 𝕊            (the coupling element)
    Ĥ_RB(σ_RB) = L_C   (x ↦ C·x)      Ĥ_BR(σ_RB) = R_C   (x ↦ x·C)           16×16 real matrices
    Ĥ_RB − Ĥ_BR = L_C − R_C = ad_C = J_red + J_blue  (the author's current balance; the commutator map)
    C lies in the plane span(e₀, û): C = α + β·û with α = Σ p^(−σ_ζ) cos(τ ln p), β = −Σ p^(−σ_ζ) sin(τ ln p).
    e₀ commutes with everything, so  L_C − R_C = β · ad_û  EXACTLY: the magnitude β is the imaginary part of the Dirichlet
    sum at s = σ_ζ + iτ, and the direction dependence is ad_û alone (a fixed 16×16 matrix per direction û).
    Corollaries: on the real axis (τ = 0) Ĥ_RB = Ĥ_BR (the current balance J_red + J_blue vanishes identically);
    the balance also vanishes wherever β = 0. Unlike A, B depends on the direction û (non-associative, non-commutative).

Status labels: every number computed here is CALCULATED. The two lifts are definitions chosen to be testable, not
the author's final σ_RB. Status of the lifts themselves: OPEN.

d* faces (all four are needed to chart ln(10) in Universal Native Space):
  d*         = 0.24600          the value the code runs with (Boundary, σ_ζ=½ plane)
  d*_taut    = 0.246307201473  A_π/ln10, the Flow (radial unit)
  d*_RG      = dimension 8; numeric OPEN, no closed form  the Stability (centre r=0)
  d*_ln(10)  = 0.5671432904   d*_taut·ln10 = A_π, the Translator (log bridge)

Full story of d*: Ainulindale/wiki/17_alpha_omega_d_star.md; ~/.clauderc_canonical_maths @RCCM_FOUR_DSTAR; FourthAgePapers/DStarRG
"""
from typing import Dict, List, Sequence

import numpy as np

from ...engine import constants as _C
from ..box_kite.maths import basis_mul
from .maths import PRIMES, blue_energy, red_energy

DIM = 16
GAP = abs(_C.A_PI - _C.D_STAR * np.log(10.0))        # the onset residual, 0.000707...
GAP_CLOSED_FORM = 1.0 / (1000.0 * np.sqrt(2.0))        # 1/(1000√2) = 0.000707106...

# structure constants: e_i e_k = SIGN[i,k] · e_{IDX[i,k]}
SIGN = np.zeros((DIM, DIM))
IDX = np.zeros((DIM, DIM), dtype=int)
for _i in range(DIM):
    for _k in range(DIM):
        _s, _j = basis_mul(_i, _k)
        SIGN[_i, _k], IDX[_i, _k] = _s, _j


def L(a: Sequence[float]) -> np.ndarray:
    """Left-multiplication matrix of a:  L(a) @ x = a·x.

    :param a: sedenion as a 16-vector
    :returns: 16×16 real matrix
    """
    M = np.zeros((DIM, DIM))
    for i in np.flatnonzero(a):
        for k in range(DIM):
            M[IDX[i, k], k] += a[i] * SIGN[i, k]
    return M


def R(a: Sequence[float]) -> np.ndarray:
    """Right-multiplication matrix of a:  R(a) @ x = x·a.

    :param a: sedenion as a 16-vector
    :returns: 16×16 real matrix
    """
    M = np.zeros((DIM, DIM))
    for i in np.flatnonzero(a):
        for k in range(DIM):
            M[IDX[k, i], k] += a[i] * SIGN[k, i]
    return M


def mul(a: Sequence[float], b: Sequence[float]) -> np.ndarray:
    """Sedenion product a·b.

    :param a: left factor
    :param b: right factor
    :returns: the 16-vector a·b
    """
    return L(a) @ np.asarray(b, dtype=float)


def sigma_rb_vector(sigma_riemann: float, u: Sequence[float] = None, tau: float = None) -> np.ndarray:
    """Build the sedenion σ_RB = σ_ζ e₀ + u.

    :param sigma_riemann: the real scalar σ_ζ
    :param u: 15 imaginary components (indices 1..15); a 16-vector with u[0] ignored is also accepted
    :param tau: if given, rescale u to norm tau (u must be non-zero)
    :returns: the 16-vector σ_RB
    """
    s = np.zeros(DIM)
    s[0] = sigma_riemann
    if u is not None:
        u = np.asarray(u, dtype=float)
        u = u[-15:] if len(u) in (15, 16) else u
        s[1:] = u
        if tau is not None:
            s[1:] *= tau / np.linalg.norm(s[1:])
    return s


def sed_exp(a: Sequence[float]) -> np.ndarray:
    """Exact sedenion exponential: exp(a) = e^{a₀}(cos|u| + û sin|u|), u = Im a.

    :param a: sedenion
    :returns: exp(a) as a 16-vector
    """
    a = np.asarray(a, dtype=float)
    u = a[1:]
    t = np.linalg.norm(u)
    out = np.zeros(DIM)
    out[0] = np.cos(t)
    if t > 0:
        out[1:] = np.sin(t) / t * u
    return np.exp(a[0]) * out


def prime_power(p: int, sigma_rb: Sequence[float]) -> np.ndarray:
    """p^(−σ_RB) = exp(−σ_RB ln p) for a sedenion σ_RB.

    :param p: prime
    :param sigma_rb: sedenion σ_RB
    :returns: the 16-vector p^(−σ_RB)
    """
    return sed_exp(-np.asarray(sigma_rb, dtype=float) * np.log(p))


def coupling(sigma_rb: Sequence[float], n_primes: int = 20) -> np.ndarray:
    """The coupling element C(σ_RB) = Σ_p p^(−σ_RB) over the first n_primes primes.

    :param sigma_rb: sedenion σ_RB
    :param n_primes: number of primes (the code's PRIMES list)
    :returns: C(σ_RB) as a 16-vector
    """
    return sum(prime_power(p, sigma_rb) for p in PRIMES[:n_primes])


# ── LIFT A ──────────────────────────────────────────────────────────────────
def lift_a(sigma_rb: Sequence[float], x: float = 1.0, p_momentum: float = 1.0, n_primes: int = 20) -> Dict[str, np.ndarray]:
    """Lift A: Σ_RB(σ_RB; x, p) = Σ_p p^(−σ_RB)·[E_red + E_blue], with the real energies of ``maths``.

    :param sigma_rb: sedenion σ_RB
    :param x: position
    :param p_momentum: momentum
    :param n_primes: number of primes
    :returns: dict with 'total', 'red' (J_red part), 'blue' (J_blue part): 16-vectors
    """
    er, eb = red_energy(x, p_momentum), blue_energy(x, p_momentum)
    C = coupling(sigma_rb, n_primes)
    return {"total": C * (er + eb), "red": C * er, "blue": C * eb, "coupling": C}


def lift_a_equivariance(sigma_riemann: float, tau: float, trials: int = 50, seed: int = 0) -> float:
    """Largest spread of |Σ_RB| over random directions û at fixed (σ_ζ, τ): 0 means û is a gauge for lift A.

    :param sigma_riemann: real part
    :param tau: modulus of the imaginary part
    :param trials: number of random directions
    :param seed: RNG seed
    :returns: max − min of the output norm over the trials
    """
    rng = np.random.default_rng(seed)
    norms = [np.linalg.norm(lift_a(sigma_rb_vector(sigma_riemann, rng.normal(size=15), tau))["total"]) for _ in range(trials)]
    return float(max(norms) - min(norms))


# ── LIFT B ──────────────────────────────────────────────────────────────────
def lift_b(sigma_rb: Sequence[float], n_primes: int = 20) -> Dict[str, np.ndarray]:
    """Lift B: Ĥ_RB = L_C, Ĥ_BR = R_C, asymmetry L_C − R_C (= J_red + J_blue), symmetric part L_C + R_C.

    :param sigma_rb: sedenion σ_RB
    :param n_primes: number of primes
    :returns: dict of 16×16 matrices and the coupling element
    """
    C = coupling(sigma_rb, n_primes)
    Lc, Rc = L(C), R(C)
    return {"coupling": C, "H_RB": Lc, "H_BR": Rc, "asym": Lc - Rc, "sym": Lc + Rc}


def invariants(M: np.ndarray, tol: float = 1e-9) -> Dict[str, object]:
    """Rank, nullity, singular values and Frobenius norm of a 16×16 operator.

    :param M: matrix
    :param tol: singular values below tol count as zero
    :returns: dict with 'rank', 'nullity', 'sv' (descending), 'fro'
    """
    sv = np.linalg.svd(M, compute_uv=False)
    rank = int((sv > tol).sum())
    return {"rank": rank, "nullity": DIM - rank, "sv": sv, "fro": float(np.linalg.norm(M))}


def asym_of_unit(a: Sequence[float]) -> Dict[str, object]:
    """Invariants of ad_a = L_a − R_a for one sedenion a (direction analysis without the Euler sum).

    :param a: sedenion
    :returns: invariants dict of L_a − R_a
    """
    return invariants(L(a) - R(a))


def direction_atlas() -> List[Dict[str, object]]:
    """ad-invariants for the 15 basis directions e_k and the 84 + 84 zero-divisor directions (e_i ± e_j)/√2.

    :returns: list of dicts {label, class, direction (16-vector), rank, nullity, sv}
    """
    out = []
    for k in range(1, DIM):
        a = np.zeros(DIM)
        a[k] = 1.0
        inv = asym_of_unit(a)
        out.append({"label": f"e{k}", "class": "basis", "dir": a, **inv})
    for i in range(1, 8):
        for j in range(9, 16):
            for sgn in (1, -1):
                a = np.zeros(DIM)
                a[i], a[j] = 1.0, sgn * 1.0
                a /= np.linalg.norm(a)
                inv = invariants(L(a))
                inv_ad = asym_of_unit(a)
                out.append({"label": f"(e{i}{'+' if sgn > 0 else '−'}e{j})/√2", "class": "zd-candidate", "dir": a,
                            "L_rank": inv["rank"], **inv_ad})
    return out


def zero_divisor_partners(a: Sequence[float], tol: float = 1e-9) -> int:
    """Dimension of the right annihilator of a: nullity of L_a (0 for an invertible a).

    :param a: sedenion
    :param tol: singular value tolerance
    :returns: nullity of L_a
    """
    return invariants(L(a), tol)["nullity"]


def spectrum_of_L(a: Sequence[float]) -> np.ndarray:
    """Eigenvalues of L_a (real parts and imaginary parts): where α + β·L_û is singular is read from here.

    :param a: sedenion (typically a unit imaginary û)
    :returns: complex eigenvalues of L_a sorted by (real, imag)
    """
    ev = np.linalg.eigvals(L(a))
    return ev[np.lexsort((ev.imag, ev.real))]


def beta_alpha(sigma_riemann: float, tau: float, n_primes: int = 20) -> Dict[str, float]:
    """The two real coefficients of C = α + β·û (the truncated Dirichlet sum at s = σ_ζ + iτ).

    :param sigma_riemann: real part
    :param tau: |Im σ_RB|
    :param n_primes: number of primes
    :returns: dict alpha, beta, modulus
    """
    lnp = np.log(np.array(PRIMES[:n_primes], dtype=float))
    w = np.array(PRIMES[:n_primes], dtype=float) ** (-sigma_riemann)
    a, b = float((w * np.cos(tau * lnp)).sum()), float(-(w * np.sin(tau * lnp)).sum())
    return {"alpha": a, "beta": b, "modulus": float(np.hypot(a, b))}
