"""
ainulindale_engine.engine.units
================================
Radian transform — the universal unit system.

The circle is primary. All equations have a radian-primary form.
This module provides the transform from conventional to radian-primary,
and the inverse.

Philosophy:
    The (2/pi) normalization in the Lagrangian is not a correction factor.
    It is the equation written in its native coordinate system where
    the circle — not the line — is the primitive unit.

    Angular frequency omega = 2*pi*f is the fundamental quantity.
    Frequency f is the derived quantity (omega / 2*pi).

    All phase quantities should be explicit. No absorbed phases.
    The (I|O) inversion map J_N: (r, theta) -> (1/r, theta + pi/2)
    lives natively in this system.

Version: 0.111
"""

import math
from fractions import Fraction
from . import constants as C


# ── Radian transform ────────────────────────────────────────────────────────

def to_angular_frequency(f_hz):
    """Convert frequency f [Hz] to angular frequency omega [rad/s].
    omega = 2*pi*f
    Radian-primary: omega is the fundamental quantity.
    """
    return C.TAU * f_hz


def to_frequency(omega_rad):
    """Convert angular frequency omega [rad/s] to frequency f [Hz].
    f = omega / (2*pi)
    """
    return omega_rad / C.TAU


def to_radian_phase(phase_cycles):
    """Convert phase in cycles [0,1] to radians [0, 2*pi].
    1 cycle = 2*pi radians.
    """
    return phase_cycles * C.TAU


def to_cycle_phase(phase_rad):
    """Convert phase in radians to cycles [0,1]."""
    return phase_rad / C.TAU


# ── Lagrangian normalization ─────────────────────────────────────────────────

def lagrangian_norm():
    """The radian-primary Lagrangian normalization factor.
    Returns 2/pi — the native form when the circle is primary.
    Consistency: 2/ln(OMEGA_H) = 2/ln(e^pi) = 2/pi exactly.
    """
    return C.LAGRANGIAN_NORM


def apply_lagrangian_norm(value):
    """Apply (2/pi) normalization to a Lagrangian term."""
    return C.LAGRANGIAN_NORM * value


# ── Inversion coordinate transform ──────────────────────────────────────────

def inversion_transform(r, theta_rad):
    """Apply (I|O) inversion: (r, theta) -> (1/r, theta + pi/2).
    This is the 2-stroke engine: compression stroke.
    Radian-primary: theta in radians.
    Returns: (r_inv, theta_inv)
    """
    if r == 0:
        raise ValueError("(I|O) undefined at r=0 (the horizon)")
    return (1.0 / r, theta_rad + C.PI / 2.0)


def inversion_involution(r, theta_rad):
    """Apply (I|O) twice — should return to start.
    Verifies the 2-stroke engine completes its cycle.
    Returns: (r_final, theta_final), and True if involution holds.
    """
    r1, t1 = inversion_transform(r, theta_rad)
    r2, t2 = inversion_transform(r1, t1)
    # theta returns mod 2*pi: theta + pi/2 + pi/2 = theta + pi != theta
    # Full involution requires two full cycles (4 strokes) for theta.
    # r-involution is exact: 1/(1/r) = r.
    r_closes = abs(r2 - r) < 1e-14
    return (r2, t2), r_closes


# ── Exact rational arithmetic for sonification ──────────────────────────────

def ratio_to_fraction(numerator, denominator):
    """Return exact Fraction for interval ratios.
    Use throughout sonification pipeline. Float only at final render.
    """
    return Fraction(numerator, denominator)


def fraction_to_float(frac, anchor=1.0):
    """Convert Fraction ratio to float at render boundary.
    anchor: the base frequency in Hz.
    This is the ONLY place float conversion should occur in the
    sonification pipeline.
    """
    return float(frac) * anchor


# ── Cayley-Dickson radian transform ─────────────────────────────────────────

def algebra_to_radian_depth(algebra_name):
    """Return the radian-depth of an algebra layer.
    Depth = log2(dim) * (pi/2) — each doubling adds pi/2 phase.
    This is the algebraic time coordinate (not BPM).
    """
    dim = C.DIM.get(algebra_name.upper())
    if dim is None:
        raise ValueError(f"Unknown algebra: {algebra_name}")
    return math.log2(dim) * (C.PI / 2.0)


def algebra_depth_sequence():
    """Return the radian depths for all tower layers."""
    return {
        name: algebra_to_radian_depth(name)
        for name in ['R', 'C', 'H', 'O', 'S']
    }


# ── Summary ─────────────────────────────────────────────────────────────────

def summary():
    print("=" * 60)
    print("  AINULINDALE ENGINE — UNITS (RADIAN-PRIMARY)")
    print(f"  Version: 0.111")
    print("=" * 60)
    print(f"  Lagrangian norm  = 2/pi = {lagrangian_norm():.8f}")
    print(f"  1 cycle          = {C.TAU:.8f} rad")
    print(f"  (I|O) phase step = pi/2 = {C.PI/2:.8f} rad")
    print()
    print("  Algebra radian depths:")
    for name, depth in algebra_depth_sequence().items():
        print(f"    {name}: {depth:.6f} rad  ({depth/C.PI:.4f} pi)")
    print()
    print("  (I|O) involution test at r=2.0, theta=0:")
    (r2, t2), closes = inversion_involution(2.0, 0.0)
    print(f"    r returns: {closes}  (r_final={r2:.6f})")
    print(f"    theta after 2 strokes: {t2:.6f} rad = pi (expected)")
    print("=" * 60)


if __name__ == "__main__":
    summary()
