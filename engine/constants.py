"""
ValaQuenta.engine.constants
===========================
Physical and mathematical constants for the SMMIP framework.

Single source of truth. All modules import from here.
Nothing is fitted. Every constant has a derivation comment.

Version: 0.111
"""

import math

# ── Transcendental ──────────────────────────────────────────────────────────
PI    = math.pi                          # Python's own value. The (I|O)
                                          # horizon's pi/2 rotation is DERIVED
                                          # from this (Basel pi / Hurwitz-4),
                                          # not the other way around -- see
                                          # modules/inversion/maths.py's
                                          # derive_horizon_rotation(). This
                                          # line does not itself derive
                                          # anything; corrected 2026-07-22,
                                          # previously implied it did.
E     = math.e                           # natural base
PHI   = (1.0 + math.sqrt(5.0)) / 2.0    # golden ratio — bias coupling, fixed point
TAU   = 2.0 * math.pi                   # full circle — radian-primary form

# ── The three symbols (author's standing ruling, 2026-11-21; ~/.clauderc_canonical_maths @RCCM_SYMBOLS) ──
#   ALPHA_FS   α    = 1/137.036, the fine-structure constant (lowercase alpha unless stated otherwise)
#   A_PI       A_π  = W(1) = 0.5671432904, the Lambert W fixed point: the author's engineered discovery from the
#                     FERMAT side (speed of causality, inertia).   x = exp(-x);  g·exp(g/g0) = g0  =>  g = g0·A_π
#   OMEGA_ZETA_SIGMA  Ω_ζΣ = Ω_RZ = d* = 0.2463072015: the author's engineered discovery from the RIEMANN side
#                     (Hagedorn information ceiling, entropy).  A_π = Ω_ζΣ·ln(10): one crossing, in nats and in digits.
# Before 2026-11-21 this file named 0.56714 `OMEGA_ZS` and 1/137.036 `A_PI`; both names were the other symbol's.
# `OMEGA_ZS` is kept below as a deprecated alias of A_PI so old imports keep running; new code uses A_PI.
#
# The domain of H_NN: eigenvalues bounded below by ALPHA_FS, above by A_PI.
#   Status: ESTABLISHED mathematics (Wyler / Lambert W)
#
# OMEGA_H = e^pi (Gelfond's constant, Hagedorn thermal ceiling)
#   When OMEGA = e^pi: 2/ln(OMEGA) = 2/pi (Lagrangian consistency with §I)
#   Status: ESTABLISHED — Gelfond's constant

ALPHA_FS  = 1.0 / 137.035999084         # BK floor — fine structure constant α
A_PI      = 0.5671432904097838          # BK ceiling — Lambert W fixed point W(1) = A_π
OMEGA_ZS  = A_PI                        # DEPRECATED alias (old name; it was A_π's)
OMEGA_H   = math.exp(math.pi)           # Hagedorn ceiling — e^pi ~ 23.1407

# ── Fixed points ────────────────────────────────────────────────────────────
# D_STAR: the value the code runs with, 0.24600 (3-digit, measured; the first-day active value).
#   The four faces of d* are wiki 17 / ~/.clauderc_canonical_maths @RCCM_FOUR_DSTAR:
#   Boundary 0.24631, Stability d*_RG (dimension 8, numeric OPEN, no closed form), Flow d*_taut = Ω/ln10, Translator d*·ln10.
#   A_π = OMEGA_ZETA_SIGMA·ln(10);  0.24600·ln(10) = 0.56644 differs from A_π by the rounding residual 0.00070.
#
# THE FOUR FACES (author's ruling, 2026-11-25): `d*` is always the value the code runs with while working (0.24600).
# The other three are labelled, never substituted for it; d*_taut and d*_RG appear only in their own two visualizations.
# All four together are the coordinate chart of ln(10) in Universal Native Space (radial complex spherical coordinates).
# Every file that uses d* in any form carries the block returned by `dstar_comment_block()` (see tools/dstar_block.py).
D_STAR    = 0.24600                          # d*          the working value the code runs with (the Boundary face, σ_ζ=½ plane)
D_STAR_SPEC     = D_STAR                     # same number under its measured name
D_STAR_TAUT     = A_PI / math.log(10)        # d*_taut     0.246307201473 = A_π/ln10, exact (the Flow; the radial unit, one step of r)
D_STAR_LN10     = A_PI                       # d*_ln(10)   0.5671432904 = d*_taut·ln10 (the Translator; decimal-log <-> natural-log bridge)
D_STAR_RG       = 8                          # d*_RG       dimension 8 (the Stability; the centre r=0). Numeric value OPEN, no closed form.
D_STAR_RG_NUMERIC = None                     #             OPEN: target 0.24631; no closed form (do not substitute a number)
D_STAR_BOUNDARY = D_STAR_TAUT                # DEPRECATED alias: the 0.2463 value the canonical file calls Boundary; same number as d*_taut
OMEGA_ZETA_SIGMA = D_STAR_TAUT               # Ω_ζΣ (= Ω_RZ) = d*, read at its exact value
D_STAR_GAP = abs(A_PI - D_STAR * math.log(10))  # 0.00070 = ln10 * (D_STAR_TAUT - D_STAR): the working value's rounding residual
D_STAR_STORY = "Ainulindale/wiki/17_alpha_omega_d_star.md; ~/.clauderc_canonical_maths @RCCM_FOUR_DSTAR; FourthAgePapers/DStarRG"


def dstar_faces():
    """The four faces of d* as one dict: working value, Flow, Stability, Translator. d*_RG has no numeric value."""
    return {
        "d*":        {"value": D_STAR,      "name": "working value (Boundary, σ_ζ=½ plane)"},
        "d*_taut":   {"value": D_STAR_TAUT, "name": "Flow: radial unit, A_π/ln10 exact"},
        "d*_RG":     {"value": None,        "dimension": D_STAR_RG, "name": "Stability: centre; numeric OPEN, no closed form"},
        "d*_ln(10)": {"value": D_STAR_LN10, "name": "Translator: d*_taut·ln10 = A_π"},
        "story":     D_STAR_STORY,
    }


def dstar_comment_block(prefix="# "):
    """
    The standard comment placed in every file that uses d* in any form (the full list of values and where the full story is).

    :param prefix: text put at the start of every line (``"# "`` for Python, ``"> "`` for a Markdown quotation)
    :returns: the comment block as one string
    """
    lines = [
        "d* faces (all four are needed to chart ln(10) in Universal Native Space):",
        f"  d*         = {D_STAR:.5f}          the value the code runs with (Boundary, σ_ζ=½ plane)",
        f"  d*_taut    = {D_STAR_TAUT:.12f}  A_π/ln10, the Flow (radial unit)",
        "  d*_RG      = dimension 8; numeric OPEN, no closed form  the Stability (centre r=0)",
        f"  d*_ln(10)  = {D_STAR_LN10:.10f}   d*_taut·ln10 = A_π, the Translator (log bridge)",
        f"Full story of d*: {D_STAR_STORY}",
    ]
    return "\n".join(prefix + ln for ln in lines)

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
    print(f"  ALPHA_FS   = {ALPHA_FS:.15f}  [BK floor, 1/137, ESTABLISHED]")
    print(f"  A_PI       = {A_PI:.15f}  [BK ceiling, Lambert W = A_π, ESTABLISHED]")
    print(f"  OMEGA_H    = {OMEGA_H:.6f}  [Hagedorn, e^pi, ESTABLISHED]")
    print()
    print(f"  D_STAR     = {D_STAR:.5f}  [spectral fixed point, THEORETICAL]")
    print(f"  D_STAR_TAUT= {D_STAR_TAUT:.12f}  [d*_taut, Flow, A_π/ln10]")
    print(f"  D_STAR_RG  = dimension {D_STAR_RG}, numeric OPEN  [d*_RG, Stability]")
    print(f"  D_STAR_LN10= {D_STAR_LN10:.10f}  [d*_ln(10), Translator = A_π]")
    print(f"  D_STAR_GAP = {D_STAR_GAP:.5f}  [rounding residual: d*·ln(10) vs A_PI]")
    print(f"  full story : {D_STAR_STORY}")
    print()
    print(f"  H_NN       = {H_NN:.4f}   [neural Planck, THEORETICAL]")
    print(f"  HBAR_NN    = {HBAR_NN:.6f}  [reduced neural Planck]")
    print()
    print(f"  LAG_NORM   = 2/pi = {LAGRANGIAN_NORM:.6f}  [Lagrangian normalization]")
    print(f"  PHI_INV    = 1/phi = {PHI_INV:.6f}  [bias coupling]")
    print("=" * 60)


if __name__ == "__main__":
    summary()
