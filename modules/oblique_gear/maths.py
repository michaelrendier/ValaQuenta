r"""
ValaQuenta.modules.oblique_gear.maths
========================================
The Oblique Gear, tested across scale — does the black-hole-scale crank
angle (h_rb_hat's `oblique_crank()`, arctan(d\*), the Witches Hat half-angle,
2026-06-17) govern the galaxy-scale rotation curve (`ValaQuenta/
galactic_cavity.py`'s Stokes-drift arctan profile, SPARC-confirmed
p=0.794) as the SAME mechanism, or merely the same constant?

Born 2026-09-26 from `FourthAgePapers/ChiralityBlackHole/README.md`'s
second claim (Cody: "one is the witches hat, the other is a galaxy. the
dependent structure is the oblique gearing"). That paper's own rule is
strict: a claim is either shown running in code, or the paper isn't done.
This module is that check, run honestly -- including where it fails.

WHAT IS ALREADY ESTABLISHED (not re-derived here, only reused)::

  - Black-hole side: theta_crank = arctan(d*) ~ 13.82 deg, the Witches Hat
    half-angle, "not a tuning parameter" (h_rb_hat/maths.py, ESTABLISHED
    2026-06-17).
  - Galaxy side: v(r) = v_flat * (2/pi) * arctan(r/r_t), r_t = d* * R_max,
    confirmed against 175 SPARC galaxies (galactic_cavity.py, mean 0.249
    vs prediction 0.246, p=0.794).
  - Both keyed to the same D_STAR value (0.2460 / 0.24600 -- h_rb_hat/
    maths.py and engine/constants.py each declare it independently, a
    pre-existing duplication, not touched here). This module imports
    D_STAR from h_rb_hat.maths specifically, so theta_crank below is
    exactly the value h_rb_hat's own ESTABLISHED crank-angle result uses,
    not a separately-sourced copy.

WHAT THIS MODULE ACTUALLY TESTS (new, 2026-09-26)::

  Is theta_crank the TANGENT ANGLE of the (dimensionless) galaxy rotation
  curve at its own transition point r=r_t, rather than merely a value both
  sides reference? That would make the two `arctan` usages the same fact
  twice, matching this paper's own bar for its first claim (Fano-plane
  orientation / Schwarzschild SIGN flip).

RESULT (computed, sympy-verified, 2026-09-26): REFUTED as stated.

::

  Dimensionless galaxy curve: y(x) = (2/pi)*atan(x), x = r/r_t.
  dy/dx at x=1 (r=r_t) = 1/pi ~ 0.3183 -> tangent angle ~ 17.657 deg.
  theta_crank = arctan(d*) ~ 13.820 deg.
  Difference: ~3.837 deg -- real, not a rounding artifact.
  The radius where the tangent angle WOULD equal theta_crank solves to
  x ~ 1.2601 (r ~ 1.26 * r_t) -- checked against phi, sqrt(pi/2), cbrt(2),
  1/d*; none match to a precision better than d*'s own input precision
  (3 decimal places), so this is not treated as a second hidden constant,
  it is treated as an unremarkable root of the equation being solved.

WHAT SURVIVES: the shared-constant, shared-arctan-family observation is
real (both sides independently confirmed, long before this module), but it
is NOT independent evidence of a single shared mechanism -- d\* is already
claimed as a broadly universal constant across this framework (see
feedback_0rb_scope_discipline), so its appearance on both sides is
consistent with, not proof of, "one dependent oblique-gear structure."
The TANGENT-ANGLE formulation of that stronger claim is the one thing
actually tested here, and it does not hold.

Version: 0.1 -- first build, one honest negative result.
"""

from __future__ import annotations

import math
from typing import Any, Dict

from ..h_rb_hat.maths import D_STAR  # the exact value oblique_crank() uses


# ── black-hole side (reused, not re-derived) ────────────────────────────────

def crank_angle_deg() -> float:
    r"""
    theta_crank = arctan(d\*), the Witches Hat half-angle. h_rb_hat's own
    result, reused here only so both sides of the comparison are computed
    in one place.
    """
    return math.degrees(math.atan(D_STAR))


# ── galaxy side (dimensionless form of galactic_cavity.py's stokes_velocity) ─

def stokes_dimensionless(x: float) -> float:
    r"""
    y(x) = (2/pi) \* atan(x)  -- v(r)/v_flat with x = r/r_t.
    Same function as ValaQuenta/galactic_cavity.py's stokes_velocity(),
    non-dimensionalised so its slope is directly comparable (as an angle)
    to theta_crank, which is dimensionless by construction.

    :param x: r / r_t
    :returns: (2/π)·atan(x)
    """
    return (2.0 / math.pi) * math.atan(x)


def stokes_tangent_angle_deg(x: float) -> float:
    """
    The tangent angle of the dimensionless rotation curve at x = r/r_t.
    dy/dx = (2/pi) / (1+x^2); angle = arctan(dy/dx).

    :param x: r / r_t
    :returns: the tangent angle, in degrees
    """
    slope = (2.0 / math.pi) / (1.0 + x * x)
    return math.degrees(math.atan(slope))


# ── the actual cross-scale check ────────────────────────────────────────────

def crank_vs_galaxy_tangent_check() -> Dict[str, Any]:
    """
    Tests: is theta_crank the tangent angle of the galaxy curve AT r=r_t
    (x=1)? Reports the exact computed numbers either way -- this is the
    check itself, not a claim about its outcome.
    """
    theta_crank = crank_angle_deg()
    theta_galaxy_at_rt = stokes_tangent_angle_deg(1.0)
    diff = theta_galaxy_at_rt - theta_crank
    # Tolerance: generous, 0.5 deg -- if it's the same fact, it should be
    # exact up to d*'s own input precision, not merely "in the neighbourhood."
    matches = abs(diff) < 0.5
    return {
        'theta_crank_deg':          theta_crank,
        'theta_galaxy_at_rt_deg':   theta_galaxy_at_rt,
        'difference_deg':           diff,
        'matches':                  matches,
        'verdict': ('SAME FACT TWICE — tangent angle equals crank angle at r=r_t'
                    if matches else
                    'REFUTED AS STATED — real ~{:.3f} deg gap, not a rounding artifact'
                    .format(abs(diff))),
        'confidence': 'OPEN:CALCULATED',
        'what_survives': ('Both sides independently keyed to the same d*, both use '
                           'arctan to convert an unbounded ratio into a bounded angle '
                           '-- a real structural kinship, not proof of one mechanism. '
                           'd* is already claimed broadly universal across this '
                           'framework, so shared-constant alone is expected, not new '
                           'evidence.'),
    }


def find_matching_radius() -> Dict[str, Any]:
    r"""
    Solves for x = r/r_t such that the galaxy curve's tangent angle at x
    equals theta_crank exactly. Reports the root and checks it against a
    short list of named constants -- honestly, as "no match found" if none
    fit to better precision than d\*'s own 3-decimal input.

    2/(pi\*(1+x^2)) = d\*  =>  x = sqrt(2/(pi\*d\*) - 1)
    """
    x = math.sqrt(2.0 / (math.pi * D_STAR) - 1.0)
    candidates = {
        'phi (golden ratio)': (1 + math.sqrt(5)) / 2,
        'sqrt(pi/2)':          math.sqrt(math.pi / 2),
        'cbrt(2)':             2.0 ** (1.0 / 3.0),
        '1/d*':                1.0 / D_STAR,
    }
    nearest_name, nearest_val = min(candidates.items(), key=lambda kv: abs(kv[1] - x))
    nearest_gap = abs(nearest_val - x)
    return {
        'x_solution':        x,
        'r_over_r_t':        x,
        'nearest_candidate': nearest_name,
        'nearest_value':     nearest_val,
        'gap':               nearest_gap,
        'significant':       nearest_gap < 1e-4,  # tighter than d*'s 3-dp input warrants
        'note': ('No candidate matches tighter than d*\'s own input precision -- '
                 'treated as an unremarkable root, not a second hidden constant.'),
    }


def full_report() -> Dict[str, Any]:
    """Everything this module currently knows, in one call."""
    return {
        'black_hole_side': {
            'source': 'h_rb_hat/maths.py::oblique_crank()',
            'theta_crank_deg': crank_angle_deg(),
            'd_star': D_STAR,
            'status': 'ESTABLISHED — 2026-06-17',
        },
        'galaxy_side': {
            'source': 'ValaQuenta/galactic_cavity.py::stokes_velocity()',
            'form': 'v(r) = v_flat * (2/pi) * atan(r/r_t),  r_t = d* * R_max',
            'sparc_confirmation': 'mean d_ratio 0.249 vs prediction 0.246, p=0.794, 175 galaxies',
            'status': 'ESTABLISHED — confirmed against SPARC',
        },
        'cross_scale_check': crank_vs_galaxy_tangent_check(),
        'matching_radius_probe': find_matching_radius(),
    }
