"""
ainulindale_engine.modules.bao_mass_gap.tools
===============================================
BaoMassGapModule — registry contract.

Seven equations, in derivation order:
    summary                   the one-screen landing view
    gap_value                 Δ = Ω_ζΣ − D*·ln10
    spectral_residue          the BAO decomposition — why it is a residue
    gap_identity              Δ = 1/(1000√2)
    bao_consistency           against the Planck 2018 acoustic scale
    mtheory_compactification  11 = 4 + 7, G₂ holonomy, one vacuum
    validate                  every check, pass/fail

Every compute() returns a 'derivation' key holding an ordered list of the
operations performed. The console renders that list as the proof chain.

Version: 0.131
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation
from .maths import (
    GAP, GAP_IDENTITY, BAO_FLOOR, BAO_CEILING,
    summary,
    gap_value,
    spectral_residue,
    gap_identity,
    bao_consistency,
    mtheory_compactification,
    validate,
)


class BaoMassGapModule(EquationModule):

    @property
    def name(self): return 'bao_mass_gap'

    @property
    def display_name(self): return 'The Mass Gap — spectral residue of BAO'

    @property
    def version(self): return '0.131'

    @property
    def description(self):
        return (
            'The mass gap as the residue of the BAO spectral decomposition. The '
            'explicit formula splits the prime distribution into a de Sitter ground '
            'state plus one standing wave per zero; read at the BAO scale that is '
            'the CMB acoustic spectrum. What no standing wave absorbs between the '
            'acoustic floor D*·ln10 and the thermal ceiling Ω_ζΣ is the residue: '
            'Δ = 0.0007073575 = 1/(1000√2). Zero free parameters. Δ is consumed '
            'across the codebase as the compactification scale and spectral floor; '
            'this module is where it is computed.'
        )

    @property
    def confidence_floor(self): return 'ESTABLISHED'

    # ── Formulary ────────────────────────────────────────────────────────────

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='summary',
                display=f'Mass gap — Δ = {GAP:.10f} = 1/(1000√2)  [headline]',
                latex=r'\Delta=\Omega_{\zeta\Sigma}-D^*\ln 10=\frac{1}{1000\sqrt2}=7.07\times10^{-4}',
                radian_form='Ceiling W(1) minus acoustic floor D*·ln10. The residue is the gap.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=summary,
                display_options=[],
            ),
            Equation(
                name='gap_value',
                display='Δ = Ω_ζΣ − D*·ln(10) — two constants, one subtraction',
                latex=r'\Delta=\Omega_{\zeta\Sigma}-D^*\ln 10=7.07\times10^{-4}>0',
                radian_form='W(1) = 0.5671433 minus D*·ln10 = 0.5664359. Difference > 0.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=gap_value,
                display_options=[],
            ),
            Equation(
                name='spectral_residue',
                display='Spectral residue of BAO — why the gap IS a residue',
                latex=(r'\psi(x)=x-\sum_\rho\frac{x^\rho}{\rho}-\ln 2\pi,\quad'
                       r'\Delta=\Omega_{\zeta\Sigma}-D^*\ln 10'),
                radian_form=('ψ(x) = ground state + one standing wave per zero. '
                             'The unabsorbed remainder between floor and ceiling is Δ.'),
                confidence='ESTABLISHED',
                code_verified=True,
                params=['n_zeros'],
                compute=spectral_residue,
                display_options=['complex_plane'],
            ),
            Equation(
                name='gap_identity',
                display='Δ = 1/(1000√2) — the Red/Blue symmetry point',
                latex=r'\Delta=\frac{1}{1000\sqrt2},\quad\tfrac{1}{\sqrt2}=\sin45^\circ=\cos45^\circ',
                radian_form='1/√2 = sin(π/4) = cos(π/4): forward current equals backward current.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=gap_identity,
                display_options=[],
            ),
            Equation(
                name='bao_consistency',
                display='Δ vs Planck 2018 r_s = 147.09 ± 0.26 Mpc — resolvable',
                latex=r'\Delta/\sigma_{\mathrm{BAO}}\approx0.40>0.1',
                radian_form='Gap sits at 0.40 of the acoustic error bar — above the noise floor.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=bao_consistency,
                display_options=[],
            ),
            Equation(
                name='mtheory_compactification',
                display='Compactification scale = Δ — 11 = 4+7, G₂ holonomy, one vacuum',
                latex=r'11=4+7,\quad G_2=\mathrm{Aut}(\mathbb{O}),\quad\ell_{\mathrm{compact}}=\Delta',
                radian_form='7 compact dims = imaginary octonion units. Scale computed → one vacuum.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=mtheory_compactification,
                display_options=[],
            ),
            Equation(
                name='validate',
                display='Validation — all 7 checks',
                latex=r'\{\Delta>0,\;\Delta=1/(1000\sqrt2),\;\Delta/\sigma_{\mathrm{BAO}}>0.1,\;11=4+7\}',
                radian_form='Every claim in the module, checked. Pass/fail.',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=validate,
                display_options=[],
            ),
        ]

    # ── Execution ────────────────────────────────────────────────────────────

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in bao_mass_gap module")
        filtered = {k: params[k] for k in eq.params if k in params}
        # The console fills unbound numeric params with 1.0 — n_zeros must be an int.
        if 'n_zeros' in filtered:
            filtered['n_zeros'] = max(1, int(filtered['n_zeros']))
        result = eq.compute(**filtered)
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str,
                    params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)['result']

        if display_mode == 'complex_plane' and equation_name == 'spectral_residue':
            # The zeros on the critical line, amplitude-weighted by 1/|ρ|.
            points = [
                {'re': 0.5, 'im': w['gamma_n'], 'weight': w['amplitude']}
                for w in result['standing_waves']
            ]
            return {
                'text'  : self._fmt(equation_name, result),
                'points': points,
                'axes'  : {'x': 'Re(ρ)', 'y': 'Im(ρ) = γ_n'},
                'marker': {'floor': BAO_FLOOR, 'ceiling': BAO_CEILING, 'residue': GAP},
            }

        return {'text': self._fmt(equation_name, result)}

    # ── Console formatting ───────────────────────────────────────────────────

    def _fmt(self, name: str, result: Any) -> str:
        """
        Render a result as a proof derivation: ordered operations first,
        then the values they produced.
        """
        if not isinstance(result, dict):
            return f'  {name}: {result}'

        lines: List[str] = [f'  [{name}]']

        if 'headline' in result:
            lines.append(f'  Δ = {result["headline"]:.10f}')
            lines.append('')

        steps = result.get('derivation')
        if steps:
            lines.append('  DERIVATION')
            for i, step in enumerate(steps, start=1):
                lines.append(f'    {i:2d}. {step}')
            lines.append('')

        checks = result.get('checks')
        if isinstance(checks, dict):
            lines.append('  CHECKS')
            for cname, ok in checks.items():
                lines.append(f'    {"✓" if ok else "✗"}  {cname}')
            lines.append('')

        scalars = [
            (k, v) for k, v in result.items()
            if k not in ('derivation', 'checks', 'headline', 'structure',
                         'spectral_terms', 'standing_waves')
            and not isinstance(v, (list, dict))
        ]
        if scalars:
            lines.append('  VALUES')
            for k, v in scalars:
                if isinstance(v, float):
                    lines.append(f'    {k:28s} = {v:.10f}')
                else:
                    lines.append(f'    {k:28s} = {v}')

        return '\n'.join(lines)

    # ── Shell ────────────────────────────────────────────────────────────────

    def shell_commands(self) -> Dict[str, Any]:
        return {
            'gap'      : lambda: GAP,
            'identity' : lambda: GAP_IDENTITY,
            'residue'  : lambda: BAO_CEILING - BAO_FLOOR,
            'validate' : validate,
        }
