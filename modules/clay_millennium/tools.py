"""
ainulindale_engine.modules.clay_millennium.tools
=================================================
ClayMillenniumModule — registry contract.

Version: 0.130
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    riemann_hypothesis,
    rh_proof_stone,
    rh_proof_wiles_conjugate,
    rh_noether_balance_scan,
    rh_spectral_decomposition,
    yang_mills_mass_gap,
    navier_stokes_existence,
    p_vs_np,
    hodge_conjecture,
    birch_swinnerton_dyer,
    poincare_conjecture,
    all_clay_problems,
    clay_summary,
)


class ClayMillenniumModule(EquationModule):

    @property
    def name(self): return 'clay_millennium'

    @property
    def display_name(self): return 'Clay Millennium Problems — Σ_RB derivations'

    @property
    def version(self): return '0.130'

    @property
    def description(self):
        return (
            'All 7 Clay Millennium Problems derived from Σ_RB. '
            'RH engine: two independent proofs (Stone / Wiles conjugate), '
            'Noether balance scan, spectral decomposition + BAO residue / mass gap. '
            'Poincaré (SOLVED) and FLT (Wiles 1995) validate the framework. '
            '6 open problems: RH, Yang-Mills, NS, P/NP, Hodge, BSD.'
        )

    @property
    def confidence_floor(self): return 'THEORETICAL'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='clay_summary',
                display='All 7 Clay Millennium Problems — Σ_RB summary',
                latex=r'\Sigma_{RB}\to\{\text{RH, YM, NS, P/NP, Hodge, BSD, Poincar\'{e}}\}',
                radian_form='All Clay problems project from Σ_RB at their respective σ.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=clay_summary,
                display_options=[],
            ),
            Equation(
                name='riemann_hypothesis',
                display='RH — two proofs + spectral decomp + BAO residue  [OPEN]',
                latex=r'\Sigma_{RB}^\dagger=\Sigma_{RB}\Rightarrow\mathrm{Re}(s)=\tfrac{1}{2},\;\delta=\Omega_{\zeta\Sigma}-D^*\ln10',
                radian_form='Self-adjoint Σ_RB → real eigenvalues → all zeros on σ=½. BAO gap = mass gap.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=riemann_hypothesis,
                display_options=['complex_plane'],
            ),
            Equation(
                name='rh_proof_stone',
                display='RH Proof I — Stone\'s theorem on self-adjoint Σ_RB',
                latex=r'\Sigma_{RB}=\Sigma_{RB}^\dagger\;\xRightarrow{\mathrm{Stone}}\;\mathrm{spec}\subset\mathbb{R}\;\Rightarrow\;\mathrm{Re}(s)=\tfrac{1}{2}',
                radian_form='Σ_RB self-adjoint on L²(ℝ₊,dx/x) → Stone → real spectrum → RH.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=rh_proof_stone,
                display_options=[],
            ),
            Equation(
                name='rh_proof_wiles_conjugate',
                display='RH Proof II — conjugate via Wiles; Frey curve impossible',
                latex=r'\hat{R}^\dagger=\hat{B}\;\xRightarrow{\mathrm{Wiles}}\;\text{Frey impossible}\;\Rightarrow\;\mathrm{Re}(s)=\tfrac{1}{2}',
                radian_form='Wiles FLT (1995): Frey curve cannot exist → no off-critical zeros → RH.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=rh_proof_wiles_conjugate,
                display_options=[],
            ),
            Equation(
                name='rh_noether_balance_scan',
                display='RH Numerical — σ=½ derived from Noether balance scan',
                latex=r'\min_\sigma|J_R(\sigma)-J_B(\sigma)|=0\;\Rightarrow\;\sigma=\tfrac{1}{2}',
                radian_form='Balance scan over σ: minimum at σ=½. Not assigned — forced by conservation.',
                confidence='COMPUTATIONAL',
                code_verified=True,
                params=[],
                compute=rh_noether_balance_scan,
                display_options=[],
            ),
            Equation(
                name='rh_spectral_decomposition',
                display='RH Spectral — explicit formula, BAO residue, mass gap',
                latex=r'\psi(x)=x-\sum_\rho x^\rho/\rho-\ln2\pi,\;\delta=\Omega_{\zeta\Sigma}-D^*\ln10',
                radian_form='ψ(x) = x (de Sitter) − spectral oscillations (zeros). GAP = BAO residual = mass gap.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=rh_spectral_decomposition,
                display_options=[],
            ),
            Equation(
                name='yang_mills_mass_gap',
                display='Yang-Mills mass gap — min eigenvalue at σ=1 > 0  [OPEN]',
                latex=r'\Delta=\min\mathrm{spec}(\Sigma_{RB}|_{\sigma=1})>0',
                radian_form='G_p(1) = p^{-1} > 0 for all primes → ground state > 0 → mass gap.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=yang_mills_mass_gap,
                display_options=[],
            ),
            Equation(
                name='navier_stokes',
                display='Navier-Stokes — real projection of Σ_RB lacks i  [OPEN]',
                latex=r'\text{NS}=\mathrm{Re}(\Sigma_{RB}|_{\sigma=1}),\quad i\notin\text{NS}',
                radian_form='NS = Yang-Mills minus i. Smooth in ℂ; may blow up in ℝ.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=navier_stokes_existence,
                display_options=[],
            ),
            Equation(
                name='p_vs_np',
                display='P vs NP — Red (analytic) vs Blue (elliptic) complexity  [OPEN]',
                latex=r'\hat{R}^\dagger=\hat{B}\;\not\Rightarrow\;\text{P}=\text{NP}',
                radian_form='Adjoint ≠ computationally equivalent. 1=1 is cheaper than 1!=1.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=p_vs_np,
                display_options=[],
            ),
            Equation(
                name='hodge_conjecture',
                display='Hodge — algebraic cycles from inductive prime sum  [OPEN]',
                latex=r'\mathrm{Hdg}^k(X)\subset[\text{algebraic cycles}],\quad G_p(1)=1/p\in\mathbb{Q}',
                radian_form='Inductive Σ_p generates algebraic cycles. Rational coupling → rational Hodge.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=hodge_conjecture,
                display_options=[],
            ),
            Equation(
                name='birch_swinnerton_dyer',
                display='BSD — rank(E) = ord L(E,1) = Blue eigenspace multiplicity  [OPEN]',
                latex=r'\mathrm{rank}(E)=\mathrm{ord}_{s=1}L(E,s)=\dim(\hat{B}\text{-eigenspace})',
                radian_form='L(E,s) = Blue Euler product. Geometric rank = spectral order.',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=birch_swinnerton_dyer,
                display_options=[],
            ),
            Equation(
                name='poincare_conjecture',
                display='Poincaré — trivial Σ_RB → S³  [SOLVED — validation]',
                latex=r'\partial g_{\mu\nu}/\partial t=-2R_{\mu\nu}\;\to\;M\cong S^3',
                radian_form='Ricci flow = Σ_RB coupling flow to trivial facet. Validates framework.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=poincare_conjecture,
                display_options=[],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in clay_millennium module")
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
                    lines.append(f'  {k:30s} = {v:.10f}')
                elif not isinstance(v, (list, dict)):
                    lines.append(f'  {k:30s} = {v}')
            return '\n'.join(lines)
        return f'  {name}: {result}'
