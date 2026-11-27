"""
ValaQuenta.modules.basile.maths
===============================
Invertible location ↔ content maps of the Library of Babel family (J. Basile).

The Library of Babel site and its image sibling, Babelia, place every page (or
image) at a numeric location that is *computed*, never stored. Basile publishes
the method for Babelia as a README recipe plus C++ source: a linear
congruential generator (LCG) followed by shift/XOR steps, inverted with the
modular inverse of the multiplier and the shifts undone in reverse order.

This module has four parts.

* **A. The ordered address** (bijective base-N): the same set of contents in
  rank order. It is the contrast case for the scrambled maps.
* **B. The recipe, generic**: xorshift steps with exact inverses, an LCG with
  its modular inverse, a Hull–Dobell checker, and a scrambler of ``[0, N)``
  (LCG modulo ``2^e``, two xorshifts, cycle-walking). Written from the recipe;
  no published source text or constant is used.
* **C. The published Babelia engine**, run on the published constants. The
  constants are read at run time from a local copy of Basile's files
  (``librarianofbabel/libraryofbabel.info-algo``, CC BY-SA-NC, uploaded
  2019-01-02) and are **never vendored here**: ValaQuenta is GPL-3.0-only.
  :func:`fetch_published` downloads the files into a cache directory.
* **D. The smaller published pieces**: the Extended Euclid file (a fixed
  25-entry array), and the request the LobThis extension posts to the site's
  resource locator (built, never sent).

The text library's own algorithm is **not published** (its README says the
published one is the more efficient rewrite for Babelia); nothing here claims
to reproduce the site's page contents.

Pure Python 3. ``gmpy2`` is used when importable and only for speed; results
are identical without it.

Version: 1.3
"""

import hashlib
import math
import os
import re
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

try:                                    # optional accelerator; never required
    import gmpy2 as _gmpy2
    _num = _gmpy2.mpz
except ImportError:                     # pragma: no cover - environment dependent
    _gmpy2 = None
    _num = int

BABEL_ALPHABET: str = "abcdefghijklmnopqrstuvwxyz ,."
PAGE_CHARS = 3200
LINES_PER_PAGE = 40
CHARS_PER_LINE = 80
PAGES_PER_BOOK = 410
BOOKS_PER_SHELF = 32
SHELVES_PER_WALL = 5
WALLS_PER_HEXAGON = 4

PUBLISHED_REPO = "librarianofbabel/libraryofbabel.info-algo"
PUBLISHED_FILES: Dict[str, str] = {
    "README.md": "README.md",
    "PRNG": "PRNG",
    "imagesearch.cpp": "imagesearch.cpp",
    "euclid_extended.cpp": "Euclid's%20Extended",
}
_RAW = "https://raw.githubusercontent.com/" + PUBLISHED_REPO + "/master/"
RESOURCE_LOCATOR_URL = "http://libraryofbabel.info/resourcelocator.cgi"

# ── A. The ordered address ─────────────────────────────────────────────────


def ordered_address(text: str, alphabet: str) -> int:
    """
    Rank of ``text`` among all strings over ``alphabet``, shortest first and alphabetical within a length.

    :param text: a string over ``alphabet`` (the empty string is at -1, before the first symbol)
    :param alphabet: the ordered symbols; the first symbol is digit value 1
    :returns: the rank: -1 for the empty string, 0 for the first symbol alone
    :raises ValueError: if ``text`` contains a symbol outside ``alphabet``
    """
    n, a = len(alphabet), 0
    for ch in text:
        i = alphabet.find(ch)
        if i < 0:
            raise ValueError(f"symbol {ch!r} is not in the alphabet")
        a = a * n + i + 1
    return a - 1


def ordered_text_at(address: int, alphabet: str) -> str:
    """
    Inverse of :func:`ordered_address`.

    :param address: an integer at least -1 (the empty word is at -1)
    :param alphabet: the ordered symbols
    :returns: the string whose rank is ``address``
    :raises ValueError: if ``address`` is below -1
    """
    if address < -1:
        raise ValueError("address must be at least -1 (the empty word)")
    n, out, a = len(alphabet), [], address + 1
    while a > 0:
        a, r = divmod(a - 1, n)
        out.append(alphabet[r])
    return "".join(reversed(out))


def page_at(location: int, alphabet: str, length: int) -> str:
    """
    The fixed-length page at an ordered location: the ``length``-digit base-N numeral of the location.

    :param location: integer in ``[0, N**length)``
    :param alphabet: the ordered symbols (digit 0 is the first symbol)
    :param length: characters per page
    :returns: the page
    """
    n, out = len(alphabet), []
    for _ in range(length):
        location, r = divmod(location, n)
        out.append(alphabet[r])
    return "".join(reversed(out))


def location_of(page: str, alphabet: str) -> int:
    """
    Inverse of :func:`page_at`.

    :param page: a fixed-length page over ``alphabet``
    :param alphabet: the ordered symbols
    :returns: the ordered location
    :raises ValueError: if ``page`` contains a symbol outside ``alphabet``
    """
    n, loc = len(alphabet), 0
    for ch in page:
        i = alphabet.find(ch)
        if i < 0:
            raise ValueError(f"symbol {ch!r} is not in the alphabet")
        loc = loc * n + i
    return loc


# ── B. The recipe, generic ─────────────────────────────────────────────────


def xorshift_right(x: int, s: int) -> int:
    """
    The right xorshift ``x ^ (x >> s)``.

    :param x: non-negative integer
    :param s: shift, at least 1
    :returns: the transformed integer
    """
    return x ^ (x >> s)


def xorshift_right_inverse(y: int, s: int) -> int:
    """
    Exact inverse of :func:`xorshift_right` for any width: ``y ^ (y>>s) ^ (y>>2s) ^ …``.

    :param y: output of :func:`xorshift_right`
    :param s: the shift used
    :returns: the original integer
    """
    x, sh = y, s
    while (y >> sh):
        x ^= y >> sh
        sh += s
    return x


def xorshift_left_masked(x: int, mask_bits: int, s: int) -> int:
    """
    The masked left xorshift ``x ^ ((x mod 2^mask_bits) << s)``.

    :param x: non-negative integer
    :param mask_bits: number of low bits of ``x`` that are shifted
    :param s: shift, at least 1
    :returns: the transformed integer
    """
    return x ^ ((x & ((1 << mask_bits) - 1)) << s)


def xorshift_left_masked_inverse(y: int, mask_bits: int, s: int) -> int:
    """
    Exact inverse of :func:`xorshift_left_masked`: ``ceil(mask_bits / s)`` fixed-point iterations.

    Each iteration fixes ``s`` more low bits of the original, because bits
    ``[0, s)`` of ``y`` are unchanged by the shift.

    :param y: output of :func:`xorshift_left_masked`
    :param mask_bits: the mask width used
    :param s: the shift used
    :returns: the original integer
    """
    mask, q = (1 << mask_bits) - 1, y
    for _ in range(-(-mask_bits // s)):
        q = y ^ ((q & mask) << s)
    return q


def modular_inverse(a: int, m: int) -> int:
    """
    Inverse of ``a`` modulo ``m``.

    :param a: integer coprime to ``m``
    :param m: modulus, at least 2
    :returns: ``a**-1 mod m``
    :raises ValueError: if ``a`` and ``m`` are not coprime
    """
    try:
        return pow(a, -1, m)
    except ValueError:
        raise ValueError("a is not invertible modulo m") from None


def prime_power(n: int, primes=(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)) -> Optional[Tuple[int, int]]:
    """
    Whether ``n`` is a power of a small prime, and which.

    :param n: integer at least 2
    :param primes: the primes to try
    :returns: ``(p, k)`` with ``n == p**k``, or None
    """
    bits = int(n).bit_length()
    for p in primes:
        k = round((bits - 0.5) * math.log(2) / math.log(p))
        for kk in (k - 1, k, k + 1):
            if kk >= 1 and pow(p, kk) == n:
                return (p, kk)
    return None


def hull_dobell(m: int, a: int, c: int, prime_factors: List[int]) -> Dict[str, Any]:
    """
    The Hull–Dobell conditions for a full-period LCG ``x -> (a x + c) mod m``.

    They are the three conditions in Basile's README: ``gcd(m, c) = 1``;
    ``a - 1`` divisible by every prime factor of ``m``; ``a - 1`` divisible by
    4 when 4 divides ``m``. The prime factors are supplied by the caller.

    :param m: modulus
    :param a: multiplier
    :param c: increment
    :param prime_factors: distinct prime factors of ``m``
    :returns: dict with the three booleans and their conjunction ``full_period``
    """
    c1 = math.gcd(m, c) == 1
    c2 = all((a - 1) % p == 0 for p in prime_factors)
    c3 = (a - 1) % 4 == 0 if m % 4 == 0 else True
    return {"gcd_m_c_is_1": c1, "a_minus_1_divisible_by_prime_factors": c2,
            "a_minus_1_divisible_by_4_if_4_divides_m": c3, "full_period": c1 and c2 and c3}


def power_of_two_scrambler(n: int, a: int = 1664525, c: int = 1013904223,
                           s1: int = 7, s2: int = 5):
    """
    An invertible scrambler of ``[0, n)``: LCG modulo ``2^e``, two xorshifts, cycle-walked into range.

    ``e`` is the bit length of ``n - 1``. With ``a ≡ 1 (mod 4)`` and ``c`` odd
    the LCG is a full-period bijection on ``[0, 2^e)`` (Hull–Dobell for a power
    of two); each xorshift is a bijection; cycle-walking (repeat until the value
    is below ``n``) restricts the composition to a bijection on ``[0, n)``.

    :param n: size of the range, at least 2
    :param a: LCG multiplier, ≡ 1 (mod 4)
    :param c: LCG increment, odd
    :param s1: right-xorshift shift
    :param s2: masked left-xorshift shift
    :returns: the pair ``(scramble, unscramble)`` of functions on ``[0, n)``
    """
    e = max(1, (n - 1).bit_length())
    big_m = 1 << e
    mask = big_m - 1
    a_inv = pow(a, -1, big_m)

    def f(x):
        x = (a * x + c) & mask
        x ^= x >> s1
        x ^= (x << s2) & mask
        return x

    def finv(y):
        z = y
        for _ in range(e // s2 + 1):
            z = y ^ ((z << s2) & mask)
        y = z
        for _ in range(e // s1 + 1):
            z = y ^ (z >> s1)
        return (a_inv * (z - c)) & mask

    def scramble(x):
        x = f(x)
        while x >= n:
            x = f(x)
        return x

    def unscramble(y):
        y = finv(y)
        while y >= n:
            y = finv(y)
        return y

    return scramble, unscramble


def babel_page(location: int, length: int = 3, alphabet: str = BABEL_ALPHABET) -> str:
    """
    A page of the toy scrambled library: ``length`` characters over ``alphabet``, at ``location``.

    :param location: integer in ``[0, len(alphabet)**length)``
    :param length: characters per page
    :param alphabet: the symbols
    :returns: the page at that location (scrambled order)
    """
    scramble, _ = power_of_two_scrambler(len(alphabet) ** length)
    return page_at(scramble(location), alphabet, length)


def babel_location(page: str, alphabet: str = BABEL_ALPHABET) -> int:
    """
    Inverse of :func:`babel_page`: the location of a page, computed from the page.

    :param page: a page over ``alphabet``
    :param alphabet: the symbols
    :returns: the location in the toy scrambled library
    """
    _, unscramble = power_of_two_scrambler(len(alphabet) ** len(page))
    return unscramble(location_of(page, alphabet))


def permutation_cycles(f, n: int) -> List[int]:
    """
    Cycle lengths of a permutation of ``[0, n)``, longest first.

    A permutation of ``[0, n)`` written as an ``n x n`` permutation matrix has
    as its spectrum the roots of unity of every cycle length present, each
    cycle of length ``L`` contributing all ``L``-th roots of unity once. One
    cycle of length ``n`` is the "cyclic" case.

    :param f: a callable, a permutation of ``[0, n)``
    :param n: size of the range
    :returns: the cycle lengths in descending order
    """
    seen = [False] * n
    out = []
    for i in range(n):
        if not seen[i]:
            j, k = i, 0
            while not seen[j]:
                seen[j] = True
                j = f(j)
                k += 1
            out.append(k)
    return sorted(out, reverse=True)


# ── C. The published Babelia engine ────────────────────────────────────────

_CONST_RE = re.compile(r'static const boost::multiprecision::mpz_int (\w+)\("(\d+)"\);')
_RIGHT_RE = re.compile(r'\*pointer\s*\^=\s*\(\*pointer\s*>>\s*(\d+)\)\s*;')
_LEFT_RE = re.compile(r'\*pointer\s*\^=\s*\(\(\*pointer\s*%\s*(\w+)\)\s*<<\s*(\d+)\)\s*;')


def default_cache_dir() -> str:
    """
    Where the published files are looked for: ``$VALAQUENTA_BASILE_CACHE`` or ``~/.cache/valaquenta/basile``.

    :returns: the cache directory path
    """
    return os.environ.get("VALAQUENTA_BASILE_CACHE") or os.path.expanduser("~/.cache/valaquenta/basile")


def fetch_published(cache_dir: Optional[str] = None, timeout: int = 120) -> Dict[str, int]:
    """
    Download Basile's published files into a local cache. Network access; never called implicitly.

    The files are CC BY-SA-NC. They are kept in the cache only and are not part of this package.

    :param cache_dir: destination directory (default :func:`default_cache_dir`)
    :param timeout: per-file timeout in seconds
    :returns: ``{file name: bytes written}``
    """
    cache_dir = cache_dir or default_cache_dir()
    os.makedirs(cache_dir, exist_ok=True)
    sizes = {}
    for name, remote in PUBLISHED_FILES.items():
        with urllib.request.urlopen(_RAW + remote, timeout=timeout) as r:
            data = r.read()
        with open(os.path.join(cache_dir, name), "wb") as f:
            f.write(data)
        sizes[name] = len(data)
    return sizes


def parse_constants(source: str) -> Dict[str, int]:
    """
    Read the ``static const … mpz_int name("digits");`` constants out of a published C++ source text.

    :param source: text of ``PRNG`` or ``imagesearch.cpp``
    :returns: ``{name: integer}``
    """
    import sys
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    return {name: int(digits) for name, digits in _CONST_RE.findall(source)}


def parse_forward_steps(source: str) -> List[Tuple]:
    """
    Read the forward shift/XOR chain, in order, from the text of the ``PRNG`` file.

    :param source: text of ``PRNG``
    :returns: steps as ``('R', shift)`` or ``('L', mask_constant_name, shift)``
    """
    steps = []
    for line in source.splitlines():
        if "pointer" not in line or "^=" not in line:
            continue
        r = _RIGHT_RE.search(line)
        l = _LEFT_RE.search(line)
        if r:
            steps.append(("R", int(r.group(1))))
        elif l:
            steps.append(("L", l.group(1), int(l.group(2))))
    return steps


class Published:
    """
    Basile's Babelia engine, driven by the constants in his published files.

    :param cache_dir: directory holding ``PRNG`` and ``imagesearch.cpp`` (default :func:`default_cache_dir`)
    :raises FileNotFoundError: if the published files are not in the cache (see :func:`fetch_published`)
    """

    PIXELS_PER_QUARTER = 33280
    BITS_PER_PIXEL = 12
    QUARTERS = 8
    WIDTH, HEIGHT = 640, 416

    def __init__(self, cache_dir: Optional[str] = None):
        cache_dir = cache_dir or default_cache_dir()
        p, s = os.path.join(cache_dir, "PRNG"), os.path.join(cache_dir, "imagesearch.cpp")
        for path in (p, s):
            if not os.path.exists(path):
                raise FileNotFoundError(f"{path} not found; run fetch_published() first")
        prng, search = open(p).read(), open(s).read()
        self.constants = parse_constants(prng)
        self.constants["ainverse"] = parse_constants(search)["ainverse"]
        self.search_constants = parse_constants(search)
        self.steps = parse_forward_steps(prng)
        self._prng_text = prng
        self.m = _num(self.constants["m"])
        self.a = _num(self.constants["a"])
        self.c = _num(self.constants["c"])
        self.ainverse = _num(self.constants["ainverse"])
        self.divver = int(self.constants["divver"])
        self.chunk_bits = self.divver.bit_length() - 1        # divver is 2**chunk_bits (checked in audit())
        self.drawn_bits = self.PIXELS_PER_QUARTER * self.BITS_PER_PIXEL

    @staticmethod
    def _mod_pow2_or_general(x, k):
        """Return ``x mod k`` where ``k`` is a constant; a mask when ``k`` is a power of two."""
        return x & (k - 1) if k & (k - 1) == 0 else x % k

    def _apply_left(self, p, name, s):
        k = _num(self.constants[name])
        return p ^ (self._mod_pow2_or_general(p, k) << s)

    def forward(self, location: int) -> int:
        """
        The forward transform: LCG then the published shift/XOR chain (the ``pointer`` of ``PRNG``).

        :param location: integer in ``[0, m)``
        :returns: the transformed integer whose bits are drawn as the image
        """
        p = (self.a * _num(location) + self.c) % self.m
        for st in self.steps:
            p = p ^ (p >> st[1]) if st[0] == "R" else self._apply_left(p, st[1], st[2])
        return p

    def inverse(self, value: int) -> int:
        """
        The inverse, as ``imagesearch.cpp`` applies it: undo the chain in reverse, then ``a⁻¹ (p - c) mod m``.

        :param value: an integer produced by :meth:`forward`
        :returns: the location
        """
        p = _num(value)
        for st in reversed(self.steps):
            if st[0] == "R":
                x, sh = p, st[1]
                y = p
                while (y >> sh):
                    x ^= y >> sh
                    sh += st[1]
                p = x
            else:
                k = _num(self.constants[st[1]])
                bits = int(k).bit_length() - 1 if int(k) & (int(k) - 1) == 0 else int(k).bit_length()
                q, y, s = p, p, st[2]
                for _ in range(-(-bits // s)):
                    q = y ^ (self._mod_pow2_or_general(q, k) << s)
                p = q
        return int((self.ainverse * (p - self.c)) % self.m)

    def chunks(self, value: int) -> List[int]:
        """
        The eight 399,360-bit pixel words that :meth:`forward`'s output yields (bit 399,360 of each 399,361-bit chunk is never drawn).

        :param value: an integer produced by :meth:`forward`
        :returns: eight integers, one per quarter of the image
        """
        v = int(value)
        step, keep = self.chunk_bits, (1 << self.drawn_bits) - 1
        return [(v >> (step * i)) & keep for i in range(self.QUARTERS)]

    def pixels(self, value: int) -> List[List[int]]:
        """
        The 12-bit colour codes of each quarter, first pixel first (``#RGB`` = red·256 + green·16 + blue).

        :param value: an integer produced by :meth:`forward`
        :returns: eight lists of 33,280 codes in ``[0, 4096)``
        """
        out = []
        for w in self.chunks(value):
            bits = format(w, "0%db" % self.drawn_bits)[::-1]
            out.append([int(bits[k:k + 12][::-1], 2) for k in range(0, self.drawn_bits, 12)])
        return out

    def value_from_pixels(self, quarters: List[List[int]]) -> int:
        """
        Build the integer that :meth:`inverse` receives from eight lists of 12-bit codes (undrawn bits zero), as ``imagesearch.cpp`` does.

        :param quarters: eight lists of 33,280 codes in ``[0, 4096)``
        :returns: the integer
        """
        total = 0
        for i, q in enumerate(quarters):
            w = 0
            for j, code in enumerate(q):
                w |= code << (12 * j)
            total |= w << (self.chunk_bits * i)
        return total

    def search(self, quarters: List[List[int]]) -> int:
        """
        Location of an image given as eight quarters of 12-bit codes: the inverse applied to the drawn bits.

        :param quarters: eight lists of 33,280 codes in ``[0, 4096)``
        :returns: a location whose image is exactly ``quarters``
        """
        return self.inverse(self.value_from_pixels(quarters))

    def unread_positions(self) -> List[int]:
        """
        Bit positions of :meth:`forward`'s output that the image never reads.

        One per quarter (the 399,361st bit of each chunk) and every bit above the eighth chunk.

        :returns: the sorted list of positions
        """
        dropped = [self.chunk_bits * i + self.drawn_bits for i in range(self.QUARTERS)]
        top = list(range(self.chunk_bits * self.QUARTERS, int(self.m).bit_length()))
        return sorted(dropped + top)

    def sibling(self, location: int, position: int) -> Dict[str, Any]:
        """
        A second location showing the same image: flip one unread bit of the transformed value and invert.

        :param location: a location
        :param position: an unread bit position (see :meth:`unread_positions`)
        :returns: dict with the sibling location, whether ``forward(sibling)`` is the flipped value, whether the images match, and whether it differs from ``location``
        """
        p = self.forward(location)
        p2 = p ^ (_num(1) << position)
        loc2 = self.inverse(p2)
        return {"sibling_differs": loc2 != location,
                "forward_matches": self.forward(loc2) == p2,
                "same_image": self.chunks(p2) == self.chunks(p),
                "sibling_digest": hashlib.sha256(str(loc2).encode()).hexdigest()[:16]}

    def sibling_offsets(self, location: int, pairs: int = 6, seed: int = 0) -> Dict[str, Any]:
        """
        The offsets (mod m) from a location to its siblings, and whether they add.

        For each valid unread bit ``b`` the offset is ``inverse(forward(L) ^ 2^b) - L (mod m)``.
        Checked: the single offsets are distinct; ``pairs`` random pairs of bits
        give the sum of their two offsets; all valid bits flipped together give
        the sum of all offsets. Additivity makes the fibre of an image
        ``{L + sum of a subset of the offsets}``, a 2^k-point box in Z_m whose
        generators depend on ``L``.

        :param location: a location
        :param pairs: number of random bit pairs to test for additivity
        :param seed: seed for choosing the pairs
        :returns: dict with the valid bit count, distinctness, pair and total additivity, and bit lengths of the offsets
        """
        import random as _r
        m = int(self.m)
        p = self.forward(location)
        bits = [b for b in self.unread_positions()
                if self.forward(self.inverse(p ^ (_num(1) << b))) == p ^ (_num(1) << b)]
        off = lambda S: (int(self.inverse(p ^ sum((_num(1) << b for b in S), _num(0)))) - int(location)) % m
        single = {b: off([b]) for b in bits}
        rnd = _r.Random(seed)
        chosen = [tuple(rnd.sample(bits, 2)) for _ in range(pairs)]
        pairs_ok = all(off(list(pr)) == (single[pr[0]] + single[pr[1]]) % m for pr in chosen)
        total_ok = off(bits) == sum(single.values()) % m
        signed = lambda o: o if o < m // 2 else o - m
        return {"valid_unread_bits": len(bits), "single_offsets_distinct": len(set(single.values())) == len(bits),
                "pairs_tested": pairs, "pairs_additive": pairs_ok, "all_bits_together_additive": total_ok,
                "offset_bit_lengths": sorted(abs(signed(o)).bit_length() for o in single.values()),
                "fibre_size_if_all_combinations_valid": 2 ** len(bits)}

    def mean_locations_per_image(self) -> Dict[str, Any]:
        """
        Average number of locations per image: ``m / 2^(image bits)``.

        :returns: dict with the image bit count, the bit length of ``m``, and the ratio as ``mantissa * 2**exponent``
        """
        image_bits = self.QUARTERS * self.drawn_bits
        ratio = int(self.m >> (image_bits - 64)) / float(1 << 64)      # m / 2^image_bits as a float
        return {"image_bits": image_bits, "m_bits": int(self.m).bit_length(),
                "mean_locations_per_image": ratio}

    def audit(self) -> Dict[str, Any]:
        """
        Checks on the published constants: sizes, the modular inverse, the masks, the palette, consistency between the two programs.

        :returns: dict of measured facts and boolean checks
        """
        c, s = self.constants, self.search_constants
        bl = lambda x: int(x).bit_length()
        pow2 = lambda x: int(x) & (int(x) - 1) == 0
        palette = re.findall(r'"#([0-9A-F]{3})"', self._prng_text)
        pp = prime_power(int(self.m))
        return {
            "bit_lengths": {k: bl(v) for k, v in c.items()},
            "shared_constants_identical": {k: c[k] == s[k] for k in ("m", "c", "maskone", "masktwo") if k in s},
            "a_times_ainverse_mod_m_is_1": (self.a * self.ainverse) % self.m == 1,
            "gcd_a_m_is_1": math.gcd(int(self.a), int(self.m)) == 1,
            "gcd_c_m_is_1": math.gcd(int(self.c), int(self.m)) == 1,
            "m_mod_4": int(self.m % 4), "a_mod_4": int(self.a % 4),
            "m_prime_power": pp,
            "hull_dobell": (hull_dobell(int(self.m), int(self.a), int(self.c), [pp[0]]) if pp else None),
            "a_over_m_bits": bl(self.a) - bl(self.m),
            "maskone_is_power_of_two": pow2(c["maskone"]), "masktwo_is_power_of_two": pow2(c["masktwo"]),
            "divver_is_power_of_two": pow2(self.divver),
            "chunk_bits": self.chunk_bits, "drawn_bits_per_chunk": self.drawn_bits,
            "image_bits": self.QUARTERS * self.drawn_bits, "m_bits": bl(self.m),
            "forward_steps": self.steps,
            "palette_entries": len(palette),
            "palette_is_hex_of_index": palette == ["%03X" % i for i in range(4096)],
            "unread_bit_positions": len(self.unread_positions()),
        }


# ── D. The smaller published pieces ────────────────────────────────────────

EUCLID_QARRAY_SIZE = 25


def euclid_steps(a: int, m: int) -> int:
    """
    Number of division steps of the Euclidean algorithm on ``(m, a)``, as the published loop counts them.

    :param a: the divisor
    :param m: the dividend
    :returns: the number of iterations of ``while (m % a > 0)``
    """
    n = 0
    while m % a > 0:
        m, a = a, m % a
        n += 1
    return n


def euclid_inverse_qarray(a: int, m: int, qmax: int = EUCLID_QARRAY_SIZE) -> int:
    """
    The published ``lcgreverse.cpp`` extended Euclid, ported with its fixed-size ``qarray``.

    The C++ keeps the running coefficients in ``mpz_int qarray[25]`` and writes
    ``qarray[i]`` for ``i = 2, 3, …``; more than 23 divisions write past the
    array. Here that case raises instead of running off the end.

    :param a: multiplier to invert
    :param m: modulus
    :param qmax: the array size (25 in the published file)
    :returns: ``a**-1 mod m``
    :raises OverflowError: if the division count exceeds the array
    """
    reset = m
    q = [0, 1]
    i = 2
    while m % a > 0:
        if i >= qmax:
            raise OverflowError(f"qarray[{qmax}] exceeded after {i - 2} divisions")
        rem, quo = m % a, m // a
        q.append(q[i - 2] - q[i - 1] * quo)
        m, a = a, rem
        i += 1
    last = q[i - 1]
    return last + reset if last < 0 else last


def parse_babel_address(address: str) -> Dict[str, Any]:
    """
    Split a site address ``<hexagon>-w<wall>-s<shelf>-v<volume>[:<page>]`` into its fields.

    The structure is the site's (Reference Hex page): 4 walls, 5 shelves per wall, 32 volumes per shelf, 410 pages per volume.

    :param address: e.g. ``jeb0110jlb-w2-s4-v16:19``
    :returns: dict with hexagon, wall, shelf, volume, page (or None) and the 0-based volume index within the hexagon (0…639)
    :raises ValueError: if the text is not an address or a field is out of range
    """
    m = re.fullmatch(r"([0-9a-z]+)-w(\d+)-s(\d+)-v(\d+)(?::(\d+))?", address)
    if not m:
        raise ValueError(f"not a Library of Babel address: {address!r}")
    hexname, wall, shelf, vol = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
    page = int(m.group(5)) if m.group(5) else None
    if not (1 <= wall <= WALLS_PER_HEXAGON and 1 <= shelf <= SHELVES_PER_WALL
            and 1 <= vol <= BOOKS_PER_SHELF and (page is None or 1 <= page <= PAGES_PER_BOOK)):
        raise ValueError(f"field out of range in {address!r}")
    volume_index = ((wall - 1) * SHELVES_PER_WALL + (shelf - 1)) * BOOKS_PER_SHELF + (vol - 1)
    return {"hexagon": hexname, "wall": wall, "shelf": shelf, "volume": vol, "page": page,
            "volume_index": volume_index}


def resource_locator_request(page_text: str) -> Dict[str, Any]:
    """
    The request the LobThis extension posts to the site's resource locator, built and not sent.

    The extension submits the current page's HTML as the ``extension`` field of
    a POST form to ``resourcelocator.cgi``. This function returns that request
    as data; it performs no network access.

    :param page_text: the text the extension would submit
    :returns: dict with method, url and form fields
    """
    return {"method": "POST", "url": RESOURCE_LOCATOR_URL, "fields": {"extension": page_text}}


def library_scale(alphabet_size: int = 29, page_chars: int = PAGE_CHARS,
                  pages_per_book: int = PAGES_PER_BOOK) -> Dict[str, float]:
    """
    The size of the text library in orders of magnitude (log10), computed.

    :param alphabet_size: symbols (29)
    :param page_chars: characters per page (3,200)
    :param pages_per_book: pages per volume (410)
    :returns: dict with log10 of the number of pages, of books, and of all 1,312,000-character books
    """
    lp = page_chars * math.log10(alphabet_size)
    return {"log10_pages": lp, "log10_books": lp - math.log10(pages_per_book),
            "log10_full_books": page_chars * pages_per_book * math.log10(alphabet_size)}
