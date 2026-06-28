"""
ainulindale_engine.modules.singularity_null.tools
Version: 0.100
"""
import json
from typing import Dict, List, Any
from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    circle_null_modes, tower_collapse_snakes,
    berry_keating_singularity, flt_prime_extinction_sieve,
    full_singularity_null,
)


class SingularityNullModule(EquationModule):
    @property
    def name(self): return 'singularity_null'
    @property
    def display_name(self): return 'Singularity-NULL Engine — The Singularity IS Identity. Tower Collapses.'
    @property
    def version(self): return '0.100'
    @property
    def description(self):
        return (
            'The Singularity IS identity. The Hamiltonian sees only one thing: AWAY. '
            'Engines: circle-null modes (Ptolemy inversion = 1 word), '
            'tower collapse snakes (n-ball volume = Snakes & Ladders board, peak n*≈5.257), '
            'Berry-Keating singularity (H=xp, repulsive fixed point, σ=½ equatorial geodesic), '
            'FLT prime extinction sieve (primes defined by negative space, σ=½ as FLT boundary).'
        )
    @property
    def confidence_floor(self): return 'THEORETICAL'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                'full_singularity_null',
                'All 4 Singularity-NULL engines',
                r'\text{Singularity}=\text{identity},\;V(n)_{\max}=n^*\approx5.257,\;H=xp,\;\text{FLT}\Rightarrow\text{primes}',
                'Complete Singularity-NULL module.',
                'THEORETICAL', True, [],
                lambda: full_singularity_null(), ['text'],
            ),
            Equation(
                'circle_null_modes',
                'How many ways can circle say NULL? Exactly 1: Ptolemy inversion.',
                r'z\to R_H^2/\bar{z},\;0\leftrightarrow\infty,\;\text{one word}',
                'The Ptolemy inversion is the unique conformal map exchanging 0 and ∞. One vocabulary word.',
                'ESTABLISHED', True, [],
                lambda: circle_null_modes(), ['text'],
            ),
            Equation(
                'tower_collapse_snakes',
                'Snakes & Ladders = Cayley-Dickson tower. V(n) = board height. Peak n*≈5.257.',
                r'V(n)=\pi^{n/2}/\Gamma(n/2+1),\;n^*\approx5.257,\;\text{snake}=\phi_{\rm ZD}',
                'After n*: all snakes. Tower collapses to V→0 ≡ singularity.',
                'ESTABLISHED', True, ['n_max'],
                lambda n_max=30: tower_collapse_snakes(n_max), ['text'],
            ),
            Equation(
                'berry_keating_singularity',
                'H=xp: singularity is repulsive fixed point. σ=½ is equatorial geodesic.',
                r'H=xp,\;\dot{x}=x,\;\dot{p}=-p;\;\sigma=\tfrac{1}{2}\text{ fixed locus}',
                'The singularity has H=0, S=0, one eigenvalue=0. Only direction: AWAY.',
                'ESTABLISHED', True, ['max_t'],
                lambda max_t=50.0: berry_keating_singularity(max_t), ['text'],
            ),
            Equation(
                'flt_prime_extinction_sieve',
                'FLT defines primes by extinction. Negative space = primary identity.',
                r'a^n+b^n\ne c^n\;(n\ge3);\;p\text{ prime}\Leftrightarrow\text{maximal negative space}',
                'Primes on σ=½: their negative space (what they cannot be) defines them first.',
                'ESTABLISHED', True, ['N'],
                lambda N=100: flt_prime_extinction_sieve(N), ['text'],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"'{equation_name}' not in singularity_null")
        if params:
            return eq.compute(**params)
        return eq.compute()

    def viewer_data(self, equation_name: str, params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)
        return {'mode': display_mode, 'module': self.name,
                'equation': equation_name, 'data': result,
                'text': json.dumps(result, indent=2, default=str)[:4000]}
