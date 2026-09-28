r"""
ValaQuenta.modules.oblique_gear.tools
========================================
The Oblique Gear, tested across scale -- Module Tools.

Implements the EquationModule registry contract.
Provides: formulary, run(), viewer_data(), shell_commands()

Tests whether the black-hole-scale crank angle (h_rb_hat's theta_crank =
arctan(d\*), the Witches Hat half-angle) is the same fact as the
galaxy-scale rotation curve's own tangent angle at its transition radius,
or merely the same constant appearing twice. See maths.py for the full
account, including the negative result this module reports honestly.

Version: 0.1
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    crank_angle_deg, stokes_dimensionless, stokes_tangent_angle_deg,
    crank_vs_galaxy_tangent_check, find_matching_radius, full_report,
)


class ObliqueGearModule(EquationModule):
    """The Oblique Gear, tested across scale -- black hole crank angle vs
    galaxy rotation-curve tangent angle."""

    @property
    def name(self):
        return "oblique_gear"

    @property
    def display_name(self):
        return "The Oblique Gear Across Scale (Black Hole / Galaxy)"

    @property
    def version(self):
        return "0.1"

    @property
    def description(self):
        return (
            "Tests FourthAgePapers/ChiralityBlackHole's second claim: is "
            "the black-hole-scale crank angle theta_crank = arctan(d*) "
            "(h_rb_hat's Witches Hat half-angle, ESTABLISHED 2026-06-17) "
            "the same fact as the galaxy-scale Stokes-drift rotation "
            "curve's own tangent angle at its transition radius r=r_t "
            "(galactic_cavity.py, SPARC-confirmed p=0.794), or merely the "
            "same constant d* appearing on both sides independently? "
            "Computed directly (sympy-verified): REFUTED as stated -- a "
            "real ~3.84 degree gap between 13.82 deg (crank) and 17.66 deg "
            "(galaxy tangent at r_t), not a rounding artifact. The "
            "shared-constant, shared-arctan-family kinship survives; the "
            "stronger 'same mechanism' claim, in this specific formulation, "
            "does not. Reported honestly per this framework's Chase Every "
            "Anomaly rule -- a legal, computed result, not a failure."
        )

    @property
    def confidence_floor(self):
        return "OPEN"

    # -- Formulary ---------------------------------------------------------

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='crank_angle_deg',
                display='Black-hole side: theta_crank = arctan(d*)',
                latex=r'\theta_{\rm crank} = \arctan(d^*) \approx 13.82^\circ',
                radian_form='h_rb_hat.maths.oblique_crank() — ESTABLISHED, reused not re-derived',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: crank_angle_deg(),
                display_options=['text'],
            ),
            Equation(
                name='stokes_dimensionless',
                display='Galaxy side: y(x) = (2/pi)*atan(x), x = r/r_t',
                latex=r'y(x) = \frac{2}{\pi}\arctan(x)',
                radian_form='dimensionless form of galactic_cavity.py stokes_velocity()',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['x'],
                compute=lambda x: stokes_dimensionless(x),
                display_options=['text'],
            ),
            Equation(
                name='stokes_tangent_angle_deg',
                display='Tangent angle of the galaxy curve at any x = r/r_t',
                latex=r'\arctan\!\left(\frac{dy}{dx}\right),\ \ \frac{dy}{dx}=\frac{2/\pi}{1+x^2}',
                radian_form='sympy-differentiated, evaluated numerically',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['x'],
                compute=lambda x: stokes_tangent_angle_deg(x),
                display_options=['text'],
            ),
            Equation(
                name='crank_vs_galaxy_tangent_check',
                display='THE CHECK: does the galaxy tangent angle at r=r_t equal theta_crank?',
                latex=r'\left.\arctan\!\frac{dy}{dx}\right|_{x=1} \overset{?}{=} \arctan(d^*)',
                radian_form='17.657 deg vs 13.820 deg — REFUTED, real ~3.84 deg gap',
                confidence='OPEN',
                code_verified=True,
                params=[],
                compute=lambda: crank_vs_galaxy_tangent_check(),
                display_options=['text'],
            ),
            Equation(
                name='find_matching_radius',
                display='Where WOULD the tangent angle equal theta_crank?',
                latex=r'x = \sqrt{\frac{2}{\pi d^*} - 1} \approx 1.2601',
                radian_form='checked against phi, sqrt(pi/2), cbrt(2), 1/d* — no significant match',
                confidence='OPEN',
                code_verified=True,
                params=[],
                compute=lambda: find_matching_radius(),
                display_options=['text'],
            ),
            Equation(
                name='full_report',
                display='Everything this module knows, in one call',
                latex=r'\text{black hole} \Vert \text{galaxy} \Vert \text{check} \Vert \text{probe}',
                radian_form='the complete, honest state of the cross-scale claim',
                confidence='OPEN',
                code_verified=True,
                params=[],
                compute=lambda: full_report(),
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
            'crank':      lambda: crank_angle_deg(),
            'stokes':     lambda x: stokes_dimensionless(x),
            'tangent':    lambda x: stokes_tangent_angle_deg(x),
            'check':      lambda: crank_vs_galaxy_tangent_check(),
            'probe':      lambda: find_matching_radius(),
            'report':     lambda: full_report(),
        }
