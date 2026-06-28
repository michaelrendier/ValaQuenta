"""
ainulindale_engine.modules.constants.tools
==========================================
ConstantsModule — registry contract.

Version: 0.100
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    derive_i,
    derive_sqrt,
    derive_e,
    derive_pi,
    derive_phi,
    euler_identity,
    derive_omega_zs,
    derive_alpha_fermat,
    derive_d_star,
    derive_lambda,
    all_constants,
)


class ConstantsModule(EquationModule):

    @property
    def name(self): return 'constants'

    @property
    def display_name(self): return 'Tier 0 Constants — π φ e √ i derived from H_RB'

    @property
    def version(self): return '0.120'

    @property
    def description(self):
        return (
            'Tier 0 Root Constants: π, φ, e, √, i, OMEGA_ZS, α_F, d*, Λ — '
            'all drop out of H_RB algebraic structure. '
            'Two ceilings force domain [α_F, OMEGA_ZS]. d* has 4 values (tower→ln(10) Open Prob 2). '
            'Λ: J_neg at cosmological scale; Sombrero = Hawking pair; OMEGA_ZS = de Sitter attractor. '
            'Einstein wrote it in 1915, removed it 1917, universe re-inserted 1998 at 40σ.'
        )

    @property
    def confidence_floor(self): return 'ESTABLISHED'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='derive_lambda',
                display='Λ — Einstein cosmological constant: J_neg at cosmological scale',
                latex=r'G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi GT_{\mu\nu},\;\Lambda=J_{\rm neg},\;\Omega_\Lambda\to\Omega_{\zeta\Sigma}',
                radian_form='Three-phase balance forces Λ. Sombrero=Hawking waveform. OMEGA_ZS=de Sitter attractor.',
                confidence='σ=∞ (existence); σ>40 (Nobel 1998); OPEN (value from f)',
                code_verified=True,
                params=[],
                compute=derive_lambda,
                display_options=[],
            ),
            Equation(
                name='all_constants',
                display='All 9 constants — Tier 0: π φ e √ i Ω_ζΣ α_F d* Λ',
                latex=r'i,\sqrt{\cdot},e,\pi,\varphi\;\text{drop out of }\Sigma_{RB}',
                radian_form='Every constant emerges from the prime distribution. No geometric definition used.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=all_constants,
                display_options=[],
            ),
            Equation(
                name='derive_i',
                display='i — Cayley-Dickson closure: x²+1=0  [σ=i, democratic facet]',
                latex=r'i:=(0,1)\in\mathbb{C},\;i^2=-1,\;|p^{-i}|=1\;\forall p',
                radian_form='CD first doubling forces (0,1)²=(−1,0). i drops out as closure element.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=derive_i,
                display_options=[],
            ),
            Equation(
                name='derive_sqrt',
                display='√ — σ=½ IS the square root: G_p(½)=1/√p  [critical line]',
                latex=r'G_p(\tfrac{1}{2})=p^{-1/2},\quad x^{\frac{1}{2}+i\gamma}=\sqrt{x}\cdot e^{i\gamma\ln x}',
                radian_form='Critical coupling = inverse √ of prime. Every Riemann oscillation carries √x envelope.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=derive_sqrt,
                display_options=[],
            ),
            Equation(
                name='derive_e',
                display='e — Berry-Keating canonical: ẋ=x → x(t)=e^t  [σ=e, thermodynamic]',
                latex=r'\dot{x}=x\;\Rightarrow\;x(t)=x_0 e^t,\quad p=\ln\dot{x}\Rightarrow\dot{x}=e^p',
                radian_form='BK Hamilton equations force x(t)=e^t. e = base satisfying d/dt(e^t)=e^t.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=derive_e,
                display_options=[],
            ),
            Equation(
                name='derive_pi',
                display='π — U(1) normalisation (2/π)·π=2 AND Basel ζ(2)=π²/6  [σ=π, gauge]',
                latex=r'\zeta(2)=\frac{\pi^2}{6},\quad\frac{2}{\pi}\cdot\pi=2',
                radian_form='Two independent derivations from prime distribution. No circle drawn.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=derive_pi,
                display_options=[],
            ),
            Equation(
                name='derive_phi',
                display='φ — CD recursion eigenvalue f(x)=1+1/x  [σ=φ, structural]',
                latex=r'\varphi^2=\varphi+1,\quad H_{RB}(\varphi)=H_{RB}(1)\cdot H_{RB}(1/\varphi)',
                radian_form='Fixed point of f(x)=1+1/x. Fibonacci series is integer shadow. H_RB factorises.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=derive_phi,
                display_options=[],
            ),
            Equation(
                name='euler_identity',
                display='e^{iπ}+1=0 — theorem of H_RB, not a definition',
                latex=r'e^{i\pi}+1=0\;\Leftrightarrow\;J_R+J_G+J_B=0',
                radian_form='e (BK) + i (CD) + π (U(1)) composed. Three-channel conservation law.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=euler_identity,
                display_options=[],
            ),
            Equation(
                name='derive_omega_zs',
                display='Ω_ζΣ = W(1) — thermal information ceiling T·e^T=1',
                latex=r'T=e^{-T}\Leftrightarrow T\cdot e^T=1\Rightarrow\Omega_{\zeta\Sigma}=W(1)=0.56714\ldots',
                radian_form='Self-referential Boltzmann fixed point. Banach theorem → unique solution W(1).',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=derive_omega_zs,
                display_options=[],
            ),
            Equation(
                name='derive_alpha_fermat',
                display='α_F = 1/137... — causality ceiling v_1=α·c<c',
                latex=r'\alpha_F=\frac{e^2}{4\pi\varepsilon_0\hbar c},\;v_1=\alpha_F c<c',
                radian_form='Causality ceiling: Bohr velocity v_1<c forces α_F as domain floor.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=derive_alpha_fermat,
                display_options=[],
            ),
            Equation(
                name='derive_d_star',
                display='d* — 4 values: BK spectral floor, gap=0.000707, tower→ln(10) [OPEN]',
                latex=r'd^*=0.24600,\;\delta=\Omega_{\zeta\Sigma}-d^*\ln10=0.000707',
                radian_form='BK spectral floor. GAP=Yang-Mills mass gap. Full tower d*_R+d*_C+d*_H+d*_O=ln(10) OPEN.',
                confidence='ESTABLISHED (d*_R); OPEN (full tower)',
                code_verified=True,
                params=[],
                compute=derive_d_star,
                display_options=[],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in constants module")
        filtered = {k: params[k] for k in eq.params if k in params}
        result = eq.compute(**filtered)
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str,
                    params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)['result']
        return {'text': self._fmt(equation_name, result)}

    def _fmt(self, name: str, result: Any) -> str:
        if isinstance(result, dict):
            lines = [f'  [{name}]']
            for k, v in result.items():
                if isinstance(v, list) and v and isinstance(v[0], str):
                    lines.append(f'  {k}:')
                    for item in v:
                        lines.append(f'    • {item}')
                elif isinstance(v, float):
                    lines.append(f'  {k:35s} = {v:.10f}')
                elif isinstance(v, bool):
                    lines.append(f'  {k:35s} = {v}')
                elif not isinstance(v, (list, dict)):
                    lines.append(f'  {k:35s} = {v}')
            return '\n'.join(lines)
        return f'  {name}: {result}'
