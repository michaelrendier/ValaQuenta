# ValaQuenta

**The derivation engine.** Pure mathematics. Runnable code. No physical substrate required.

```
Ainulindale (the Music) → ValaQuenta (the engines) → VAPMIP (the world)
```

Version **0.159** · Python ≥ 3.9 · License **GPL-3.0-only** ([LICENSE](LICENSE))

ValaQuenta is a Python package of exact mathematical engines. Each engine is a
module you can import and call, and each is also a plugin of the ValaQuenta
Format ([FORMAT.md](FORMAT.md)) that the derivation browser lists and runs.
38 engines are registered (321 equations); 41 module directories in all.

## Current Repo Focus

Public release preparation: the API: Code Reference. Every registered module has
a manifest and a `maths.py` / `tools.py` split; docstrings are Sphinx reST field lists; the
README is the index, the wiki holds the results and the record, the notebooks
run the derivations, and Sphinx (`docs/`) builds the per-function reference.

## Quick start

```bash
git clone https://github.com/michaelrendier/ValaQuenta
cd ValaQuenta
bash install.sh                        # creates .venv, installs, verifies
source .venv/bin/activate
python3 verify_install.py              # recomputes the arithmetic, not just the imports
```

A session at the registry. The prompt is a literal `>>>`; the output is what it
printed.

```python
>>> from ValaQuenta.noether import NoetherCurrents
>>> NoetherCurrents().forced_sigma(1000.0, sigma_0=-3.0)   # any E, any σ₀
0.5
>>> from ValaQuenta.hamiltonian import HamiltonianXP
>>> HamiltonianXP().scale_check(2, 3, lam=2.0)             # H(λx, p/λ) = H(x, p)
True
>>> from ValaQuenta.__main__ import _register_all
>>> registry = _register_all()
>>> registry.list_equations('noether')
['noether.conservation_diagnostic', 'noether.violation_scan',
 'noether.resonance_artifacts', 'noether.blockchain_record',
 'noether.blockchain_verify', 'noether.blockchain_summary']
>>> out = registry.run('noether.conservation_diagnostic',
...                    {'psi_norms': [0.5, 0.5, 0.7], 'g': 1.0, 'algebra': 2})
>>> out['result']['status'], out['result']['conserved']
('PASS', True)
```

## API: Code Reference

Two kinds of code. **Standalone engines** are single files you import by name.
**Registry modules** live in `modules/<name>/` and share one contract; each has
`maths.py` (the mathematics, plain functions), `tools.py` (the `EquationModule`
class that publishes them as a formulary), and `manifest.json` (provenance and
UI registration).

### Standalone engines

| Import | What it is | Public API | Results |
|---|---|---|---|
| `ValaQuenta.bao_mass_gap` | Yang-Mills Mass Gap | `gap_value`, `identity_check`, `bao_consistency`, `mtheory_geometry`, `validate` | [wiki](wiki/bao_mass_gap.md) |
| `ValaQuenta.capacitor` | Capacitor — The semantic low-pass filter. | `Capacitor` | [wiki](wiki/capacitor.md) |
| `ValaQuenta.corpus` | CorpusProcessor — Feed any text archive to the ValaQuenta. | `CorpusProcessor` | [wiki](wiki/corpus.md) |
| `ValaQuenta.fixed_point` | Fixed Point Engine — The Boundary | `v_nball`, `v_nball_peak`, `transformer_profile`, `FixedPoint`, `two_fixed_points`, `angular_quantum_sequence` … | [wiki](wiki/fixed_point.md) |
| `ValaQuenta.galactic_cavity` | Galactic Particle Derivation Engine | `CavityMode`, `CosmologicalSMIG` | [wiki](wiki/galactic_cavity.md) |
| `ValaQuenta.hamiltonian` | HamiltonianXP — H = xp (Berry & Keating, 1999) | `HamiltonianXP`, `FermatEllipticHamiltonian`, `RedBlueHamiltonian` | [wiki](wiki/hamiltonian.md) |
| `ValaQuenta.lexicon` | Lexicon — The accumulated experience of the ValaQuenta. | `Lexicon` | [wiki](wiki/lexicon.md) |
| `ValaQuenta.noether` | Forward and backward Noether currents from one symmetry. | `NoetherCurrents` | [wiki](wiki/noether.md) |
| `ValaQuenta.prime_gate` | PrimeGate — the Boundary-Crossing Alarm | `sieve`, `BoundaryAlarm`, `sigma_half_alarm`, `PrimeGateEngine` | [wiki](wiki/prime_gate.md) |
| `ValaQuenta.semantic_domain` | SemanticDomain — The description bounds the semantic space. | `SemanticDomain` | [wiki](wiki/semantic_domain.md) |
| `ValaQuenta.semantic_word` | SemanticWord — A word is its multidimensional context. | `SemanticWord` | [wiki](wiki/semantic_word.md) |
| `ValaQuenta.telperion` | The Swimming Engine  v0.100 | `m87_compression`, `BellPhase`, `GalaxyType`, `LindbladMode`, `BaoTowerMapping`, `ResonanceCoupling` … | [wiki](wiki/telperion.md) |
| `ValaQuenta.understand` | Understand — Read, Listen, Ponder, Calculate, Understand. | `Understand` | [wiki](wiki/understand.md) |
| `ValaQuenta.zero_lattice` | Zero Lattice Engine — Telperion | `build_mul_table`, `multiply`, `norm_sq`, `e_k`, `find_zd_pairs`, `classify_zd_pairs` … | [wiki](wiki/zero_lattice.md) |

### Registry modules

`python3 -m ValaQuenta --info` prints this table from the live registry. Each
module is imported as `from ValaQuenta.modules.<name> import <Class>`; its
functions are in `ValaQuenta.modules.<name>.maths`. The **toolbox** page lists
every equation with its parameters, confidence and a worked call.

| Module | Engine | Equations | Confidence floor | Reference |
|---|---|---|---|---|
| `bao_mass_gap` | The Mass Gap — spectral residue of BAO | 7 | ESTABLISHED | [toolbox](wiki/toolbox/11_bao_mass_gap.md) · [wiki](wiki/bao_mass_gap.md) |
| `inversion` | Inside-Out Inversion Engine (I\|O) | 7 | ESTABLISHED | [toolbox](wiki/toolbox/07_inversion.md) · [wiki](wiki/inversion.md) |
| `lagrangian` | L_NN Ainulindale Lagrangian | 8 | THEORETICAL | [toolbox](wiki/toolbox/08_lagrangian.md) · [wiki](wiki/lagrangian.md) |
| `noether` | Noether Currents ∂_μJ^μ = 0 | 6 | THEORETICAL | [toolbox](wiki/toolbox/09_noether.md) · [wiki](wiki/noether.md) |
| `noether_information` | J_info Information Current | 4 | CONJECTURE | [toolbox](wiki/toolbox/10_noether_information.md) · [wiki](wiki/noether_information.md) |
| `berry_keating` | H_NN Berry-Keating Operator | 6 | OPEN | [toolbox](wiki/toolbox/06_berry_keating.md) · [wiki](wiki/berry_keating.md) |
| `sonification` | Sonification ω = pitch | 19 | ESTABLISHED | [toolbox](wiki/toolbox/25_sonification.md) · [wiki](wiki/sonification.md) |
| `hyperwebster` | HyperWebster Horner Bijection | 6 | THEORETICAL | [toolbox](wiki/toolbox/15_hyperwebster.md) · [wiki](wiki/hyperwebster.md) |
| `jwst` | JWST Spectral Pixel → 𝕆 | 5 | THEORETICAL | [toolbox](wiki/toolbox/22_jwst.md) · [wiki](wiki/jwst.md) |
| `turing_diagonal` | Turing Diagonal Engine — i²=-1 = Cantor = Gödel = Enigma = UDOE | 5 | ESTABLISHED | [toolbox](wiki/toolbox/13_turing_diagonal.md) · [wiki](wiki/turing_diagonal.md) |
| `singularity_null` | Singularity-NULL Engine — The Singularity IS Identity. Tower Collapses. | 5 | THEORETICAL | [toolbox](wiki/toolbox/14_singularity_null.md) · [wiki](wiki/singularity_null.md) |
| `sigma_expansion` | Sigma Expansion — J_red/J_blue Balance Curve | 4 | THEORETICAL | [toolbox](wiki/toolbox/36_sigma_expansion.md) · [wiki](wiki/sigma_expansion.md) |
| `t32_nilpotency` | T32 Nilpotency — Hyperwebster Address Primitives | 1 | ESTABLISHED | [toolbox](wiki/toolbox/37_t32_nilpotency.md) · [wiki](wiki/t32_nilpotency.md) |
| `hypergon_constructibility` | Hypergon Constructibility — Gauss-Wantzel + Factorization Test | 3 | OPEN | [toolbox](wiki/toolbox/33_hypergon_constructibility.md) · [wiki](wiki/hypergon_constructibility.md) |
| `l_io_photon_path` | L_(I\|O) Photon Path Engine (GR) | 6 | THEORETICAL | [toolbox](wiki/toolbox/34_l_io_photon_path.md) · [wiki](wiki/l_io_photon_path.md) |
| `archimedes_screw` | The Archimedes Screw (Prime Coordinate Engine) | 29 | THEORETICAL | [toolbox](wiki/toolbox/29_archimedes_screw.md) · [wiki](wiki/archimedes_screw.md) |
| `box_kite` | The Box-Kite Debugger (ZD Geometry) | 18 | ESTABLISHED | [toolbox](wiki/toolbox/28_box_kite.md) · [wiki](wiki/box_kite.md) |
| `angular_rank` | The 16D Oscilloscope (Angular Rank) | 12 | ESTABLISHED | [toolbox](wiki/toolbox/30_angular_rank.md) · [wiki](wiki/angular_rank.md) |
| `scale` | The Scale (Decompositional Analysis, Forwards and Backwards) | 10 | ESTABLISHED | [toolbox](wiki/toolbox/31_scale.md) · [wiki](wiki/scale.md) |
| `units` | Units (The Equation Index) | 4 | ESTABLISHED | [toolbox](wiki/toolbox/32_units.md) · [wiki](wiki/units.md) |
| `add_scale_sign` | ADD:SCALE:SIGN (the tier-0 datatype) | 6 | ESTABLISHED | [toolbox](wiki/toolbox/02_add_scale_sign.md) · [wiki](wiki/add_scale_sign.md) |
| `desitter_cavitation` | De Sitter Cavitation Engine — No Singularity: the Abrikosov-Vortex Core | 8 | THEORETICAL | [toolbox](wiki/toolbox/23_desitter_cavitation.md) · [wiki](wiki/desitter_cavitation.md) |
| `emerger` | The Emerger (Sedenion Bracketing & Firing Order) | 8 | THEORETICAL | [toolbox](wiki/toolbox/24_emerger.md) · [wiki](wiki/emerger.md) |
| `constants` | Tier 0 Constants — π φ e √ i derived from H_RB | 11 | ESTABLISHED | [toolbox](wiki/toolbox/03_constants.md) · [wiki](wiki/constants.md) |
| `derivation_chain` | Derivation Chain — Tiers 1–5 | 14 | THEORETICAL | [toolbox](wiki/toolbox/04_derivation_chain.md) · [wiki](wiki/derivation_chain.md) |
| `h_rb_hat` | Σ_RB RedBlue Summed Integral | 16 | THEORETICAL | [toolbox](wiki/toolbox/05_h_rb_hat.md) · [wiki](wiki/h_rb_hat.md) |
| `clay_millennium` | Clay Millennium Problems — Σ_RB derivations | 12 | THEORETICAL | [toolbox](wiki/toolbox/12_clay_millennium.md) · [wiki](wiki/clay_millennium.md) |
| `tier6_physics` | Tier 6 — Full Physics: QM + Standard Model | 10 | THEORETICAL | [toolbox](wiki/toolbox/18_tier6_physics.md) · [wiki](wiki/tier6_physics.md) |
| `tier7_cosmos` | Tier 7 — Cosmology + Mathematics + Standard Model from H_RB | 15 | THEORETICAL | [toolbox](wiki/toolbox/19_tier7_cosmos.md) · [wiki](wiki/tier7_cosmos.md) |
| `tier8_sedenion` | Tier 8 — D-CS: Sedenion Self-Organisation Paper | 8 | THEORETICAL | [toolbox](wiki/toolbox/20_tier8_sedenion.md) · [wiki](wiki/tier8_sedenion.md) |
| `tier9_chem` | Tier 9 — D-CHEM: Cancer Drugs from Algebraic Signature (Erika Schafer) | 6 | THEORETICAL | [toolbox](wiki/toolbox/21_tier9_chem.md) · [wiki](wiki/tier9_chem.md) |
| `translator_discocat` | The Translator v1 — DisCoCat (pregroup . tensor) | 5 | OPEN | [toolbox](wiki/toolbox/26_translator_discocat.md) · [wiki](wiki/translator_discocat.md) |
| `translator_vsa` | The Translator v2 — VSA / hyperdimensional (bind.bundle.permute) | 6 | OPEN | [toolbox](wiki/toolbox/27_translator_vsa.md) · [wiki](wiki/translator_vsa.md) |
| `udeo_crypto` | UDEO RSA Key-Recovery — Five Candidate Mechanisms, Honestly Scored | 8 | OPEN | [toolbox](wiki/toolbox/38_udeo_crypto.md) · — |
| `bracketing_firing_order` | Bracketing, Firing Order, and Set Membership | 7 | ESTABLISHED | [toolbox](wiki/toolbox/01_bracketing_firing_order.md) · [wiki](wiki/bracketing_firing_order.md) |
| `oblique_gear` | The Oblique Gear Across Scale (Black Hole / Galaxy) | 6 | OPEN | [toolbox](wiki/toolbox/16_oblique_gear.md) · — |
| `prime_gauge_field` | The Prime Gauge Field | 5 | THEORETICAL | [toolbox](wiki/toolbox/35_prime_gauge_field.md) · [wiki](wiki/prime_gauge_field.md) |
| `spectral_primes` | Spectral Representation of the Primes (Spin / Wobble) | 5 | OPEN | [toolbox](wiki/toolbox/17_spectral_primes.md) · — |

Library modules — mathematics only, not registered as engines:

| Module | What it is | | | Reference |
|---|---|---|---|---|
| `spherical` | Spherical harmonics, Courant nodal domains, Schumann modes | — | — | [wiki](wiki/spherical.md) |
| `sigma_cavitation` | σ-parameterised sedenion cavitation SVG renderer (`generate`) | — | — | [wiki](wiki/sigma_cavitation.md) |
| `translator_common` | Shared vector space of the two Translator engines | — | — | [wiki](wiki/translator_common.md) |

### The registry contract

```python
from ValaQuenta.engine.registry import EquationModule, Equation, get_registry, register
```

| Name | Role |
|---|---|
| `Equation` | One named equation: `name`, `display`, `latex`, `radian_form`, `confidence`, `code_verified`, `params`, `compute`, `process`. |
| `EquationModule` | Base class of every `tools.py`: `name`, `display_name`, `version`, `description`, `confidence_floor`, `formulary()`, `run(equation_name, params)`, `viewer_data(equation_name, params, display_mode)`. |
| `ModuleRegistry` | `register(module)`, `get_module(name)`, `get_equation('module.equation')`, `list_modules()`, `list_equations(module_name=None)`, `run('module.equation', params)`. |

Confidence tiers, strongest first: `ESTABLISHED` · `THEORETICAL` · `CONJECTURE` ·
`OPEN`. A tier is a claim about the mathematics, not about the code: the code
runs at every tier.

To add an engine, follow the six steps in the docstring of
[`engine/registry.py`](engine/registry.py) and validate it with
`python3 -m ValaQuenta.engine.manifest validate` and
`python3 -m ValaQuenta.engine.format validate`.

### Listings

Five short mechanisms are shown as complete, self-contained code, each executed
cold with its output: the Horner address of a word, the P1 word-to-zero hash, the
prime-channel signature, the collision test of a stepped process, and the one-step
solution of the σ balance. See **Listings** in the docs (`docs/listings.rst`,
generated by `docs/gen_listings.py`; `tests/test_listings.py` runs them).

### Tests

```bash
pip install pytest
python3 -m pytest                    # 71 tests: registry, manifests, listings, docstrings, README
```

### Building the documentation

The per-function reference is published at **https://michaelrendier.github.io/ValaQuenta/** (GitHub Pages, rebuilt on every push to `main`; `.github/workflows/docs.yml`). It is built by Sphinx from the docstrings:

```bash
pip install -e ".[docs]"
python3 docs/gen_api.py                          # regenerate docs/api/ after adding a module
sphinx-build -b html docs docs/_build/html       # open docs/_build/html/index.html
```

`.readthedocs.yaml` builds the same tree for Read the Docs, and CI treats warnings
as errors. The parts of the repository that are not importable package code
(`code/`, `addenda/`, notebooks, the wiki) are listed with their locations on the
docs page *Elsewhere in the repository*.

### Conventions

- **Docstrings** are Sphinx reST field lists (`:param x:`, `:returns:`,
  `:raises E:`), consumed by `sphinx.ext.autodoc`; types come from the
  annotations. A docstring tells the caller what to do, not what happened. The
  history of a result lives in the wiki.
- **Arithmetic** is `fractions.Fraction` exact where the maths is exact; floats
  appear only at an output boundary.
- **Numbers that fail stay in the data.** Refuted results are reported as
  refuted, with the number that refuted them.
- **Plugins** declare a licence. Every built-in engine is `GPL-3.0-only`.

## Install

```bash
git clone <this repo>            # into a directory on your PATH-able parent
cd ValaQuenta

bash install.sh                  # Linux   — creates .venv, installs, verifies
bash install-macos.sh            # macOS   — same, prefers Homebrew python
powershell -ExecutionPolicy Bypass -File .\install.ps1   # Windows
```

Flags: `--user` (no venv), `--system` (use distro packages), `--no-jupyter`.
Run the scripts with `bash install.sh`, not `./install.sh` — the executable bit
does not survive every filesystem.

Then, any time:

```bash
python3 verify_install.py
```

This does not merely check that imports succeed. It recomputes GAP from its two
inputs, confirms OMEGA_ZS satisfies `W·e^W = 1`, counts the zero-divisor pairs
(84), and checks that `H=xp` conserves energy. If the arithmetic is broken it
will say so.

Dependencies are in `requirements.txt`: numpy, scipy and matplotlib are
required; JupyterLab is needed only to open the notebooks.

### ⚠ The venv is the general-purpose environment for every repo

**`ValaQuenta/.venv` is provisioned to run code in ANY repo in ThePlace** —
ValaQuenta, Ainulindale, VAPMIP, PtolC, RiemannHypothesisProof, FourthAgePapers,
SedenionSpectralRelativity. Only **BulletCluster** keeps a separate venv, because
its telescope pins are specific to that work.

```bash
source env.sh          # activate
./env.sh check         # verify — prints every module and its version
```

**Do not use the system python for project code.** It has numpy 2.4.6 (pip,
`~/.local`) shadowing numpy 1.26.4 (apt), and every apt-built C extension is
still linked against 1.x. Confirmed broken system-wide: `pandas`,
`scikit-learn`, **`nltk`**, `bottleneck`, `numcodecs`, `zarr`, `reproject`,
`aplpy`. pip cannot repair it in place — PEP 668, externally managed.
**All of them work inside the venv.**

> The 2026-08-06 primer recorded "NLTK is broken in this environment — do not
> spend time fixing it." That was never NLTK's fault. It is the numpy ABI split,
> and the venv fixes it. WordNet corpora still need
> `python -m nltk.downloader wordnet`.

Verified 2026-08-14, Python 3.12.3, **35/35 imports clean**. `requirements.txt`
records the version actually installed and tested beside each pin, plus the
packages deliberately *excluded* (whisper, PyQt, rtlsdr, bpy, qtermwidget) and
the system libraries some entries imply.

## Run

```bash
python3 -c "from ValaQuenta.bao_mass_gap import validate; validate()"
python3 -c "from ValaQuenta.understand import Understand; u=Understand(); print(u.process('the prime'))"
python3 -m ValaQuenta --info        # registry summary
python3 -m ValaQuenta --curses      # THE DERIVATION BROWSER, no Qt needed
```

### The Derivation Browser (`--curses`)

A file-manager over the registry — you pick ValaQuenta apart one scope at a
time, `dir()`-style, the way a package browser walks a package. The breadcrumb
**is** the API path (`/ <engine> / <equation>`); the engine naming conventions
**are** the function breadcrumbs.

- **Left pane** — the current listing (engines → equations → run). `..` goes up.
- **Right pane** — the **DECLARATION**: a plain-English, outside-observer line
  of *what this does as a derivation step* (`Equation.process`,
  `EquationModule.process_description`), then `latex` / `radian_form` / params.
  An equation with no `process=` shows a visible `[process= not set]` TODO.
- **`Enter`** runs the equation; **`p`** shows the proof-on-the-fly INPUTS a
  sympy guided derivation would consume (the seam is wired, the tour is TODO).
- **`a`** opens the **analysis lenses** — run a tool *across any engine's
  mathematics, including its own*: `emerge` (sedenion bracketing & firing
  order), `spectral` and `lineage` (`GenerationalLineage`), `calibrate`
  (the generational-lineage decomposition of the current engine). Sibling
  repos are imported lazily; a missing one is reported, not fatal.

Keys: `↑↓` nav · `→/Enter` open·run · `←/⌫` up · `Tab` focus · `/` filter ·
`d` display mode · `a` lenses · `p` proof inputs · `q` quit.

## Where to start

| If you want | Go to |
|---|---|
| Results without running anything | [wiki/00_index.md](wiki/00_index.md) |
| The order the derivation goes in | [wiki/derivation_chain.md](wiki/derivation_chain.md) |
| The top-level engines, worked | [notebooks/engines/](notebooks/engines/) |
| One module per Millennium problem / tier | [notebooks/core/](notebooks/core/) |
| What is known to be broken | [wiki/00_index.md](wiki/00_index.md) § Known defects |
| What each engine printed when last run | [wiki/results_at_a_glance.md](wiki/results_at_a_glance.md) |
| Every function, with parameters | [Code Reference](#api-code-reference) below, and `docs/` (Sphinx) |

The 70 notebooks that existed on 2026-07-28 executed clean (393/393 code cells). `notebooks/` now holds 87; the 17 added since have not been re-run as a set. `python3 verify_install.py` checks the arithmetic they rely on.

---

---

## Relation to Other Repos

| Repo | Role |
|------|------|
| `Ainulindale/` | The Music — theory, wikis, derivation notebooks, addenda |
| `ValaQuenta/` | The Engines — runnable mathematics, this repo |
| `VAPMIP/` | The World — LSHS system, Ptolemy corpus engine, SVG outputs |
