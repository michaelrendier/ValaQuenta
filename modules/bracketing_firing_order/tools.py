"""
ValaQuenta.modules.bracketing_firing_order.tools
====================================================
The Bracketing Engine, the Firing Order Engine, and Set Membership --
Module Tools.

Implements the EquationModule registry contract.
Provides: formulary, run(), viewer_data(), shell_commands()

Three general-purpose, domain-independent tools -- consumed by
`add_scale_sign` (3 generators) and the sedenion Emerger bracket (16
components) alike, not tied to either. See maths.py for the full account.

Version: 0.1
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    bell_number, set_partitions, bracketing_report,
    firing_order_count, apply_firing_order, all_firing_orders,
    trajectory, collisions, would_collide, jurisdiction_violation,
    ENUMERATION_CEILING_N,
)


class BracketingFiringOrderModule(EquationModule):
    """The arena (bracketing), the sequencing (firing order), and the
    memory (set membership) -- three general tools, one module."""

    @property
    def name(self):
        return "bracketing_firing_order"

    @property
    def display_name(self):
        return "Bracketing, Firing Order, and Set Membership"

    @property
    def version(self):
        return "0.1"

    @property
    def description(self):
        return (
            "Three general-purpose, domain-independent tools, not one "
            "thing tied to add_scale_sign. BRACKETING: how many unordered "
            "ways can n things be grouped (exact Bell-number count always; "
            "exhaustive enumeration only when feasible, n<=12 -- refuses "
            "rather than silently hangs above that). FIRING ORDER: how "
            "many ways can n things be sequenced (n!), and applying a "
            "specific firing order is a literal permutation action -- "
            "verified worked example: (3,1,2) applied to [Scale,Sign,Add] "
            "gives [Add,Scale,Sign], ASS's own canonical name reached by "
            "resequencing, not relabeling. SET MEMBERSHIP, two jobs: has a "
            "firing recurred before (trajectory/collision detection, "
            "generalizing Recaman's own defining rule to any sequence of "
            "callables); and did a bracketing cause one jurisdiction's "
            "maths to be used on an object native to a different "
            "jurisdiction (grounded in GenerationalLineage's own "
            "decomposition/emerger 'two jurisdictions', parametrized here "
            "not hardcoded)."
        )

    @property
    def confidence_floor(self):
        return "ESTABLISHED"

    # -- Formulary ---------------------------------------------------------

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='bell_number',
                display='BRACKETING: exact count of unordered groupings — the Bell number',
                latex=r'B(n) = \sum_{k=0}^{n-1}\binom{n-1}{k}B(k)',
                radian_form='Bell triangle, arbitrary precision — B(3)=5, B(16)=10,480,142,147',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['n'],
                compute=lambda n: bell_number(n),
                display_options=['text'],
            ),
            Equation(
                name='bracketing_report',
                display='BRACKETING: exact count always, exhaustive list only when feasible',
                latex=r'n \le 12 \Rightarrow \text{list};\ \ \text{else count only}',
                radian_form='honest infeasibility report above the enumeration ceiling, never a silent hang',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['items'],
                compute=lambda items: bracketing_report(items),
                display_options=['text'],
            ),
            Equation(
                name='firing_order_count',
                display='FIRING ORDER: exact count of sequencings — n!',
                latex=r'n!',
                radian_form='firing_order_count(3)=6',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['n'],
                compute=lambda n: firing_order_count(n),
                display_options=['text'],
            ),
            Equation(
                name='apply_firing_order',
                display='FIRING ORDER: resequence a written order by a chosen permutation',
                latex=r'(3,1,2)\ \text{applied to}\ [Scale,Sign,Add] = [Add,Scale,Sign]',
                radian_form='verified worked example — ASS\'s own canonical name, reached by resequencing',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['written', 'firing_order'],
                compute=lambda written, firing_order: apply_firing_order(written, firing_order),
                display_options=['text'],
            ),
            Equation(
                name='collisions',
                display='SET MEMBERSHIP: has a firing recurred? (Recaman, generalized)',
                latex=r'\exists\, i<j : \text{traj}(i) = \text{traj}(j)',
                radian_form='domain-independent — works on any sequence of callables, not just ASS',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['steps', 'x0'],
                compute=lambda steps, x0=1.0: collisions(steps, x0),
                display_options=['text'],
            ),
            Equation(
                name='would_collide',
                display='SET MEMBERSHIP: the operator-level flip test, before committing',
                latex=r'\text{candidate}(\text{traj}[-1]) \in \text{visited}?',
                radian_form='Recaman\'s own a(n-1)-n candidate check, generalized',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['steps_so_far', 'candidate_next', 'x0'],
                compute=lambda steps_so_far, candidate_next, x0=1.0: would_collide(steps_so_far, candidate_next, x0),
                display_options=['text'],
            ),
            Equation(
                name='jurisdiction_violation',
                display='SET MEMBERSHIP: did a bracketing use another jurisdiction\'s language illegally?',
                latex=r'\text{op} \notin \text{legal\_ops}(\text{object}) \Rightarrow \text{violation}',
                radian_form='grounded in GenerationalLineage\'s decomposition/emerger jurisdictions, parametrized',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['object_name', 'requested_operation', 'jurisdiction_map'],
                compute=lambda object_name, requested_operation, jurisdiction_map:
                    jurisdiction_violation(object_name, requested_operation, jurisdiction_map),
                display_options=['text'],
            ),
        ]

    # -- Run / viewer --------------------------------------------------------

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not found in {self.name} module")
        result = eq.compute(**params) if params else eq.compute()
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str, params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        return {'text': self._format_text(equation_name, self.run(equation_name, params))}

    def _format_text(self, equation_name: str, result: Dict) -> str:
        eq = result['equation']
        r = result['result']
        if isinstance(r, dict):
            body = '\n'.join(f"      {k:<28} {v}" for k, v in r.items()
                             if not isinstance(v, (list, dict)))
            summary = '\n' + body
        elif isinstance(r, list):
            summary = f"{r[:10]}{' ...' if len(r) > 10 else ''}  (n={len(r)})"
        else:
            summary = r
        return (
            f"  {eq.display}\n"
            f"  Status: {eq.confidence}  |  Code-verified: {eq.code_verified}\n"
            f"  Radian form: {eq.radian_form}\n"
            f"  Result: {summary}"
        )

    # -- Shell commands ------------------------------------------------------

    def shell_commands(self) -> Dict[str, Any]:
        return {
            'bell':          lambda n: bell_number(n),
            'partitions':    lambda items: set_partitions(items),
            'bracket_report':lambda items: bracketing_report(items),
            'fire_count':    lambda n: firing_order_count(n),
            'fire_apply':    lambda written, order: apply_firing_order(written, order),
            'collisions':    lambda steps, x0=1.0: collisions(steps, x0),
            'jurisdiction':  lambda obj, op, jmap: jurisdiction_violation(obj, op, jmap),
        }
