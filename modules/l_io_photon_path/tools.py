"""
ainulindale_engine.modules.l_io_photon_path.tools
====================================================
L_(I|O) Photon Path Engine (GR) — Module Tools

Implements the EquationModule registry contract.
Provides: formulary, run(), viewer_data(), shell_commands()

This is the GR-grounded companion to modules/inversion (the abstract
(I|O) coordinate map). Where inversion.InversionMap implements the
geometric J_N: (r,theta) -> (1/r, theta+pi/2), this module implements
the physical statement wiki/52 actually makes: a real photon's path is
bent by real mass, and that bending IS the L_(I|O) - L difference.
Requires real (gamma1, gamma2) shear data as input -- see
BulletCluster/optical/jwst/pixel_vector_field.py for the source.

Boundary role (2026-07-21): (I|O)_RB (renamed from H_hat_RB) defines a
boundary/degenerate locus; this module is the general template for
crossing one -- see maths.py's module docstring addendum for the k=0
zeroing convention and the (flagged, not established) zeta-pole
category match.

Version: 0.2
"""

from typing import Dict, List, Any
import numpy as np

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    kaiser_squires_kappa, lensing_potential, deflection_field,
    trace_photon, l_io_deficit, bounded_lensing_pipeline,
)


class LIOPhotonPathModule(EquationModule):
    """L_(I|O) Photon Path Engine — GR light bending from real shear."""

    @property
    def name(self):
        return "l_io_photon_path"

    @property
    def display_name(self):
        return "L_(I|O) Photon Path Engine (GR)"

    @property
    def version(self):
        return "0.2"

    @property
    def description(self):
        return (
            "GR version of L_(I|O): Kaiser-Squires shear->convergence, "
            "Poisson solve for the lensing potential, deflection field, "
            "and the lens equation beta=theta-alpha(theta). The difference "
            "between the clean (undeflected) path theta and the actual "
            "(bent) source position beta is the real, measured L_(I|O) "
            "deviation. L_(I|O)-L is identified with -psi(theta), the "
            "Fermat potential -- established GR, not a new operator. "
            "Requires real shear input; no synthetic fallback."
        )

    @property
    def confidence_floor(self):
        return "THEORETICAL"

    # ── Formulary ─────────────────────────────────────────────────────────────

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='bounded_lensing_pipeline',
                display='Full pipeline w/ non-periodic boundary handler',
                latex=r'\gamma \to \text{taper+pad} \to (\kappa,\psi,\vec\alpha) \to \text{crop}',
                radian_form='taper (Tukey) + zero-pad gamma before FFT, crop kappa/psi/alpha after',
                confidence='THEORETICAL',
                code_verified=True,
                params=['gamma1', 'gamma2', 'pixel_scale_arcsec', 'taper_frac', 'pad_factor'],
                compute=lambda gamma1, gamma2, pixel_scale_arcsec, taper_frac=0.1, pad_factor=2.0:
                    bounded_lensing_pipeline(gamma1, gamma2, pixel_scale_arcsec, taper_frac, pad_factor),
                display_options=['text'],
            ),
            Equation(
                name='kaiser_squires_kappa',
                display='Kaiser-Squires: shear -> convergence',
                latex=r'\hat\kappa(\vec k) = \hat D^*(\vec k)\,\hat\gamma(\vec k)',
                radian_form='kappa_hat(k) = conj(D(k)) * gamma_hat(k), D=(k1^2-k2^2+2i k1 k2)/|k|^2',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['gamma1', 'gamma2'],
                compute=lambda gamma1, gamma2: kaiser_squires_kappa(gamma1, gamma2),
                display_options=['text'],
            ),
            Equation(
                name='lensing_potential',
                display='Poisson solve: convergence -> lensing potential',
                latex=r'\nabla^2\psi = 2\kappa \;\Rightarrow\; \hat\psi(\vec k) = -2\hat\kappa(\vec k)/|\vec k|^2',
                radian_form='psi_hat(k) = -2*kappa_hat(k)/|k|^2',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['kappa'],
                compute=lambda kappa: lensing_potential(kappa),
                display_options=['text'],
            ),
            Equation(
                name='deflection_field',
                display='alpha = grad(psi)  -- the actual bending',
                latex=r'\vec\alpha(\vec\theta) = \nabla\psi(\vec\theta)',
                radian_form='alpha1 = d(psi)/dx / pixel_scale, alpha2 = d(psi)/dy / pixel_scale',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['psi', 'pixel_scale_arcsec'],
                compute=lambda psi, pixel_scale_arcsec: deflection_field(psi, pixel_scale_arcsec),
                display_options=['text'],
            ),
            Equation(
                name='trace_photon',
                display='Lens equation: beta = theta - alpha(theta)',
                latex=r'\vec\beta = \vec\theta - \vec\alpha(\vec\theta)',
                radian_form='beta = theta - alpha  (theta=clean/apparent, beta=actual source)',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['theta1', 'theta2', 'alpha1', 'alpha2'],
                compute=lambda theta1, theta2, alpha1, alpha2: trace_photon(theta1, theta2, alpha1, alpha2),
                display_options=['text'],
            ),
            Equation(
                name='l_io_deficit',
                display='L_(I|O) - L := -psi(theta)  [wiki/52 target #1, formalized]',
                latex=r'L_{(I|O)} - L \equiv -\psi(\vec\theta) \quad \text{(Fermat potential)}',
                radian_form='L_IO_minus_L = -psi  (raw stats, no rescaling)',
                confidence='THEORETICAL',
                code_verified=True,
                params=['psi'],
                compute=lambda psi: l_io_deficit(psi),
                display_options=['text'],
            ),
        ]

    # ── Run ──────────────────────────────────────────────────────────────────

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not found in {self.name} module")
        result = eq.compute(**params) if params else eq.compute()
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    # ── Viewer data ───────────────────────────────────────────────────────────

    def viewer_data(self, equation_name: str, params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)
        return {'text': self._format_text(equation_name, result)}

    def _format_text(self, equation_name: str, result: Dict) -> str:
        eq = result['equation']
        r = result['result']
        summary = r if not isinstance(r, (np.ndarray, dict)) else (
            {'shape': r.shape, 'mean': float(np.nanmean(r))} if isinstance(r, np.ndarray) else r
        )
        return (
            f"  {eq.display}\n"
            f"  Status: {eq.confidence}  |  Code-verified: {eq.code_verified}\n"
            f"  Radian form: {eq.radian_form}\n"
            f"  Result: {summary}"
        )

    # ── Shell commands ────────────────────────────────────────────────────────

    def shell_commands(self) -> Dict[str, Any]:
        return {
            'ks_kappa':  lambda g1, g2: kaiser_squires_kappa(g1, g2),
            'psi':       lambda kappa: lensing_potential(kappa),
            'alpha':     lambda psi, pxscl: deflection_field(psi, pxscl),
            'trace':     lambda t1, t2, a1, a2: trace_photon(t1, t2, a1, a2),
            'l_io_stats': lambda psi: l_io_deficit(psi),
        }

    def on_register(self, registry) -> None:
        pass
