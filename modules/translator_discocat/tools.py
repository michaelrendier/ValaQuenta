"""
ainulindale_engine.modules.translator_discocat.tools
======================================================
The Translator, version 1 (DisCoCat) — Module Tools.

Implements the EquationModule registry contract.

Confidence tiers here are NOT flattened. maths.py hedges its claims and
those hedges are carried through verbatim — see _crosscutting item 3 in
.clauderc_ValaQuenta, which records tier-flattening in tools.py as a known
failure mode in this codebase.

Display modes: text (always), complex_plane (sentence vector as 8 complex
pairs over the 16 channels).

Version: 0.111
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation
from .maths import (
    N, S, TRANSITIVE_VERB, PregroupType,
    reduce_type, is_grammatical, MeaningSpace, DisCoCatTranslator,
    verify_reduction_algebra, word_order_sensitivity,
)
from ..translator_common.maths import N_CHANNELS, D_HYPER, norm


class DisCoCatTranslatorModule(EquationModule):
    """The Translator, version 1 of 2 — DisCoCat."""

    def __init__(self):
        self.engine = DisCoCatTranslator()

    @property
    def name(self):
        return "translator_discocat"

    @property
    def display_name(self):
        return "The Translator v1 — DisCoCat (pregroup . tensor)"

    @property
    def version(self):
        return "0.111"

    @property
    def description(self):
        return (
            "Version 1 of two Translator constructions. Categorical "
            "compositional distributional semantics: syntax is a pregroup "
            "grammar, semantics is vector spaces, and the pregroup reduction "
            "n.(n^r.s.n^l).n -> s maps functorially onto contraction of an "
            "order-3 verb tensor against subject and object vectors. Noun and "
            "sentence spaces are the 16 prime channels (the sedenion basis); "
            "the verb tensor is 16^3 = 4096 and is the verb token's own "
            "prime-channel harmonics reshaped — derived, never trained. "
            "Shares its vector space with translator_vsa so the two versions "
            "can be combined and cross-tested."
        )

    @property
    def confidence_floor(self):
        # OPEN, because the claim that this IS The Translator is unproven.
        # The pregroup algebra underneath it is ESTABLISHED; the two tiers
        # are kept distinct rather than averaged.
        return "OPEN"

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='pregroup_reduction',
                display='Pregroup type reduction  x^(a) x^(a+1) -> 1',
                latex=r'x^{(a)}\,x^{(a+1)} \to 1',
                radian_form='n/a — symbolic (no angular quantity)',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['atoms'],
                display_options=['text'],
            ),
            Equation(
                name='grammaticality',
                display='Transitive clause reduces to s',
                latex=r'n\cdot(n^{r}\, s\, n^{l})\cdot n \to s',
                radian_form='n/a — symbolic',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                display_options=['text'],
            ),
            Equation(
                name='functor_contraction',
                display='Functor: reduction -> tensor contraction',
                latex=r's_j=\sum_{i,k} \mathrm{subj}_i\, T_{ijk}\, \mathrm{obj}_k',
                radian_form='n/a — components are cosine projections '
                            '(radian-primary via cos(2*pi*i/p_k))',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['subject', 'verb', 'object'],
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='sentence_meaning',
                display='Composed sentence vector in S (16-dim)',
                latex=r'\overline{s} = (\mathrm{subj}\otimes\mathrm{obj})\lrcorner\, T',
                radian_form='cos(2*pi*i/p_k) channel basis',
                # THEORETICAL, not ESTABLISHED: the composition is
                # well-defined, but that the output is "the meaning" is not.
                confidence='THEORETICAL',
                code_verified=True,
                params=['subject', 'verb', 'object'],
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='word_order_sensitivity',
                display='DOG BITES MAN vs MAN BITES DOG',
                latex=r'\cos(\overline{svo},\ \overline{ovs})',
                radian_form='cosine of the angle between sentence vectors',
                confidence='THEORETICAL',
                code_verified=True,
                params=['subject', 'verb', 'object'],
                display_options=['text'],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"unknown equation '{equation_name}' in {self.name}")

        if equation_name == 'pregroup_reduction':
            atoms = params.get('atoms', [('n', 0), ('n', 1)])
            red = reduce_type(PregroupType(atoms))
            result = {'reduced': repr(red['reduced']), 'witness': red['witness'],
                      'algebra_selftest': verify_reduction_algebra()}
        elif equation_name == 'grammaticality':
            result = is_grammatical(N, TRANSITIVE_VERB, N)
        elif equation_name in ('functor_contraction', 'sentence_meaning'):
            result = self.engine.explain(params['subject'], params['verb'],
                                         params['object'])
        elif equation_name == 'word_order_sensitivity':
            result = word_order_sensitivity(self.engine, params['subject'],
                                            params['verb'], params['object'])
        else:
            raise KeyError(equation_name)

        return {'result': result, 'equation': eq, 'params': params}

    def viewer_data(self, equation_name: str, params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        out = self.run(equation_name, params)
        res = out['result']
        if display_mode == 'complex_plane' and isinstance(res, dict) \
                and 'sentence_vector' in res:
            v = res['sentence_vector']
            return {'mode': 'complex_plane',
                    'points': [(v[i], v[i + 1]) for i in range(0, N_CHANNELS, 2)],
                    'label': 'sentence vector, 16 channels as 8 complex pairs'}
        return {'mode': 'text', 'text': repr(res)}

    def shell_commands(self) -> Dict[str, Any]:
        return {
            'discocat_selftest': lambda: verify_reduction_algebra(),
            'discocat_compose': lambda s, v, o: self.engine.explain(s, v, o),
        }
