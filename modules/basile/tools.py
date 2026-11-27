"""
ValaQuenta.modules.basile.tools
===============================
Basile engines — Module Tools.

Implements the EquationModule registry contract: formulary, run(), viewer_data(), shell_commands().

Equations::

   1. ordered_address       rank of a string among all strings (bijective base-N)
   2. ordered_text_at       inverse
   3. scramble              invertible scrambler of [0, N) (LCG + xorshift + cycle-walk)
   4. toy_library           the toy Library of Babel page at a location, both orders
   5. scrambler_exhaustive  every location of the toy library, checked
   6. neighbour_statistics  how far neighbouring locations are apart in content
   7. hull_dobell_check     the three Hull–Dobell conditions
   8. xorshift_inverse_check exact inverses of the two xorshift steps
   9. euclid_qarray_limit   the published Extended Euclid file's 25-entry array
  10. address_parse         <hexagon>-w-s-v[:page] address fields
  11. lobthis_request       the LobThis extension's request, as data
  12. library_scale         orders of magnitude of the text library
  13. published_audit       the published Babelia constants, audited
  14. published_roundtrip   forward and inverse on the published constants
  15. published_multiplicity  locations that share one image
  16. scrambler_cycles      cycle structure of the scrambler (the spectrum of its permutation)
  17. published_sibling_structure  offsets between sibling locations: additive, location-dependent

Version: 1.3
"""

import random
import time
from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation
from . import maths as M


def _ordered_address(text="hello", alphabet="abcdefghijklmnopqrstuvwxyz"):
    a = M.ordered_address(text, alphabet)
    return {"text": text, "address": a, "round_trip": M.ordered_text_at(a, alphabet) == text}


def _ordered_text_at(address=702, alphabet="abcdefghijklmnopqrstuvwxyz"):
    t = M.ordered_text_at(address, alphabet)
    return {"address": address, "text": t, "round_trip": M.ordered_address(t, alphabet) == address}


def _scramble(n=24389, location=12345):
    sc, un = M.power_of_two_scrambler(n)
    y = sc(location)
    return {"n": n, "location": location, "scrambled": y, "inverse_ok": un(y) == location}


def _toy_library(location=0, length=3):
    n = len(M.BABEL_ALPHABET) ** length
    scrambled = M.babel_page(location, length)
    ordered = M.page_at(location, M.BABEL_ALPHABET, length)
    return {"location": location, "pages": n, "scrambled_page": scrambled, "ordered_page": ordered,
            "location_of_scrambled_page": M.babel_location(scrambled)}


def _scrambler_exhaustive(n=24389):
    sc, un = M.power_of_two_scrambler(n)
    seen = set()
    for x in range(n):
        y = sc(x)
        assert 0 <= y < n and un(y) == x
        seen.add(y)
    return {"n": n, "distinct_values": len(seen), "bijection": len(seen) == n, "all_round_trip": True}


def _neighbour_statistics(length=3):
    alpha = M.BABEL_ALPHABET
    n = len(alpha) ** length
    sc, _ = M.power_of_two_scrambler(n)
    pages_o = [M.page_at(i, alpha, length) for i in range(n)]
    pages_s = [M.page_at(sc(i), alpha, length) for i in range(n)]
    d = lambda a, b: sum(x != y for x, y in zip(a, b))
    ordered = sum(d(pages_o[i], pages_o[i + 1]) for i in range(n - 1)) / (n - 1)
    scrambled = sum(d(pages_s[i], pages_s[i + 1]) for i in range(n - 1)) / (n - 1)
    k = len(alpha)
    return {"pages": n, "ordered_mean_chars_differing": ordered, "scrambled_mean_chars_differing": scrambled,
            "independent_pages_expected": length * (k - 1) / k}


def _hull_dobell_check(m=1 << 15, a=1664525, c=1013904223, prime_factors=(2,)):
    return M.hull_dobell(m, a, c, list(prime_factors))


def _xorshift_inverse_check(width=64, s=7, samples=2000):
    rnd = random.Random(1)
    ok_r = ok_l = True
    for _ in range(samples):
        x = rnd.getrandbits(width)
        ok_r &= M.xorshift_right_inverse(M.xorshift_right(x, s), s) == x
        k = max(1, width - s)
        ok_l &= M.xorshift_left_masked_inverse(M.xorshift_left_masked(x, k, s), k, s) == x
    return {"width": width, "shift": s, "samples": samples, "right_inverse_exact": ok_r,
            "left_masked_inverse_exact": ok_l}


def _euclid_qarray_limit(bits=64, trials=200):
    rnd = random.Random(2)
    over = 0
    steps: List[int] = []
    for _ in range(trials):
        m = rnd.getrandbits(bits) | (1 << (bits - 1)) | 1
        a = rnd.getrandbits(bits - 1) | 1
        steps.append(M.euclid_steps(a, m))
        try:
            M.euclid_inverse_qarray(a, m)
        except OverflowError:
            over += 1
    return {"bits": bits, "trials": trials, "overflow_count": over,
            "mean_divisions": sum(steps) / trials, "array_allows_divisions": M.EUCLID_QARRAY_SIZE - 2}


def _address_parse(address="jeb0110jlb-w2-s4-v16:19"):
    return M.parse_babel_address(address)


def _lobthis_request(page_text="text of the page in the browser"):
    return M.resource_locator_request(page_text)


def _library_scale():
    return M.library_scale()


def _published_audit(cache_dir=None):
    return M.Published(cache_dir).audit()


def _published_roundtrip(seed=1, cache_dir=None):
    pub = M.Published(cache_dir)
    rnd = random.Random(seed)
    loc = rnd.getrandbits(int(pub.m).bit_length() - 2) % int(pub.m)
    t0 = time.perf_counter()
    p = pub.forward(loc)
    t1 = time.perf_counter()
    back = pub.inverse(p)
    t2 = time.perf_counter()
    return {"location_bits": loc.bit_length(), "value_bits": int(p).bit_length(),
            "inverse_of_forward_is_identity": back == loc,
            "forward_seconds": t1 - t0, "inverse_seconds": t2 - t1}


def _published_multiplicity(seed=1, cache_dir=None):
    pub = M.Published(cache_dir)
    rnd = random.Random(seed)
    loc = rnd.getrandbits(int(pub.m).bit_length() - 2) % int(pub.m)
    unread = pub.unread_positions()
    sample = [unread[0], unread[len(unread) // 2], unread[-1]]
    witnesses = {pos: pub.sibling(loc, pos) for pos in sample}
    return {"unread_bit_positions": len(unread), "sampled_positions": sample,
            "witnesses": witnesses, **pub.mean_locations_per_image()}


def _scrambler_cycles(n=24389):
    sc, _ = M.power_of_two_scrambler(n)
    c = M.permutation_cycles(sc, n)
    e = max(1, (n - 1).bit_length())
    big = 1 << e
    lcg = M.permutation_cycles(lambda x: (1664525 * x + 1013904223) % big, big)
    return {"n": n, "cycles": len(c), "longest": c[0], "shortest": c[-1], "fixed_points": c.count(1),
            "top_cycle_lengths": c[:8], "single_cycle": len(c) == 1,
            "lcg_alone_cycles": len(lcg), "lcg_alone_longest": lcg[0], "lcg_modulus": big}


def _published_sibling_structure(seed=1, cache_dir=None, pairs=6):
    pub = M.Published(cache_dir)
    rnd = random.Random(seed)
    loc = rnd.getrandbits(int(pub.m).bit_length() - 2) % int(pub.m)
    other = rnd.getrandbits(int(pub.m).bit_length() - 2) % int(pub.m)
    a = pub.sibling_offsets(loc, pairs=pairs, seed=seed)
    b = pub.sibling_offsets(other, pairs=pairs, seed=seed)
    pos = pub.unread_positions()[0]
    same = [((pub.inverse(pub.forward(L) ^ (1 << pos)) - L) % int(pub.m)) for L in (loc, other)]
    return {"first_location": a, "second_location": b,
            "same_bit_same_offset_at_two_locations": same[0] == same[1]}


class BasileModule(EquationModule):
    """
    Basile engines: the invertible location ↔ content maps of the Library of Babel family.

    Registry module for ``basile``: :meth:`formulary` lists the equations,
    :meth:`run` executes one, and :meth:`viewer_data` formats a result for a
    viewer. The mathematics lives in :mod:`ValaQuenta.modules.basile.maths`.
    """

    @property
    def name(self):
        return 'basile'

    @property
    def display_name(self):
        return 'Basile: Invertible Location Maps (Library of Babel / Babelia)'

    @property
    def version(self):
        return '1.3'

    @property
    def description(self):
        return (
            'The invertible location-to-content maps of J. Basile\'s Library of Babel family. '
            'A location is a number and a page (or image) is computed from it, and back, with nothing stored: '
            'a linear congruential generator followed by shift/XOR steps, inverted with the modular inverse and '
            'the shifts undone in reverse. Provides the ordered (rank) address as the contrast case, a generic '
            'scrambler written from the recipe and checked exhaustively on a toy library, and the published '
            'Babelia engine run on its published constants (read from a local copy, never vendored): the two '
            'programs share their constants, a times a-inverse is 1 modulo m, the masks are powers of two, and the '
            'image reads fewer bits than the location space holds, so several locations show one image. '
            'Also the published Extended Euclid file with its fixed 25-entry array and the request the LobThis '
            'extension posts to the site. The text library\'s own algorithm is not published and is not reproduced.'
        )

    @property
    def confidence_floor(self):
        return 'ESTABLISHED'

    def formulary(self) -> List[Equation]:
        return [
            Equation(name='ordered_address',
                     display='Ordered address: rank of a string among all strings over an alphabet',
                     latex=r'a(w) = \sum_{i} (d_i)\,N^{|w|-1-i} - 1,\quad d_i \in \{1..N\}',
                     radian_form='shortlex rank; bijective base-N with digits 1..N',
                     confidence='ESTABLISHED', code_verified=True, params=['text', 'alphabet'],
                     compute=_ordered_address, display_options=['text'],
                     process='Given a string and an alphabet, computes its rank among all strings by repeated multiply-and-add over digit values 1..N.'),
            Equation(name='ordered_text_at',
                     display='Ordered address, inverse: the string at a rank',
                     latex=r'w = a^{-1}(n)',
                     radian_form='repeated division of n+1 with digits shifted by one',
                     confidence='ESTABLISHED', code_verified=True, params=['address', 'alphabet'],
                     compute=_ordered_text_at, display_options=['text'],
                     process='Given a rank and an alphabet, recovers the string by repeated division.'),
            Equation(name='scramble',
                     display='Invertible scrambler of [0, N): LCG mod 2^e + xorshifts + cycle-walk',
                     latex=r'x \mapsto \mathrm{xs}_L(\mathrm{xs}_R(a x + c \bmod 2^e))\ \text{(repeat until } <N)',
                     radian_form='bijection on [0, N) built from bijections on [0, 2^e)',
                     confidence='ESTABLISHED', code_verified=True, params=['n', 'location'],
                     compute=_scramble, display_options=['text'],
                     process='Given a range size and a location, applies an LCG and two xorshifts modulo a power of two and repeats until the value is in range.'),
            Equation(name='toy_library',
                     display='Toy Library of Babel: the page at a location, scrambled and ordered',
                     latex=r'p = \mathrm{page}(\mathrm{scramble}(\ell)),\quad p_0 = \mathrm{page}(\ell)',
                     radian_form='29 symbols, 3-character pages, 24,389 pages',
                     confidence='ESTABLISHED', code_verified=True, params=['location', 'length'],
                     compute=_toy_library, display_options=['text'],
                     process='Given a location, computes the page at that location in the scrambled library and in the ordered library, and the location of the scrambled page.'),
            Equation(name='scrambler_exhaustive',
                     display='Every location of the toy library round-trips; the map is a bijection',
                     latex=r'|\{\mathrm{scramble}(x)\}| = N \wedge \mathrm{unscramble}\circ\mathrm{scramble} = \mathrm{id}',
                     radian_form='exhaustive over [0, N), not sampled',
                     confidence='ESTABLISHED', code_verified=True, params=['n'],
                     compute=_scrambler_exhaustive, display_options=['text'],
                     process='Given a range size, checks the scrambler on every location: distinct outputs and exact inverse.'),
            Equation(name='neighbour_statistics',
                     display='Neighbouring locations: how many characters differ, ordered vs scrambled',
                     latex=r'\mathbb{E}\,d(p_\ell, p_{\ell+1})',
                     radian_form='ordered ~1.04 of 3; scrambled ~2.91 of 3 (independent pages 2.90)',
                     confidence='ESTABLISHED', code_verified=True, params=['length'],
                     compute=_neighbour_statistics, display_options=['text'],
                     process='Given a page length, averages the number of differing characters between the pages at consecutive locations in both libraries.'),
            Equation(name='hull_dobell_check',
                     display='Hull–Dobell conditions for a full-period LCG',
                     latex=r'\gcd(m,c)=1,\ \ p\mid m\Rightarrow p\mid a-1,\ \ 4\mid m\Rightarrow 4\mid a-1',
                     radian_form='three integer conditions on (m, a, c)',
                     confidence='ESTABLISHED', code_verified=True, params=['m', 'a', 'c', 'prime_factors'],
                     compute=_hull_dobell_check, display_options=['text'],
                     process='Given m, a, c and the prime factors of m, evaluates the three Hull–Dobell conditions.'),
            Equation(name='xorshift_inverse_check',
                     display='Exact inverses of the right xorshift and the masked left xorshift',
                     latex=r'y \oplus (y\gg s)\oplus (y\gg 2s)\cdots,\quad \lceil k/s\rceil\ \text{fixed-point steps}',
                     radian_form='both steps are bijections; inverses checked on random words',
                     confidence='ESTABLISHED', code_verified=True, params=['width', 's', 'samples'],
                     compute=_xorshift_inverse_check, display_options=['text'],
                     process='Given a word width and a shift, applies each xorshift and its inverse to random words and checks equality.'),
            Equation(name='euclid_qarray_limit',
                     display='Published Extended Euclid: the fixed 25-entry array vs random 64-bit inputs',
                     latex=r'\#\text{divisions} \approx 0.843\,\ln a \gg 23',
                     radian_form='array holds 23 divisions; random 64-bit inputs need about 37',
                     confidence='ESTABLISHED', code_verified=True, params=['bits', 'trials'],
                     compute=_euclid_qarray_limit, display_options=['text'],
                     process='Given an operand size, runs the ported Extended Euclid with its 25-entry array on random operands and counts overflows.'),
            Equation(name='address_parse',
                     display='Site address fields: hexagon, wall, shelf, volume, page',
                     latex=r'v = ((w-1)\cdot 5 + (s-1))\cdot 32 + (v_0 - 1)',
                     radian_form='4 walls x 5 shelves x 32 volumes = 640 volumes per hexagon; 410 pages each',
                     confidence='ESTABLISHED', code_verified=True, params=['address'],
                     compute=_address_parse, display_options=['text'],
                     process='Given a site address, splits it into fields and computes the volume index within the hexagon.'),
            Equation(name='lobthis_request',
                     display='The LobThis extension request, built as data and not sent',
                     latex=r'\text{POST } \texttt{resourcelocator.cgi},\ \text{field extension}',
                     radian_form='one form field; no network access performed',
                     confidence='ESTABLISHED', code_verified=True, params=['page_text'],
                     compute=_lobthis_request, display_options=['text'],
                     process='Given text, returns the POST request that the LobThis extension submits to the site, without sending it.'),
            Equation(name='library_scale',
                     display='Scale of the text library, recomputed',
                     latex=r'29^{3200} \approx 10^{4679.67}\ \text{pages};\ /410 \approx 10^{4677.06}\ \text{books}',
                     radian_form='log10 of pages, books, full 1,312,000-character books',
                     confidence='ESTABLISHED', code_verified=True, params=[],
                     compute=_library_scale, display_options=['text'],
                     process='Computes the number of pages and books of the text library in orders of magnitude.'),
            Equation(name='published_audit',
                     display='Published Babelia constants: sizes, a·a⁻¹ ≡ 1, masks, palette, shared constants',
                     latex=r'a\,a^{-1} \equiv 1 \pmod m',
                     radian_form='reads the published files from a local copy; needs fetch_published() once',
                     confidence='ESTABLISHED', code_verified=True, params=['cache_dir'],
                     compute=_published_audit, display_options=['text'],
                     process='Given the directory holding the published files, parses their constants and checks their internal consistency.'),
            Equation(name='published_roundtrip',
                     display='Published forward and inverse transforms on the published constants',
                     latex=r'\mathrm{inverse}(\mathrm{forward}(\ell)) = \ell',
                     radian_form='3.19-million-bit integers; exact inverse',
                     confidence='ESTABLISHED', code_verified=True, params=['seed', 'cache_dir'],
                     compute=_published_roundtrip, display_options=['text'],
                     process='Given a seed, applies the published forward transform to a random location and the published inverse to the result.'),
            Equation(name='published_multiplicity',
                     display='Several locations show one image: bits of the transform the image never reads',
                     latex=r'\bar n = m / 2^{3\,194\,880} \approx 2^{17}',
                     radian_form='8 undrawn bits (one per chunk) + the bits above the eighth chunk',
                     confidence='ESTABLISHED', code_verified=True, params=['seed', 'cache_dir'],
                     compute=_published_multiplicity, display_options=['text'],
                     process='Given a seed, flips bits of the transformed value that the image does not draw, inverts, and checks that a different location gives the same image.'),
            Equation(name='scrambler_cycles',
                     display='Cycle structure of the scrambler: the spectrum of its permutation',
                     latex=r'\mathrm{spec}(P_\pi) = \bigcup_{\text{cycles }L}\{e^{2\pi i k/L}\}',
                     radian_form='one cycle of length N would be cyclic; the pure LCG mod 2^e is one full cycle (Hull-Dobell), the scrambler is not',
                     confidence='ESTABLISHED', code_verified=True, params=['n'],
                     compute=_scrambler_cycles, display_options=['text'],
                     process='Given a range size, follows every cycle of the scrambler and of its LCG part and reports the cycle lengths.'),
            Equation(name='published_sibling_structure',
                     display='Sibling locations of one image: offsets add, and depend on the location',
                     latex=r'F = \{L + \textstyle\sum_{b\in S} o_b(L) \bmod m : S\subseteq B\}',
                     radian_form='additive within a location (a box in Z_m), not a fixed coset across locations',
                     confidence='ESTABLISHED', code_verified=True, params=['seed', 'cache_dir', 'pairs'],
                     compute=_published_sibling_structure, display_options=['text'],
                     process='Given a seed, computes the offsets to sibling locations at two locations and checks that they add within a location and differ between locations.'),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not found in {self.name} module")
        result = eq.compute(**params) if params else eq.compute()
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str, params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        return {'text': self._format_text(self.run(equation_name, params))}

    def _format_text(self, result: Dict) -> str:
        eq, r = result['equation'], result['result']
        body = '\n'.join(f"      {k:<34} {v}" for k, v in r.items() if not isinstance(v, (list, dict))) \
            if isinstance(r, dict) else str(r)
        return (f"  {eq.display}\n  Status: {eq.confidence}  |  Code-verified: {eq.code_verified}\n"
                f"  Radian form: {eq.radian_form}\n  Result:\n{body}")

    def shell_commands(self) -> Dict[str, Any]:
        return {
            'babel':   lambda location=0, length=3: _toy_library(location, length),
            'ordered': lambda text='hello': _ordered_address(text),
            'scale':   _library_scale,
        }
