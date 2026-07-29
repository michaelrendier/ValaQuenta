"""
ainulindale_engine.modules.translator_common.maths
====================================================
The Translator — SHARED SUBSTRATE for both Translator engines.

This is NOT itself a registered engine. It has no tools.py and does not
appear in the registry. It exists so that translator_discocat and
translator_vsa operate in the SAME derived vector space and can therefore
be combined and cross-tested later (Cody, 2026-07-28: "Ensure they can
both be combined for testing later").

Source of the two versions: "The Algebraic Geodesics of Language and
Interfacial Physics", Part A — two suggested formal frameworks for mapping
prime concepts into syntactically valid sentences:
    version 1  DisCoCat  (Coecke/Clark/Grefenstette) -> translator_discocat
    version 2  VSA/HDC   (Kanerva)                   -> translator_vsa

────────────────────────────────────────────────────────────────────────────
PRIME DIRECTIVE #1 COMPLIANCE — read before changing anything here
────────────────────────────────────────────────────────────────────────────
NOTHING in this file is fitted, trained, tuned, seeded from a PRNG, or
normalised to hit a target. Every vector is a deterministic function of the
input string and the first 16 primes. There are no free parameters.

In particular, the dimensions are DERIVED, not chosen:

    N_CHANNELS = 16     the sedenion basis e0..e15 — the framework's own
                        algebra, already the carrier in layer_spectrograph.py
                        (16 prime channels, p = 2..53).

    D_HYPER    = 4096   NOT a tuned "big enough for HDC" number. In DisCoCat
                        a transitive verb has pregroup type n^r·s·n^l, so its
                        meaning is an order-3 tensor in N x S x N. With
                        N = S = 16 that tensor has exactly 16^3 = 4096
                        components. D_HYPER IS that tensor order, flattened.

That coincidence is the whole reason the two engines are combinable: the
DisCoCat verb tensor and the VSA hypervector are THE SAME 4096 numbers in
the same derived basis, just reshaped. Neither engine was adjusted to make
this line up — it falls out of taking the sedenion as the noun space.

Kanerva's stated HDC regime is "~10,000 dimensions"; 4096 is below that and
we do NOT raise it to please the citation. If quasi-orthogonality is too
weak at 4096, that is a real result about this construction and must be
REPORTED, not fixed by enlarging D (Prime Directive #2).

Confidence:
    prime-channel encoding is deterministic and reproducible: ESTABLISHED
    pregroup reduction (translator_discocat): ESTABLISHED (standard algebra)
    VSA bind/bundle/permute algebra (translator_vsa): ESTABLISHED (standard)
    that either one constitutes "The Translator" in the VAPMIP sense: OPEN

Version: 0.111
"""

import math
from abc import ABC, abstractmethod
from fractions import Fraction
from typing import List, Sequence, Dict, Any


# ── Derived dimensions ───────────────────────────────────────────────────────

# The 16 prime channels e0..e15. Cited from the existing framework
# (SedenionSpectralRelativity/layer_spectrograph.py), not invented here.
PRIME_CHANNELS: List[int] = [2, 3, 5, 7, 11, 13, 17, 19,
                             23, 29, 31, 37, 41, 43, 47, 53]

N_CHANNELS = len(PRIME_CHANNELS)          # 16 — the sedenion basis
N_HARMONICS = N_CHANNELS * N_CHANNELS     # 256 — two further CD doublings
D_HYPER = N_CHANNELS * N_HARMONICS        # 4096 = 16^3 — the verb tensor order

assert N_CHANNELS == 16
assert D_HYPER == N_CHANNELS ** 3


# ── The prime-channel encoder ────────────────────────────────────────────────

def channel_signature(token: str) -> List[float]:
    """
    The 16-dimensional prime-channel signature of a token.

        x_k = sum_i  c_i * i^(-1/2) * cos(2*pi*i / p_k)

    where c_i is the codepoint of the i-th character (i is 1-indexed) and
    p_k is the k-th prime channel. This is the Dirichlet-weighted cosine
    projection already used in the framework, applied to characters.

    Deterministic. No parameters. Empty token -> zero vector (kept as an
    honest zero, NOT special-cased to something non-degenerate).
    """
    out = []
    for p in PRIME_CHANNELS:
        acc = 0.0
        for i, ch in enumerate(token, start=1):
            acc += ord(ch) * (i ** -0.5) * math.cos(2.0 * math.pi * i / p)
        out.append(acc)
    return out


def hypervector(token: str) -> List[float]:
    """
    The 4096-dimensional harmonic extension of channel_signature().

        j = h * 16 + k        k = prime channel, h = harmonic 0..255
        x_j = sum_i c_i * i^(-1/2) * cos(2*pi*(h+1)*i / p_k)

    At h = 0 this reduces EXACTLY to channel_signature() (verified by
    verify_harmonic_reduction below). Deterministic, no parameters.
    """
    out = [0.0] * D_HYPER
    codes = [(i, ord(ch)) for i, ch in enumerate(token, start=1)]
    for h in range(N_HARMONICS):
        for k, p in enumerate(PRIME_CHANNELS):
            acc = 0.0
            for i, c in codes:
                acc += c * (i ** -0.5) * math.cos(2.0 * math.pi * (h + 1) * i / p)
            out[h * N_CHANNELS + k] = acc
    return out


def verify_harmonic_reduction(token: str, tol: float = 1e-12) -> Dict[str, Any]:
    """
    Check that hypervector()[0:16] == channel_signature(token).

    This is the joint that holds the two engines together. If it ever fails,
    the engines are no longer in the same space and must NOT be combined.
    Returns the residual; does not raise.
    """
    sig = channel_signature(token)
    hyp = hypervector(token)[:N_CHANNELS]
    resid = max((abs(a - b) for a, b in zip(sig, hyp)), default=0.0)
    return {'token': token, 'max_residual': resid, 'matches': resid <= tol}


# ── Vector helpers (pure Python — registry contract forbids deps in maths) ───

def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(a: Sequence[float]) -> float:
    return math.sqrt(dot(a, a))


def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    """
    Cosine similarity. Returns 0.0 for a zero vector — that is a genuine
    'no direction' answer, not a fallback that hides a degenerate input.
    """
    na, nb = norm(a), norm(b)
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot(a, b) / (na * nb)


# ── The shared engine interface ──────────────────────────────────────────────

class TranslatorEngine(ABC):
    """
    Contract both Translator versions satisfy, so a later harness can run
    them side by side on identical input without knowing which is which.

    Deliberately minimal: the two frameworks disagree about almost
    everything internally, and forcing more shared surface than this would
    mean distorting one of them to match the other.
    """

    @property
    @abstractmethod
    def version_name(self) -> str:
        """'discocat' or 'vsa'."""

    @abstractmethod
    def encode(self, token: str) -> List[float]:
        """Token -> that engine's native vector for it."""

    @abstractmethod
    def compose(self, subject: str, verb: str, obj: str) -> List[float]:
        """
        Compose a transitive sentence into the 16-dim sentence space S.
        Both engines MUST return length-16 so results are comparable.
        """

    def sentence_similarity(self, a: Sequence[str], b: Sequence[str]) -> float:
        """Cosine between two composed (subject, verb, object) triples."""
        return cosine(self.compose(*a), self.compose(*b))


# ── The combination harness ──────────────────────────────────────────────────

def compare_engines(engine_a: TranslatorEngine,
                    engine_b: TranslatorEngine,
                    triples: Sequence[Sequence[str]]) -> Dict[str, Any]:
    """
    Run both Translator versions over the same (subject, verb, object)
    triples and report where they agree and where they do not.

    This reports. It does not score, rank, or tune. A low agreement figure
    is a finding about the two constructions, not a defect to be corrected
    by adjusting either engine.
    """
    rows = []
    for t in triples:
        va = engine_a.compose(*t)
        vb = engine_b.compose(*t)
        rows.append({
            'triple': tuple(t),
            'cos_between_engines': cosine(va, vb),
            f'norm_{engine_a.version_name}': norm(va),
            f'norm_{engine_b.version_name}': norm(vb),
        })

    # Do the two engines induce the same ORDERING on sentence pairs?
    # (Rank agreement matters more than absolute cosine: the engines use
    #  different normalisations by construction.)
    pair_rows = []
    for i in range(len(triples)):
        for j in range(i + 1, len(triples)):
            pair_rows.append({
                'pair': (tuple(triples[i]), tuple(triples[j])),
                engine_a.version_name: engine_a.sentence_similarity(triples[i], triples[j]),
                engine_b.version_name: engine_b.sentence_similarity(triples[i], triples[j]),
            })
    concordant = discordant = 0
    for x in range(len(pair_rows)):
        for y in range(x + 1, len(pair_rows)):
            da = pair_rows[x][engine_a.version_name] - pair_rows[y][engine_a.version_name]
            db = pair_rows[x][engine_b.version_name] - pair_rows[y][engine_b.version_name]
            if da * db > 0:
                concordant += 1
            elif da * db < 0:
                discordant += 1
    total = concordant + discordant
    tau = Fraction(concordant - discordant, total) if total else None

    return {
        'per_triple': rows,
        'per_pair': pair_rows,
        'kendall_tau_concordant': concordant,
        'kendall_tau_discordant': discordant,
        # Fraction until the output boundary, per the registry contract.
        'kendall_tau': float(tau) if tau is not None else None,
        'note': ('tau is rank agreement between the two Translator versions. '
                 'It is a measurement, not a target.'),
    }
