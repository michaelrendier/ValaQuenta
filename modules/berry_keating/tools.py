"""
ainulindale_engine.modules.berry_keating.tools
================================================
BerryKeatingModule — registry contract.

Equations:
  1. d_star_gap_report    complete gap workbench
  2. gap_candidates       candidate expressions for d*
  3. h_nn_eigenvalues     H_NN spectrum (harmonic approx)
  4. xp_spectrum          classical xp torus
  5. T_map                T coordinate scaffold at single x
  6. T_map_trajectory     T map curve for viewer

Version: 0.111
"""

import math
from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    D_STAR_SPEC, OMEGA_ZS, GAP,
    d_star_gap_report, gap_candidates,
    h_nn_eigenvalues, xp_spectrum_discrete,
    T_map_scaffold, T_map_trajectory,
)


class BerryKeatingModule(EquationModule):

    @property
    def name(self): return 'berry_keating'

    @property
    def display_name(self): return 'H_NN  Berry-Keating Operator'

    @property
    def version(self): return '0.111'

    @property
    def description(self):
        return (
            f'H_NN candidate xp operator. d* gap workbench (gap={GAP:.6f}). '
            f'T coordinate map scaffold. Open Problems 2 & 3.'
        )

    @property
    def confidence_floor(self): return 'OPEN'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='d_star_gap_report',
                display=f'd* gap workbench  [gap = {GAP:.6f}  OPEN]',
                latex=r'd^*\times\ln10\approx\Omega\quad(\Delta\approx0.000707)',
                radian_form='d* x ln(10) = 0.56644  vs  Omega = 0.56714  gap = 0.000707',
                confidence='OPEN',
                code_verified=True,
                params=[],
                compute=d_star_gap_report,
                display_options=['text'],
            ),
            Equation(
                name='gap_candidates',
                display='Gap candidate expressions — sorted by proximity to Ω',
                latex=r'\text{candidates for }d^*\text{ from elementary constants}',
                radian_form='expressions evaluated and gap from Omega computed',
                confidence='OPEN',
                code_verified=True,
                params=[],
                compute=gap_candidates,
                display_options=['text', '3d_cartesian'],
            ),
            Equation(
                name='h_nn_eigenvalues',
                display='H_NN eigenvalues — harmonic oscillator approximation',
                latex=r'E_n=\hbar_{NN}(n+\tfrac{1}{2})',
                radian_form='E_n = hbar_nn * (n + 0.5)  for n = 0..n_max',
                confidence='OPEN',
                code_verified=True,
                params=['hbar_nn', 'n_max'],
                compute=lambda hbar_nn=0.1, n_max=10: h_nn_eigenvalues(hbar_nn, int(n_max)),
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='xp_spectrum',
                display='Classical xp torus  x·p = d*·ħ_NN',
                latex=r'H_{xp}=xp,\quad x\cdot p=d^*\cdot\hbar_{NN}',
                radian_form='hyperbola x*p = E at E = d_star * hbar_nn',
                confidence='OPEN',
                code_verified=True,
                params=['hbar_nn'],
                compute=lambda hbar_nn=0.1: xp_spectrum_discrete(hbar_nn),
                display_options=['text', 'complex_plane', '3d_cartesian'],
            ),
            Equation(
                name='T_map',
                display='T coordinate map at single x  [Open Problem 3]',
                latex=r'T:x\mapsto x\,e^{i\,d^*\ln x}',
                radian_form='T_re = x*cos(d*ln(x)),  T_im = x*sin(d*ln(x))',
                confidence='OPEN',
                code_verified=True,
                params=['x'],
                compute=lambda x=1.0: T_map_scaffold(x),
                display_options=['text'],
            ),
            Equation(
                name='T_map_trajectory',
                display='T map curve  x ∈ [x_min, x_max]',
                latex=r'T(x)=x\,e^{id^*\ln x},\quad x\in[x_{min},x_{max}]',
                radian_form='T map trajectory for viewer — complex plane spiral',
                confidence='OPEN',
                code_verified=True,
                params=['x_min', 'x_max'],
                compute=lambda x_min=0.1, x_max=10.0: T_map_trajectory(x_min, x_max),
                display_options=['text', 'complex_plane', '3d_cartesian'],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in berry_keating module")
        filtered = {k: params[k] for k in eq.params if k in params}
        result = eq.compute(**filtered)
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str,
                    params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)['result']
        if display_mode == 'text':
            return {'text': self._fmt(equation_name, result)}
        elif display_mode == 'complex_plane':
            return self._complex_data(equation_name, params, result)
        elif display_mode == '3d_cartesian':
            return self._3d_data(equation_name, result)
        return {'text': self._fmt(equation_name, result)}

    def _fmt(self, name, result) -> str:
        if isinstance(result, list):
            lines = [f"  {name}"]
            for item in result[:12]:
                if isinstance(item, dict):
                    lines.append(f"  {item.get('expression','?'):20s}  val={item.get('value',0):.6f}  gap={item.get('gap',0):.6f}  {'✓ better' if item.get('better') else ''}")
            return '\n'.join(lines)
        if isinstance(result, dict):
            lines = [f"  {name}"]
            for k, v in result.items():
                if isinstance(v, float):
                    lines.append(f"  {k:24s} = {v:.10f}")
                elif isinstance(v, list) and v and isinstance(v[0], float):
                    lines.append(f"  {k:24s} = [{', '.join(f'{x:.4f}' for x in v[:6])}{'...' if len(v)>6 else ''}]")
                elif not isinstance(v, (list, dict)):
                    lines.append(f"  {k:24s} = {v}")
            return '\n'.join(lines)
        return f"  {name}: {result}"

    def _complex_data(self, name, params, result) -> Dict:
        if name == 'T_map_trajectory':
            cartesian = result.get('cartesian', [])
            return {'type': 'polar_trajectory', 'cartesian': cartesian,
                    'trajectory': [(i, c[0]) for i, c in enumerate(cartesian)]}
        elif name == 'h_nn_eigenvalues':
            eigs = result.get('eigenvalues', [])
            import math as _m
            cartesian = [(e * _m.cos(2 * _m.pi * i / max(len(eigs), 1)),
                          e * _m.sin(2 * _m.pi * i / max(len(eigs), 1)))
                         for i, e in enumerate(eigs)]
            return {'type': 'polar_trajectory', 'cartesian': cartesian,
                    'trajectory': [(i, eigs[i]) for i in range(len(eigs))]}
        elif name == 'xp_spectrum':
            xs = result.get('x_values', [])
            ps = result.get('p_values', [])
            cartesian = list(zip(xs, ps))
            return {'type': 'polar_trajectory', 'cartesian': cartesian,
                    'trajectory': cartesian}
        return {'text': self._fmt(name, result)}

    def _3d_data(self, name, result) -> Dict:
        if name == 'T_map_trajectory':
            traj = result.get('trajectory', [])
            pts  = [(t['x'], t['T_re'], t['T_im']) for t in traj]
            return {'type': '3d_flow', 'points': pts, 'axes': ('x', 'T_re', 'T_im')}
        elif name == 'gap_candidates':
            cands = result if isinstance(result, list) else []
            pts = [(float(i), c['value'], c['gap']) for i, c in enumerate(cands)]
            return {'type': '3d_flow', 'points': pts, 'axes': ('index', 'd*_candidate', 'gap')}
        elif name == 'xp_spectrum':
            xs = result.get('x_values', [])
            ps = result.get('p_values', [])
            E  = result.get('energy_E', 0.0)
            pts = [(x, p, E) for x, p in zip(xs, ps)]
            return {'type': '3d_flow', 'points': pts, 'axes': ('x', 'p', 'E')}
        return {'text': self._fmt(name, result)}

    def shell_commands(self) -> Dict:
        return {
            'bk_gap':  d_star_gap_report,
            'T_map':   lambda x=1.0: T_map_scaffold(x),
            'H_nn':    lambda n=10, h=0.1: h_nn_eigenvalues(h, n),
        }
