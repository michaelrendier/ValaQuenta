"""
ainulindale_engine.modules.sigma_expansion.tools
==================================================
SigmaExpansionModule — registry contract.

Equations:
  1. moments               M_0..M_3, L_0..L_3 per channel (the raw inputs)
  2. taylor_coefficients   derived c1, c3 (closed form, not fitted)
  3. predict_P_red         cheap closed-form P_red(sigma) prediction
  4. verify_against_actual error-check: predicted vs. directly-computed

Version: 0.100
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    moments, taylor_coefficients, predict_P_red, verify_against_actual,
)


class SigmaExpansionModule(EquationModule):

    @property
    def name(self): return 'sigma_expansion'

    @property
    def display_name(self): return 'Sigma Expansion — J_red/J_blue Balance Curve'

    @property
    def version(self): return '0.100'

    @property
    def description(self):
        return (
            'Closed-form Taylor expansion of P_red(sigma)=|J_red|^2/(|J_red|^2+|J_blue|^2) '
            'around sigma=1/2. c1, c3 derived (not fitted) from Dirichlet-projection '
            'moments. Verified to ~1e-6 near sigma=1/2 against direct computation. '
            'Raw |J_red|^2+|J_blue|^2 is NOT constant across sigma -- minimum at 1/2, '
            'not a flat quantum-probability-style conservation.'
        )

    @property
    def confidence_floor(self): return 'THEORETICAL'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='moments',
                display='M_n, L_n moments at sigma=1/2 (raw inputs to the derivation)',
                latex=r'M_n=\sum_k k^{-1/2}(\ln k)^n,\quad L_n=\sum_k A_k\phi_k k^{-1/2}(\ln k)^n',
                radian_form='M_n = sum k^-0.5 (ln k)^n; L_n = sum A_k phi_k k^-0.5 (ln k)^n',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['text'],
                compute=lambda text='O Captain My Captain': moments(text),
                display_options=['text'],
            ),
            Equation(
                name='taylor_coefficients',
                display='c1, c3 — derived (not fitted) Taylor coefficients of P_red(sigma) at 1/2',
                latex=r'P_{red}(\sigma)-\tfrac12\approx c_1 d+c_3 d^3,\quad d=\sigma-\tfrac12',
                radian_form='P_red(sigma) - 0.5 ~= c1*(sigma-0.5) + c3*(sigma-0.5)^3',
                confidence='THEORETICAL',
                code_verified=True,
                params=['text'],
                compute=lambda text='O Captain My Captain': taylor_coefficients(text),
                display_options=['text'],
            ),
            Equation(
                name='predict_P_red',
                display='Cheap closed-form P_red(sigma) prediction (no sigma-sweep needed)',
                latex=r'\hat P_{red}(\sigma)=\tfrac12+c_1 d+c_3 d^3',
                radian_form='predicted P_red at a given sigma from the derived coefficients',
                confidence='THEORETICAL',
                code_verified=True,
                params=['text', 'sigma'],
                compute=lambda text='O Captain My Captain', sigma=0.6: predict_P_red(text, float(sigma)),
                display_options=['text'],
            ),
            Equation(
                name='verify_against_actual',
                display='Error-check: predicted vs. directly-computed P_red(sigma), residuals',
                latex=r'\text{residual}(\sigma)=P_{red}^{actual}(\sigma)-\hat P_{red}(\sigma)',
                radian_form='compares cheap prediction against expensive direct computation',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['text'],
                compute=lambda text='O Captain My Captain': verify_against_actual(text),
                display_options=['text'],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in sigma_expansion module")
        filtered = {k: params[k] for k in eq.params if k in params}
        result = eq.compute(**filtered)
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str,
                     params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)['result']
        return {'text': self._fmt(equation_name, result)}

    def _fmt(self, name, result) -> str:
        lines = [f'  {name}']
        if isinstance(result, dict):
            for k, v in result.items():
                if isinstance(v, (int, float)):
                    lines.append(f'  {k:16s} = {v:.8f}')
                elif isinstance(v, list) and k == 'rows':
                    for row in v[:19]:
                        lines.append(
                            f"    sigma={row['sigma']:.2f}  actual={row['actual']:.6f}  "
                            f"predicted={row['predicted']:.6f}  residual={row['residual']:+.6f}"
                        )
                elif k != 'L_by_channel':
                    lines.append(f'  {k:16s} = {v}')
        return '\n'.join(lines)
