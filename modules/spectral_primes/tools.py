"""
ValaQuenta.modules.spectral_primes.tools
===========================================
Spectral Representation of the Primes -- Module Tools.

Implements the EquationModule registry contract.
Provides: formulary, run(), viewer_data(), shell_commands()

Four computed results (see maths.py for full account): spin (major loop)
is non-resonant; wobble (minor loop) carries the primes, classically;
tilt-vs-wobble correlation is REFUTED as tested; the Real-Tilt/Axis
crossing is an isolated, simple zero, pinned exactly at sigma=1/2, moving
up the t-axis but never sideways.

Version: 0.1
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    get_zeros, spin_series, spin_is_monotonic, wobble_series,
    wobble_carries_primes_demo, tilt_residual_series,
    tilt_vs_wobble_correlation, crossing_does_not_drift, full_report,
    DEFAULT_N_ZEROS,
)


class SpectralPrimesModule(EquationModule):
    """Spectral Representation of the Primes -- spin/wobble decomposition
    of the Riemann-Siegel theta-spiral."""

    @property
    def name(self):
        return "spectral_primes"

    @property
    def display_name(self):
        return "Spectral Representation of the Primes (Spin / Wobble)"

    @property
    def version(self):
        return "0.1"

    @property
    def description(self):
        return (
            "The theta(t)-rotation construction (RiemannHypothesisProof/"
            "ADDENDUM_toroidal_theta_structure_2026-09-25.md) split into two "
            "rotations: spin (the major loop, theta'(t), the smooth non-"
            "resonant carrier) and wobble (the minor loop, the fluctuation "
            "riding on it). Primes are not an artifact of the wobble -- they "
            "are its genuine classical spectral content (Riemann/von "
            "Mangoldt/Weil), demonstrated here by reconstructing psi(x)'s "
            "prime-power jumps from the same zero set that gives a strictly "
            "monotonic, non-resonant spin. A separate claim -- that the "
            "real-axis tilt (Omega proportional to sin(tilt), the oblique-"
            "gearing secondary rotation) IS the wobble by minimum-"
            "information identification -- is REFUTED AS TESTED: direct "
            "correlation is ~0.037, essentially zero, with a named "
            "methodological gap (pointwise vs interval sampling) left open, "
            "not smoothed over. Finally: the crossing of the Real Tilt (the "
            "trajectory's own instantaneous position) and the Axis (the "
            "central t-axis, Re=Im=0) is an isolated, simple, transversal "
            "zero -- pinned at sigma=0.500000 to machine precision at every "
            "zero tested, moving up the t-axis but never sideways in sigma."
        )

    @property
    def confidence_floor(self):
        return "OPEN"

    # -- Formulary ---------------------------------------------------------

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='spin_is_monotonic',
                display='SPIN: theta\'(t), the major loop — non-resonant',
                latex=r"\theta'(t) \approx \tfrac{1}{2}\ln(t/2\pi)",
                radian_form='strictly monotonic over the tested sample — zero resonant peaks',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['n_zeros'],
                compute=lambda n_zeros=DEFAULT_N_ZEROS: spin_is_monotonic(
                    spin_series(get_zeros(n_zeros))),
                display_options=['text'],
            ),
            Equation(
                name='wobble_carries_primes_demo',
                display='WOBBLE: the minor loop carries the primes (psi(x) reconstruction)',
                latex=r'\psi(x) = x - \sum_\rho \frac{x^\rho}{\rho} - \ln(2\pi) - \tfrac{1}{2}\ln(1-x^{-2})',
                radian_form='classical von Mangoldt explicit formula, same zero set as spin',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['n_zeros'],
                compute=lambda n_zeros=DEFAULT_N_ZEROS: wobble_carries_primes_demo(
                    get_zeros(n_zeros)),
                display_options=['text'],
            ),
            Equation(
                name='tilt_vs_wobble_correlation',
                display='TILT vs WOBBLE — REFUTED AS TESTED',
                latex=r'\mathrm{corr}(\mathrm{Im}(e^{i\theta(t)}\zeta(0.7+it)),\ \Delta_{\rm spacing}) \approx 0.037',
                radian_form='minimum-information tilt=wobble identity does not survive direct test',
                confidence='OPEN',
                code_verified=True,
                params=['n_zeros'],
                compute=lambda n_zeros=DEFAULT_N_ZEROS: tilt_vs_wobble_correlation(
                    tilt_residual_series(get_zeros(n_zeros)),
                    wobble_series(get_zeros(n_zeros), spin_series(get_zeros(n_zeros)))),
                display_options=['text'],
            ),
            Equation(
                name='crossing_does_not_drift',
                display='THE CROSSING: isolated, simple, pinned at sigma=1/2',
                latex=r'\{t : \mathrm{Re}(Z_{\rm rot}(t))=\mathrm{Im}(Z_{\rm rot}(t))=0\} \Rightarrow \sigma=\tfrac{1}{2}\ \text{exactly}',
                radian_form='tested across 5 zeros: pinned to machine precision, moves in t not sigma',
                confidence='ESTABLISHED (for zeros tested)',
                code_verified=True,
                params=['n_zeros', 'n_test'],
                compute=lambda n_zeros=DEFAULT_N_ZEROS, n_test=5: crossing_does_not_drift(
                    get_zeros(n_zeros), n_test),
                display_options=['text'],
            ),
            Equation(
                name='full_report',
                display='Everything this module knows, in one call',
                latex=r'\text{spin} \Vert \text{wobble} \Vert \text{tilt-check} \Vert \text{crossing}',
                radian_form='the complete, honest state of all four results',
                confidence='OPEN',
                code_verified=True,
                params=['n_zeros'],
                compute=lambda n_zeros=DEFAULT_N_ZEROS: full_report(n_zeros),
                display_options=['text'],
            ),
        ]

    # -- Run / viewer --------------------------------------------------------

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not found in {self.name} module")
        result = eq.compute(**params) if params else eq.compute()
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str, params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        return {'text': self._format_text(equation_name, self.run(equation_name, params))}

    def _format_text(self, equation_name: str, result: Dict) -> str:
        eq = result['equation']
        r = result['result']
        if isinstance(r, dict):
            body = '\n'.join(f"      {k:<28} {v}" for k, v in r.items()
                             if not isinstance(v, (list, dict)))
            summary = '\n' + body
        elif isinstance(r, list):
            summary = f"{r[:10]}{' ...' if len(r) > 10 else ''}  (n={len(r)})"
        else:
            summary = r
        return (
            f"  {eq.display}\n"
            f"  Status: {eq.confidence}  |  Code-verified: {eq.code_verified}\n"
            f"  Radian form: {eq.radian_form}\n"
            f"  Result: {summary}"
        )

    # -- Shell commands ------------------------------------------------------

    def shell_commands(self) -> Dict[str, Any]:
        return {
            'spin':      lambda n=DEFAULT_N_ZEROS: spin_is_monotonic(spin_series(get_zeros(n))),
            'wobble':    lambda n=DEFAULT_N_ZEROS: wobble_carries_primes_demo(get_zeros(n)),
            'tilt':      lambda n=DEFAULT_N_ZEROS: tilt_vs_wobble_correlation(
                             tilt_residual_series(get_zeros(n)),
                             wobble_series(get_zeros(n), spin_series(get_zeros(n)))),
            'crossing':  lambda n=DEFAULT_N_ZEROS, t=5: crossing_does_not_drift(get_zeros(n), t),
            'report':    lambda n=DEFAULT_N_ZEROS: full_report(n),
        }
