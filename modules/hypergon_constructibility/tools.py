"""
ainulindale_engine.modules.hypergon_constructibility.tools
==============================================================
HypergonConstructibilityModule — registry contract.

Equations:
  1. sedenion_hypergon_sweep            all 16 N-gons, Gauss-Wantzel test
  2. verify_nilpotent_split_conjecture  re-tested factorization mechanism
  3. prime_definition_report            synthesis (raw data included, not
                                         substituted — see NULL operator note)

Version: 0.100
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    sedenion_hypergon_sweep, verify_nilpotent_split_conjecture,
    prime_definition_report,
)


class HypergonConstructibilityModule(EquationModule):

    @property
    def name(self): return 'hypergon_constructibility'

    @property
    def display_name(self): return 'Hypergon Constructibility — Gauss-Wantzel + Factorization Test'

    @property
    def version(self): return '0.100'

    @property
    def description(self):
        return (
            'All 16 sedenion hyper-N-gons tested for Gauss-Wantzel constructibility '
            '(REAL result: 4/16 constructible, 12/16 holes). Phase 22\'s corrected '
            'nilpotent-split factorization conjecture re-tested against a magnitude-'
            'matched control (HONEST result: does not survive — likely address-mapping '
            'artifact, not a real factoring signal). Dual arithmetic/geometric prime '
            'definition, NOT unified into a working factoring mechanism.'
        )

    @property
    def confidence_floor(self): return 'OPEN'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='sedenion_hypergon_sweep',
                display='All 16 N-gons — Gauss-Wantzel constructibility, verified not assumed',
                latex=r'n\text{-gon constructible}\iff n=2^k\prod(\text{distinct Fermat primes})',
                radian_form='for each of 16 basis primes: is it 2, or a known Fermat prime?',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=sedenion_hypergon_sweep,
                display_options=['text'],
            ),
            Equation(
                name='verify_nilpotent_split_conjecture',
                display='Re-test: does p,q nilpotency survive a magnitude-matched control?',
                latex=r'\text{nilpotent}(hw(p)),\ \text{nilpotent}(hw(q))\ \text{vs. random control}',
                radian_form='close pairs vs far-apart pairs vs random (non-factor) pairs',
                confidence='OPEN',
                code_verified=True,
                params=[],
                compute=verify_nilpotent_split_conjecture,
                display_options=['text'],
            ),
            Equation(
                name='prime_definition_report',
                display='Dual definition of prime — arithmetic + geometric, not yet unified',
                latex=r'\text{prime}: \text{no factors (arithmetic)} \ \wedge\ \text{constructibility status (geometric)}',
                radian_form='synthesis, includes raw hypergon_sweep data, not a substitute for it',
                confidence='THEORETICAL',
                code_verified=True,
                params=[],
                compute=prime_definition_report,
                display_options=['text'],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in hypergon_constructibility module")
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
                if isinstance(v, (int, float, bool, str)):
                    lines.append(f'  {k:36s} = {v}')
                elif isinstance(v, list) and k == 'rows':
                    for row in v:
                        lines.append(f"    {row}")
                elif isinstance(v, dict):
                    lines.append(f'  {k}:')
                    for k2, v2 in v.items():
                        lines.append(f'    {k2:34s} = {v2}')
                elif isinstance(v, list):
                    lines.append(f'  {k:36s} = {v}')
        return '\n'.join(lines)
