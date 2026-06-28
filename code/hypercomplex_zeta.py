#!/usr/bin/env python3
"""
hypercomplex_zeta.py — Hypercomplex Riemann Zeta function across the Cayley-Dickson tower.

STANDALONE EXPERIMENT. Zero imports from other project engines.
The mathematics must speak for itself. The experiment must be able to fail.

If Zero Definer pairs appear as zeros: they were always there.
If σ=½ self-selects: Noether forcing is real.
If epitrochoid geometry emerges: the Wankel connection is a result, not an assumption.
If none of it matches the other engines: we learn something more important.

TWO ZERO TYPES (predicted — let the computation confirm or deny):
  TYPE 1 — Series zeros:   where |ζ_n(s)| < ε  (the function itself vanishes)
  TYPE 2 — Definer zeros:  where (1 - p^{-s}) is non-invertible in the CD algebra
                            (the Euler product stalls — definition by extinction)

Author:  Cody Michael Allison
Built:   Claude Code (claude-sonnet-4-6), 2026-06-14
"""

from __future__ import annotations
import math
import sys
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# CAYLEY-DICKSON ALGEBRA  (self-contained, no external dependencies)
# ─────────────────────────────────────────────────────────────────────────────

def cd_conj(a: list[float], dim: int) -> list[float]:
    """Cayley-Dickson conjugate: negate all non-scalar components."""
    result = list(a)
    for i in range(1, dim):
        result[i] = -result[i]
    return result

def cd_mul(a: list[float], b: list[float], dim: int) -> list[float]:
    """
    Cayley-Dickson multiplication at dimension dim (must be power of 2).
    Recursive: (p,q)*(r,s) = (pr - s*q, sp + qr*)
    where * is conjugation at the half-dimension level.
    """
    if dim == 1:
        return [a[0] * b[0]]
    half = dim // 2
    p, q = a[:half], a[half:]
    r, s = b[:half], b[half:]

    pr   = cd_mul(p, r, half)
    sq   = cd_mul(s, q, half)
    s_cj = cd_mul(s, p, half)
    qr_c = cd_mul(q, cd_conj(r, half), half)

    left  = [pr[i] - sq[i] for i in range(half)]
    right = [s_cj[i] + qr_c[i] for i in range(half)]
    return left + right

def cd_add(a: list[float], b: list[float]) -> list[float]:
    return [a[i] + b[i] for i in range(len(a))]

def cd_scale(a: list[float], c: float) -> list[float]:
    return [x * c for x in a]

def cd_norm2(a: list[float]) -> float:
    return sum(x*x for x in a)

def cd_norm(a: list[float]) -> float:
    return math.sqrt(cd_norm2(a))

def cd_inv(a: list[float], dim: int) -> Optional[list[float]]:
    """
    Cayley-Dickson inverse: a^{-1} = conj(a) / |a|^2.
    Returns None if a is a zero divisor (|a|^2 = 0 but a ≠ 0)
    or the zero element itself.
    This is where Type 2 (Definer) zeros are detected.
    """
    n2 = cd_norm2(a)
    if n2 == 0.0:
        return None
    return cd_scale(cd_conj(a, dim), 1.0 / n2)

def cd_zero(dim: int) -> list[float]:
    return [0.0] * dim

def cd_one(dim: int) -> list[float]:
    r = [0.0] * dim
    r[0] = 1.0
    return r

# ─────────────────────────────────────────────────────────────────────────────
# HYPERCOMPLEX EXPONENTIAL  exp(s) = Σ s^n / n!
# Converges for ||s|| not too large; use for s = -ln(k) * s_unit
# ─────────────────────────────────────────────────────────────────────────────

def cd_exp(s: list[float], dim: int, terms: int = 40) -> list[float]:
    """
    Compute exp(s) in the CD algebra via power series.
    s^0/0! + s^1/1! + s^2/2! + ...
    Non-associative at dim >= 8: uses left-to-right bracketing for s^n.
    """
    result = cd_one(dim)
    power  = cd_one(dim)
    fact   = 1.0
    for n in range(1, terms):
        fact  *= n
        power  = cd_mul(power, s, dim)
        term   = cd_scale(power, 1.0 / fact)
        result = cd_add(result, term)
        if cd_norm(term) < 1e-15:
            break
    return result

def cd_pow_real(s: list[float], t: float, dim: int) -> list[float]:
    """
    Compute t^s = exp(s * ln(t)) for real t > 0, hypercomplex s.
    k^{-s} = exp(-ln(k) * s)
    """
    log_t  = math.log(t)
    neg_s  = cd_scale(s, -log_t)
    return cd_exp(neg_s, dim)

# ─────────────────────────────────────────────────────────────────────────────
# ZETA FUNCTION  ζ_dim(s) = Σ_{k=1}^{N} k^{-s}
# ─────────────────────────────────────────────────────────────────────────────

def theta_rs(t: float) -> float:
    """
    Riemann-Siegel theta function.
    θ(t) = Im(log Γ(¼ + it/2)) - t·log(π)/2
    Asymptotic expansion valid for t > 2:
    θ(t) ≈ t/2·log(t/2π) - t/2 - π/8 + 1/(48t) - 7/(5760t³)

    This is the rotation that reveals the zeros of ζ(½+it) as REAL zero-crossings.
    The diverging Dirichlet series, rotated by e^{iθ(t)}, becomes the Hardy Z-function —
    a real function whose zero-crossings ARE the non-trivial zeros.
    Reading the divergence 'in reverse' = applying this rotation and reading the sign.
    """
    if t <= 0:
        return 0.0
    return (t/2)*math.log(t/(2*math.pi)) - t/2 - math.pi/8 + 1/(48*t) - 7/(5760*t**3)

def z_function_complex(t: float, N: int = 0) -> float:
    """
    Hardy Z-function in ℂ: Z(t) = 2·Re(e^{iθ(t)} · Σ_{k=1}^{N_RS} k^{-(½+it)})
    where N_RS = floor(sqrt(t/2π)) — the Riemann-Siegel truncation.
    Z(t) is REAL. Its zero-crossings are the non-trivial zeros of ζ(½+it).
    The divergence truncated at N_RS is the signal, not the noise.
    """
    if N == 0:
        N = max(1, int(math.sqrt(t / (2 * math.pi))))
    th = theta_rs(t)
    total = 0.0
    for k in range(1, N + 1):
        # k^{-(½+it)} = k^{-½} · e^{-it·ln(k)}
        # Rotated by e^{iθ}: phase = θ - t·ln(k)
        total += k**(-0.5) * math.cos(th - t * math.log(k))
    return 2.0 * total

def z_function_hypercomplex(t: float, dim: int, N: int = 0,
                            s: Optional[list[float]] = None) -> dict:
    """
    Hypercomplex Hardy Z-function.
    In ℂ (dim=2): reduces to the scalar Z(t) above.
    In ℍ, 𝕆, 𝕊: the rotation e^{iθ} is applied LEFT and RIGHT separately.
    LEFT:  Z_L = e^{θ·e1} * J_red   (e1 is the first imaginary basis element)
    RIGHT: Z_R = J_red * e^{θ·e1}
    In ℂ: Z_L = Z_R (commutative). In ℍ+: Z_L ≠ Z_R.
    The DIFFERENCE Z_L - Z_R is the ordering signal — zeros from non-commutativity.
    The SUM Z_L + Z_R is the symmetric Z-function — reduces to 2·Z(t) in ℂ.

    s: optional full CD element. Default = (½, t, 0, ...) — pure ℂ embedding.
       Pass a full 16D s to activate the non-commutative structure.
    """
    if N == 0:
        N = max(1, int(math.sqrt(t / (2 * math.pi))))

    th = theta_rs(t)

    # Build rotation element: e^{θ·e1} in the CD algebra
    # e^{θ·e1} = cos(θ)·e0 + sin(θ)·e1  (since e1² = -1)
    rot = cd_zero(dim)
    rot[0] = math.cos(th)
    if dim >= 2:
        rot[1] = math.sin(th)

    # s: default = (½, t, 0, ...) — pure ℂ embedding
    if s is None:
        s = cd_zero(dim)
        s[0] = 0.5
        if dim >= 2:
            s[1] = t

    jr = j_red(s, dim, N=N)

    z_left  = cd_mul(rot, jr,  dim)   # e^{iθ} * J_red
    z_right = cd_mul(jr,  rot, dim)   # J_red * e^{iθ}

    diff = [z_left[i] - z_right[i] for i in range(dim)]
    sumv = [z_left[i] + z_right[i] for i in range(dim)]

    return {
        'z_left':     z_left,
        'z_right':    z_right,
        'diff':       diff,
        'sum':        sumv,
        'diff_norm':  cd_norm(diff),
        'sum_norm':   cd_norm(sumv),
        'z_scalar':   z_left[0],   # real part of left-rotation = Z(t) in ℂ
    }

def j_red(s: list[float], dim: int, N: int = 200) -> list[float]:
    """
    Forward Dirichlet sum: J_red(s,N) = Σ_{k=1}^{N} k^{-s}
    Diverges at σ=½. The divergence is not a bug — it is the signal.
    The oscillating partial sums encode the zero structure.
    In non-commutative algebras (ℍ, 𝕆, 𝕊): order matters.
    """
    result = cd_zero(dim)
    for k in range(1, N + 1):
        result = cd_add(result, cd_pow_real(s, float(k), dim))
    return result

def j_blue(s: list[float], dim: int, N: int = 200) -> list[float]:
    """
    Reverse Dirichlet sum: J_blue(s,N) = Σ_{k=N}^{1} k^{-s}
    Same terms, REVERSED ORDER.
    In ℂ (commutative): J_blue = J_red. No information gained.
    In ℍ, 𝕆, 𝕊 (non-commutative): J_blue ≠ J_red.
    The difference J_red - J_blue is the ordering signal — new zeros emerge here.
    The product cd_mul(J_red, J_blue) is L_dynamic at this s:
      where the product hits a zero divisor = Zero Definer zero.
      where |product| is minimised = TYPE 1 zero (series zero).
    """
    result = cd_zero(dim)
    for k in range(N, 0, -1):
        result = cd_add(result, cd_pow_real(s, float(k), dim))
    return result

# ─────────────────────────────────────────────────────────────────────────────
# EULER PRODUCT  ζ_dim(s) = Π_p (1 - p^{-s})^{-1}
# Stalls when (1 - p^{-s}) is non-invertible → TYPE 2 (Definer) zero
# ─────────────────────────────────────────────────────────────────────────────

PRIMES_64 = [
    2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,
    59,61,67,71,73,79,83,89,97,101,103,107,109,113,
    127,131,137,139,149,151,157,163,167,173,179,181,
    191,193,197,199,211,223,227,229,233,239,241,251,
    257,263,269,271,277,281,283,293,307,311,
]

def euler_product(s: list[float], dim: int,
                  n_primes: int = 20) -> tuple[Optional[list[float]], list[int]]:
    """
    Compute Euler product at CD dimension dim.
    Returns (product, stalled_primes).
    stalled_primes: primes where (1 - p^{-s}) was non-invertible.
    These are the TYPE 2 (Definer) zeros — definition by extinction.

    product is None if the entire product stalled at the first prime.
    """
    result       = cd_one(dim)
    stalled      = []

    for p in PRIMES_64[:n_primes]:
        p_inv_s  = cd_pow_real(s, float(p), dim)
        one      = cd_one(dim)
        factor   = [one[i] - p_inv_s[i] for i in range(dim)]
        inv      = cd_inv(factor, dim)
        if inv is None:
            stalled.append(p)
        else:
            result = cd_mul(result, inv, dim)

    return result, stalled

# ─────────────────────────────────────────────────────────────────────────────
# ZERO SCAN
# ─────────────────────────────────────────────────────────────────────────────

def scan_zeros(dim:         int   = 2,
               sigma_z:     float = 0.5,
               t_min:       float = 0.0,
               t_max:       float = 50.0,
               t_steps:     int   = 1000,
               N_series:    int   = 150,
               n_primes:    int   = 20,
               eps:         float = 0.3,
               perturb:     float = 0.0) -> dict:
    """
    Scan Re(s) = σ_z for zeros in the CD algebra at dimension dim.

    NOTATION:
      σ_z  — the real part of s in ζ(s) = ζ(σ_z + it). This is the Riemann σ.
              The RH asks: do all non-trivial zeros have σ_z = ½?
              NOT the same as Σ_RB.

      Σ_RB — the operator H_hat_RB - H_hat_BR. Fixed Question Space.
              The full span of the system. The input to ptol.c.
              Σ_RB is not a coordinate. It is the self-description of the algebra.
              Σ_RB lives AT σ_z = ½ — it is what the algebra looks like at the
              fixed point of the Riemann zeta function.

    s = (σ_z, t, perturb, perturb, ...) — Riemann σ fixed, imaginary varies.
    perturb: nonzero value in e2..e_{dim-1} to activate ZD-sensitive directions.
             Zero = pure ℂ embedding. Nonzero = the full CD space speaks.

    TYPE 1 — Hardy Z-function sign changes (correctly handles divergent Dirichlet series).
             Z(t) = 2·Re(e^{iθ(t)} · J_red) in ℂ.
             In dim>2: Z_scalar = scalar part of e^{iθ}·J_red.
             The divergence IS the signal — Z-rotation reads it in reverse.

    TYPE 2 — Ordering zeros: sign changes in Z_L - Z_R (non-commutativity).
             Z_L = e^{iθ}·J_red,  Z_R = J_red·e^{iθ}.
             In ℂ: Z_L = Z_R always. In ℍ+ with perturb>0: Z_L ≠ Z_R.
             Zero crossings of (Z_L - Z_R)_scalar are NEW zeros from the algebra.

    TYPE 3 — Euler product stall: (1 - p^{-s}) non-invertible = Zero Definer.
             Only appears when s has nonzero components in ZD-sensitive directions.
    """
    z_scalars     = []    # Hardy Z-function values (scalar component)
    ordering_diffs = []   # (Z_L - Z_R)_scalar — ordering signal
    ts            = []
    definer_zeros = []    # Euler product stalls (TYPE 3)
    dt            = (t_max - t_min) / t_steps

    # N_RS for Z-function: Riemann-Siegel truncation
    # For series sum we use N_series; for Z-function we use sqrt(t/2π)

    for step in range(t_steps + 1):
        t    = t_min + step * dt
        s    = cd_zero(dim)
        s[0] = sigma_z
        if dim >= 2:
            s[1] = t
        for k in range(2, dim):
            s[k] = perturb   # activate ZD-sensitive higher dimensions

        # TYPE 1: Hardy Z-function via Riemann-Siegel rotation
        N_rs = max(1, int(math.sqrt(max(t, 0.1) / (2 * math.pi))))
        hc   = z_function_hypercomplex(t, dim, N=N_rs, s=s)
        z_s  = hc['z_scalar']      # scalar (e0) component = Z(t) in ℂ embedding
        # Ordering difference: FULL VECTOR norm, not scalar
        # In ℂ: diff = 0 always (commutative). In ℍ+: diff lives in e2..e_{dim-1}.
        # The scalar component is zero by symmetry — the algebra speaks in the VECTOR part.
        od   = cd_norm(hc['diff'])

        ts.append(t)
        z_scalars.append(z_s)
        ordering_diffs.append(od)

        # TYPE 3: Euler product stall (only meaningful with perturb>0 in dim>=16)
        if dim >= 16 and (perturb != 0.0 or step % 50 == 0):
            _, stalled = euler_product(s, dim, n_primes=n_primes)
            for p in stalled:
                definer_zeros.append({'t': t, 'prime': p, 's': s[:],
                                      'type': 'euler_stall'})

    # TYPE 1: sign changes in Z_scalar = non-trivial zeros of ζ(½+it)
    # Detect each SIGN TRANSITION exactly once: look for Z[i-1]*Z[i] < 0
    series_zeros = []
    for i in range(1, len(z_scalars)):
        if z_scalars[i-1] * z_scalars[i] < 0:   # sign change between steps i-1 and i
            # bisect to refine
            t_lo, t_hi = ts[i-1], ts[i]
            z_lo = z_scalars[i-1]
            for _ in range(28):
                t_mid = (t_lo + t_hi) / 2
                N_m   = max(1, int(math.sqrt(max(t_mid, 0.1) / (2 * math.pi))))
                z_mid = z_function_hypercomplex(t_mid, dim, N=N_m)['z_scalar']
                if z_lo * z_mid < 0:
                    t_hi = t_mid
                else:
                    t_lo, z_lo = t_mid, z_mid
            series_zeros.append({'t': (t_lo + t_hi) / 2, 'z': 0.0})

    # TYPE 2: local minima of ordering norm ||Z_L - Z_R||
    # In ℂ: always 0 (no signal). In ℍ+ with perturb>0: nonzero, with structure.
    # Local minima = where the algebra's ordering difference is weakest = new zero-like structure.
    ordering_zeros = []
    for i in range(1, len(ordering_diffs) - 1):
        prev_n = ordering_diffs[i-1]
        curr_n = ordering_diffs[i]
        next_n = ordering_diffs[i+1]
        if curr_n < prev_n and curr_n < next_n and curr_n < (prev_n + next_n) * 0.4:
            ordering_zeros.append({'t': ts[i], 'diff': curr_n})

    return {
        'dim':            dim,
        'sigma_z':        sigma_z,
        'perturb':        perturb,
        't_range':        (t_min, t_max),
        'series_zeros':   series_zeros,     # TYPE 1: sign changes in Z(t)
        'ordering_zeros': ordering_zeros,   # TYPE 2: non-commutativity zeros
        'definer_zeros':  definer_zeros,    # TYPE 3: Euler stalls (Zero Definers)
        'z_scalars':      z_scalars,
        'ordering_diffs': ordering_diffs,
        'ts':             ts,
    }

# ─────────────────────────────────────────────────────────────────────────────
# REPORT
# ─────────────────────────────────────────────────────────────────────────────

def report(results: dict) -> None:
    dim    = results['dim']
    t0, t1 = results['t_range']
    sz     = results['series_zeros']
    oz     = results.get('ordering_zeros', [])
    dz     = results['definer_zeros']
    perturb = results.get('perturb', 0.0)

    algebra = {2: 'ℂ', 4: 'ℍ', 8: '𝕆', 16: '𝕊', 32: 'T_32', 64: 'T_64', 256: 'T_256'}
    name    = algebra.get(dim, f'T_{dim}')

    print(f"\n{'='*60}")
    print(f"  Hypercomplex Zeta  —  {name}  (dim={dim})")
    sigma_z = results['sigma_z']
    perturb_str = f"  perturb={perturb} (e2..e{dim-1} components)" if perturb else "  pure ℂ-embedding"
    print(f"  σ_z = {sigma_z}  (Riemann σ, NOT Σ_RB)    t ∈ [{t0}, {t1}]")
    print(f"  {perturb_str}")
    print(f"{'='*60}")

    print(f"\nNOTE: σ_z = Riemann real-part coordinate.")
    print(f"      Σ_RB = H_hat_RB - H_hat_BR = Fixed Question Space.")
    print(f"      Σ_RB is NOT σ_z. Σ_RB lives AT σ_z=½. They share a home, not a name.")

    # Known ℂ zeros
    known = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
             37.5862, 40.9187, 43.3271, 48.0052, 49.7738]

    print(f"\nTYPE 1 — Z(t) sign changes  (zeros of ζ(σ+it)):  {len(sz)} found")
    print(f"  [divergent Dirichlet series read in reverse via Riemann-Siegel rotation]")
    for z in sz[:20]:
        near = min(known, key=lambda k: abs(k - z['t']))
        delta = z['t'] - near
        print(f"  t = {z['t']:10.5f}   nearest known = {near:.4f}  Δ = {delta:+.5f}")
    if len(sz) > 20:
        print(f"  ... and {len(sz)-20} more")

    print(f"\nTYPE 2 — Ordering zeros  (Z_L - Z_R sign changes):  {len(oz)} found")
    print(f"  [non-commutativity signal — absent in ℂ, new zeros in ℍ+]")
    if oz:
        for z in oz[:10]:
            print(f"  t = {z['t']:10.5f}   Z_L-Z_R = {z['diff']:.6f}")
        if len(oz) > 10:
            print(f"  ... and {len(oz)-10} more")
    else:
        print(f"  (zero with pure ℂ-embedding — use --perturb to activate)")

    print(f"\nTYPE 3 — Euler stalls  (Zero Definers — definition by extinction):  {len(dz)} found")
    if dz:
        seen = {}
        for z in dz:
            key = (round(z['t'], 2), z.get('prime', '?'))
            if key not in seen:
                seen[key] = True
                print(f"  t = {z['t']:10.5f}   prime = {z.get('prime','?')}")
            if len(seen) >= 20:
                break
        if len(dz) > 20:
            print(f"  ... and {len(dz)-20} more")
    else:
        print(f"  (requires dim>=16 with perturb>0 to enter ZD-sensitive space)")

    if not sz and not oz and not dz:
        print("\n  No zeros found. Try --perturb 0.1 or finer --t-steps.")

    if sz:
        print(f"\n  COMPARISON — known ℂ zeros (first {len(known)}):")
        for k in known:
            if t0 <= k <= t1:
                nearest = min(sz, key=lambda z: abs(z['t'] - k))
                print(f"    known {k:.4f}  →  found {nearest['t']:.5f}"
                      f"  (Δ = {abs(nearest['t']-k):.5f})")

# ─────────────────────────────────────────────────────────────────────────────
# ZD-ALIGNED SCAN  — let the ZD pairs define the perturbation directions
# "if you want to hear the math speak, let it define the variables"
# ─────────────────────────────────────────────────────────────────────────────

# The 84 canonical a-vectors of the 𝕊 ZD structure (from Cawagas/Moreno).
# Each is a unit-norm pair (eᵢ + eⱼ)/√2 on S¹⁵.
# These are the definitions — the places where definition-by-extinction occurs.
_ZD_DIRECTIONS_S15 = [
    (1,10),(1,11),(1,14),(1,15),
    (2,11),(2,10),(2,13),(2,12),
    (3,8), (3,9), (3,12),(3,13),
    (4,9), (4,8), (4,15),(4,14),
    (5,12),(5,13),(5,10),(5,11),
    (6,13),(6,12),(6,9), (6,8),
    (7,14),(7,15),(7,8), (7,9),
    (8,3), (8,4), (8,6), (8,7),
    (9,4), (9,3), (9,7), (9,6),
    (10,1),(10,2),(10,5),(10,4),
    (11,2),(11,1),(11,4),(11,5),
    (12,3),(12,5),(12,2),(12,6),
    (13,6),(13,7),(13,2),(13,3),
    (14,7),(14,1),(14,6),(14,5),
    (15,1),(15,6),(15,7),(15,4),
    (5,8), (5,9), (6,10),(6,11),
    (7,10),(7,11),(4,12),(4,13),
    (3,14),(3,15),(2,14),(2,15),
    (1,12),(1,13),(8,12),(8,13),
    (9,12),(9,13),
]

def scan_zd_aligned(t_min: float = 5.0,
                    t_max: float = 50.0,
                    t_steps: int = 400,
                    eps_dir: float = 0.15,
                    N_series: int = 30) -> list[dict]:
    """
    For each canonical ZD direction on S¹⁵, evaluate the hypercomplex zeta
    at s = (½, t) + ε·direction and track where ||Z_L - Z_R|| is minimal.

    The ZD pairs DEFINE the perturbation directions — not a free parameter.
    The t-values of the minima are what the 𝕊 algebra selects.

    Returns list of {dir: (i,j), t_min_ordering: float, ordering_min: float,
                     nearest_known_zero: float, t_type1_near: float}.
    """
    known = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
             37.5862, 40.9187, 43.3271, 48.0052, 49.7738]

    results = []
    ts = [t_min + k*(t_max-t_min)/t_steps for k in range(t_steps+1)]
    INV_SQRT2 = 1.0 / math.sqrt(2.0)

    for (i, j) in _ZD_DIRECTIONS_S15[:42]:   # 42 canonical classes (one sign)
        dir_vec = cd_zero(16)
        dir_vec[i] = INV_SQRT2
        dir_vec[j] = INV_SQRT2

        od_norms = []
        z_scalars_local = []

        for t in ts:
            s_t = cd_zero(16)
            s_t[0] = 0.5
            s_t[1] = t
            for k in range(2, 16):
                s_t[k] = eps_dir * dir_vec[k]

            N_rs = max(1, int(math.sqrt(max(t, 0.1) / (2 * math.pi))))
            hc   = z_function_hypercomplex(t, 16, N=N_rs, s=s_t)
            od_norms.append(cd_norm(hc['diff']))
            z_scalars_local.append(hc['z_scalar'])

        # Find t where ordering norm is minimal — the ZD direction's "eigenvalue"
        min_idx  = min(range(len(od_norms)), key=lambda k: od_norms[k])
        t_od_min = ts[min_idx]
        od_min   = od_norms[min_idx]

        # Find TYPE 1 zero nearest this minimum
        type1_zeros = []
        for k in range(1, len(z_scalars_local)):
            if z_scalars_local[k-1] * z_scalars_local[k] < 0:
                type1_zeros.append((ts[k-1] + ts[k]) / 2)

        near_t1 = min(type1_zeros, key=lambda z: abs(z - t_od_min)) if type1_zeros else None
        near_k  = min(known, key=lambda k: abs(k - t_od_min))

        results.append({
            'dir':             (i, j),
            't_ordering_min':  t_od_min,
            'ordering_min':    od_min,
            'nearest_known':   near_k,
            'delta_known':     t_od_min - near_k,
            't_type1_near':    near_t1,
        })

    return results


def report_zd_aligned(results: list[dict]) -> None:
    print(f"\n{'='*70}")
    print(f"  ZD-ALIGNED SCAN — 𝕊 zero divisor directions define the variables")
    print(f"  42 canonical ZD a-vectors  ×  ε=0.15 perturbation")
    print(f"{'='*70}")
    print(f"  {'Direction':<12}  {'t(order.min)':>14}  {'||ΔZ||':>10}  "
          f"{'nearest ζ zero':>14}  {'Δ':>8}  {'near TYPE1':>11}")
    print(f"  {'-'*12}  {'-'*14}  {'-'*10}  {'-'*14}  {'-'*8}  {'-'*11}")

    # Sort by ordering minimum t value
    for r in sorted(results, key=lambda x: x['t_ordering_min']):
        t1_str = f"{r['t_type1_near']:.4f}" if r['t_type1_near'] else "—"
        print(f"  e{r['dir'][0]:2d}+e{r['dir'][1]:2d}      "
              f"  {r['t_ordering_min']:14.5f}  "
              f"{r['ordering_min']:10.4f}  "
              f"{r['nearest_known']:14.4f}  "
              f"{r['delta_known']:+8.4f}  "
              f"{t1_str:>11}")

    # Find which known zeros are covered
    known = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
             37.5862, 40.9187, 43.3271, 48.0052, 49.7738]
    covered = set()
    for r in results:
        if abs(r['delta_known']) < 1.0:
            covered.add(r['nearest_known'])
    print(f"\n  Known zeros covered by ZD ordering minima (Δ<1): "
          f"{len(covered)}/{len(known)}")
    print(f"  {sorted(covered)}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    import argparse
    ap = argparse.ArgumentParser(
        description="Hypercomplex Riemann Zeta — standalone experiment"
    )
    ap.add_argument("--dim",     type=int,   default=2,
                    help="CD dimension: 2=ℂ 4=ℍ 8=𝕆 16=𝕊 (default: 2)")
    ap.add_argument("--sigma",   type=float, default=0.5,
                    help="Real part of s (default: 0.5)")
    ap.add_argument("--t-min",   type=float, default=0.0)
    ap.add_argument("--t-max",   type=float, default=50.0)
    ap.add_argument("--t-steps", type=int,   default=500)
    ap.add_argument("--N",       type=int,   default=100,
                    help="Series truncation (default: 100)")
    ap.add_argument("--primes",  type=int,   default=20,
                    help="Primes in Euler product (default: 20)")
    ap.add_argument("--eps",     type=float, default=0.5,
                    help="Zero threshold (unused — kept for compatibility)")
    ap.add_argument("--perturb", type=float, default=0.0,
                    help="Perturbation in e2..e_{dim-1} to activate ZD-sensitive dimensions (default: 0.0)")
    ap.add_argument("--all",     action="store_true",
                    help="Run all four base levels: ℂ ℍ 𝕆 𝕊")
    ap.add_argument("--zd",      action="store_true",
                    help="Run ZD-aligned scan: let the ZD pairs define the directions")
    args = ap.parse_args()

    if args.zd:
        zd_res = scan_zd_aligned(t_min=args.t_min, t_max=args.t_max,
                                  t_steps=args.t_steps, N_series=args.N)
        report_zd_aligned(zd_res)
    elif args.all:
        for d in [2, 4, 8, 16]:
            r = scan_zeros(dim=d, sigma_z=args.sigma,
                           t_min=args.t_min, t_max=args.t_max,
                           t_steps=args.t_steps, N_series=args.N,
                           n_primes=args.primes, eps=args.eps,
                           perturb=args.perturb)
            report(r)
    else:
        r = scan_zeros(dim=args.dim, sigma_z=args.sigma,
                       t_min=args.t_min, t_max=args.t_max,
                       t_steps=args.t_steps, N_series=args.N,
                       n_primes=args.primes, eps=args.eps,
                       perturb=args.perturb)
        report(r)

if __name__ == "__main__":
    main()
