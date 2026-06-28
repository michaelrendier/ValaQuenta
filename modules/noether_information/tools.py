"""
ainulindale_engine.modules.noether_information.tools
======================================================
NoetherInformationModule — registry contract.

Equations:
  1. information_current     J_info^μ, I_info, Φ_flux, t_e
  2. entropic_arrow          ∂_l I ≥ 0 across layer history
  3. delta_J_info            cycle-averaged violation
  4. information_capacity    C_max = n × log₂(dim) bits

Version: 0.111
"""

import math
from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    ALG_R, ALG_C, ALG_H, ALG_O, ALG_NAME, ALG_DIM,
    shannon_information, phi_flux, information_current,
    entropic_arrow, delta_J_info, information_capacity,
)


class NoetherInformationModule(EquationModule):

    @property
    def name(self): return 'noether_information'

    @property
    def display_name(self): return 'J_info  Information Current'

    @property
    def version(self): return '0.111'

    @property
    def description(self):
        return (
            'Noether current for information-translation symmetry of L_NN. '
            'I_information = Shannon entropy of activation distribution. '
            'Phi_flux = information flux through algebra boundary. '
            't_e = entropic time (layer where I_info is maximal). '
            'Entropic arrow: ∂_l I_info ≥ 0.'
        )

    @property
    def confidence_floor(self): return 'CONJECTURE'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='information_current',
                display='J_info^μ — information Noether current',
                latex=r'J_{info}^\mu = \frac{\partial\mathcal{L}}{\partial(\partial_\mu\Phi)}\delta\Phi',
                radian_form='J_info^0 = I_info/layer,  J_info^1 = Phi_flux',
                confidence='CONJECTURE',
                code_verified=True,
                params=['psi_norms', 'algebra', 'layer', 'total_layers'],
                compute=None,
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='entropic_arrow',
                display='Entropic arrow: ∂_l I_info ≥ 0',
                latex=r'\partial_l I_{info} \geq 0',
                radian_form='I_info grows monotonically with layer depth (until sedenion)',
                confidence='CONJECTURE',
                code_verified=True,
                params=['n_steps', 'algebra'],
                compute=None,
                display_options=['text', '3d_cartesian', 'complex_plane'],
            ),
            Equation(
                name='delta_J_info',
                display='ΔJ_info — cycle-averaged information current violation',
                latex=r'\Delta J_{info} = |J^0_{info,l} - J^0_{info,l-1}|',
                radian_form='delta_J_info = |J_info_0_curr - J_info_0_prev|',
                confidence='CONJECTURE',
                code_verified=True,
                params=['psi_norms', 'algebra', 'layer'],
                compute=None,
                display_options=['text'],
            ),
            Equation(
                name='information_capacity',
                display='C_max = n_neurons × log₂(dim_algebra) bits',
                latex=r'C_{max} = n_{neurons}\,\log_2(\dim\mathcal{A})',
                radian_form='C_max bits — max info storage at algebra stratum',
                confidence='THEORETICAL',
                code_verified=True,
                params=['algebra', 'n_neurons'],
                compute=lambda algebra, n_neurons: information_capacity(int(algebra), int(n_neurons)),
                display_options=['text', '3d_cartesian'],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in noether_information module")

        psi   = self._get_psi(params)
        alg   = int(params.get('algebra', ALG_C))
        layer = int(params.get('layer', 1))
        total = int(params.get('total_layers', 10))

        if equation_name == 'information_current':
            result = information_current(psi, alg, layer, total)

        elif equation_name == 'entropic_arrow':
            n_steps = int(params.get('n_steps', 20))
            # Build a psi history with information growing then saturating
            history = []
            for s in range(n_steps):
                t = (s + 1) / n_steps
                # Information grows with layer: activate more neurons
                n_active = max(1, int(len(psi) * t))
                psi_s = [psi[i] * (1.0 - 0.3 * (1 - t)) for i in range(n_active)]
                history.append(psi_s)
            result = entropic_arrow(history, alg)

        elif equation_name == 'delta_J_info':
            J_curr = information_current(psi, alg, layer, total)
            psi_prev = [p * 0.9 for p in psi]
            J_prev = information_current(psi_prev, alg, max(layer-1, 1), total)
            dJ = delta_J_info(J_curr, J_prev)
            result = {
                'delta_J_info'  : dJ,
                'J_info_0_curr' : J_curr['J_info_0'],
                'J_info_0_prev' : J_prev['J_info_0'],
                'I_curr'        : J_curr['I_info'],
                'I_prev'        : J_prev['I_info'],
            }

        elif eq.compute is not None:
            result = eq.compute(**{k: params[k] for k in eq.params if k in params})

        else:
            result = {'note': 'no compute path'}

        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str,
                    params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)
        r = result['result']

        if display_mode == 'text':
            return {'text': self._fmt(equation_name, r)}
        elif display_mode == 'complex_plane':
            return self._complex_data(equation_name, params, r)
        elif display_mode == '3d_cartesian':
            return self._3d_data(equation_name, params, r)
        return {'text': self._fmt(equation_name, r)}

    def _fmt(self, name, result) -> str:
        if isinstance(result, dict):
            lines = [f"  {name}"]
            for k, v in result.items():
                if isinstance(v, float):
                    lines.append(f"  {k:24s} = {v:.8f}")
                elif isinstance(v, list) and v and isinstance(v[0], float):
                    lines.append(f"  {k:24s} = [{', '.join(f'{x:.4f}' for x in v[:6])}{'...' if len(v)>6 else ''}]")
                else:
                    lines.append(f"  {k:24s} = {v}")
            return '\n'.join(lines)
        return f"  {name}: {result}"

    def _get_psi(self, params) -> List[float]:
        psi = params.get('psi_norms', [0.5, 0.4, 0.3, 0.2, 0.1])
        if isinstance(psi, (int, float)):
            psi = [float(psi)]
        return psi

    def _complex_data(self, name, params, result) -> Dict:
        if name == 'information_current':
            # Plot J_info spiral: layer vs I_info vs Phi_flux
            alg = int(params.get('algebra', ALG_C))
            total = int(params.get('total_layers', 10))
            psi = self._get_psi(params)
            pts = []
            import math as _m
            for l in range(1, total + 1):
                J = information_current(psi, alg, l, total)
                r = J['t_e']
                theta = 2 * _m.pi * l / total
                pts.append((r * _m.cos(theta), r * _m.sin(theta)))
            return {'type': 'polar_trajectory', 'cartesian': pts,
                    'trajectory': [(i, pts[i][0]) for i in range(len(pts))]}
        elif name == 'entropic_arrow':
            I_vals = result.get('I_values', [])
            pts = [(float(i), I_vals[i]) for i in range(len(I_vals))]
            cartesian = pts
            return {'type': 'polar_trajectory', 'cartesian': cartesian,
                    'trajectory': pts}
        return {'text': self._fmt(name, result)}

    def _3d_data(self, name, params, result) -> Dict:
        if name == 'entropic_arrow':
            I_vals = result.get('I_values', [])
            J_vals = result.get('J0_values', [])
            pts = [(float(i), I_vals[i], J_vals[i]) for i in range(min(len(I_vals), len(J_vals)))]
            return {'type': '3d_flow', 'points': pts, 'axes': ('layer', 'I_info', 'J_info_0')}
        elif name == 'information_capacity':
            pts = [(float(a), information_capacity(a, int(params.get('n_neurons', 4)))['C_max_bits'], float(ALG_DIM[a]))
                   for a in (ALG_R, ALG_C, ALG_H, ALG_O)]
            return {'type': '3d_flow', 'points': pts, 'axes': ('algebra', 'C_max_bits', 'dim')}
        return {'text': self._fmt(name, result)}

    def shell_commands(self) -> Dict:
        return {
            'J_info':   lambda psi=None, alg=ALG_C, layer=1:
                            information_current(psi or [0.5,0.4,0.3,0.2], alg, layer),
            'I_info':   lambda psi=None:
                            shannon_information(psi or [0.5,0.4,0.3,0.2]),
            'capacity': lambda alg=ALG_O, n=4: information_capacity(alg, n),
        }
