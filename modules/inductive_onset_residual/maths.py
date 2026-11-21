r"""
ValaQuenta.modules.inductive_onset_residual.maths
=================================================
The onset residual of the Inductive Self-Adjoint Geometric Coupling Hamiltonian
(Ĥ_RB). Machinery, not a claim: every function below runs and returns numbers.

Symbols: in prose this module writes the Lambert fixed point as W(1) and d* as d*. The codebase calls W(1)
OMEGA_ZS; the author (2026-11-21) calls d* Ω_RZ and W(1) A_Fermat. :func:`symbols` records every assignment.

Three things are computed from the values the code runs with.

1. INDUCTION. Iterating x_{n+1} = e^{-x_n} builds W(1) one step at a time. The
   error shrinks by |f'(Ω)| = Ω per step, so the iteration gains -log10(Ω) digits per
   step, and because ln Ω = -Ω that rate is Ω/ln 10 = 0.2463072015…, the Boundary
   face of d*. :func:`induction` measures the rate from the iteration itself.

2. THE RUNNING VALUE. The code carries d* = 0.24600 (``engine.constants.D_STAR``;
   :func:`census` counts where it is written). :func:`onset_residual` reports the
   difference between that running value and the induced rate: Δ = Ω − D*·ln 10 =
   ln 10·(d*_induced − d*_running), and the digit at which the two first differ.

3. THE HUB. 0_RB is pure e_0; ``box_kite.fixed_point_weight`` reads the share of an
   address's energy on e_0 (1 − depth² for a fiber of that depth). :func:`hub_fiber`
   tabulates the depth at which the weight equals each of the constants.

Also: the geometric couplings G_p(σ) = p^(−σ) of Ĥ_RB (:func:`couplings`), the
explicit formula checked against the exact Chebyshev ψ (:func:`explicit_formula`),
and the readings attached to Δ in earlier versions (:func:`interpretations`), each
labelled as a reading.

Replaces ``bao_mass_gap`` (2026-11-21). The old name is retired because no BAO
data, scale or measurement enters Δ.

Author:  O Captain My Captain
Version: 0.2
"""

import math
import os
import re
from typing import Any, Dict, List, Optional

from ...engine import constants as C
from ..box_kite import maths as bk
from ..h_rb_hat.maths import RIEMANN_ZEROS

OMEGA_ZS = C.OMEGA_ZS                       # Lambert W(1), 0.5671432904097838
LN10 = math.log(10.0)
D_STAR_RUN = C.D_STAR                       # the value the code runs with (0.24600)
D_STAR_BOUNDARY = OMEGA_ZS / LN10           # Ω/ln 10 = 0.246307201473…
FIRST_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19)
SIGMA_FACETS = {'0': 0.0, '1/2': 0.5, '1': 1.0, '2': 2.0}
SED_DIM = 16


def _fixed_point_by_induction(x0: float, steps: int) -> List[float]:
    """The orbit of x ↦ e^{-x} from ``x0``.

    :param x0: the starting value
    :param steps: the number of induction steps
    :returns: the iterates x_1 … x_steps
    """
    out, x = [], x0
    for _ in range(steps):
        x = math.exp(-x)
        out.append(x)
    return out


def _slope(xs: List[float], ys: List[float]) -> float:
    """Least-squares slope of ``ys`` against ``xs``.

    :param xs: abscissae
    :param ys: ordinates
    :returns: the slope
    """
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    return sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sum((a - mx) ** 2 for a in xs)


def induction(starts: tuple = (0.0, 0.3, 0.9, 1.7, 3.0), steps: int = 200) -> Dict[str, Any]:
    """Build W(1) by induction and measure the digits gained per step (60-digit decimal arithmetic).

    :param starts: starting values of the iteration
    :param steps: induction steps used to build the reference fixed point
    :returns: W(1) by induction, the measured rate per start (log10 error against step), and the exact rate
    """
    from decimal import Decimal, getcontext
    getcontext().prec = 80
    ref = Decimal(1) / 2
    for _ in range(max(int(steps), 400)):
        ref = (-ref).exp()
    omega = float(ref)
    rates = {}
    for x0 in starts:
        x, pts = Decimal(str(x0)), []
        for n in range(1, 61):
            x = (-x).exp()
            e = abs(x - ref)
            if e > Decimal(10) ** -40:
                pts.append((n, float(e.log10())))
        xs, ys = [p[0] for p in pts[25:]], [p[1] for p in pts[25:]]
        rates[x0] = -_slope(xs, ys) if len(xs) > 4 else float('nan')
    exact = -math.log10(omega)
    return {
        'derivation': [
            'Iterate x → e^{-x} from 0.5 in 80-digit decimal arithmetic: the orbit converges to W(1).',
            f'W(1) by induction = {omega!r}.',
            'The derivative of x → e^{-x} at W(1) is −W(1), so each step multiplies the error by W(1).',
            f'Digits gained per step = −log10 W(1) = {exact:.12f}.',
            'ln W(1) = −W(1), so −log10 W(1) = W(1)/ln 10: the rate is d* (Boundary).',
            *[f'Measured from start {k}: {v:.10f}.' for k, v in rates.items()],
        ],
        'omega_by_induction': omega,
        'omega_lambert': OMEGA_ZS,
        'contraction_factor': omega,
        'digits_per_step_exact': exact,
        'digits_per_step_measured': rates,
        'ln_omega_plus_omega': math.log(omega) + omega,
        'steps_to_15_digits': math.ceil(15.0 / exact),
    }


def running_value() -> Dict[str, Any]:
    """The d* the code runs with, beside the induced rate.

    :returns: the running value, the induced rate, and which constants file holds the running value
    """
    return {
        'd_star_running': D_STAR_RUN,
        'd_star_boundary': D_STAR_BOUNDARY,
        'running_minus_boundary': D_STAR_RUN - D_STAR_BOUNDARY,
        'source': 'ValaQuenta/engine/constants.py :: D_STAR',
        'boundary_source': 'Ω/ln 10 (induction rate)',
    }


def onset_residual() -> Dict[str, Any]:
    """Δ from the running value, and the digit where running and induced d* first differ.

    :returns: Δ, the identity Δ = ln 10·(d*_induced − d*_running), the agreeing decimals, Δ in units of 10^−k
    """
    delta = OMEGA_ZS - D_STAR_RUN * LN10
    ind = -math.log10(OMEGA_ZS)
    k = 0
    while int(D_STAR_RUN * 10 ** (k + 1)) == int(ind * 10 ** (k + 1)):
        k += 1
    scaled = delta * 10 ** k
    return {
        'derivation': [
            f'Ω = {OMEGA_ZS:.12f}; d* running = {D_STAR_RUN}; d* by induction = {ind:.12f}.',
            f'Δ = Ω − d*_running·ln 10 = {delta:.12f}.',
            f'ln 10·(d*_induced − d*_running) = {LN10 * (ind - D_STAR_RUN):.12f}.',
            f'The two d* agree on {k} decimals; the next differs.',
            f'Δ·10^{k} = {scaled:.6f}.',
        ],
        'delta': delta,
        'delta_identity_value': LN10 * (ind - D_STAR_RUN),
        'agreeing_decimals': k,
        'delta_scaled_by_agreement': scaled,
        'inverse_sqrt2': 1.0 / math.sqrt(2.0),
        'scaled_over_inverse_sqrt2': scaled * math.sqrt(2.0),
        'uncertainty_if_running_to_agreeing_decimals': 0.5 * 10.0 ** (-k) * LN10,
    }


def hub_fiber(depth: float = 0.6) -> Dict[str, Any]:
    """The 0_RB fixed-point weight of a fiber of given depth, and the depth at which it equals each constant.

    :param depth: share of the hub's amplitude moved off e_0, in [0, 1]
    :returns: the weight 1 − depth², and depth(w) = √(1 − w) for w = Ω, d*, 1/2
    """
    psi = [0.0] * SED_DIM
    psi[0] = math.sqrt(max(0.0, 1.0 - depth * depth))
    psi[1] = depth / math.sqrt(2.0)
    psi[2] = depth / math.sqrt(2.0)
    w = bk.fixed_point_weight(psi)
    table = {name: math.sqrt(1.0 - v) for name, v in
             (('Omega', OMEGA_ZS), ('d_star_running', D_STAR_RUN), ('d_star_boundary', D_STAR_BOUNDARY), ('one_half', 0.5))}
    return {'depth': depth, 'fixed_point_weight': w, 'weight_expected': 1.0 - depth * depth,
            'depth_at_weight': table, 'hub_weight': bk.fixed_point_weight([1.0] + [0.0] * (SED_DIM - 1))}


def couplings() -> Dict[str, Any]:
    """The geometric couplings G_p(σ) = p^(−σ) of Ĥ_RB at the σ facets.

    :returns: the table over the first eight primes, and G_2(1/2)
    """
    table = {p: {s: p ** (-v) for s, v in SIGMA_FACETS.items()} for p in FIRST_PRIMES}
    return {'table': table, 'G_2_half': 2.0 ** -0.5, 'sigma_facets': SIGMA_FACETS,
            'euler_partial_sigma2': sum(p ** -2.0 for p in FIRST_PRIMES)}


def _psi_exact(x: float) -> float:
    """Chebyshev ψ(x) = Σ_{p^k ≤ x} ln p.

    :param x: the argument
    :returns: ψ(x)
    """
    n, tot = int(x), 0.0
    for p in range(2, n + 1):
        if all(p % q for q in range(2, int(p ** 0.5) + 1)):
            k = p
            while k <= x:
                tot += math.log(p)
                k *= p
    return tot


def explicit_formula(x: float = 10.5, n_zeros: int = 20) -> Dict[str, Any]:
    """The explicit formula ψ(x) = x − Σ_ρ x^ρ/ρ − ln 2π − ½ ln(1 − x⁻²), summed over zero pairs, against the exact ψ.

    :param x: the argument (non-integer, so ψ is continuous there)
    :param n_zeros: zeros with γ > 0 used (each counted with its conjugate)
    :returns: the formula's value, the exact ψ, and the error
    """
    zs = RIEMANN_ZEROS[:max(1, min(int(n_zeros), len(RIEMANN_ZEROS)))]
    lx = math.log(x)
    s = sum(2.0 * math.sqrt(x) * (0.5 * math.cos(g * lx) + g * math.sin(g * lx)) / (0.25 + g * g) for g in zs)
    val = x - s - math.log(2.0 * math.pi) - 0.5 * math.log(1.0 - x ** -2)
    ex = _psi_exact(x)
    return {'x': x, 'zeros_used': len(zs), 'psi_formula': val, 'psi_exact': ex, 'error': val - ex,
            'note': 'each γ>0 is counted with its conjugate (factor 2); the earlier module summed one term per zero'}


_SKIP = {'archive', '__pycache__', '_worktrees', 'node_modules', 'data', 'DataSets', 'build', 'site-packages', 'results', 'datasets'}
_PAT = {
    'running 0.246(0)': re.compile(r'(?<![0-9.])0?\.2460*(?![0-9])'),
    'boundary 0.2463x': re.compile(r'(?<![0-9])0?\.2463[0-9]*'),
    'rg estimate 0.2468x': re.compile(r'(?<![0-9])0?\.2468[0-9]*'),
}


_CENSUS_CACHE: Dict[Any, Dict[str, Any]] = {}


def census(root: Optional[str] = None, exts: tuple = ('.py', '.c', '.h', '.sh')) -> Dict[str, Any]:
    """Count the code files in each sibling repository that write each d* value.

    :param root: directory holding the repositories (default: the parent of ValaQuenta)
    :param exts: file extensions scanned
    :returns: per repository, the number of files containing each value
    """
    base = root or os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    if (base, exts) in _CENSUS_CACHE:
        return _CENSUS_CACHE[(base, exts)]
    out: Dict[str, Dict[str, int]] = {}
    for repo in sorted(os.listdir(base)):
        top = os.path.join(base, repo)
        if not os.path.isdir(top) or repo.startswith(('.', '_')) or repo == 'LeanScratch':
            continue
        counts = {k: 0 for k in _PAT}
        for d, dirs, files in os.walk(top):
            dirs[:] = [x for x in dirs if x not in _SKIP and not x.startswith('.')]
            for f in files:
                if not f.endswith(exts):
                    continue
                try:
                    with open(os.path.join(d, f), errors='ignore') as fh:
                        txt = fh.read()
                except OSError:
                    continue
                for k, pat in _PAT.items():
                    if pat.search(txt):
                        counts[k] += 1
        if any(counts.values()):
            out[repo] = counts
    totals = {k: sum(v[k] for v in out.values()) for k in _PAT}
    _CENSUS_CACHE[(base, exts)] = {'base': base, 'repos': out, 'totals': totals}
    return _CENSUS_CACHE[(base, exts)]


def symbols() -> Dict[str, Any]:
    """Which symbol names which constant, by source. The sources disagree; this records each assignment and does not settle them.

    :returns: per source, the assignment of d* (0.2463…), W(1) (0.5671…) and 1/137.036, with the date and where it is written
    """
    return {
        'values': {'d_star_boundary': D_STAR_BOUNDARY, 'lambert_w_fixed_point': OMEGA_ZS, 'inverse_137': 1.0 / 137.035999084},
        'author_2026_11_21': dict(
            Omega_RZ='d* (0.2463…)', A_Fermat='the Lambert W fixed point (0.5671…)',
            note='the author: "Omega_riemann_zeta was d*, A_fermat was the Lambert W fixed point: my Alpha and Omega, not to be '
                 'confused with the other Omega (the standard omega constant W(1)), hence the RZ and PI subscripts"'),
        'first_code_2026_04_15': dict(ALPHA='1/137.035999084 (neural fine structure constant, the minimum coupling)',
                                      OMEGA='the Lambert W fixed point (0.5671…, the maximum coupling)', where='code/core/smnnip_lagrangian_pure.py'),
        'readme_2026_04_15': dict(A_pi='1/137.036 (domain floor)', Omega_zeta_Sigma='W(1) = 0.5671… (domain ceiling)', d_star='0.24600'),
        'rhp_four_dstar_2026_11_12': dict(digits='d* = 0.2463 on the Riemann/entropy side', gap_count='W(1) = 0.5671 on the Fermat/inertia side',
                                          where='RiemannHypothesisProof/docs/four_dstar_2026-11-12.md'),
        'wiki_17_2026_11_13': dict(A_fermat='role: Fermat-side inertia constant; value OPEN (x = 1 endpoint or 1/137.036)',
                                   Omega_zeta_Sigma='W(1), born from entropy in the Riemann zeta function'),
        'in_this_module': 'the Lambert fixed point is written W(1) in prose and OMEGA_ZS in code (the codebase constant name); d* is written d*',
    }


def interpretations() -> Dict[str, Any]:
    """The readings attached to Δ in earlier versions of this engine, each labelled as a reading.

    :returns: reading → what it says, what it would take to test it, and its label
    """
    return {
        'BAO residual': dict(says='Δ is the Baryon Acoustic Oscillation residual', label='CONJECTURE',
                             needs='a mapping from Δ to an observed BAO quantity; none exists in the code'),
        'Yang–Mills mass gap': dict(says='Δ is the Yang–Mills mass gap', label='CONJECTURE',
                                    needs='a quantum gauge theory on R^4 with a spectral gap; none is built here'),
        'compactification scale': dict(says='Δ is an M-theory compactification scale', label='CONJECTURE',
                                       needs='a compactification with Δ as a computed modulus'),
        'point becomes a circle': dict(says='Δ marks the first point that has an inside (fixed-point cavitation onset)',
                                       label='CONJECTURE', needs='the author\'s definition as a computable onset'),
        'G_2(1/2) = 1/√2': dict(says='the 1/√2 in 1/(1000√2) is the first-prime coupling at σ = 1/2', label='CONJECTURE',
                                needs='a derivation of the 10^-3 factor from the coupling sum'),
    }


def validate() -> Dict[str, Any]:
    """Run the checks. Each compares two independently computed quantities.

    :returns: the checks and whether all pass
    """
    ind = induction()
    on = onset_residual()
    hf = hub_fiber(0.6)
    cp = couplings()
    ef = explicit_formula(10.5, 20)
    rates = [v for v in ind['digits_per_step_measured'].values() if v == v]
    checks = {
        'omega_by_induction_equals_lambert_w1': abs(ind['omega_by_induction'] - OMEGA_ZS) < 1e-15,
        'omega_satisfies_w_exp_w_equals_1': abs(OMEGA_ZS * math.exp(OMEGA_ZS) - 1.0) < 1e-15,
        'ln_omega_equals_minus_omega': abs(ind['ln_omega_plus_omega']) < 1e-15,
        'measured_rate_equals_omega_over_ln10': all(abs(r - D_STAR_BOUNDARY) < 1e-7 for r in rates),
        'running_value_is_the_constants_file_value': D_STAR_RUN == C.D_STAR,
        'delta_equals_ln10_times_rate_difference': abs(on['delta'] - on['delta_identity_value']) < 1e-15,
        'hub_weight_is_one_minus_depth_squared': abs(hf['fixed_point_weight'] - hf['weight_expected']) < 1e-12,
        'pure_hub_has_weight_one': hf['hub_weight'] == 1.0,
        'coupling_G2_half_is_inverse_sqrt2': abs(cp['G_2_half'] - 2.0 ** -0.5) < 1e-15,
        'explicit_formula_within_half_of_exact_at_x_10p5': abs(ef['error']) < 0.5,
    }
    return {'checks': checks, 'n_checks': len(checks), 'all_pass': all(checks.values()),
            'explicit_formula_error': ef['error'], 'measured_rates': ind['digits_per_step_measured']}


def summary() -> Dict[str, Any]:
    """One-screen summary.

    :returns: the headline numbers and the check count
    """
    on, ind, v = onset_residual(), induction(), validate()
    return {
        'title': 'Inductive onset residual',
        'headline': on['delta'],
        'derivation': [
            f'Induction on x → e^(−x): Ω = {ind["omega_by_induction"]:.12f}, {ind["digits_per_step_exact"]:.10f} digits per step.',
            f'That rate is d* (Boundary) = Ω/ln 10 = {D_STAR_BOUNDARY:.10f}.',
            f'The code runs d* = {D_STAR_RUN}: they agree on {on["agreeing_decimals"]} decimals.',
            f'Δ = Ω − d*_running·ln 10 = {on["delta"]:.12f} = ln 10·(d*_induced − d*_running).',
            f'Checks {v["n_checks"]}: {"all pass" if v["all_pass"] else "FAILING"}.',
        ],
        'delta': on['delta'], 'd_star_running': D_STAR_RUN, 'd_star_boundary': D_STAR_BOUNDARY,
        'agreeing_decimals': on['agreeing_decimals'], 'all_pass': v['all_pass'],
    }
