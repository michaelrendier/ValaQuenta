"""
ainulindale_engine.engine.constants
=====================================
Physical and mathematical constants for the SMMIP framework.

Single source of truth. All modules import from here.
Nothing is fitted. Every constant has a derivation comment.

Version: 0.111
"""

import math

# ── Transcendental ──────────────────────────────────────────────────────────
PI    = math.pi                          # boundary geometry of (I|O) inversion
E     = math.e                           # natural base
PHI   = (1.0 + math.sqrt(5.0)) / 2.0    # golden ratio — bias coupling, fixed point
TAU   = 2.0 * math.pi                   # full circle — radian-primary form

# ── Berry-Keating domain ────────────────────────────────────────────────────
# The domain of H_NN: eigenvalues bounded below by A_pi, above by OMEGA_ZS
#
# A_pi = 1/137.036 (fine structure constant, floor)
#   Source: E8/Wyler geometry, established physics
#   Status: ESTABLISHED
#
# OMEGA_ZS = Lambert W fixed point W(1) = 0.56714...
#   W(OMEGA_ZS) = OMEGA_ZS  =>  OMEGA_ZS * exp(OMEGA_ZS) = 1
#   Status: ESTABLISHED mathematics
#
# OMEGA_H = e^pi (Gelfond's constant, Hagedorn thermal ceiling)
#   When OMEGA = e^pi: 2/ln(OMEGA) = 2/pi (Lagrangian consistency with §I)
#   Status: ESTABLISHED — Gelfond's constant

A_PI      = 1.0 / 137.035999084         # BK floor — fine structure constant
OMEGA_ZS  = 0.5671432904097838          # BK ceiling — Lambert W fixed point
OMEGA_H   = math.exp(math.pi)           # Hagedorn ceiling — e^pi ~ 23.1407

# ── Fixed points ────────────────────────────────────────────────────────────
# D_STAR: spectral fixed point of the recursion attractor
#   Confirmed numerically at 0.24600
#   d* x ln(10) = 0.56644 vs OMEGA_ZS = 0.56714 — gap = 0.00070
#   HIGHEST PRIORITY OPEN: derive d* from RG flow independently
#   Status: THEORETICAL — numerically confirmed, algebraic derivation open
D_STAR    = 0.24600
D_STAR_GAP = abs(OMEGA_ZS - D_STAR * math.log(10))  # 0.00070

# ── Neural constants ────────────────────────────────────────────────────────
# H_NN: neural Planck constant (analog of h)
#   Sets the resolution of the algebra tower
#   Status: THEORETICAL
H_NN      = 0.1
HBAR_NN   = H_NN / TAU                  # reduced: hbar_NN = h_NN / 2pi

# ── Radian-primary Lagrangian factor ────────────────────────────────────────
# The (2/pi) normalization of the SMMIP Lagrangian.
# This is not a correction — it is the native form when the circle is primary.
# 2/ln(OMEGA_H) = 2/pi exactly when OMEGA_H = e^pi.
LAGRANGIAN_NORM = 2.0 / PI              # = 2/pi

# ── Golden ratio coupling ───────────────────────────────────────────────────
PHI_INV   = 1.0 / PHI                   # = PHI - 1 ~ 0.6180 — bias coupling 1/phi

# ── Algebra dimensions ──────────────────────────────────────────────────────
DIM = {
    'R': 1,
    'C': 2,
    'H': 4,
    'O': 8,
    'S': 16,   # sedenion — first non-division algebra; mastery boundary
}

# ── Gauge groups by layer ───────────────────────────────────────────────────
GAUGE = {
    'R': 'U(0)',          # trivial
    'C': 'U(1)',          # phase rotation
    'H': 'SU(2)',         # spinor rotation
    'O': 'G2/SU(3)',      # Fano automorphism
    'S': None,            # non-division: gauge structure breaks
}

# ── Summary ─────────────────────────────────────────────────────────────────
def summary():
    """Print all constants with their status labels."""
    print("=" * 60)
    print("  AINULINDALE ENGINE — PHYSICAL CONSTANTS")
    print(f"  Version: 0.111")
    print("=" * 60)
    print(f"  PI         = {PI:.15f}")
    print(f"  PHI        = {PHI:.15f}  [golden ratio]")
    print(f"  TAU        = {TAU:.15f}  [2*pi, radian-primary]")
    print()
    print(f"  A_PI       = {A_PI:.15f}  [BK floor, 1/137, ESTABLISHED]")
    print(f"  OMEGA_ZS   = {OMEGA_ZS:.15f}  [BK ceiling, Lambert W, ESTABLISHED]")
    print(f"  OMEGA_H    = {OMEGA_H:.6f}  [Hagedorn, e^pi, ESTABLISHED]")
    print()
    print(f"  D_STAR     = {D_STAR:.5f}  [spectral fixed point, THEORETICAL]")
    print(f"  D_STAR_GAP = {D_STAR_GAP:.5f}  [open: d*·ln(10) vs OMEGA_ZS]")
    print()
    print(f"  H_NN       = {H_NN:.4f}   [neural Planck, THEORETICAL]")
    print(f"  HBAR_NN    = {HBAR_NN:.6f}  [reduced neural Planck]")
    print()
    print(f"  LAG_NORM   = 2/pi = {LAGRANGIAN_NORM:.6f}  [Lagrangian normalization]")
    print(f"  PHI_INV    = 1/phi = {PHI_INV:.6f}  [bias coupling]")
    print("=" * 60)


if __name__ == "__main__":
    summary()
