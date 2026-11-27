# Engine: Basile — Invertible Location Maps (Library of Babel / Babelia)

**Module:** `modules/basile/` (`maths.py`, `tools.py`)
**Class:** `BasileModule` · **Version:** 1.3 (the empty word is at address −1)
**Claim:** the Library of Babel family joins a location (a number) to a page or image by an invertible pseudo-random map, so nothing is stored. The published recipe (an LCG, then shift/XOR steps, inverted by the modular inverse and the shifts undone in reverse) is exact and invertible; run on Basile's published constants it also shows that the image reads fewer bits than the location space holds, so an image is shown at about 7×10⁴ locations on average.
**Status:** `ESTABLISHED` (each result below is computed by the code, exhaustively where the range allows).

---

## What is published, and what is not

Checked 2026-09-30.

| Repository (`librarianofbabel/…`) | Contents | Licence | Used here |
|---|---|---|---|
| `libraryofbabel.info-algo` | `PRNG` (= `babelia.cpp`: location → image), `imagesearch.cpp` (image → location), `Euclid's Extended` (`lcgreverse.cpp`), README with the recipe | CC BY-SA-NC, "No liability", uploaded 2019-01-02 | yes: recipe implemented generically; the two programs run on their constants read from a local copy |
| `LoB-API` | a `LICENSE` file only, no code | CC0-1.0 | nothing to use |
| `LobThis`, `LoBThis-Firefox` | browser extension, 5 small JavaScript/JSON files; fork of `rik-degraaff/LobThis` | not stated | its one request is reproduced as data and never sent |
| `newsometimesatdawn`, `Dezmediah-site` | web sites | — | no |

The **text library's own algorithm is not published**: the README says the published one is "significantly more efficient than the one I wrote for libraryofbabel.info". Nothing in this module reproduces the site's page contents.

**Licence handling.** ValaQuenta is GPL-3.0-only; the published files are CC BY-SA-NC. The package contains none of their text or constants. `fetch_published()` downloads them into `$VALAQUENTA_BASILE_CACHE` (default `~/.cache/valaquenta/basile`); `Published` parses the constants from that copy at run time.

## Results (run)

**The generic recipe, on a toy library** (29 symbols, 3-character pages, N = 24,389):

```
scrambler is a bijection on [0, N): True   every location round-trips: True     (exhaustive)
neighbouring pages differ in:  ordered 1.036 of 3 characters | scrambled 2.910 (independent pages 2.897)
```

**The published constants** (`Published(cache).audit()`):

```
bit lengths            m 3,194,897 | a 1,597,519 | c 1,628,205 | ainverse 3,194,897 | maskone 2,496,010 | masktwo 1,697,290 | divver 399,362
shared constants       m, c, maskone, masktwo identical in PRNG and imagesearch.cpp
a * ainverse mod m     == 1     gcd(a, m) = gcd(c, m) = 1     m mod 4 = 3     a mod 4 = 3
m                      = 3^2,015,755 exactly (a prime power)  ->  Hull-Dobell: gcd(c,m)=1, 3 | a-1  =>  the LCG alone is ONE cycle of length m
masks                  maskone, masktwo, divver are exact powers of two (bit masks); divver = 2^399361
palette                4,096 entries, exactly "#%03X" of the index
image                  640*416*12 = 3,194,880 bits; 8 chunks of 399,361 bits, 399,360 drawn
forward chain          R 1098239, L(maskone) 698879, L(masktwo) 1497599, R 1797118
```

**Forward and inverse** on a random location: `inverse(forward(loc)) == loc` (0.04 s and 0.05 s with gmpy2; 7.7 s and 15.2 s in plain Python, identical digest).

**Several locations, one image.** The location space `m` has 3,194,897 bits, the image 3,194,880. Seventeen bit positions of the transformed value are never read by the image: the 399,361st bit of each chunk (8) and the bits above the eighth chunk (9). For 16 of the 17, flipping the bit and inverting gives a different location whose image is identical; the highest gives a value no location produces. Mean locations per image is `m / 2^3,194,880` = 69,544 (2¹⁶ × 1.06). `search(image)` returns one of them, not necessarily the one the image was drawn from.

**Cyclic structure** (`scrambler_cycles`, `published_sibling_structure`, `Published.sibling_offsets`):

```
pure LCG mod 2^15 (Hull-Dobell)    1 cycle of 32,768
xorshift part alone                2,198 cycles, longest 16
scrambler (Listing 2), N = 24,389  11 cycles, longest 9,943, one fixed point   -> not a single cycle
published constants, one location: 16 valid unread bits; the 16 sibling offsets (mod m) are distinct;
   6 random pairs and all 16 together are ADDITIVE: siblings = L + a subset sum of the 16 offsets (a 2^16-point box in Z_m)
   the same bit gives a DIFFERENT offset at a second location: a box with location-dependent generators, not a fixed coset
```

The published `m` is exactly `3^2,015,755`; with `gcd(c, m) = 1` and `3 | a − 1`, Hull–Dobell holds, so the published LCG alone is a single cycle of length `m` (on ℤ/3ᵏ an affine map with `a ≡ 1 (mod 3)` and `c` a unit is conjugate to the 3-adic odometer `x ↦ x + 1`, whose spectrum is the 3-power roots of unity). The spectrum of a permutation is the roots of unity of each cycle length present; one cycle of length N is the cyclic case. The fibre's indicator has the Fourier transform `e^(2πikL/m) · ∏_b (1 + e^(2πik·o_b/m))` (from the measured additivity).

**`Euclid's Extended`.** The file is a template (`m("")`, `a("")`) that keeps its coefficients in `qarray[25]`: it holds 23 divisions. On random 64-bit operands 199 of 200 need more (mean 36.0). The port raises `OverflowError` where the C++ would write past the array. For the published `a` (1,597,519 bits) about 9.3×10⁵ divisions would be needed (estimate, 0.843·ln a).

## Mechanism

| Step | Function | Confidence |
|---|---|---|
| ordered address (bijective base-N) | `ordered_address`, `ordered_text_at`, `page_at`, `location_of` | ESTABLISHED |
| right xorshift and its inverse `y ⊕ y≫s ⊕ y≫2s …` | `xorshift_right`, `xorshift_right_inverse` | ESTABLISHED |
| masked left xorshift and its inverse (⌈k/s⌉ iterations) | `xorshift_left_masked`, `xorshift_left_masked_inverse` | ESTABLISHED |
| Hull–Dobell conditions | `hull_dobell` | ESTABLISHED |
| scrambler of [0, N) (LCG mod 2^e, two xorshifts, cycle-walking) | `power_of_two_scrambler`, `babel_page`, `babel_location` | ESTABLISHED (exhaustive on the toy) |
| cycle lengths of a permutation; sibling-offset additivity | `permutation_cycles`, `Published.sibling_offsets` | ESTABLISHED (computed) |
| published engine on published constants | `Published.forward`, `.inverse`, `.pixels`, `.search`, `.sibling`, `.audit` | ESTABLISHED (computed) |
| Extended Euclid port with the fixed array | `euclid_inverse_qarray` | ESTABLISHED |
| site address fields; LobThis request as data | `parse_babel_address`, `resource_locator_request` | ESTABLISHED |

## Open

- The live site's image service was not observed; only the published source was read.
- The text library's algorithm is unpublished.
- README says `a`, `c` should be "fairly close to but less than `m`"; the published `a` and `c` are about half the size of `m`.

## Reference

Every equation with its parameters: [toolbox](toolbox/39_basile.md) · API: [basile](https://michaelrendier.github.io/ValaQuenta/api/modules/basile.html) · notebooks: `notebooks/basile/` (4).

---

## Sources

Basile, *libraryofbabel.info* (About; "Grains of Sand", `theory4.html`); Basile, `libraryofbabel.info-algo` (2019, CC BY-SA-NC; read from a local copy, not redistributed); Borges, "The Library of Babel" (1941). Predecessor engine: [hyperwebster](hyperwebster.md) (the ordered address). Version 1.0 (2026-09-30).
