"""
ainulindale_engine.modules.jwst.tools
=======================================
JWSTModule — registry contract.

Equations:
  1. spectral_to_octonion   8 filter intensities → 𝕆 element
  2. cd_spectral_address    full Cayley-Dickson pixel address
  3. synthetic_hydrogen     Paschen series test spectrum
  4. synthetic_stellar      blackbody T=5000K test spectrum
  5. lambda_to_r            wavelength → radial coordinate

Version: 0.111
"""

import math
from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    JWST_FILTERS, FILTER_NAMES, FILTER_LAMBDA,
    lambda_to_r, r_to_lambda,
    spectral_to_octonion, octonion_to_spectral,
    cd_spectral_address, synthetic_spectrum,
)


class JWSTModule(EquationModule):

    @property
    def name(self): return 'jwst'

    @property
    def display_name(self): return 'JWST  Spectral Pixel  →  𝕆'

    @property
    def version(self): return '0.111'

    @property
    def description(self):
        return (
            'JWST NIRCam spectral pixel module. '
            '8 filter intensities (900–4440nm) → 8 octonion components. '
            'Cayley-Dickson addressing: λ → r ∈ (0,1). '
            'One 𝕆 element per sky pixel.'
        )

    @property
    def confidence_floor(self): return 'THEORETICAL'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='spectral_to_octonion',
                display='8 NIRCam filters → 𝕆 element',
                latex=r'\Psi = \sum_{k=0}^{7} I_k\,e_k \in \mathbb{O}',
                radian_form='Psi = I_0*e0 + I_1*e1 + ... + I_7*e7',
                confidence='THEORETICAL',
                code_verified=True,
                params=['intensities'],
                compute=None,
                display_options=['text', 'fano', '3d_cartesian'],
            ),
            Equation(
                name='cd_spectral_address',
                display='Cayley-Dickson spectral pixel address',
                latex=r'(\mathbb R,\mathbb C,\mathbb H,\mathbb O)\text{ address of pixel}',
                radian_form='ℝ=mean, ℂ=(short,long), ℍ=alternate, 𝕆=all 8',
                confidence='THEORETICAL',
                code_verified=True,
                params=['intensities', 'pixel_x', 'pixel_y'],
                compute=None,
                display_options=['text', '3d_cartesian'],
            ),
            Equation(
                name='synthetic_hydrogen',
                display='Synthetic Paschen series spectrum (hydrogen)',
                latex=r'I(\lambda)\propto e^{-(\lambda-\lambda_{Pa})^2/\sigma^2}',
                radian_form='Gaussian proximity to Paschen lines (1005, 1094, 1282, 1875 nm)',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: synthetic_spectrum('hydrogen'),
                display_options=['text', '3d_cartesian'],
            ),
            Equation(
                name='synthetic_stellar',
                display='Synthetic blackbody T=5000K spectrum',
                latex=r'B_\lambda(T)=\frac{2hc^2}{\lambda^5}\frac{1}{e^{hc/\lambda kT}-1}',
                radian_form='Planck function, T=5000K, wavelengths at NIRCam filters',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: synthetic_spectrum('stellar'),
                display_options=['text', '3d_cartesian'],
            ),
            Equation(
                name='lambda_to_r',
                display='λ (nm) → r ∈ (0,1)  radial coordinate',
                latex=r'r = \frac{\lambda - \lambda_{min}}{\lambda_{max}-\lambda_{min}}',
                radian_form='r = (lambda - 900) / (4440 - 900)',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['wavelength_nm'],
                compute=lambda wavelength_nm=2000.0: {
                    'wavelength_nm': float(wavelength_nm),
                    'r': lambda_to_r(float(wavelength_nm)),
                    'lambda_back': r_to_lambda(lambda_to_r(float(wavelength_nm))),
                },
                display_options=['text'],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in jwst module")

        if equation_name == 'spectral_to_octonion':
            intensities = params.get('intensities', [1.0]*8)
            if isinstance(intensities, (int, float)):
                intensities = [float(intensities)] * 8
            result = spectral_to_octonion(intensities)

        elif equation_name == 'cd_spectral_address':
            intensities = params.get('intensities', [1.0]*8)
            if isinstance(intensities, (int, float)):
                intensities = [float(intensities)] * 8
            result = cd_spectral_address(
                intensities,
                int(params.get('pixel_x', 0)),
                int(params.get('pixel_y', 0)),
            )

        elif eq.compute is not None:
            filtered = {k: params[k] for k in eq.params if k in params}
            result = eq.compute(**filtered)
        else:
            result = {}

        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str,
                    params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)['result']
        if display_mode == 'text':
            return {'text': self._fmt(equation_name, result)}
        elif display_mode == 'fano':
            gens = result.get('fano_gens', [])
            return {'type': 'fano', 'highlight': gens,
                    'labels': FILTER_NAMES, 'text': self._fmt(equation_name, result)}
        elif display_mode == '3d_cartesian':
            return self._3d_data(equation_name, result)
        return {'text': self._fmt(equation_name, result)}

    def _fmt(self, name, result) -> str:
        if isinstance(result, dict):
            lines = [f"  {name}"]
            for k, v in result.items():
                if isinstance(v, float):
                    lines.append(f"  {k:22s} = {v:.6f}")
                elif isinstance(v, list) and v and isinstance(v[0], float):
                    pairs = list(zip(FILTER_NAMES, v)) if len(v) == 8 else []
                    if pairs:
                        for fn, val in pairs:
                            lines.append(f"  {fn:8s}  {val:.4f}")
                    else:
                        lines.append(f"  {k:22s} = {[f'{x:.3f}' for x in v]}")
                elif not isinstance(v, (list, dict)):
                    lines.append(f"  {k:22s} = {v}")
            return '\n'.join(lines)
        return f"  {name}: {result}"

    def _3d_data(self, name, result) -> Dict:
        if name in ('synthetic_hydrogen', 'synthetic_stellar'):
            intensities = result.get('intensities', [])
            lams = result.get('wavelengths', FILTER_LAMBDA)
            pts  = [(lam/1000.0, I, float(i)) for i, (lam, I) in enumerate(zip(lams, intensities))]
            return {'type': '3d_flow', 'points': pts,
                    'axes': ('wavelength_um', 'intensity', 'filter_index')}
        elif name in ('spectral_to_octonion', 'cd_spectral_address'):
            comps = result.get('components') or result.get('alg_O', [])
            r_coords = result.get('r_coords', [lambda_to_r(l) for l in FILTER_LAMBDA])
            pts = [(r_coords[i], comps[i], float(i)) for i in range(min(len(comps), len(r_coords)))]
            return {'type': '3d_flow', 'points': pts,
                    'axes': ('r_coord', 'intensity', 'filter_index')}
        return {'text': self._fmt(name, result)}

    def shell_commands(self) -> Dict:
        return {
            'jwst_oct':   lambda I=None: spectral_to_octonion(I or [1.0]*8),
            'jwst_H':     lambda: synthetic_spectrum('hydrogen'),
            'jwst_star':  lambda: synthetic_spectrum('stellar'),
            'lambda_r':   lambda lam=2000.0: lambda_to_r(lam),
        }
