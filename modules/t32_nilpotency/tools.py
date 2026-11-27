"""
ValaQuenta.modules.t32_nilpotency.tools
=======================================
T32NilpotencyModule — registry contract.

The reusable primitive module -- Hyperwebster address, T32/GF(2)
multiplication, nilpotency test. Imported by hypergon_constructibility
and by FourthAgePapers/FermatMonster/engine/fermat_monster_engine.py.

Version: 0.110
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import hw_address, hw_to_t32, t32_mul, is_nilpotent, prime_nilpotency_report, radical_census

_DEFAULT_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]


class T32NilpotencyModule(EquationModule):
    """
    T32 Nilpotency — Hyperwebster Address Primitives

    Standalone, minimal, verified-correct primitives: Hyperwebster base-97
    address encoding, T32/GF(2) Cayley-Dickson multiplication, nilpotency test.
    Meant to be imported by other engines (hypergon_constructibility,
    fermat_monster_engine.py) rather than each maintaining its own copy.

    Registry module for ``t32_nilpotency``: :meth:`formulary` lists the equations, :meth:`run` executes one, and :meth:`viewer_data` formats a result for a viewer. The mathematics lives in :mod:`ValaQuenta.modules.t32_nilpotency.maths`.
    """
    @property
    def name(self): return 't32_nilpotency'

    @property
    def display_name(self): return 'T32 Nilpotency — Hyperwebster Address Primitives'

    @property
    def version(self): return '0.110'

    @property
    def description(self):
        return (
            'Standalone, minimal, verified-correct primitives: Hyperwebster base-97 '
            'address encoding, T32/GF(2) Cayley-Dickson multiplication, nilpotency test. '
            'Meant to be imported by other engines (hypergon_constructibility, '
            'fermat_monster_engine.py) rather than each maintaining its own copy.'
        )

    @property
    def confidence_floor(self): return 'ESTABLISHED'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='prime_nilpotency_report',
                display='Nilpotency status of a set of primes in T32/GF(2)',
                latex=r'\text{nilpotent}(a) \iff a\neq0 \wedge a\cdot a=0 \text{ (T32/GF(2))}',
                radian_form='for each prime: hw_to_t32(p), then is_nilpotent',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['primes'],
                compute=lambda primes=None: prime_nilpotency_report(primes or _DEFAULT_PRIMES),
                display_options=['text'],
                process='Nilpotency status of a set of primes in T32/GF(2)',
            ),
            Equation(
                name='radical_census',
                display='GF(2) square law: nilpotent / involutory census, with the Δ(w) = w·𝟏 detector check',
                latex=r'x^2\in\{0,e_0\};\quad \Delta(w)=w\cdot\mathbf 1=0\iff w^2=0',
                radian_form='for every word: classify w² as 0 or e0; check the detector; 𝟏 is not an annihilator',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['dim'],
                compute=lambda dim=8: radical_census(int(dim)),
                display_options=['text'],
                process='Exhaustive square-law census of the T32/GF(2) algebra of a given dimension',
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in t32_nilpotency module")
        filtered = {k: params[k] for k in eq.params if k in params}
        result = eq.compute(**filtered)
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str,
                     params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)['result']
        lines = [f'  {equation_name}']
        if equation_name == 'radical_census':
            lines += [f'    {k:18s} = {v}' for k, v in result.items()]
            return {'text': '\n'.join(lines)}
        for row in result.get('rows', []):
            lines.append(f"    p={row['prime']:6d}  t32=0x{row['t32_word']:08X}  nilpotent={row['nilpotent']}")
        lines.append(f"  nilpotent: {result['nilpotent_count']}/{result['total']} = {result['nilpotent_pct']:.1f}%")
        return {'text': '\n'.join(lines)}
