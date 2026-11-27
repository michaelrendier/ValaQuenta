"""
ValaQuenta.modules.hypergon_constructibility.tools
==================================================
HypergonConstructibilityModule — registry contract.

Equations::

  1. sedenion_hypergon_sweep            all 16 N-gons, Gauss-Wantzel test
  2. verify_nilpotent_split_conjecture  re-tested factorization mechanism
  3. prime_definition_report            synthesis (raw data included, not
                                         substituted — see NULL operator note)
  4. niemeier_gap_theorem               the 23 Niemeier root systems and the residues of h mod 16 they miss ({1, 11, 15})
  5. moonshine_gap_fill                 which Moonshine primes land in the gap residues
  6. moonshine_fill_control             exact count: how often a prime set of that size does the same
  7. totient_constructibility_check     Gauss-Wantzel by phi(n) a power of 2, against the Fermat-prime list

Version: 0.200
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    sedenion_hypergon_sweep, verify_nilpotent_split_conjecture,
    prime_definition_report, niemeier_gap_theorem, moonshine_gap_fill,
    moonshine_fill_control, totient_constructibility_check,
)


class HypergonConstructibilityModule(EquationModule):
    """
    Hypergon Constructibility — Gauss-Wantzel + Factorization Test

    All 16 sedenion hyper-N-gons tested for Gauss-Wantzel constructibility (REAL
    result: 4/16 constructible, 12/16 holes). Phase 22's corrected nilpotent-
    split factorization conjecture re-tested against a magnitude-matched control
    (HONEST result: does not survive — likely address-mapping artifact, not a
    real factoring signal). Dual arithmetic/geometric prime definition, NOT
    unified into a working factoring mechanism.

    Registry module for ``hypergon_constructibility``: :meth:`formulary` lists the equations, :meth:`run` executes one, and :meth:`viewer_data` formats a result for a viewer. The mathematics lives in :mod:`ValaQuenta.modules.hypergon_constructibility.maths`.
    """
    @property
    def name(self): return 'hypergon_constructibility'

    @property
    def display_name(self): return 'Hypergon Constructibility — Gauss-Wantzel + Factorization Test'

    @property
    def version(self): return '0.200'

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
                process="THE comprehensive test across all 16 hyper-N-gons for the sedenion basis -- generalizes Phase 19's single '13-gon' example.",
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
                process="Re-test Phase 22's corrected factorization conjecture (individual p, q nilpotency, not the earlier Fermat-midpoint a,b) against THREE datasets: close real factor…",
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
                process="What 'prime' actually means, per what THIS engine has verified — dual definition, arithmetic and geometric, explicitly NOT unified by a working factoring mechanism…",
            ),
            Equation(
                name='niemeier_gap_theorem',
                display='The Niemeier gap: h mod 16 of the 23 Niemeier root systems misses {1, 11, 15}',
                latex=r'h\ \text{odd}\Rightarrow A_{h-1}^{24/(h-1)},\ (h-1)\mid 24\Rightarrow h\in\{3,5,7,9,13,25\}\Rightarrow h\bmod 16\notin\{1,11,15\}',
                radian_form='enumerate every ADE root system of rank 24 with one Coxeter number; reduce h mod 16',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=niemeier_gap_theorem,
                display_options=['text'],
                process="Proof in the docstring; the 23 root systems are generated from the defining condition and the proof's steps are checked against them.",
            ),
            Equation(
                name='moonshine_gap_fill',
                display='Moonshine primes modulo 16: which residues they reach',
                latex=r'p\bmod 16,\ p\in\{2,3,5,7,11,13,17,19,23,29,31,41,47,59,71\}',
                radian_form='bucket the 15 primes dividing |Monster| by residue mod 16',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=moonshine_gap_fill,
                display_options=['text'],
                process="Arithmetic on a published list (Ogg 1975); no interpretation attached.",
            ),
            Equation(
                name='moonshine_fill_control',
                display='Control: how often 14 of the 19 odd primes up to 71 cover the gap',
                latex=r'P(\text{a random 14-subset of the 19 odd primes}\le 71\ \text{covers}\ \{1,11,15\})',
                radian_form='exact enumeration of all 11,628 subsets',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=moonshine_fill_control,
                display_options=['text'],
                process="Exact count over every subset. About 68 % of them cover the gap and 45 % cover all eight odd residues, so the fill alone is not evidence of structure.",
            ),
            Equation(
                name='totient_constructibility_check',
                display='Gauss-Wantzel by Euler phi, with no list of Fermat primes',
                latex=r'n\text{-gon constructible}\iff\varphi(n)=2^k',
                radian_form='phi sieve to the limit; compare with the Fermat-prime test',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['limit'],
                compute=totient_constructibility_check,
                display_options=['text'],
                process="Agreement for every n up to the limit shows the list of five known Fermat primes is complete to there.",
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
