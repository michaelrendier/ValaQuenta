"""
ainulindale_engine.modules.translator_vsa.tools
=================================================
The Translator, version 2 (VSA / hyperdimensional computing) — Module Tools.

Implements the EquationModule registry contract.

Confidence tiers are NOT flattened. The bind/bundle/permute algebra is
ESTABLISHED; the claim that bundling is RECOVERABLE at this dimension with
derived (non-random) vectors is THEORETICAL and is measured, not asserted.

Version: 0.111
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation
from .maths import (
    permute, bind, bundle, role_vector, ROLE_NAMES,
    fold_to_channels, VSATranslator,
    verify_vsa_identities, capacity_probe, unbind_probe,
)
from ..translator_common.maths import N_CHANNELS, D_HYPER, hypervector, norm


class VSATranslatorModule(EquationModule):
    """The Translator, version 2 of 2 — VSA / HDC."""

    def __init__(self):
        self.engine = VSATranslator()

    @property
    def name(self):
        return "translator_vsa"

    @property
    def display_name(self):
        return "The Translator v2 — VSA / hyperdimensional (bind.bundle.permute)"

    @property
    def version(self):
        return "0.111"

    @property
    def description(self):
        return (
            "Version 2 of two Translator constructions. Kanerva's "
            "vector-symbolic architecture: concepts are 4096-dimensional "
            "hypervectors, structure is built by non-commutative binding "
            "(P(a).b), superposing bundle, and cyclic permutation for "
            "sequence. Role vectors are the prime-channel expansions of their "
            "own names — no PRNG anywhere, so results are reproducible and no "
            "seed can be selected. Folds to the same 16 prime channels as "
            "translator_discocat so the two versions can be combined and "
            "cross-tested. Quasi-orthogonality, which textbook VSA assumes, "
            "is measured here instead."
        )

    @property
    def confidence_floor(self):
        return "OPEN"

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='permute',
                display='Permute P — cyclic shift (sequence/position)',
                latex=r'\Pi(a)_i = a_{(i-1) \bmod D}',
                radian_form='n/a — index permutation',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['vector', 'shift'],
                display_options=['text'],
            ),
            Equation(
                name='bind',
                display='Bind (x) — non-commutative role-filler pairing',
                latex=r'a \otimes b = \Pi(a) \odot b',
                radian_form='n/a — elementwise product',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['a', 'b'],
                display_options=['text'],
            ),
            Equation(
                name='bundle',
                display='Bundle (+) — superposition, un-normalised',
                latex=r'\textstyle\sum_m v^{(m)}',
                radian_form='n/a — elementwise sum',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['vectors'],
                display_options=['text'],
            ),
            Equation(
                name='sentence_hypervector',
                display='Bound-and-bundled sentence (4096-dim)',
                latex=r'\overline{svo}=\sum_{r}\, \Pi(\rho_r)\odot f_r',
                radian_form='cos(2*pi*(h+1)*i/p_k) harmonic basis',
                confidence='THEORETICAL',
                code_verified=True,
                params=['subject', 'verb', 'object'],
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='capacity_probe',
                display='Quasi-orthogonality of derived hypervectors',
                latex=r'\langle |\cos(v_a,v_b)| \rangle_{a\neq b}',
                radian_form='cosine of angle between hypervectors',
                # The measurement is solid; what it implies for capacity
                # is the open part. Tier reflects the weaker of the two.
                confidence='THEORETICAL',
                code_verified=True,
                params=['tokens'],
                display_options=['text'],
            ),
            Equation(
                name='unbind_probe',
                display='Constituent recovery from the bundle',
                latex=r'\arg\max_f \cos(\overline{svo},\ \Pi(\rho_r)\odot f)',
                radian_form='cosine similarity',
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

        if equation_name == 'permute':
            v = params.get('vector') or hypervector(params.get('token', 'dog'))
            result = {'shifted_head': permute(v, params.get('shift', 1))[:8],
                      'identities': verify_vsa_identities()}
        elif equation_name == 'bind':
            a = params.get('a') or hypervector(params.get('a_token', 'dog'))
            b = params.get('b') or hypervector(params.get('b_token', 'man'))
            result = {'head': bind(a, b)[:8], 'norm': norm(bind(a, b)),
                      'identities': verify_vsa_identities()}
        elif equation_name == 'bundle':
            vs = params.get('vectors') or [hypervector(t) for t in
                                           params.get('tokens', ['dog', 'man'])]
            result = {'head': bundle(*vs)[:8], 'norm': norm(bundle(*vs))}
        elif equation_name == 'sentence_hypervector':
            result = self.engine.explain(params['subject'], params['verb'],
                                         params['object'])
        elif equation_name == 'capacity_probe':
            result = capacity_probe(params.get(
                'tokens', ['dog', 'man', 'bites', 'cat', 'runs', 'water']))
        elif equation_name == 'unbind_probe':
            result = unbind_probe(params.get('subject', 'dog'),
                                  params.get('verb', 'bites'),
                                  params.get('object', 'man'))
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
                    'label': 'folded sentence vector, 8 complex pairs'}
        return {'mode': 'text', 'text': repr(res)}

    def shell_commands(self) -> Dict[str, Any]:
        return {
            'vsa_selftest': lambda: verify_vsa_identities(),
            'vsa_capacity': lambda *toks: capacity_probe(list(toks)),
            'vsa_unbind': lambda s, v, o: unbind_probe(s, v, o),
        }
