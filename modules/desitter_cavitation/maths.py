"""
ValaQuenta.modules.desitter_cavitation.maths
============================================
The De Sitter Cavitation engine — pure calculation, no simulation.

CLAIM (Fourth Age paper "No Singularity"):
    The interior of a black hole is not a singularity.  It is a finite,
    sub-Planckian de Sitter core — the Abrikosov vortex core made
    gravitational: the arithmetic/spectral condensate goes to zero
    (a Riemann zero / a vortex core, winding number 1) while density,
    pressure and curvature stay finite.  Over the hole's life the core
    releases stiff space (metric / Λ-signed) and stiff matter (radiative),
    and at evaporation it unwraps completely — the De Sitter Cavitation.

HOLCUS PREDICTION (pre-registered):
    The maximum curvature inside any black hole is the de Sitter Kretschmann
    scalar evaluated at L_dS = r_s:

        K_core(M) = 24 / L_dS(M)^4 = (3/2) · c^8 / (G^4 M^4)

    — mass-dependent, scaling as M^-4, finite for all M > 0, and
    sub-Planckian for every black hole with M > m_Pl.  A ringdown-echo
    delay of order the interior light-crossing time r_s/c is its
    observational shadow.

    FALSIFIER: a core curvature that either diverges (classical GR
    singularity) or pins to the Planck value K_Pl independent of M
    (limiting-curvature / Planck-star).  Observationally: no ringdown
    echoes to the reflectivity bound a finite core requires.

This module is CALCULATION not SIMULATION: closed-form scalars, ratios and
timescales.  No ODE integration, no field solve.

Protocol requirements honoured:
  - Pure Python 3, stdlib only (math, fractions).  No numpy in this file.
  - Exact ratios via fractions.Fraction; float only at the output boundary.
  - Every formulary entry carries a confidence tier and a radian-primary form
    (see tools.py).

Version: 0.100 — 2026-08-30
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Dict, List

# ── Physical constants (SI; CODATA 2018 where not exact) ─────────────────────
# Provenance: c and k_B are exact by SI definition; G, ħ from CODATA 2018.
C_LIGHT   = 299_792_458.0                 # m/s        (exact)
G_NEWTON  = 6.674_30e-11                  # m^3 kg^-1 s^-2
H_BAR     = 1.054_571_817e-34             # J s
K_BOLTZ   = 1.380_649e-23                 # J/K        (exact)
M_SUN     = 1.988_92e30                   # kg

# ── Planck scale (derived) ──────────────────────────────────────────────────
L_PLANCK   = math.sqrt(H_BAR * G_NEWTON / C_LIGHT**3)      # ~1.616e-35 m
T_PLANCK   = L_PLANCK / C_LIGHT                            # ~5.391e-44 s
M_PLANCK   = math.sqrt(H_BAR * C_LIGHT / G_NEWTON)        # ~2.176e-8 kg
RHO_PLANCK = C_LIGHT**5 / (H_BAR * G_NEWTON**2)           # J/m^3, ~4.6e113
# Planck Kretschmann scale: K ~ 1/L_Pl^4 = c^6 / (ħ G)^2
K_PLANCK   = C_LIGHT**6 / (H_BAR * G_NEWTON)**2           # m^-4, ~2.3e139

# ── Ainulindale constants (provenance: ~/.clauderc_canonical_maths) ─────────
OMEGA_ZS = 0.567_143_290_409_783_8        # Lambert W(1); W·e^W = 1 exactly
D_STAR   = 0.246_00                       # BK spectral d* (5 sig figs)
GAP      = OMEGA_ZS - D_STAR * math.log(10.0)   # Yang-Mills gap ≈ 7.0736e-4

# ── QGP / deconfinement threshold (lattice QCD; Bazavov et al.) ────────────
QGP_ENERGY_DENSITY = 1.6e35               # J/m^3  ≈ 1 GeV/fm^3
QGP_TEMPERATURE    = 2.0e12               # K      ≈ 170 MeV

# Bounce-time coefficient family (Haggard–Rovelli / Rovelli–Vidotto).
# The "short" bounce τ ~ (M/m_Pl)^2 t_Pl is used as the default; a linear
# family τ ~ (M/m_Pl) t_Pl is offered for contrast.  Coefficient is O(1) and
# model dependent — flagged THEORETICAL.
_BOUNCE_EXPONENT_DEFAULT = 2


# ══════════════════════════════════════════════════════════════════════════════
#  1. Horizon, core radius, interior timescale
# ══════════════════════════════════════════════════════════════════════════════

def r_schwarzschild(M: float) -> float:
    """r_s = 2 G M / c^2.  ESTABLISHED (Schwarzschild 1916)."""
    return 2.0 * G_NEWTON * M / C_LIGHT**2


def L_desitter(M: float) -> float:
    """
    Interior de Sitter radius.  Gravastar matching (Mazur–Mottola 2001):
    the interior de Sitter metric 1 − (r/L)^2 joins Schwarzschild 1 − r_s/r
    at the shell r ≈ r_s, forcing  L_dS = r_s.  ESTABLISHED (matching identity).
    """
    return r_schwarzschild(M)


def H_desitter(M: float) -> float:
    """Interior de Sitter Hubble rate H = c / L_dS = c^3 / (2 G M)."""
    return C_LIGHT / L_desitter(M)


def tau_interior(M: float) -> float:
    """
    Interior BANG time = one e-fold of the de Sitter core
        τ = 1/H_dS = L_dS/c = r_s/c = 2 G M / c^3.
    The core cannot 'sit there': it doubles on a light-crossing time.
    ESTABLISHED (de Sitter kinematics).  Radian-primary: one radian of
    expansion phase.
    """
    return L_desitter(M) / C_LIGHT


# ══════════════════════════════════════════════════════════════════════════════
#  2. The Holcus prediction — core curvature is finite and de Sitter
# ══════════════════════════════════════════════════════════════════════════════

def kretschmann_core(M: float) -> float:
    """
    HOLCUS.  Maximum curvature invariant inside the hole = the de Sitter
    Kretschmann scalar  R_abcd R^abcd = 24 / L^4  at L = L_dS = r_s:

        K_core(M) = 24 / r_s^4 = (3/2) · c^8 / (G^4 M^4)          [m^-4]

    Finite for every M > 0.  Scales as M^-4.  Contrast the Schwarzschild
    interior, K = 48 G^2 M^2 / (c^4 r^6) → ∞ as r → 0.
    Confidence: ESTABLISHED as a de Sitter identity; THEORETICAL as the
    claim that this is what a real interior realises.
    """
    L = L_desitter(M)
    # exact rational prefactor 24, kept symbolic until the float boundary
    return float(Fraction(24)) / L**4


def kretschmann_core_closed(M: float) -> float:
    """Same number via the closed form (3/2) c^8 / (G^4 M^4) — cross-check."""
    return float(Fraction(3, 2)) * C_LIGHT**8 / (G_NEWTON**4 * M**4)


def kretschmann_schwarzschild(M: float, r: float) -> float:
    """
    Schwarzschild Kretschmann K(r) = 48 G^2 M^2 / (c^4 r^6).  Provided for
    contrast only: it is what DIVERGES at r → 0 in the singular solution.
    ESTABLISHED.
    """
    return 48.0 * G_NEWTON**2 * M**2 / (C_LIGHT**4 * r**6)


def kretschmann_ratio_planck(M: float) -> float:
    """K_core(M) / K_Planck.  < 1 ⟺ the core is sub-Planckian (smooth)."""
    return kretschmann_core(M) / K_PLANCK


def planck_mass_crossover() -> Dict[str, float]:
    """
    The single mass at which K_core = K_Planck.  Solve
        (3/2) c^8 / (G^4 M^4) = c^6 / (ħ G)^2
    ⟹ M^4 = (3/2) ħ^2 c^2 / G^2  ⟹ M = (3/2)^{1/4} · m_Pl.
    Below this the core would be Planck-curved; every astrophysical and
    primordial hole is far above it.  ESTABLISHED (algebra).
    """
    M_cross = (1.5) ** 0.25 * M_PLANCK
    return {
        'M_crossover_kg':      M_cross,
        'M_crossover_over_mPl': M_cross / M_PLANCK,
        'note': 'K_core = K_Planck only here; M > this ⟹ sub-Planckian core',
    }


# ══════════════════════════════════════════════════════════════════════════════
#  3. Stiff space / stiff matter — the two release channels
# ══════════════════════════════════════════════════════════════════════════════

def stiff_matter_ceiling() -> Dict[str, object]:
    """
    The stiffest causal equation of state: p = ρ c^2, sound speed c_s = c
    (Zel'dovich 1961).  No state is more incompressible without superluminal
    sound.  This is the 'stiff matter' channel's ceiling; the gravastar
    shell is modelled at exactly this EoS.  ESTABLISHED.
    """
    return {
        'eos':            'p = rho * c^2',
        'sound_speed_over_c': 1.0,
        'note': ('stiffest causal state; the incompressibility ceiling. '
                 'The de Sitter core itself is p = -rho c^2 (Lambda-signed) '
                 '— the "stiff space" channel.'),
    }


def core_energy_density(M: float) -> float:
    """
    Energy density of the de Sitter core (the stiff-space channel):
        ρ_dS c^2 = 3 c^4 / (8π G L_dS^2) = 3 c^8 / (32π G^3 M^2)   [J/m^3]
    Scales as M^-2.  ESTABLISHED (de Sitter).
    """
    L = L_desitter(M)
    return 3.0 * C_LIGHT**4 / (8.0 * math.pi * G_NEWTON * L**2)


def reheating_reaches_qgp(M: float) -> bool:
    """
    Does the core's energy density reach the quark–gluon deconfinement
    threshold (~1 GeV/fm^3)?  True for stellar & low-intermediate mass,
    False for supermassive.  ENGINEERING calculation.
    """
    return core_energy_density(M) >= QGP_ENERGY_DENSITY


def energy_partition(M: float, space_fraction: float | None = None) -> Dict[str, float]:
    """
    SECONDARY prediction (CONJECTURE).  Over the full lifetime the
    mass-energy Mc^2 partitions into a stiff-space (metric / Λ-signed)
    channel and a stiff-matter (radiative) channel.  Default split is the
    Ainulindale boundary constant:

        E_space  / E_total = 1 − d*  = 0.75400
        E_matter / E_total =     d*  = 0.24600

    space_fraction overrides the split so 01_predictions.ipynb can test
    alternatives (½, Ω_ZS, 1−Ω_ZS, …).
    """
    f = (1.0 - D_STAR) if space_fraction is None else float(space_fraction)
    E_total = M * C_LIGHT**2
    return {
        'space_fraction':  f,
        'matter_fraction': 1.0 - f,
        'E_total_J':       E_total,
        'E_space_J':       f * E_total,
        'E_matter_J':      (1.0 - f) * E_total,
        'basis': ('1 - d* (default)' if space_fraction is None
                  else 'caller-supplied'),
    }


# ══════════════════════════════════════════════════════════════════════════════
#  4. Hawking / de Sitter temperatures, lifetimes, bounce & echo
# ══════════════════════════════════════════════════════════════════════════════

def T_hawking(M: float) -> float:
    """T_H = ħ c^3 / (8π G M k_B).  ESTABLISHED (Hawking 1975)."""
    return H_BAR * C_LIGHT**3 / (8.0 * math.pi * G_NEWTON * M * K_BOLTZ)


def T_desitter(M: float) -> float:
    """
    de Sitter temperature of the core horizon:
        T_dS = ħ H_dS / (2π k_B) = ħ c^3 / (4π G M k_B) = 2 · T_H(M).
    Both go as c^3/GM — the core inherits the hole's temperature scale,
    exactly doubled.  ESTABLISHED (Gibbons–Hawking 1977).
    """
    return H_BAR * H_desitter(M) / (2.0 * math.pi * K_BOLTZ)


def t_evaporation(M: float) -> float:
    """
    Hawking evaporation time, t_evap = 5120π G^2 M^3 / (ħ c^4)
    (geometric-optics, massless-photon coefficient).  ESTABLISHED to the
    prefactor's model dependence.
    """
    return 5120.0 * math.pi * G_NEWTON**2 * M**3 / (H_BAR * C_LIGHT**4)


def t_bounce_exterior(M: float, exponent: int = _BOUNCE_EXPONENT_DEFAULT) -> float:
    """
    Exterior-frame delay before the black→white bounce, τ ~ (M/m_Pl)^n t_Pl.
    n = 2 (default, 'short' bounce — Haggard–Rovelli): observationally live
    only at primordial mass.  n = 1 gives the 'long' family (≈ Hawking).
    Coefficient O(1), model dependent.  THEORETICAL.
    """
    return (M / M_PLANCK) ** exponent * T_PLANCK


def echo_delay(M: float) -> float:
    """
    Ringdown-echo delay for a reflective core at proper distance ~ℓ_Pl inside
    the light ring (Cardoso–Pani ECO estimate):

        Δt_echo ≈ (2 r_s / c) · ln(r_s / ℓ_Pl)

    i.e. of order the interior light-crossing time τ_interior, log-enhanced.
    The observational shadow of "there is a core to reflect off".
    THEORETICAL (coefficient model dependent).
    """
    rs = r_schwarzschild(M)
    return (2.0 * rs / C_LIGHT) * math.log(rs / L_PLANCK)


# ══════════════════════════════════════════════════════════════════════════════
#  5. The no-singularity check
# ══════════════════════════════════════════════════════════════════════════════

def no_singularity_check(masses_kg: List[float] | None = None) -> Dict[str, object]:
    """
    THEORETICAL.  Verify, across a mass sweep, the three properties the
    no-singularity claim requires of K_core(M):

      (a) FINITE     — K_core(M) < ∞ for every M > 0
      (b) M^-4       — K_core scales as M^-4 (ratio test between rungs)
      (c) SUB-PLANCK — K_core(M) < K_Planck for every M > m_Pl crossover

    and the contrast property:

      (d) the Schwarzschild interior K(r) → ∞ as r → 0  (the thing the
          claim denies is realised)

    Returns a scorecard.  This is a CHECK of internal consistency, not a
    proof that nature picks this interior.
    """
    if masses_kg is None:
        masses_kg = [1e12, 10 * M_SUN, 1e4 * M_SUN, 1e9 * M_SUN]
    masses_kg = sorted(masses_kg)

    finite = all(math.isfinite(kretschmann_core(M)) and kretschmann_core(M) > 0
                 for M in masses_kg)

    # M^-4: K(M1)/K(M2) should equal (M2/M1)^4
    m4_ok = True
    m4_detail = []
    for i in range(len(masses_kg) - 1):
        M1, M2 = masses_kg[i], masses_kg[i + 1]
        ratio_K = kretschmann_core(M1) / kretschmann_core(M2)
        ratio_pred = (M2 / M1) ** 4
        rel = abs(ratio_K - ratio_pred) / ratio_pred
        m4_ok &= rel < 1e-9
        m4_detail.append({'M1': M1, 'M2': M2, 'K_ratio': ratio_K,
                          'M4_pred': ratio_pred, 'rel_err': rel})

    cross = planck_mass_crossover()['M_crossover_kg']
    subplanck = all(kretschmann_ratio_planck(M) < 1.0
                    for M in masses_kg if M > cross)

    # contrast: Schwarzschild K at shrinking r for the stellar case
    M0 = 10 * M_SUN
    sch = [(r, kretschmann_schwarzschild(M0, r))
           for r in (r_schwarzschild(M0), r_schwarzschild(M0) * 1e-3,
                     r_schwarzschild(M0) * 1e-9)]
    sch_diverges = sch[-1][1] > sch[0][1] * 1e40

    verdict = finite and m4_ok and subplanck and sch_diverges
    return {
        'claim': 'No singularity: K_core is finite, M^-4, sub-Planckian; '
                 'the Schwarzschild K→∞ is the artifact the claim denies.',
        'finite':               finite,
        'scales_as_M_minus_4':  m4_ok,
        'sub_planckian_above_crossover': subplanck,
        'schwarzschild_diverges_at_r0':  sch_diverges,
        'M_crossover_over_mPl': cross / M_PLANCK,
        'm4_detail':            m4_detail,
        'schwarzschild_contrast': sch,
        'PASS':                 verdict,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  6. Mass-class engineering table  (the paper's engineering portion)
# ══════════════════════════════════════════════════════════════════════════════

_CLASSES = [
    ('kugelblitz / primordial', 1e12),
    ('stellar (10 M_sun)',      10 * M_SUN),
    ('intermediate (1e4 M_sun)', 1e4 * M_SUN),
    ('supermassive (1e9 M_sun)', 1e9 * M_SUN),
]


def mass_class_table() -> List[Dict[str, object]]:
    """
    ENGINEERING (ESTABLISHED — all closed form).  One row per black-hole
    class, with every quantity the paper quotes.
    """
    rows = []
    for label, M in _CLASSES:
        rows.append({
            'class':                 label,
            'M_kg':                  M,
            'M_over_Msun':           M / M_SUN,
            'r_s_m':                 r_schwarzschild(M),
            'tau_interior_s':        tau_interior(M),
            'T_hawking_K':           T_hawking(M),
            'T_desitter_K':          T_desitter(M),
            't_evaporation_s':       t_evaporation(M),
            't_evaporation_yr':      t_evaporation(M) / 3.15576e7,
            't_bounce_exterior_s':   t_bounce_exterior(M),
            'kretschmann_core_m^-4': kretschmann_core(M),
            'K_core_over_K_Planck':  kretschmann_ratio_planck(M),
            'core_energy_density_Jm3': core_energy_density(M),
            'reaches_QGP':           reheating_reaches_qgp(M),
            'echo_delay_s':          echo_delay(M),
        })
    return rows


# ══════════════════════════════════════════════════════════════════════════════
#  7. Cosmic cavitation budget  (SECONDARY — expected to fall short)
# ══════════════════════════════════════════════════════════════════════════════

def cosmic_cavitation_budget(omega_bh: float = 1.0e-5,
                             space_fraction: float | None = None) -> Dict[str, float]:
    """
    SECONDARY (CONJECTURE, expected FALSIFIED-as-stated, kept in data).

    Naive accounting: if the present black-hole mass density is Ω_BH of the
    critical density, and a fraction (1 − d*) of each hole's mass-energy is
    eventually released into the stiff-space (Λ-signed) channel, the
    cumulative contribution to Ω_Λ is

        Ω_cav ≈ Ω_BH · (1 − d*)

    Observed Ω_Λ ≈ 0.6847 (Planck 2018).  The ratio Ω_cav / Ω_Λ is the
    scorecard.  A value ≪ 1 means the naive budget does not source dark
    energy — the mechanism may still matter (it is directional and
    cumulative → a dark-flow rather than dark-energy signature) but the
    magnitude fails as written.
    """
    f = (1.0 - D_STAR) if space_fraction is None else float(space_fraction)
    OMEGA_LAMBDA_OBS = 0.6847
    omega_cav = omega_bh * f
    return {
        'omega_bh_assumed':   omega_bh,
        'space_fraction':     f,
        'omega_cavitation':   omega_cav,
        'omega_lambda_obs':   OMEGA_LAMBDA_OBS,
        'ratio_to_lambda':    omega_cav / OMEGA_LAMBDA_OBS,
        'verdict': ('reaches Omega_Lambda' if omega_cav / OMEGA_LAMBDA_OBS > 0.5
                    else 'falls short — dark-flow (directional) signature, '
                         'not a dark-energy magnitude'),
    }


# ══════════════════════════════════════════════════════════════════════════════
#  8. Full run
# ══════════════════════════════════════════════════════════════════════════════

def full_desitter_cavitation() -> Dict[str, object]:
    """Run the whole formulary argument-free; return the summary dict."""
    return {
        'theme': 'No Singularity — the Abrikosov-Vortex Core and '
                 'De Sitter Cavitation over a Black Hole\'s Life',
        'claim': 'The interior is a finite sub-Planckian de Sitter core, '
                 'not a singularity.',
        'holcus': {
            'formula': 'K_core(M) = 24 / r_s^4 = (3/2) c^8 / (G^4 M^4)',
            'stellar_10Msun_m^-4':  kretschmann_core(10 * M_SUN),
            'stellar_K_over_KPlanck': kretschmann_ratio_planck(10 * M_SUN),
            'closed_form_matches':  math.isclose(
                kretschmann_core(10 * M_SUN),
                kretschmann_core_closed(10 * M_SUN), rel_tol=1e-12),
            'planck_crossover_over_mPl':
                planck_mass_crossover()['M_crossover_over_mPl'],
        },
        'no_singularity_check': no_singularity_check(),
        'stiff_matter_ceiling': stiff_matter_ceiling(),
        'energy_partition_default_1_minus_dstar': energy_partition(10 * M_SUN),
        'mass_class_table':     mass_class_table(),
        'cosmic_cavitation_budget': cosmic_cavitation_budget(),
        'constants': {
            'c': C_LIGHT, 'G': G_NEWTON, 'hbar': H_BAR, 'k_B': K_BOLTZ,
            'l_Planck': L_PLANCK, 't_Planck': T_PLANCK, 'm_Planck': M_PLANCK,
            'K_Planck': K_PLANCK, 'OMEGA_ZS': OMEGA_ZS, 'D_STAR': D_STAR,
            'GAP': GAP,
        },
    }


if __name__ == '__main__':
    import json
    print(json.dumps(full_desitter_cavitation(), indent=2, default=str))
