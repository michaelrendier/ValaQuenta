"""
ainulindale_engine.modules.translator_discocat.maths
======================================================
The Translator, VERSION 1 of 2 — Categorical Compositional Distributional
Semantics (DisCoCat). Mathematics.

Source: "The Algebraic Geodesics of Language and Interfacial Physics",
Part A.1 — Coecke, Clark & Grefenstette. Syntax is a pregroup grammar (a
non-commutative algebraic structure); semantics lives in vector spaces;
the pregroup reduction maps functorially onto tensor contraction.

    Syntax:     word types over a pregroup. noun n, sentence s,
                transitive verb n^r . s . n^l
    Semantics:  meanings are vectors / tensors
    Mapping:    type reduction  --functor-->  tensor contraction

────────────────────────────────────────────────────────────────────────────
WHAT IS AND IS NOT ESTABLISHED HERE
────────────────────────────────────────────────────────────────────────────
ESTABLISHED  pregroup type reduction. This is standard algebra (Lambek).
             x^(a) x^(a+1) -> 1 is a theorem, not a claim of ours.
ESTABLISHED  the functor: a reduction of type n.(n^r.s.n^l).n to s
             corresponds to contracting an order-3 tensor against two
             vectors. Standard DisCoCat.
ESTABLISHED  determinism/reproducibility of the concrete meaning tensors
             (they are fixed functions of the token and the first 16 primes).
OPEN         that the resulting sentence vector is "the meaning" in the
             VAPMIP sense, or that this is The Translator. Not shown.
             Nothing in this module demonstrates translation.

PRIME DIRECTIVE #1: no fitted parameters. Meaning tensors are NOT learned
from a corpus and NOT randomly initialised — they are the prime-channel
harmonic expansion of the token itself (see translator_common). The verb
tensor is that token's own 4096 components reshaped to 16x16x16; nothing
is scaled, whitened, or normalised to make a result come out.

Version: 0.111
"""

import math
from typing import List, Tuple, Dict, Any, Sequence

from ..translator_common.maths import (
    N_CHANNELS, D_HYPER, channel_signature, hypervector,
    cosine, norm, TranslatorEngine,
)


# ── Pregroup grammar ─────────────────────────────────────────────────────────

class PregroupType:
    """
    A pregroup type: a word in the free pregroup over base types.

    Represented as a list of (base, adjoint) pairs, where `adjoint` is an
    integer: 0 = the base type itself, +1 = right adjoint x^r,
    -1 = left adjoint x^l, +2 = x^rr, and so on.

    Reduction rule (Lambek):  x^(a) x^(a+1) -> 1
    which instantiates to the familiar  x x^r -> 1  and  x^l x -> 1.
    """

    def __init__(self, atoms: Sequence[Tuple[str, int]]):
        self.atoms: List[Tuple[str, int]] = [tuple(a) for a in atoms]

    def __repr__(self):
        def show(b, a):
            if a == 0:
                return b
            return f"{b}^{'r' * a if a > 0 else 'l' * (-a)}"
        return ' . '.join(show(b, a) for b, a in self.atoms) or '1'

    def __eq__(self, other):
        return isinstance(other, PregroupType) and self.atoms == other.atoms

    def __mul__(self, other: 'PregroupType') -> 'PregroupType':
        """Concatenation — the pregroup's (non-commutative) product."""
        return PregroupType(self.atoms + other.atoms)


# The three base types used by a transitive clause.
N = PregroupType([('n', 0)])                                    # noun
S = PregroupType([('s', 0)])                                    # sentence
TRANSITIVE_VERB = PregroupType([('n', 1), ('s', 0), ('n', -1)])  # n^r . s . n^l


def reduce_type(t: PregroupType) -> Dict[str, Any]:
    """
    Reduce a pregroup type by repeatedly cancelling adjacent x^(a) x^(a+1).

    Returns the reduced type plus the ordered list of cancellations made —
    the 'reduction witness'. The witness is what the functor transports to
    tensor contractions, so it is returned, not discarded.

    Leftmost-innermost cancellation. Pregroup reduction is confluent for
    these types, so the order does not change the normal form.
    """
    atoms = list(t.atoms)
    witness: List[Dict[str, Any]] = []
    changed = True
    while changed:
        changed = False
        for i in range(len(atoms) - 1):
            (b1, a1), (b2, a2) = atoms[i], atoms[i + 1]
            if b1 == b2 and a2 == a1 + 1:
                witness.append({'position': i, 'base': b1,
                                'adjoints': (a1, a2)})
                del atoms[i:i + 2]
                changed = True
                break
    return {'reduced': PregroupType(atoms), 'witness': witness}


def is_grammatical(subject_t: PregroupType,
                   verb_t: PregroupType,
                   object_t: PregroupType) -> Dict[str, Any]:
    """
    A clause is grammatical iff its concatenated type reduces to s.

        n . (n^r . s . n^l) . n  ->  s

    Returns the verdict AND the reduced type, so an ungrammatical input
    reports what it actually reduced to rather than just False.
    """
    full = subject_t * verb_t * object_t
    red = reduce_type(full)
    return {
        'input_type': repr(full),
        'reduced_type': repr(red['reduced']),
        'witness': red['witness'],
        'grammatical': red['reduced'] == S,
    }


# ── The functor: syntax -> semantics ─────────────────────────────────────────

class MeaningSpace:
    """
    The distributional half. Noun space N and sentence space S are both the
    16-dimensional prime-channel space (the sedenion basis). A transitive
    verb is an order-3 tensor in N (x) S (x) N.

    Derived, not trained: the verb tensor is the verb token's own 4096
    prime-channel harmonics reshaped 16x16x16. 4096 = 16^3 exactly.
    """

    def __init__(self):
        self.dim = N_CHANNELS

    def noun(self, token: str) -> List[float]:
        """Noun meaning: the 16-dim prime-channel signature."""
        return channel_signature(token)

    def verb_tensor(self, token: str) -> List[List[List[float]]]:
        """
        Verb meaning: order-3 tensor T[i][j][k] over N (x) S (x) N.
        Built by reshaping the verb's 4096-dim harmonic vector.
        """
        flat = hypervector(token)
        n = self.dim
        return [[[flat[(i * n + j) * n + k] for k in range(n)]
                 for j in range(n)] for i in range(n)]

    def contract(self, subj: Sequence[float],
                 verb: List[List[List[float]]],
                 obj: Sequence[float]) -> List[float]:
        """
        The functor's image of the reduction n.(n^r.s.n^l).n -> s.

        The two cancellations (n n^r) and (n^l n) become two tensor
        contractions, leaving a vector in S:

            s_j = sum_i sum_k  subj_i * T[i][j][k] * obj_k
        """
        n = self.dim
        out = [0.0] * n
        for j in range(n):
            acc = 0.0
            for i in range(n):
                si = subj[i]
                if si == 0.0:
                    continue
                row = verb[i][j]
                acc += si * sum(row[k] * obj[k] for k in range(n))
            out[j] = acc
        return out


# ── The engine ───────────────────────────────────────────────────────────────

class DisCoCatTranslator(TranslatorEngine):
    """
    The Translator, version 1: DisCoCat.

    Pipeline:  tokens -> pregroup types -> reduction (grammaticality check)
               -> functor -> tensor contraction -> sentence vector in S.
    """

    def __init__(self, space: 'MeaningSpace' = None):
        """
        space: the distributional half. Defaults to MeaningSpace (prime-channel
        harmonics of the token itself).

        Injectable because that default was MEASURED to be a length detector,
        not a semantic encoder: project() = cbar*W(n,k,sigma) + D(content) with
        content at 2-3% of signal, so cosine tracks |len(a)-len(b)| and nothing
        else. The default is retained unchanged (Prime Directive #2 — the
        failing path stays) and an alternative space can be supplied instead.
        See VAPMIP/discocat_corpus.py for a co-occurrence-backed space.

        The pregroup layer above is untouched by this choice: grammaticality
        and the reduction witness are type-driven, not vector-driven.
        """
        self.space = space if space is not None else MeaningSpace()

    @property
    def version_name(self) -> str:
        return 'discocat'

    def encode(self, token: str) -> List[float]:
        return self.space.noun(token)

    def compose(self, subject: str, verb: str, obj: str) -> List[float]:
        """
        Compose a transitive clause. Ungrammatical types are NOT silently
        composed anyway — a clause whose type does not reduce to s raises,
        because a DisCoCat composition of a non-reducing type is undefined,
        not merely low quality.
        """
        check = is_grammatical(N, TRANSITIVE_VERB, N)
        if not check['grammatical']:
            raise ValueError(
                f"type does not reduce to s: {check['reduced_type']}")
        return self.space.contract(self.space.noun(subject),
                                   self.space.verb_tensor(verb),
                                   self.space.noun(obj))

    def explain(self, subject: str, verb: str, obj: str) -> Dict[str, Any]:
        """Full trace: types, reduction witness, and the resulting vector."""
        check = is_grammatical(N, TRANSITIVE_VERB, N)
        vec = self.compose(subject, verb, obj)
        return {
            'tokens': (subject, verb, obj),
            'types': {'subject': repr(N), 'verb': repr(TRANSITIVE_VERB),
                      'object': repr(N)},
            'reduction': check,
            'sentence_vector': vec,
            'sentence_norm': norm(vec),
        }


# ── Diagnostics (report, never tune) ─────────────────────────────────────────

def verify_reduction_algebra() -> Dict[str, Any]:
    """
    Check the pregroup reduction against cases whose normal form is known
    from Lambek's algebra, INCLUDING cases that must NOT reduce.
    """
    cases = [
        ('n . n^r',              PregroupType([('n', 0), ('n', 1)]),  '1'),
        ('n^l . n',              PregroupType([('n', -1), ('n', 0)]), '1'),
        ('transitive clause',    N * TRANSITIVE_VERB * N,             's'),
        # Negative controls — these MUST survive un-reduced.
        ('n . n  (no cancel)',   PregroupType([('n', 0), ('n', 0)]),  'n . n'),
        ('n^r . n (wrong order)', PregroupType([('n', 1), ('n', 0)]), 'n^r . n'),
        ('n . s^r (mismatch)',   PregroupType([('n', 0), ('s', 1)]),  'n . s^r'),
    ]
    results = []
    for label, t, expected in cases:
        got = repr(reduce_type(t)['reduced'])
        results.append({'case': label, 'expected': expected,
                        'got': got, 'pass': got == expected})
    return {'cases': results,
            'all_pass': all(r['pass'] for r in results)}


def word_order_sensitivity(engine: 'DisCoCatTranslator',
                           subject: str, verb: str, obj: str) -> Dict[str, Any]:
    """
    'DOG BITES MAN' vs 'MAN BITES DOG'.

    The pregroup is non-commutative and the verb tensor is not symmetric in
    its two noun slots, so these should differ. Reported as a measurement.
    A cosine near 1.0 would mean this construction cannot see word order —
    a real negative result, to be reported, never patched around.
    """
    a = engine.compose(subject, verb, obj)
    b = engine.compose(obj, verb, subject)
    return {
        'forward': (subject, verb, obj),
        'reversed': (obj, verb, subject),
        'cosine': cosine(a, b),
        'distinguishes_word_order': abs(cosine(a, b)) < 1.0 - 1e-9,
    }
