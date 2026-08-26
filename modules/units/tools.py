"""
ainulindale_engine.modules.units.tools
=========================================
UNITS -- Module Tools

Implements the EquationModule registry contract.

Version: 0.1
"""

from typing import Any, Dict, List

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    SI_BASE, unit_vector, unit_mul, unit_div, unit_pow,
    unit_lineage_decompose, LINEAGE_TABLE, verify_lineage_table,
    verify_cancellation, EQUATION_INDEX, equation_index_lookup,
)


class UnitsModule(EquationModule):
    """UNITS -- dimensional exponent vectors as the fourth domain for this
    project's factoral-decomposition discipline; the equation index."""

    @property
    def name(self):
        return "units"

    @property
    def display_name(self):
        return "Units (The Equation Index)"

    @property
    def version(self):
        return "0.1"

    @property
    def description(self):
        return (
            "A unit is a point in the 7-axis SI base-dimension lattice "
            "(kg,m,s,A,K,mol,cd) -- the same leaf/composite structure this "
            "project already runs on numbers (factor_lineage) and processes "
            "(pathway_decompose), a fourth domain, not a new mechanism. "
            "Every named compound (Newton, Joule, Watt, Tesla...) has an "
            "exact, computable lineage back to the 7 leaves; cancellation "
            "is exact vector arithmetic, not string bookkeeping. A unit "
            "carries no numeric content and does no work itself -- a "
            "geometry, in this project's established sense -- but it "
            "determines which permutations of content (which equations) "
            "are even dimensionally possible: EQUATION_INDEX makes that "
            "claim concrete, looking up the standard physical laws that "
            "produce a given dimension signature."
        )

    @property
    def confidence_floor(self):
        return "ESTABLISHED"

    # -- Formulary ---------------------------------------------------------

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='unit_compose',
                display='UNIT ARITHMETIC: multiply/divide as exponent-vector add/subtract',
                latex=r'[u_1 \cdot u_2] = \exp(u_1) + \exp(u_2),\quad [u_1 / u_2] = \exp(u_1) - \exp(u_2)',
                radian_form='cancellation is a component landing on zero -- no special-casing',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['a', 'b', 'op'],
                compute=lambda a, b, op='mul': (unit_mul(a, b) if op == 'mul' else unit_div(a, b)),
                display_options=['text'],
            ),
            Equation(
                name='lineage_table_verified',
                display='THE UNIT LINEAGE: named compounds trace exactly back to the 7 leaves',
                latex=r'T = \mathrm{Wb} \cdot m^{-2} = \mathrm{V}\cdot s \cdot m^{-2} = \dots = kg^1 s^{-2} A^{-1}',
                radian_form='every named compound recombines to its own declared exponent vector',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: verify_lineage_table(),
                display_options=['text'],
            ),
            Equation(
                name='cancellation_demo',
                display='THE CHEMISTRY CASE: mol/L * L cancels back to mol exactly',
                latex=r'(n/V) \cdot V = n',
                radian_form='real vector arithmetic, not approximate or string-based',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: verify_cancellation(),
                display_options=['text'],
            ),
            Equation(
                name='equation_index',
                display='THE EQUATION INDEX: a dimension signature narrows the candidate laws',
                latex=r'[\mathrm{kg}\,\mathrm{m}^2\,\mathrm{s}^{-2}] \Rightarrow '
                      r'\{E=\tfrac12 mv^2,\ E=mgh,\ W=Fd,\ \dots\}',
                radian_form='the SAME move as context_vector narrowing a word to its candidate '
                            'synsets -- units are "word possibilities" for equations',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['exponents'],
                compute=lambda exponents: {'exponents': tuple(exponents),
                                           'candidates': equation_index_lookup(exponents)},
                display_options=['text'],
            ),
        ]

    # -- Run -----------------------------------------------------------------

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not found in {self.name} module")
        result = eq.compute(**params) if params else eq.compute()
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    # -- Viewer data -----------------------------------------------------------

    def viewer_data(self, equation_name: str, params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        return {'text': self._format_text(self.run(equation_name, params))}

    def _format_text(self, result: Dict) -> str:
        eq = result['equation']
        r = result['result']
        if isinstance(r, dict):
            body = '\n'.join(f"      {k:<28} {v}" for k, v in r.items()
                             if not isinstance(v, (list, dict, tuple)) or k == 'candidates')
            summary = '\n' + body
        else:
            summary = r
        return (
            f"  {eq.display}\n"
            f"  Status: {eq.confidence}  |  Code-verified: {eq.code_verified}\n"
            f"  Radian form: {eq.radian_form}\n"
            f"  Result: {summary}"
        )

    # -- Shell commands ----------------------------------------------------

    def shell_commands(self) -> Dict[str, Any]:
        return {
            'uvec':    lambda exps, name=None: unit_vector(exps, name=name),
            'umul':    lambda a, b: unit_mul(a, b),
            'udiv':    lambda a, b: unit_div(a, b),
            'upow':    lambda a, n: unit_pow(a, n),
            'ulineage': lambda: verify_lineage_table(),
            'ucancel': lambda: verify_cancellation(),
            'eqindex': lambda exps: equation_index_lookup(exps),
        }

    def on_register(self, registry) -> None:
        pass
