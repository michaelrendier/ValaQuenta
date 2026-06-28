"""
ainulindale_engine.modules.lagrangian.tools
=============================================
LagrangianModule — registry contract implementation.

Equations:
  1. polar_lagrangian        full L_NN polar integral
  2. L_kinetic               -1/4 · F²
  3. L_matter                i·Ψ̄·D·Ψ kinetic
  4. L_bias                  Mexican hat / Higgs
  5. L_coupling              (1/φ)·Yukawa
  6. alpha_nn_running        α_NN(r) running coupling
  7. rg_flow                 RG flow α_NN, ħ_NN vs layer
  8. mastery_check           crystallization condition

Display modes: complex_plane (running coupling), 3d_cartesian (RG flow), text

Version: 0.111
"""

import math
from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    FieldState, polar_lagrangian, rg_flow,
    L_kinetic, L_matter, L_bias, L_coupling,
    alpha_nn_from_r, layer_to_r, mastery_check,
    ALG_C, ALG_H, ALG_O,
)


class LagrangianModule(EquationModule):

    @property
    def name(self): return 'lagrangian'

    @property
    def display_name(self): return 'L_NN  Ainulindale Lagrangian'

    @property
    def version(self): return '0.111'

    @property
    def description(self):
        return (
            'The four-term SMNNIP Lagrangian density L_NN = (2/π)∮[L_kin + L_mat '
            '+ (1/φ)L_bias + L_coup] r dr dθ. Running coupling α_NN(r) = g²/(4π·ħ_NN·ln(1/r)). '
            'RG flow per algebra stratum. Mastery crystallization condition.'
        )

    @property
    def confidence_floor(self): return 'THEORETICAL'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='polar_lagrangian',
                display='Full L_NN — polar integral',
                latex=r'\mathcal{L}_{NN} = \frac{2}{\pi}\oint\bigl[L_{kin}+L_{mat}+\tfrac{1}{\varphi}L_{bias}+L_{coup}\bigr]\,r\,dr\,d\theta',
                radian_form='L_NN = (2/pi) * integral [Lk+Lm+Lb+Lc] r dr dtheta',
                confidence='THEORETICAL',
                code_verified=True,
                params=['psi_norms', 'A_comps', 'beta_norms', 'algebra', 'layer'],
                compute=None,
                display_options=['text', '3d_cartesian'],
            ),
            Equation(
                name='L_kinetic',
                display='L_kin = -1/4 · F_μν^a · F^{μν,a}',
                latex=r'\mathcal{L}_{kin} = -\tfrac{1}{4}F_{\mu\nu}^a F^{\mu\nu,a}',
                radian_form='L_kin = -0.25 * sum(F_a^2)',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['A_comps', 'g', 'algebra'],
                compute=lambda A_comps, g, algebra: L_kinetic(A_comps, g, algebra),
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='L_matter',
                display='L_mat = i·Ψ̄·γ^μ·D_μ·Ψ',
                latex=r'\mathcal{L}_{mat} = i\bar{\Psi}\gamma^\mu D_\mu\Psi',
                radian_form='L_mat ~ sum |Psi_i|^2 * (g*A_i)^2',
                confidence='THEORETICAL',
                code_verified=True,
                params=['psi_norms', 'A_comps', 'g', 'hbar_nn', 'algebra'],
                compute=lambda psi_norms, A_comps, g, hbar_nn, algebra: L_matter(psi_norms, A_comps, g, hbar_nn, algebra),
                display_options=['text'],
            ),
            Equation(
                name='L_bias',
                display='L_bias — Mexican hat / Higgs potential',
                latex=r'\mathcal{L}_{bias} = \tfrac{1}{2}\mu^2\beta^2 - \tfrac{1}{4}\lambda\beta^4',
                radian_form='L_bias = 0.5*mu_sq*|beta|^2 - 0.25*lambda*|beta|^4',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['beta_norms', 'mu_sq', 'lam'],
                compute=lambda beta_norms, mu_sq, lam: L_bias(beta_norms, mu_sq, lam),
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='L_coupling',
                display='L_coup = -(1/φ)·Γ_ij·Ψ̄^L·β·Ψ^R  (Yukawa)',
                latex=r'\mathcal{L}_{coup} = -\tfrac{1}{\varphi}\Gamma_{ij}\bar{\Psi}^L\beta\Psi^R',
                radian_form='L_coup = -(1/phi) * g * sum psi_i * beta_i',
                confidence='THEORETICAL',
                code_verified=True,
                params=['psi_norms', 'beta_norms', 'g'],
                compute=lambda psi_norms, beta_norms, g: L_coupling(psi_norms, beta_norms, g),
                display_options=['text'],
            ),
            Equation(
                name='alpha_nn_running',
                display='α_NN(r) = g²/(4π·ħ_NN·ln(1/r))  running coupling',
                latex=r'\alpha_{NN}(r)=\frac{g^2}{4\pi\,\hbar_{NN}\ln(1/r)}',
                radian_form='alpha_nn(r) = g^2 / (4*pi * hbar_nn * ln(1/r))',
                confidence='THEORETICAL',
                code_verified=True,
                params=['g', 'hbar_nn', 'r'],
                compute=lambda g, hbar_nn, r: alpha_nn_from_r(g, hbar_nn, r),
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='rg_flow',
                display='RG flow α_NN(l), ħ_NN(l) — all strata',
                latex=r'\alpha_{NN}(l)=\frac{\alpha_0}{1+\beta_0\alpha_0\ln(l/l_0)}',
                radian_form='alpha_nn(l) = alpha_0 / (1 + beta_0*alpha_0*ln(l/l_0))',
                confidence='THEORETICAL',
                code_verified=True,
                params=['alpha_0', 'hbar_0', 'algebra', 'max_layer'],
                compute=None,
                display_options=['text', '3d_cartesian', 'complex_plane'],
            ),
            Equation(
                name='mastery_check',
                display='Mastery: vev_distance < ħ_NN/2',
                latex=r'\bigl||\beta|-v\bigr| < \hbar_{NN}/2',
                radian_form='|beta_norm - vev| < hbar_nn / 2',
                confidence='THEORETICAL',
                code_verified=True,
                params=['beta_norms', 'vev', 'hbar_nn'],
                compute=lambda beta_norms, vev, hbar_nn: mastery_check(beta_norms, vev, hbar_nn),
                display_options=['text'],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in lagrangian module")

        if equation_name == 'polar_lagrangian':
            state = self._params_to_state(params)
            result = polar_lagrangian(state)
        elif equation_name == 'rg_flow':
            max_l = int(params.get('max_layer', 10))
            result = rg_flow(
                float(params.get('alpha_0', 0.01)),
                float(params.get('hbar_0', 0.1)),
                int(params.get('algebra', ALG_C)),
                list(range(1, max_l + 1))
            )
        elif eq.compute is not None:
            result = eq.compute(**{k: params[k] for k in eq.params if k in params})
        else:
            result = {'note': 'no direct compute — use viewer_data'}

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

    def _fmt(self, name: str, result) -> str:
        if isinstance(result, dict):
            lines = [f"  {name}"]
            for k, v in result.items():
                if isinstance(v, float):
                    lines.append(f"  {k:20s} = {v:.8f}")
                elif isinstance(v, list) and v and isinstance(v[0], float):
                    lines.append(f"  {k:20s} = [{', '.join(f'{x:.4f}' for x in v[:6])}{'...' if len(v)>6 else ''}]")
                else:
                    lines.append(f"  {k:20s} = {v}")
            return '\n'.join(lines)
        return f"  {name}: {result}"

    def _params_to_state(self, params: Dict) -> FieldState:
        def _fl(k, default): return params.get(k, default)
        psi   = _fl('psi_norms',  [0.5, 0.4, 0.3])
        A     = _fl('A_comps',    [0.1, 0.05])
        beta  = _fl('beta_norms', [1.0, 0.9, 0.8])
        if isinstance(psi, (int, float)):   psi   = [float(psi)]
        if isinstance(A, (int, float)):     A     = [float(A)]
        if isinstance(beta, (int, float)):  beta  = [float(beta)]
        return FieldState(
            psi=psi, A=A, beta=beta,
            algebra=int(_fl('algebra', ALG_C)),
            layer=int(_fl('layer', 1)),
            hbar_nn=float(_fl('hbar_nn', 0.1)),
            g_coup=float(_fl('g', 0.01)),
            mu_sq=float(_fl('mu_sq', -1.0)),
            lam=float(_fl('lam', 0.5)),
            vev=float(_fl('vev', 1.0)),
        )

    def _complex_data(self, name, params, result) -> Dict:
        """Running coupling α_NN vs r as a polar trajectory."""
        if name == 'alpha_nn_running':
            pts = []
            for i in range(1, 64):
                r = i / 64.0
                a = alpha_nn_from_r(
                    float(params.get('g', 0.1)),
                    float(params.get('hbar_nn', 0.1)),
                    r
                )
                pts.append((r, min(a, 10.0)))
            cartesian = [(r * math.cos(2 * math.pi * r),
                          r * math.sin(2 * math.pi * r)) for r, _ in pts]
            return {
                'type':       'polar_trajectory',
                'trajectory': pts,
                'cartesian':  cartesian,
            }
        elif name == 'L_bias':
            # Mexican hat: V(β) vs |β|
            pts = []
            mu_sq = float(params.get('mu_sq', -1.0))
            lam   = float(params.get('lam', 0.5))
            for i in range(-32, 33):
                b = i * 0.1
                V = 0.5 * mu_sq * b*b - 0.25 * lam * b**4
                pts.append((b, V))
            cartesian = pts
            return {'type': 'polar_trajectory', 'trajectory': pts, 'cartesian': cartesian}
        return {'text': self._fmt(name, result)}

    def _3d_data(self, name, params, result) -> Dict:
        """RG flow as 3D: x=layer, y=alpha_nn, z=algebra index."""
        if name in ('rg_flow', 'polar_lagrangian'):
            layers = list(range(1, int(params.get('max_layer', 10)) + 1))
            pts = []
            for alg in (ALG_C, ALG_H, ALG_O):
                flow = rg_flow(
                    float(params.get('alpha_0', 0.01)),
                    float(params.get('hbar_0', 0.1)),
                    alg, layers
                )
                for i, (l, a) in enumerate(zip(layers, flow['alpha'])):
                    pts.append((float(l), a, float(alg)))
            return {
                'type':   '3d_flow',
                'points': pts,
                'axes':   ('layer', 'α_NN', 'algebra'),
            }
        return {'text': self._fmt(name, result)}

    def shell_commands(self) -> Dict:
        return {
            'lagrangian': lambda layer=1, g=0.01: polar_lagrangian(FieldState(
                psi=[0.5,0.4,0.3], A=[0.1,0.05], beta=[1.0,0.9,0.8],
                algebra=ALG_C, layer=layer, g_coup=g,
            )),
            'alpha_r': lambda r=0.5, g=0.1, hbar=0.1: alpha_nn_from_r(g, hbar, r),
            'rg':      lambda alg=ALG_C, n=10: rg_flow(0.01, 0.1, alg, list(range(1, n+1))),
        }
