"""
ValaQuenta.modules.hyperwebster.maths
=====================================
HyperWebster hypergallery — Horner bijection, SemanticWord datatype.

The HyperWebster is a coordinate system, not a dictionary.
Every word is an address. Every address is exact.

Horner bijection (base-97)::

  text_index = c0·97^{k-1} + c1·97^{k-2} + ... + c_{k-1}·97^0

Fano index (base-7)::

  fano_index = (char_idx % 7) for each char — octonion path address

SemanticWord: a word with both a Horner address and a Fano address.
The monad: HyperWebster + Cayley-Dickson SMNNIP integrated.

Version: 0.111
"""

import math
import hashlib
from typing import Dict, List, Any, Tuple, Optional


# ── Character map ──────────────────────────────────────────────────────────────

US_KEYBOARD_CHARS: str = (
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '0123456789'
    '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    ' \t\n'
)
assert len(US_KEYBOARD_CHARS) == 97

VOCAB_BASE = 97
FANO_BASE  = 7

_CHAR_TO_IDX: Dict[str, int] = {c: i for i, c in enumerate(US_KEYBOARD_CHARS)}
_IDX_TO_CHAR: Dict[int, str] = {i: c for i, c in enumerate(US_KEYBOARD_CHARS)}

# Fano plane lines
FANO_LINES: List[Tuple[int,int,int]] = [
    (0,1,3),(1,2,4),(2,3,5),(3,4,6),(4,5,0),(5,6,1),(6,0,2)
]


def char_to_idx(c: str) -> int:
    """
    Return a character's index in the 97-character keyboard map; an unknown character maps to 0.

    :param c: one character
    :returns: the index, 0..96
    """
    return _CHAR_TO_IDX.get(c, 0)

def idx_to_char(i: int) -> str:
    """
    Return the character at an index of the keyboard map, taken mod 97.

    :param i: index
    :returns: the character
    """
    return _IDX_TO_CHAR.get(i % VOCAB_BASE, ' ')


# ── Horner bijection ───────────────────────────────────────────────────────────

def horner_encode(sequence: str) -> int:
    """
    Lossless base-97 Horner encoding.
    idx = c0·97^{k-1} + c1·97^{k-2} + ... + c_{k-1}
    Pure Python int — arbitrary precision.

    :param sequence: text drawn from the keyboard map
    :returns: the base-97 Horner index, an arbitrary-precision int
    """
    idx = 0
    for char in sequence:
        idx = idx * VOCAB_BASE + char_to_idx(char)
    return idx


def horner_decode(idx: int, length: int) -> str:
    """
    Invert Horner encoding. Returns original sequence.

    :param idx: Horner index
    :param length: number of characters to recover
    :returns: the original text
    """
    chars = []
    remaining = idx
    for _ in range(length):
        chars.append(idx_to_char(remaining % VOCAB_BASE))
        remaining //= VOCAB_BASE
    chars.reverse()
    return ''.join(chars)


def fano_encode(sequence: str) -> int:
    """
    Base-7 Fano/octonion path encoding.
    Each char maps to one of 7 octonion generators: char_idx % 7 → e_1..e_7

    :param sequence: text drawn from the keyboard map
    :returns: the base-7 path index
    """
    idx = 0
    for char in sequence:
        component = char_to_idx(char) % FANO_BASE
        idx = idx * FANO_BASE + component
    return idx


def fano_decode(idx: int, length: int) -> List[int]:
    """
    Decode Fano index to list of generator indices (0..6).

    :param idx: Fano path index
    :param length: number of generators
    :returns: generator indices, each 0..6
    """
    components = []
    remaining = idx
    for _ in range(length):
        components.append(remaining % FANO_BASE)
        remaining //= FANO_BASE
    components.reverse()
    return components


def fano_path_to_word(generator_indices: List[int]) -> str:
    """
    Reverse-map Fano generator indices to nearest keyboard characters.
    Each generator index g (0..6) maps to chars where char_idx % 7 == g.
    Returns canonical (alphabetically first) representative.

    :param generator_indices: generator indices, each 0..6
    :returns: the canonical word for the path
    """
    result = []
    for g in generator_indices:
        # Find first char whose index % 7 == g
        for i in range(VOCAB_BASE):
            if i % FANO_BASE == g:
                result.append(idx_to_char(i))
                break
    return ''.join(result)


# ── SemanticWord ───────────────────────────────────────────────────────────────

class SemanticWord:
    """
    A word with a Horner address (base-97) and a Fano address (base-7).

    The address is the identity — not a lookup, not a pointer.
    "Ptolemy speaks because he knows" — recognition, not construction.
    """

    __slots__ = ('text', 'horner_idx', 'fano_idx', 'length', '_hash')

    def __init__(self, text: str):
        self.text       = text
        self.length     = len(text)
        self.horner_idx = horner_encode(text)
        self.fano_idx   = fano_encode(text)
        self._hash      = hashlib.sha256(text.encode('utf-8')).hexdigest()

    @classmethod
    def from_horner(cls, idx: int, length: int) -> 'SemanticWord':
        """
        Build a word from its Horner address.

        :param idx: Horner index
        :param length: number of characters
        :returns: the word at that address
        """
        return cls(horner_decode(idx, length))

    def fano_generators(self) -> List[int]:
        """
        Return the word's octonion generator path.

        :returns: generator indices, each 0..6
        """
        return fano_decode(self.fano_idx, self.length)

    def verify(self) -> bool:
        """
        Check that decoding the word's Horner address returns its text.

        :returns: True if the round trip holds
        """
        return horner_decode(self.horner_idx, self.length) == self.text

    def to_dict(self) -> Dict[str, Any]:
        """
        Return the word as plain data.

        :returns: dict with the text, length and addresses
        """
        return {
            'text'      : self.text,
            'length'    : self.length,
            'horner_idx': self.horner_idx,
            'fano_idx'  : self.fano_idx,
            'hash'      : self._hash[:16] + '…',
            'verified'  : self.verify(),
            'fano_gens' : self.fano_generators(),
        }

    def __repr__(self):
        return f"SemanticWord({self.text!r} @ h={self.horner_idx} f={self.fano_idx})"


# ── HyperWebster gallery ───────────────────────────────────────────────────────

class HyperGallery:
    """
    The hypergallery — a navigable address space of SemanticWords.
    Coordinates instead of pointers.

    Browsing: navigate by Horner address offset or Fano generator path.
    Search: nearest-neighbour by Fano generator similarity.
    """

    def __init__(self):
        self._words: Dict[int, SemanticWord] = {}

    def add(self, text: str) -> SemanticWord:
        """
        Add a word to the gallery, keyed by its Horner address.

        :param text: the word's text
        :returns: the stored word
        """
        w = SemanticWord(text)
        self._words[w.horner_idx] = w
        return w

    def lookup_horner(self, idx: int, length: int) -> Optional[SemanticWord]:
        """
        Find a word by Horner address; an address not stored is reconstructed from the address itself.

        :param idx: Horner index
        :param length: number of characters
        :returns: the word, or None if it cannot be reconstructed
        """
        if idx in self._words:
            return self._words[idx]
        # Reconstruct from address
        try:
            return SemanticWord.from_horner(idx, length)
        except Exception:
            return None

    def fano_neighbours(self, word: SemanticWord, n: int = 5) -> List[SemanticWord]:
        r"""
        Find words whose Fano index is closest to word's Fano index.
        Distance = \|fano_idx_a - fano_idx_b\| (integer distance).

        :param word: the word to find neighbours of
        :param n: number of neighbours
        :returns: the n words whose Fano index is nearest
        """
        target = word.fano_idx
        results = sorted(
            self._words.values(),
            key=lambda w: abs(w.fano_idx - target)
        )
        return results[:n]

    def address_range(self, start_text: str, n: int = 8) -> List[SemanticWord]:
        """
        Return n consecutive addresses starting from start_text's Horner index.

        :param start_text: text whose Horner index starts the range
        :param n: number of addresses
        :returns: the n consecutive words
        """
        base = horner_encode(start_text)
        length = len(start_text)
        result = []
        for offset in range(n):
            idx = base + offset
            try:
                w = SemanticWord.from_horner(idx, length)
                result.append(w)
            except Exception:
                pass
        return result

    def summary(self) -> Dict[str, Any]:
        """
        Summarise the gallery.

        :returns: dict with the word count and the smallest and largest Horner address
        """
        return {
            'n_words'  : len(self._words),
            'min_horner': min(self._words.keys()) if self._words else None,
            'max_horner': max(self._words.keys()) if self._words else None,
        }


# ── Monad integration ──────────────────────────────────────────────────────────

def monad_address(text: str, algebra: int) -> Dict[str, Any]:
    """
    Monad: HyperWebster + Cayley-Dickson SMNNIP integrated.

    Maps a SemanticWord to coordinates in the algebra tower::

      ℝ layer : horner_idx mod dim_R
      ℂ layer : (horner_idx mod dim_C^2) complex components
      ℍ layer : (fano_idx mod dim_H^4) quaternion components
      𝕆 layer : (fano_idx mod dim_O^8) octonion components

    This is the Tongue — reverse lookup from attractor to SemanticWord.

    :param text: the word
    :param algebra: algebra dimension of the layer
    :returns: dict with the word's coordinates in the ℝ, ℂ, ℍ and 𝕆 layers
    """
    ALG_DIM = {0:1, 1:2, 2:4, 3:8}
    sw = SemanticWord(text)
    h  = sw.horner_idx
    f  = sw.fano_idx

    coords = {}
    for alg, dim in ALG_DIM.items():
        # Distribute the Horner index across algebra dimensions
        components = []
        idx = h
        for _ in range(dim):
            components.append(idx % VOCAB_BASE)
            idx //= VOCAB_BASE
        # Normalise to [-1, 1]
        norm = [c / (VOCAB_BASE - 1) * 2 - 1 for c in components]
        coords[f'alg_{alg}'] = norm

    # Fano path (octonion generators traversed)
    fano_path = fano_decode(f, len(text))

    return {
        'word'      : text,
        'horner'    : h,
        'fano'      : f,
        'fano_path' : fano_path,
        'coords'    : coords,
        'verified'  : sw.verify(),
        'algebra'   : str(algebra),
    }
