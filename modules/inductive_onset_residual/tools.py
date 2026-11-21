"""
ValaQuenta.modules.inductive_onset_residual.tools
=================================================
InductiveOnsetResidualModule: the registry contract. Ten equations, each of which runs.

    summary           the one-screen view
    induction         W(1) built by x -> e^-x; digits gained per step = d*
    running_value     the d* the code runs with, beside the induced rate
    onset_residual    the residual and the digit where the two d* first differ
    hub_fiber         0_RB fixed-point weight of a fiber, depth at each constant
    couplings         G_p(sigma) = p^(-sigma) of the Hamiltonian
    explicit_formula  the explicit formula against the exact Chebyshev psi
    census            which repositories write which d* value (live scan)
    symbols           which symbol names which constant, by source
    validate          the checks

Version: 0.2
"""
from typing import Any, Dict, List

from ...engine.registry import EquationModule, Equation
from . import maths as M


class InductiveOnsetResidualModule(EquationModule):
    """
    The onset residual of the Inductive Self-Adjoint Geometric Coupling Hamiltonian.

    Registry module for ``inductive_onset_residual``: :meth:`formulary` lists the equations,
    :meth:`run` executes one, and :meth:`viewer_data` formats a result for a viewer. The
    mathematics lives in :mod:`ValaQuenta.modules.inductive_onset_residual.maths`.
    """

    @property
    def name(self): return 'inductive_onset_residual'

    @property
    def display_name(self): return 'Inductive onset residual'

    @property
    def version(self): return '0.2'

    @property
    def description(self):
        return ('The onset residual of the inductive geometric coupling Hamiltonian: W(1) by induction, '
                'the digits gained per step (d*), the d* the code runs with, the residual between them, '
                'the 0_RB hub weight, the couplings p^(-sigma), and a live census of where each d* value is written.')

    @property
    def confidence_floor(self): return 'OPEN'

    def formulary(self) -> List[Equation]:
        def eq(name, display, latex, radian, conf, params, fn, process):
            return Equation(name=name, display=display, latex=latex, radian_form=radian, confidence=conf,
                            code_verified=True, params=params, compute=fn, display_options=[], process=process)
        return [
            eq('summary', 'Inductive onset residual: summary', r'\Delta=\Omega-d^*\ln 10', 'Induction rate against the running d*.',
               'THEORETICAL', [], M.summary, 'One-screen summary.'),
            eq('induction', 'W(1) by induction: digits per step = d*', r'-\log_{10}\Omega=\Omega/\ln 10', 'Iterate x -> exp(-x); error shrinks by W(1) per step.',
               'ESTABLISHED', [], M.induction, 'The induction construction and its measured rate.'),
            eq('running_value', 'The d* the code runs with', r'd^*_{run}=0.24600', 'engine.constants.D_STAR beside the induced rate.',
               'OPEN', [], M.running_value, 'The running value.'),
            eq('onset_residual', 'Residual between the running d* and the induced d*', r'\Delta=\ln 10\,(d^*_{ind}-d^*_{run})', 'Delta and the agreeing decimals.',
               'THEORETICAL', [], M.onset_residual, 'Delta and the first differing digit.'),
            eq('hub_fiber', '0_RB fixed-point weight of a fiber', r'w=1-\mathrm{depth}^2', 'Hub weight; depth at which w equals each constant.',
               'ESTABLISHED', ['depth'], M.hub_fiber, 'The 0_RB hub.'),
            eq('couplings', 'Geometric couplings G_p(sigma) = p^(-sigma)', r'G_p(\sigma)=p^{-\sigma}', 'Coupling table at the sigma facets.',
               'ESTABLISHED', [], M.couplings, 'The couplings.'),
            eq('explicit_formula', 'Explicit formula against exact psi', r'\psi(x)=x-\sum_\rho x^\rho/\rho-\ln 2\pi', 'Summed over zero pairs; error against the exact psi.',
               'ESTABLISHED', ['x', 'n_zeros'], M.explicit_formula, 'The explicit formula check.'),
            eq('census', 'Where each d* value is written', r'\#\{\text{files}\}', 'Live scan of the sibling repositories.',
               'COMPUTATIONAL', [], M.census, 'Census of the d* values.'),
            eq('symbols', 'Which symbol names which constant', r'\Omega_{RZ},\,A_{Fermat}', 'Assignments by source.',
               'OPEN', [], M.symbols, 'The symbol assignments, by source.'),
            eq('validate', 'Validation', r'\{\text{checks}\}', 'Each check compares two independent computations.',
               'THEORETICAL', [], M.validate, 'Run the checks.'),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in inductive_onset_residual module")
        filtered = {k: params[k] for k in eq.params if k in params}
        if 'n_zeros' in filtered:
            filtered['n_zeros'] = max(1, int(filtered['n_zeros']))
        result = eq.compute(**filtered)
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str, params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        return {'text': self._fmt(equation_name, self.run(equation_name, params)['result'])}

    def _fmt(self, name: str, result: Any) -> str:
        """Render a result: ordered derivation steps first, then the scalar values.

        :param name: the equation name
        :param result: the equation's result
        :returns: the text
        """
        if not isinstance(result, dict):
            return f'  {name}: {result}'
        lines = [f'  [{name}]']
        for i, step in enumerate(result.get('derivation', []) or [], start=1):
            lines.append(f'    {i:2d}. {step}')
        checks = result.get('checks')
        if isinstance(checks, dict):
            lines += [f'    {"✓" if ok else "✗"}  {c}' for c, ok in checks.items()]
        for k, v in result.items():
            if k in ('derivation', 'checks') or isinstance(v, (list, dict)):
                continue
            lines.append(f'    {k:36s} = {v:.12g}' if isinstance(v, float) else f'    {k:36s} = {v}')
        return '\n'.join(lines)

    def shell_commands(self) -> Dict[str, Any]:
        return {'delta': lambda: M.onset_residual()['delta'], 'rate': lambda: M.induction()['digits_per_step_exact'],
                'validate': M.validate, 'census': M.census}
