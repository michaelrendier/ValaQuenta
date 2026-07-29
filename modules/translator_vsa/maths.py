"""
ainulindale_engine.modules.translator_vsa.maths
=================================================
The Translator, VERSION 2 of 2 — Vector-Symbolic Architecture /
Hyperdimensional Computing (VSA / HDC). Mathematics.

Source: "The Algebraic Geodesics of Language and Interfacial Physics",
Part A.2 — Pentti Kanerva. Concepts are high-dimensional vectors; structure
is built by three operations:

    Bind    (x)   pairs role with filler, NON-COMMUTATIVELY
                  e.g. ROLE_SUBJECT (x) CONCEPT_DOG
    Bundle  (+)   superposes bound pairs into one vector of the same size,
                  without losing the constituents
    Permute (P)   shifts elements to encode sequence / grammatical position

────────────────────────────────────────────────────────────────────────────
WHAT IS AND IS NOT ESTABLISHED HERE
────────────────────────────────────────────────────────────────────────────
ESTABLISHED  the bind/bundle/permute algebra and its stated identities
             (permutation is orthogonal, bind distributes over bundle).
             Standard VSA.
THEORETICAL  that bundling preserves constituents recoverably AT THIS
             DIMENSION with THESE vectors. Kanerva's guarantees assume
             quasi-orthogonal (typically random) hypervectors at ~10,000
             dimensions. Ours are neither random nor 10,000-dimensional —
             they are deterministic prime-channel projections at 4096.
             capacity_probe() and unbind_probe() MEASURE this. If they come
             back poor, that is a finding about this construction.
OPEN         that this constitutes The Translator. Not shown.

PRIME DIRECTIVE #1: no fitted parameters, and specifically NO RANDOM SEED.
Textbook VSA draws hypervectors from a PRNG; that would make results
irreproducible and would let a "good" seed be selected. Every vector here —
fillers AND role vectors — is the deterministic prime-channel harmonic
expansion of its own name.

PRIME DIRECTIVE #2: the probes below are permitted to fail and their
failures are the point. Do not raise D_HYPER, switch to random vectors, or
normalise to rescue a probe.

Version: 0.111
"""

import math
from typing import List, Sequence, Dict, Any

from ..translator_common.maths import (
    N_CHANNELS, N_HARMONICS, D_HYPER, PRIME_CHANNELS,
    hypervector, channel_signature, cosine, norm, dot, TranslatorEngine,
)


# ── The three VSA operations ─────────────────────────────────────────────────

def permute(v: Sequence[float], shift: int = 1) -> List[float]:
    """
    Permute (P): cyclic shift. Orthogonal, invertible, and it is what
    encodes position/sequence. P^D = identity.
    """
    d = len(v)
    if d == 0:
        return []
    s = shift % d
    return list(v[-s:]) + list(v[:-s]) if s else list(v)


def bind(a: Sequence[float], b: Sequence[float]) -> List[float]:
    """
    Bind (x): NON-COMMUTATIVE role-filler pairing.

        a (x) b  =  P(a) . b        (elementwise product after permuting a)

    Plain elementwise multiplication is commutative, which the source
    document explicitly rules out ("Pairs role-filler concepts
    non-commutatively"). Permuting the left operand first breaks the
    symmetry: P(a).b != P(b).a in general.
    """
    if len(a) != len(b):
        raise ValueError(f"bind: dimension mismatch {len(a)} vs {len(b)}")
    pa = permute(a)
    return [x * y for x, y in zip(pa, b)]


def bundle(*vectors: Sequence[float]) -> List[float]:
    """
    Bundle (+): elementwise superposition.

    Deliberately NOT normalised. Normalising here would be a free scaling
    applied to make downstream similarities look better — exactly the kind
    of move Prime Directive #1 forbids. Cosine similarity is scale-invariant
    anyway, so normalisation would buy nothing but a hidden knob.
    """
    if not vectors:
        return []
    d = len(vectors[0])
    for v in vectors:
        if len(v) != d:
            raise ValueError("bundle: dimension mismatch")
    return [sum(v[i] for v in vectors) for i in range(d)]


# ── Derived role vectors (no PRNG) ───────────────────────────────────────────

ROLE_NAMES = ('ROLE_SUBJECT', 'ROLE_VERB', 'ROLE_OBJECT')


def role_vector(role_name: str) -> List[float]:
    """
    A role's hypervector is the prime-channel expansion of its own name.
    Deterministic and inspectable — no seed, no draw.
    """
    return hypervector(role_name)


# ── Projection back to the shared 16-dim sentence space ──────────────────────

def fold_to_channels(v: Sequence[float]) -> List[float]:
    """
    Project a 4096-dim hypervector onto the 16 prime channels by summing
    over the 256 harmonics of each channel:

        s_k = sum_h v[h*16 + k]

    Parameter-free, and it is the adjoint of the harmonic expansion that
    built the vector — the natural map back, not a chosen readout.
    Needed so this engine's compose() lands in the SAME 16-dim space as
    the DisCoCat engine's, which is what makes the two combinable.
    """
    if len(v) != D_HYPER:
        raise ValueError(f"fold_to_channels: expected {D_HYPER}, got {len(v)}")
    out = [0.0] * N_CHANNELS
    for h in range(N_HARMONICS):
        base = h * N_CHANNELS
        for k in range(N_CHANNELS):
            out[k] += v[base + k]
    return out


# ── The engine ───────────────────────────────────────────────────────────────

class VSATranslator(TranslatorEngine):
    """
    The Translator, version 2: VSA / hyperdimensional computing.

    Pipeline:  tokens -> filler hypervectors -> bind with role vectors
               -> bundle into one 4096-dim sentence hypervector
               -> fold to the shared 16-dim sentence space.
    """

    def __init__(self):
        self.roles = {name: role_vector(name) for name in ROLE_NAMES}

    @property
    def version_name(self) -> str:
        return 'vsa'

    def encode(self, token: str) -> List[float]:
        """Filler hypervector — full 4096-dim."""
        return hypervector(token)

    def sentence_hypervector(self, subject: str, verb: str,
                             obj: str) -> List[float]:
        """The 4096-dim bound-and-bundled sentence, before folding."""
        return bundle(
            bind(self.roles['ROLE_SUBJECT'], self.encode(subject)),
            bind(self.roles['ROLE_VERB'],    self.encode(verb)),
            bind(self.roles['ROLE_OBJECT'],  self.encode(obj)),
        )

    def compose(self, subject: str, verb: str, obj: str) -> List[float]:
        return fold_to_channels(self.sentence_hypervector(subject, verb, obj))

    def explain(self, subject: str, verb: str, obj: str) -> Dict[str, Any]:
        hv = self.sentence_hypervector(subject, verb, obj)
        folded = fold_to_channels(hv)
        return {
            'tokens': (subject, verb, obj),
            'roles': list(ROLE_NAMES),
            'hypervector_dim': len(hv),
            'hypervector_norm': norm(hv),
            'sentence_vector': folded,
            'sentence_norm': norm(folded),
        }


# ── Diagnostics (report, never tune) ─────────────────────────────────────────

def verify_vsa_identities(tokens: Sequence[str] = ('dog', 'bites', 'man'),
                          tol: float = 1e-9) -> Dict[str, Any]:
    """
    Check the algebraic identities VSA actually guarantees:
      1. permute is invertible:            P^-1(P(a)) == a
      2. permutation preserves norm:       |P(a)| == |a|
      3. bind is NON-commutative:          a (x) b != b (x) a
      4. bind distributes over bundle:     a (x) (b+c) == (a (x) b)+(a (x) c)
    """
    a, b, c = (hypervector(t) for t in tokens)
    inv = permute(permute(a), -1)
    lhs = bind(a, bundle(b, c))
    rhs = bundle(bind(a, b), bind(a, c))
    checks = [
        {'identity': 'P^-1(P(a)) == a',
         'residual': max(abs(x - y) for x, y in zip(inv, a)),
         'pass': max(abs(x - y) for x, y in zip(inv, a)) <= tol},
        {'identity': '|P(a)| == |a|',
         'residual': abs(norm(permute(a)) - norm(a)),
         'pass': abs(norm(permute(a)) - norm(a)) <= tol},
        {'identity': 'a (x) b != b (x) a  (non-commutativity)',
         'residual': cosine(bind(a, b), bind(b, a)),
         'pass': cosine(bind(a, b), bind(b, a)) < 1.0 - 1e-9},
        {'identity': 'bind distributes over bundle',
         'residual': max(abs(x - y) for x, y in zip(lhs, rhs)),
         'pass': max(abs(x - y) for x, y in zip(lhs, rhs)) <= tol},
    ]
    return {'checks': checks, 'all_pass': all(c['pass'] for c in checks)}


def capacity_probe(tokens: Sequence[str]) -> Dict[str, Any]:
    """
    Measure quasi-orthogonality of the DERIVED (non-random) hypervectors.

    Kanerva's capacity guarantees rest on distinct concepts being nearly
    orthogonal. Our vectors are deterministic prime projections, so this is
    an open empirical question, not an assumption. Reports the full cosine
    distribution between distinct tokens.

    A large mean |cosine| means this construction crowds its concepts
    together and bundling will not be recoverable. That is a REAL RESULT
    about deriving hypervectors instead of drawing them. It must be
    reported as such — not repaired by switching to a PRNG.
    """
    vs = {t: hypervector(t) for t in tokens}
    pairs = []
    ts = list(tokens)
    for i in range(len(ts)):
        for j in range(i + 1, len(ts)):
            pairs.append({'pair': (ts[i], ts[j]),
                          'cosine': cosine(vs[ts[i]], vs[ts[j]])})
    if not pairs:
        return {'pairs': [], 'mean_abs_cosine': None, 'max_abs_cosine': None}
    mags = [abs(p['cosine']) for p in pairs]
    return {
        'dimension': D_HYPER,
        'n_tokens': len(ts),
        'pairs': pairs,
        'mean_abs_cosine': sum(mags) / len(mags),
        'max_abs_cosine': max(mags),
        'kanerva_regime_dimension': 10000,
        'note': ('Quasi-orthogonality is ASSUMED by textbook VSA and '
                 'MEASURED here. Derived vectors are not random vectors.'),
    }


def unbind_probe(subject: str = 'dog', verb: str = 'bites',
                 obj: str = 'man') -> Dict[str, Any]:
    """
    Can a constituent be recovered from the bundled sentence?

    Probe: correlate the sentence hypervector with each role-filler binding
    and see whether the correct filler scores highest for its own role.
    Uses only cosine — no learned readout, no threshold.

    Reports per-role rank. Failure is retained and reported.
    """
    eng = VSATranslator()
    sent = eng.sentence_hypervector(subject, verb, obj)
    fillers = [subject, verb, obj]
    results = []
    for role, correct in zip(ROLE_NAMES, fillers):
        scores = [{'filler': f,
                   'cosine': cosine(sent, bind(eng.roles[role], hypervector(f)))}
                  for f in fillers]
        scores.sort(key=lambda s: -s['cosine'])
        results.append({
            'role': role,
            'correct_filler': correct,
            'ranked': scores,
            'top1_correct': scores[0]['filler'] == correct,
        })
    n_correct = sum(1 for r in results if r['top1_correct'])
    return {
        'sentence': (subject, verb, obj),
        'per_role': results,
        'top1_accuracy': n_correct / len(results),
        'chance_level': 1.0 / len(fillers),
        'note': 'top1 at or below chance means bundling is not recoverable here.',
    }
