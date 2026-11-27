"""
ValaQuenta.modules.h_rb_hat.oblique_sigma_rb
============================================
The documented sigma_rb map: a 16-component input ψ (a sedenion; real or native complex) in, a 16-component sigma_rb (a sedenion) out.

    sigma_rb[k] = ψ[k] · conj(ψ[k ⊕ 4])          k = 0..15

The ⊕4 pairing is 0↔4 1↔5 2↔6 3↔7 8↔12 9↔13 10↔14 11↔15, so the output is two 8-vectors:

    sigma_rb_tilt[j] = Re sigma_rb[rep_j]        ⊕4-even, the driven part          rep = (0, 1, 2, 3, 8, 9, 10, 11)
    sigma_rb_axis[j] = Im sigma_rb[rep_j]        ⊕4-odd,  the conserved anchor

and sigma_self (red/(red+blue), the point-shadow of sigma_rb) satisfies  sigma_self = ½ + Σ sigma_rb_tilt / (p_red + p_blue).
For a real ψ the output is real (tilt only) and still has eight independent values: 8 = 1 kept (the mean) + 7 struts.

Provenance: ported 2026-11-25 from ContextPlease/claude/scratchpad/2026-08-31_oblique-gear/oblique_gear_test.py (7/7 pass, 2026-08-31)
and ANOMALY_CHASE.md; strut-blindness and the rectifier law from Ainulindale/wiki/123_sigma_rb_mass_gap_calibration.md (Listing 1).
Tested in tests/test_h_rb_hat_oblique.py. Status: ESTABLISHED (algebra, by construction), the flow saddle: measured, see ANOMALY_CHASE.md.
Not to be confused with sigma16.py, which holds two exploratory lifts that are NOT the documented map.

d* faces (all four are needed to chart ln(10) in Universal Native Space):
  d*         = 0.24600          the value the code runs with (Boundary, σ_ζ=½ plane)
  d*_taut    = 0.246307201473  A_π/ln10, the Flow (radial unit)
  d*_RG      = dimension 8; numeric OPEN, no closed form  the Stability (centre r=0)
  d*_ln(10)  = 0.5671432904   d*_taut·ln10 = A_π, the Translator (log bridge)

Full story of d*: Ainulindale/wiki/17_alpha_omega_d_star.md; ~/.clauderc_canonical_maths @RCCM_FOUR_DSTAR; FourthAgePapers/DStarRG
"""
import math
from typing import List, Sequence, Tuple

from ...engine import constants as _C

SED = 16
REP = (0, 1, 2, 3, 8, 9, 10, 11)
PARTNER = {k: k ^ 4 for k in range(SED)}


def sigma_rb_map(psi: Sequence[complex]) -> List[complex]:
    """The documented map: sigma_rb[k] = psi[k]·conj(psi[k⊕4]).

    :param psi: 16 components (real or complex)
    :returns: the 16-component sigma_rb
    """
    return [complex(psi[k]) * complex(psi[k ^ 4]).conjugate() for k in range(SED)]


def tilt_axis(psi: Sequence[complex]) -> Tuple[List[float], List[float], List[complex]]:
    """sigma_rb_tilt (Re, 8-vector), sigma_rb_axis (Im, 8-vector) and the full 16-vector.

    :param psi: 16 components
    :returns: (tilt, axis, sigma_rb)
    """
    s = sigma_rb_map(psi)
    return [s[j].real for j in REP], [s[j].imag for j in REP], s


def p_red_blue(psi: Sequence[complex]) -> Tuple[float, float]:
    """In-phase (red) and anti-phase (blue) energy over the ⊕4 pairs; red + blue = Σ|ψ|².

    :param psi: 16 components
    :returns: (p_red, p_blue)
    """
    red = blue = 0.0
    for k in REP:
        a, b = complex(psi[k]), complex(psi[k ^ 4])
        red += abs(a + b) ** 2
        blue += abs(a - b) ** 2
    return red / 2.0, blue / 2.0


def sigma_self(psi: Sequence[complex]) -> Tuple[float, float, float]:
    """sigma_self = p_red / (p_red + p_blue), the scalar point-shadow of sigma_rb.

    :param psi: 16 components
    :returns: (sigma_self, p_red, p_blue)
    """
    red, blue = p_red_blue(psi)
    t = red + blue
    return ((red / t) if t else float("nan")), red, blue


def rot_pair(psi: Sequence[complex], j: int, theta: float) -> List[complex]:
    """Rotate the (j, j⊕4) plane by theta (one gear of the train).

    :param psi: 16 components
    :param j: a member of the pair
    :param theta: angle
    :returns: rotated copy of psi
    """
    a, b = j, j ^ 4
    c, s = math.cos(theta), math.sin(theta)
    out = list(psi)
    out[a] = c * psi[a] - s * psi[b]
    out[b] = s * psi[a] + c * psi[b]
    return out


def balance_angle(psi: Sequence[complex], k: int) -> float:
    """The angle theta* that zeroes the tilt of pair k:  cos2θ·Re z + ½ sin2θ·Δ|ψ|² = 0.

    :param psi: 16 components
    :param k: pair representative
    :returns: theta*
    """
    z = psi[k] * complex(psi[k ^ 4]).conjugate()
    d2 = abs(psi[k]) ** 2 - abs(psi[k ^ 4]) ** 2
    return 0.5 * math.atan2(-2 * z.real, d2) if (d2 or z.real) else 0.0


def balanced(psi: Sequence[complex], lam: float = 1.0) -> List[complex]:
    """Rotate every pair a fraction lam of the way to its zero-tilt angle (lam = 1: Σ tilt = 0).

    :param psi: 16 components
    :param lam: 0..1
    :returns: partially or fully balanced copy
    """
    p = list(psi)
    for k in REP:
        p = rot_pair(p, k, lam * balance_angle(p, k))
    return p


def run_train(psi: Sequence[complex], gain: float, steps: int) -> List[complex]:
    """The 8-plane gear train: each pair turned by gain·tilt, repeated (explicit Euler).

    :param psi: 16 components
    :param gain: turn per unit tilt
    :param steps: number of steps
    :returns: final psi
    """
    p = list(psi)
    for _ in range(steps):
        t, _, _ = tilt_axis(p)
        for k in REP:
            p = rot_pair(p, k, gain * t[REP.index(k)])
    return p


def sigma_self_from_tilt(tilt: Sequence[float], energy: float = 1.0) -> float:
    """Strut-blind closed form: with every pair holding energy E, sigma_self = ½ + mean(tilt)/E.

    :param tilt: the 8 tilts
    :param energy: pair energy E
    :returns: sigma_self
    """
    return 0.5 + (sum(tilt) / len(tilt)) / energy


def embed_tilt(tilt: Sequence[float], energy: float = 1.0) -> List[float]:
    """A real ψ with every ⊕4 pair at energy E and Re(a·conj b) = tilt_j (requires |tilt_j| ≤ E/2).

    :param tilt: the 8 tilts
    :param energy: pair energy E
    :returns: the 16-vector ψ (real)
    """
    psi = [0.0] * SED
    for j, t in zip(REP, tilt):
        phi = 0.5 * math.asin(max(-1.0, min(1.0, 2 * t / energy)))
        psi[j], psi[j ^ 4] = math.sqrt(energy) * math.cos(phi), math.sqrt(energy) * math.sin(phi)
    return psi


def rectifier_sigma_self(tilt: Sequence[float]) -> float:
    """The rectifier law for the energy-unnormalised embedding: sigma_self = ½ + 4Δ/Σ|tilt| with Δ = mean tilt (8Δ = Σ tilt).

    :param tilt: the 8 tilts
    :returns: sigma_self
    """
    s = sum(abs(t) for t in tilt)
    return 0.5 + (sum(tilt) / 2.0) / s if s else float("nan")


def onset_residual() -> float:
    """Δ = A_π − d*·ln10 with the working d* (0.000707357533): the number fed into the tilt in wiki 123.

    :returns: Δ
    """
    return _C.A_PI - _C.D_STAR * math.log(10.0)
