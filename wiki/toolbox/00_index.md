# THE TOOLBOX — WIKI INDEX

ValaQuenta's tool-usage reference, one page per tool. Code-reference /
API style throughout — parameters, return values, call examples. The
theory, provenance, and "why this exists" for each tool lives in its own
page under `ValaQuenta/wiki/` (linked from each Toolbox page); this index
and its pages do not repeat that content.

> **Protocol, matching `VAPMIP/docs/wiki/Tuning-the-Engine/00_index.md`'s
> own rule:** a repass on this index is part of updating the Toolbox every
> time — add the new page and its row, then re-check the whole table is
> current before calling the update done.

**Scope (Cody, 2026-09-27):** every tool Claude has written for
ValaQuenta — every `modules/<name>/tools.py` (the `EquationModule`
registry contract: `formulary()`, `run()`, `viewer_data()`,
`shell_commands()`). Not the raw `maths.py` internals underneath a
module (those are the module's own theory page's business), and not
the pre-Full-Engine-Protocol top-level files (`hamiltonian.py`,
`noether.py`, `galactic_cavity.py`, `capacitor.py`, `understand.py`,
`semantic_word.py`, `semantic_domain.py`, `fixed_point.py`,
`zero_lattice.py`, `telperion.py`, `corpus.py`, `lexicon.py`) or the
four `modules/` directories with no `tools.py` at all
(`factoral_decomposition`, `sigma_cavitation`, `spherical`,
`translator_common`) — none of those carry a `tools.py`, so there is no
"tool" part of them to document here. "Outside ValaQuenta" repos are
explicitly deferred — add an entry when a real, concrete use for it
comes up, not preemptively.

**Ordering:** follows `ValaQuenta/wiki/00_index.md`'s own section order
(top-level engines → foundations → currents → problems → physics →
sound/language), for every entry in that index that has a `tools.py`;
modules with a real `tools.py` but not yet listed in `00_index.md`
(`hypergon_constructibility`, `l_io_photon_path`, `prime_gauge_field`,
`sigma_expansion`, `t32_nilpotency`, `udeo_crypto`) are appended after,
in the order found.

---

## Tools

| Page | Tool | Date | Covers |
|------|------|------|--------|
| [01_bracketing_firing_order.md](01_bracketing_firing_order.md) | Bracketing, Firing Order, Set Membership | 2026-09-27 | `modules/bracketing_firing_order/` |
| [02_add_scale_sign.md](02_add_scale_sign.md) | ADD:SCALE:SIGN (the tier-0 datatype) | 2026-09-27 | `modules/add_scale_sign/` |
| [03_constants.md](03_constants.md) | Tier 0 Constants — π φ e √ i derived from H_RB | 2026-09-27 | `modules/constants/` |
| [04_derivation_chain.md](04_derivation_chain.md) | Derivation Chain — Tiers 1–5 | 2026-09-27 | `modules/derivation_chain/` |
| [05_h_rb_hat.md](05_h_rb_hat.md) | Σ_RB  RedBlue Summed Integral | 2026-09-27 | `modules/h_rb_hat/` |
| [06_berry_keating.md](06_berry_keating.md) | H_NN  Berry-Keating Operator | 2026-09-27 | `modules/berry_keating/` |
| [07_inversion.md](07_inversion.md) | Inside-Out Inversion Engine  (I\|O) | 2026-09-27 | `modules/inversion/` |
| [08_lagrangian.md](08_lagrangian.md) | L_NN  Ainulindale Lagrangian | 2026-09-27 | `modules/lagrangian/` |
| [09_noether.md](09_noether.md) | Noether Currents  ∂_μJ^μ = 0 | 2026-09-27 | `modules/noether/` |
| [10_noether_information.md](10_noether_information.md) | J_info  Information Current | 2026-09-27 | `modules/noether_information/` |
| [11_bao_mass_gap.md](11_bao_mass_gap.md) | The Mass Gap — spectral residue of BAO | 2026-09-27 | `modules/bao_mass_gap/` |
| [12_clay_millennium.md](12_clay_millennium.md) | Clay Millennium Problems — Σ_RB derivations | 2026-09-27 | `modules/clay_millennium/` |
| [13_turing_diagonal.md](13_turing_diagonal.md) | Turing Diagonal Engine — i²=-1 = Cantor = Gödel = Enigma = UDOE | 2026-09-27 | `modules/turing_diagonal/` |
| [14_singularity_null.md](14_singularity_null.md) | Singularity-NULL Engine — the singularity IS identity | 2026-09-27 | `modules/singularity_null/` |
| [15_hyperwebster.md](15_hyperwebster.md) | HyperWebster  Horner Bijection | 2026-09-27 | `modules/hyperwebster/` |
| [16_oblique_gear.md](16_oblique_gear.md) | The Oblique Gear Across Scale (Black Hole / Galaxy) | 2026-09-27 | `modules/oblique_gear/` |
| [17_spectral_primes.md](17_spectral_primes.md) | Spectral Representation of the Primes (Spin / Wobble) | 2026-09-27 | `modules/spectral_primes/` |
| [18_tier6_physics.md](18_tier6_physics.md) | Tier 6 — Full Physics: QM + Standard Model | 2026-09-27 | `modules/tier6_physics/` |
| [19_tier7_cosmos.md](19_tier7_cosmos.md) | Tier 7 — Cosmology + Mathematics + Standard Model from H_RB | 2026-09-27 | `modules/tier7_cosmos/` |
| [20_tier8_sedenion.md](20_tier8_sedenion.md) | Tier 8 — D-CS: Sedenion Self-Organisation Paper | 2026-09-27 | `modules/tier8_sedenion/` |
| [21_tier9_chem.md](21_tier9_chem.md) | Tier 9 — D-CHEM: Cancer Drugs from Algebraic Signature | 2026-09-27 | `modules/tier9_chem/` |
| [22_jwst.md](22_jwst.md) | JWST  Spectral Pixel → 𝕆 | 2026-09-27 | `modules/jwst/` |
| [23_desitter_cavitation.md](23_desitter_cavitation.md) | De Sitter Cavitation Engine — No Singularity | 2026-09-27 | `modules/desitter_cavitation/` |
| [24_emerger.md](24_emerger.md) | The Emerger (Sedenion Bracketing & Firing Order) | 2026-09-27 | `modules/emerger/` |
| [25_sonification.md](25_sonification.md) | Sonification  ω = pitch | 2026-09-27 | `modules/sonification/` |
| [26_translator_discocat.md](26_translator_discocat.md) | The Translator v1 — DisCoCat (pregroup · tensor) | 2026-09-27 | `modules/translator_discocat/` |
| [27_translator_vsa.md](27_translator_vsa.md) | The Translator v2 — VSA / hyperdimensional | 2026-09-27 | `modules/translator_vsa/` |
| [28_box_kite.md](28_box_kite.md) | The Box-Kite Debugger (ZD Geometry) | 2026-09-27 | `modules/box_kite/` |
| [29_archimedes_screw.md](29_archimedes_screw.md) | The Archimedes Screw (Prime Coordinate Engine) | 2026-09-27 | `modules/archimedes_screw/` |
| [30_angular_rank.md](30_angular_rank.md) | The 16D Oscilloscope (Angular Rank) | 2026-09-27 | `modules/angular_rank/` |
| [31_scale.md](31_scale.md) | The Scale (Decompositional Analysis) | 2026-09-27 | `modules/scale/` |
| [32_units.md](32_units.md) | Units (The Equation Index) | 2026-09-27 | `modules/units/` |
| [33_hypergon_constructibility.md](33_hypergon_constructibility.md) | Hypergon Constructibility — Gauss–Wantzel + Factorization | 2026-09-27 | `modules/hypergon_constructibility/` |
| [34_l_io_photon_path.md](34_l_io_photon_path.md) | L_(I\|O) Photon Path Engine (GR) | 2026-09-27 | `modules/l_io_photon_path/` |
| [35_prime_gauge_field.md](35_prime_gauge_field.md) | The Prime Gauge Field | 2026-09-27 | `modules/prime_gauge_field/` |
| [36_sigma_expansion.md](36_sigma_expansion.md) | Sigma Expansion — J_red/J_blue Balance Curve | 2026-09-27 | `modules/sigma_expansion/` |
| [37_t32_nilpotency.md](37_t32_nilpotency.md) | T32 Nilpotency — Hyperwebster Address Primitives | 2026-09-27 | `modules/t32_nilpotency/` |
| [38_udeo_crypto.md](38_udeo_crypto.md) | UDEO RSA Key-Recovery — Five Candidate Mechanisms | 2026-09-27 | `modules/udeo_crypto/` |

**Not carried here** (no `tools.py`, so no tool-level API to document —
see each one's own theory page for the maths): `hamiltonian.py`,
`ring_theory` (lives in `SedenionFactoralRelativity`, not ValaQuenta),
`galactic_cavity.py`, `capacitor.py`, `understand.py`, `semantic_word.py`,
`semantic_domain.py`, `fixed_point.py`, `zero_lattice.py`, `telperion.py`,
`corpus.py`, `lexicon.py`, `pencil_hyperstring` (proposal, no code),
`three_ring_scale` (proposal, no code), `d_star_rg` (deferred, lives in
`FourthAgePapers/DStarRG/`), `spherical`, `sigma_cavitation`,
`translator_common`, `factoral_decomposition`, `valaquenta_format`,
`generational_lineage_map`, `engine_manifest` (infrastructure, not an
`EquationModule`).

---

*Full theory pages: [`ValaQuenta/wiki/00_index.md`](../00_index.md).*
