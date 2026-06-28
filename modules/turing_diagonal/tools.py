"""
ainulindale_engine.modules.turing_diagonal.tools
Version: 0.100
"""
import json
from typing import Dict, List, Any
from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    prediction_diagonal_test, enigma_derangement,
    hypercomplex_identity_diagonal, turing_halting_diagonal,
    full_turing_diagonal,
)


class TuringDiagonalModule(EquationModule):
    @property
    def name(self): return 'turing_diagonal'
    @property
    def display_name(self): return 'Turing Diagonal Engine — i²=-1 = Cantor = Gödel = Enigma = UDOE'
    @property
    def version(self): return '0.100'
    @property
    def description(self):
        return (
            'The diagonal flip i²=[[-1,0],[0,-1]] unifies every self-referential proof. '
            'Engines: prediction diagonal test (any prediction → decidable/undecidable), '
            'enigma derangement (D_n/n!→1/e, Turing proof of concept), '
            'hypercomplex identity diagonal (eₖ²=-1 for k=1..15), '
            'halting diagonal (D(D) → σ=½ oscillation).'
        )
    @property
    def confidence_floor(self): return 'ESTABLISHED'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                'full_turing_diagonal',
                'All 4 Turing Diagonal engines',
                r'i^2=[[-1,0],[0,-1]],\;D_n/n!\to 1/e,\;e_k^2=-1,\;D(D)\to\sigma=\tfrac{1}{2}',
                'Complete Turing Diagonal module: diagonal flip = i² unifies Cantor/Gödel/Turing/Enigma/UDOE.',
                'ESTABLISHED', True, [],
                lambda: full_turing_diagonal(), ['text'],
            ),
            Equation(
                'prediction_diagonal_test',
                'Apply Turing diagonal to any prediction → decidable/undecidable',
                r'\text{diagonal depth}\;\mathrm{mod}\;4=2\Rightarrow i^2=-1\Rightarrow\text{undecidable}',
                'Self-referential predictions with negation at depth 2 are undecidable (i²=-1).',
                'ESTABLISHED', True, ['prediction'],
                lambda prediction='this statement is false': prediction_diagonal_test(prediction),
                ['text'],
            ),
            Equation(
                'enigma_derangement',
                'D_n/n! → 1/e. Enigma reflector = Cantor diagonal = Turing D(D).',
                r'D_n=n!\sum_{k=0}^n(-1)^k/k!,\;D_n/n!\to 1/e',
                'The derangement is the algebraic form of the diagonal argument.',
                'ESTABLISHED', True, ['n'],
                lambda n=26: enigma_derangement(n), ['text'],
            ),
            Equation(
                'hypercomplex_identity_diagonal',
                'i²=[[-1,0],[0,-1]]. Cantor=Gödel=Turing=Enigma=sedenion.',
                r'i^2=\begin{pmatrix}-1&0\\0&-1\end{pmatrix},\;e_k^2=-1\;\forall k=1\ldots 15',
                '15 sedenion derangements. e₀=1 is the ONLY fixed point (the singularity).',
                'ESTABLISHED', True, [],
                lambda: hypercomplex_identity_diagonal(), ['text'],
            ),
            Equation(
                'turing_halting_diagonal',
                'D(D): the program that escapes HALT. Oscillates at σ=½.',
                r'D(P_i)=1-T[i][i],\;D\notin\{P_1,\ldots,P_n\},\;\sigma_D=\tfrac{1}{2}',
                'The diagonal program lives at the critical line: equidistant between YES and NO.',
                'ESTABLISHED', True, ['n_programs'],
                lambda n_programs=50: turing_halting_diagonal(n_programs), ['text'],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"'{equation_name}' not in turing_diagonal")
        if params:
            return eq.compute(**params)
        return eq.compute()

    def viewer_data(self, equation_name: str, params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)
        return {'mode': display_mode, 'module': self.name,
                'equation': equation_name, 'data': result,
                'text': json.dumps(result, indent=2, default=str)[:4000]}
