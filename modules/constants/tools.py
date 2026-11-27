"""
ValaQuenta.modules.constants.tools
==================================
ConstantsModule — registry contract.

Version: 0.130
"""


# d* faces (all four are needed to chart ln(10) in Universal Native Space):
#   d*         = 0.24600          the value the code runs with (Boundary, σ_ζ=½ plane)
#   d*_taut    = 0.246307201473  A_π/ln10, the Flow (radial unit)
#   d*_RG      = dimension 8; numeric OPEN, no closed form  the Stability (centre r=0)
#   d*_ln(10)  = 0.5671432904   d*_taut·ln10 = A_π, the Translator (log bridge)
# Full story of d*: Ainulindale/wiki/17_alpha_omega_d_star.md; ~/.clauderc_canonical_maths @RCCM_FOUR_DSTAR; FourthAgePapers/DStarRG
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
    r"""
    Tier 0 Constants — π φ e √ i derived from H_RB

    Tier 0 Root Constants: π, φ, e, √, i, A_PI, α_F, d\*, Λ — all drop out of
    H_RB algebraic structure. Two ceilings bound the domain [α_F, A_PI]. d\* has
    four named faces (Boundary, Flow, Stability, Translator). Λ: J_neg at cosmological scale;
    Sombrero = Hawking pair; A_PI = de Sitter attractor. Einstein wrote it
    in 1915, removed it 1917, universe re-inserted 1998 at 40σ.

    Registry module for ``constants``: :meth:`formulary` lists the equations, :meth:`run` executes one, and :meth:`viewer_data` formats a result for a viewer. The mathematics lives in :mod:`ValaQuenta.modules.constants.maths`.
    """
    @property
    def name(self): return 'constants'

    @property
    def display_name(self): return 'Tier 0 Constants — π φ e √ i derived from H_RB'

    @property
    def version(self): return '0.130'

    @property
    def description(self):
        return (
            'Tier 0 Root Constants: π, φ, e, √, i, A_PI, α_F, d*, Λ — '
            'each read at a σ-facet of Ĥ_RB. '
            'Two ceilings bound the domain [α_F, A_PI]. d* has four named faces (Boundary, Flow, Stability, Translator). '
            'Λ: J_neg at cosmological scale; Sombrero = Hawking pair; A_PI = de Sitter attractor. '
            'Einstein wrote it in 1915, removed it 1917, universe re-inserted 1998 at 40σ.'
        )

    @property
    def confidence_floor(self): return 'THEORETICAL'   # lowest tier in the formulary: derive_alpha_fermat

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='derive_lambda',
                display='Λ — Einstein cosmological constant: J_neg at cosmological scale',
                latex=r'G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi GT_{\mu\nu},\;\Lambda=J_{\rm neg},\;\Omega_\Lambda\to\Omega_{\zeta\Sigma}',
                radian_form='Three-phase balance forces Λ. Sombrero=Hawking waveform. A_PI=de Sitter attractor.',
                confidence='ESTABLISHED (existence; observed at 40 standard deviations, 1998); OPEN (value from f)',
                code_verified=True,
                params=[],
                compute=derive_lambda,
                display_options=[],
                process="Derivation of Λ — Einstein's cosmological constant.",
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
                process='Run all nine Tier 0 derivations and assemble the complete table.',
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
                process='Derivation of i — the imaginary unit.',
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
                process='Derivation of √ — the square root operation.',
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
                process="Derivation of e — Euler's number / the natural base.",
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
                process='Derivation of π — the circle constant.',
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
                process='Derivation of φ — the golden ratio.',
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
                process="Euler's identity e^{iπ} + 1 = 0 — a theorem of RedBlue Geometries Engine.",
            ),
            Equation(
                name='derive_omega_zs',
                display='A_π = W(1) — thermal information ceiling T·e^T=1',
                latex=r'T=e^{-T}\Leftrightarrow T\cdot e^T=1\Rightarrow\Omega_{\zeta\Sigma}=W(1)=0.56714\ldots',
                radian_form='Self-referential Boltzmann fixed point. Banach theorem → unique solution W(1).',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=derive_omega_zs,
                display_options=[],
                process='Derivation of A_PI = W(1) = 0.56714329...',
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
                process='Derivation of α = 1/137.035999...',
            ),
            Equation(
                name='derive_d_star',
                display='d* — four faces: Boundary 0.24600, Flow A_π/ln10, Stability (dim 8, OPEN), Translator A_π',
                latex=r'd^*_{\mathrm{taut}}=A_\pi/\ln 10,\;d^*_{\ln 10}=A_\pi',
                radian_form="Four faces of one point; d*_RG numeric OPEN. A_π − d*·ln10 = 0.000707 is the working value's rounding residual.",
                confidence='ESTABLISHED (d*_taut, d*_ln(10)); OPEN (d*_RG numeric)',
                code_verified=True,
                params=[],
                compute=derive_d_star,
                display_options=[],
                process='d* — the four named faces, read from engine.constants.',
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
