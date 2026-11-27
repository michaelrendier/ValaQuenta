# ValaQuenta restructuring / update changelog

Housekeeping started 2026-11-25. One entry per engine, in dependency order (an engine is done after
its code, toolset, API/Code Reference wiki page, Ainulindale wiki page, notebook, and every downstream use are brought to canonical maths).

## Standing rules for this pass (author, 2026-11-25)

1. **d\*** is always the value the code runs with (0.24600). The other three faces are labelled, never substituted:
   `d*_taut` (0.246307201473, Flow), `d*_RG` (dimension 8, numeric OPEN), `d*_ln(10)` (0.5671432904, Translator).
   `d*_taut` and `d*_RG` appear only in their own two visualizations.
2. Every file that uses d\* in any form carries the full four-value list and a pointer to the full story
   (`engine.constants.dstar_comment_block()`; applied with `tools/dstar_block.py`).
3. Symbols: α = fine structure (`ALPHA_FS`); A_π = W(1) (`A_PI`; `OMEGA_ZS` is a deprecated alias); Ω_ζΣ = Ω_RZ = d\*.
4. Docs are API / Code Reference style; narrative lives in Ainulindale/wiki. Canonical source: `~/.clauderc_canonical_maths`.
5. **One engineering white paper for ValaQuenta** (not one per engine): section 3 is the engines, engine 0 first, then each engine in the order below. Written last.
   Per engine, in this order: code → toolset → ValaQuenta wiki → Ainulindale wiki → notebook → downstream repos →
   (author selects) visualizations → code flow chart → engineering white paper. Flow charts and papers are written last.
6. Failed results stay in code and docs (Ainulindale wiki 135 ledger). Nothing is reverted to an older name.

## Order (follows the import graph, leaves of the maths first)

0 `engine/constants.py` · 1 `h_rb_hat` · 2 `constants` · 3 `t32_nilpotency` → `hypergon_constructibility` · 4 `box_kite` ·
5 `add_scale_sign` → `bracketing_firing_order` → `relativity` · 6 `tier8_sedenion` → `pi_derivations` → `circle_atlas` ·
7 `inversion`, `berry_keating`, `derivation_chain`, `oblique_gear`, `angular_rank`, `inductive_onset_residual`, `clay_millennium` ·
8 the remaining independent engines, then the top-level files (`zero_lattice`, `fixed_point`, `telperion`, …).

## Log

### 2026-11-25 · engine 0 · `engine/constants.py`
- Added `D_STAR_TAUT`, `D_STAR_LN10`, `D_STAR_RG` (= 8), `D_STAR_RG_NUMERIC` (= None, OPEN), `D_STAR_STORY`, `dstar_faces()`, `dstar_comment_block()`.
- `D_STAR` stays 0.24600 (the working value). `D_STAR_BOUNDARY`/`OMEGA_ZETA_SIGMA` now alias `D_STAR_TAUT` (same number as before: 0.246307201473).
- `summary()` prints all four faces and the story pointer.
- Added `tools/dstar_block.py` (audit/insert the four-faces block per engine) and `tools/propagate.py` (carry a change to every downstream use;
  working tree only, skips files with uncommitted changes, appends to `PROPAGATION_LEDGER.md`). `.git/hooks/post-commit` runs
  `propagate.py --changed --apply` so a ValaQuenta commit reaches downstream automatically (the hook is local to this clone).
- Found pre-existing, unchanged by this pass (same 4 failures with my changes stashed): `tests/test_registry.py` (manifest without a `license` key; formularies),
  `tests/test_docstrings.py` (public names without docstrings; parameters without field lists). Queued for the cross-cutting pass.

### 2026-11-25 · engine 1 · `h_rb_hat`
- Code: `maths.py` took its local `D_STAR = 0.2460` / `A_PI` literals from `engine.constants` (single source); the `d*` string in `trine_configuration` now names the working value and the other three faces. Four-faces block added to `maths.py`, `tools.py`.
- Docs: block added to `wiki/h_rb_hat.md`, `wiki/toolbox/05_h_rb_hat.md` (regenerated), `NOTES_2026-11-21_d_star_and_the_vev.md`. The narrative "Generational Lineage calibration" section moved from the ValaQuenta wiki to Ainulindale wiki 14 §9 (ValaQuenta wiki is API only). Manifest `provenance.wiki.ainulindale` filled (VQ-6).
- Notebook `01_fermat_riemann_dual_currents`: constants now imported from `engine.constants`; side labels corrected (d* = Riemann/entropy side, A_π = Fermat/inertia side; they were reversed), the "Yang-Mills mass gap" label on δ replaced by "onset residual, not the Clay mass gap" (staleness catalog), the Ω_ζΣ tick label corrected to A_π; block added; re-executed clean.
- Tests: `tests/test_h_rb_hat.py` (5 tests: four faces and closure, A_π = W(1), single source, comment block, σ=½ facets share the coupling sum 4.9896332508).
- Propagated (13 downstream docs): Ainulindale (PROVENANCE, wiki 14, 18, 70, 123, 131, AgeThird ×2), FourthAgePapers/EquationSpace, GenerationalLineage wiki, PtolemyDesktop (MONAD, RedBlueHamiltonian), RiemannHypothesisProof/docs. See `PROPAGATION_LEDGER.md`.
- Left open (needs the author): VQ-7, the `Σ_RB` identifiers (`SigmaRBModule`, `sigma_rb_evaluate`, the display string) until the full rename is decided.

### 2026-11-25 · `h_rb_hat` follow-up (author's direction)
- Ĥ_RB is the **Noether Current Operator** for now (J_red = Noether current, J_blue = Noether information current); Ĥ_RB − Ĥ_BR = J_red + J_blue. UFT maths are discussed engine by engine, not obfuscated elsewhere.
- Wrote `docs/HRB_REFERENCE_CENSUS.md`: every file in the repositories naming Ĥ_RB / 0_RB / Σ_RB / J_red,J_blue (1,064 files outside archives, worktrees and build output), ranked.
- Opened `wiki/DISAMBIGUATION_NOTES.md`: the symbol-collision notepad, one entry per engine as we go; it becomes the single Disambiguation wiki page.
- Located the Chladni / hypercomplex-Laplacian work: `TuringStack/hypercomplex_laplacian.py`, `sha1_chladni_stability.py`, `sha1_chladni_figure.py` and their PNGs (the 496-bond T32 stability map).

### 2026-11-25 · `h_rb_hat` · the 16-component sigma_rb test bench and the Ĥ_RB gallery (author's direction)
- New `modules/h_rb_hat/sigma16.py`: the 16-component sigma_rb (real `sigma_riemann` + 15 imaginary) with two stated lifts. A: p^(−sigma_rb)·[E_red+E_blue] with the real energies. B: Ĥ_RB = L_C, Ĥ_BR = R_C, Ĥ_RB − Ĥ_BR = J_red + J_blue = L_C − R_C (the reading of TuringStack `RSA_DEMO.py` method 2). Definitions are OPEN; every number is CALCULATED. `tests/test_h_rb_hat_sigma16.py` (8 tests).
- Exact identity found: L_C − R_C = β·ad_û with β = −Σ p^(−sigma_riemann) sin(τ ln p); on the real axis Ĥ_RB = Ĥ_BR.
- Measured: the 15 basis directions are one class (ad rank 14); exactly 84 of the 210 (e_i ± e_j)/√2 are zero-divisor directions (L nullity 4, ad rank 10); Ĥ_RB is singular only at α = 0 in a zero-divisor direction; lift A is direction-independent; no structure at Δ = 0.000707 in either lift (|β| = c₁τ, c₁ = 12.2034).
- Finding VQ-9 (Ainulindale wiki 135): `sigma_rb_term` balance does not depend on sigma_riemann.
- `gallery/hrb/`: 26 pages + index (`experiments.py` → `data/hrb_data.js`; `build_gallery.py`; `hrb.js`; `serve_gallery.sh`). Not committed or pushed yet (pending: items listed on the Pending page, and the author's selection).
- Rule recorded: no bare sigma anywhere (`wiki/DISAMBIGUATION_NOTES.md`); the d* block text now reads σ_ζ=½ plane in 19 files.

### 2026-11-25 · `h_rb_hat` · documented map, draft paper, flow chart (author's correction)
- Correction: the documented sigma_rb is ψ[k]·conj ψ[k⊕4] (16 in, 16 out; tilt and axis; 7/7 tests of 2026-08-31). It is now in `modules/h_rb_hat/oblique_sigma_rb.py` with `tests/test_h_rb_hat_oblique.py` (9 tests: the 2026-08-31 numbers, strut-blindness ½ + Δ/E, the rectifier law, the saddle rate ≈ 6.1). `sigma16.py` and gallery pages S1–S7 are relabelled exploratory (my own lifts, not the documented map).
- Gallery: 34 pages (`gallery/hrb/index.html`): R1–R9 documented map; S1–S7 exploratory; A, B, C, D, F; FC1 code flow chart derived from the source by `ast` (`gallery/hrb/build_flowchart.py`).
- Paper: `paper/ValaQuenta_Engineering_Whitepaper_DRAFT.md` (draft 1, sections 1–3.1, generated by `paper/make_paper.py`, `--check` mode, 6 listings run cold).
- Pushed: Ainulindale, FourthAgePapers, GenerationalLineage, PtolemyDesktop (device-arch branch), RiemannHypothesisProof (d* block, sigma_ζ wording, wiki 135 VQ-9, wiki 14 §9) and ValaQuenta (main).

### 2026-11-26 · engine 2 · `constants`
- Code (0.130): `derive_d_star` now returns the four faces from `engine.constants` (single source); the Cayley-Dickson-tower sum d*_ℝ+d*_ℂ+d*_ℍ+d*_𝕆 → ln 10 and the label "BAO first acoustic peak" are withdrawn and named in the docstring and the `superseded` key (record kept). A_π, α and d* literals inside functions replaced by `engine.constants` imports.
- Staleness fixed against Ainulindale wiki 22 §6: "π φ e √ i are OUTPUTS" and "Euler's identity is a theorem of this engine" withdrawn (Euler's identity is a theorem of complex analysis; the outputs reading is THEORETICAL). Confidence strings split into identity (ESTABLISHED) and programme reading (THEORETICAL). `confidence_floor` ESTABLISHED → THEORETICAL (lowest tier: `derive_alpha_fermat`). Λ's `σ=∞` tier label (a collision with the coupling σ, and not a registry tier) → ESTABLISHED (existence) / OPEN (value). Latex/Σ_RB/Ω_ζΣ labels → Ĥ_RB, A_π, α.
- Docs: wiki/constants.md, toolbox page regenerated, manifest (Ainulindale pointer → wiki 22), notebook 01 claim cell corrected. Tests: `tests/test_constants.py` (7).
- New: `tools/flowchart.py` + `tools/flowlib.py` (ISO 5807 drawer shared with VAPMIP/docs/flowcharts): one ast-derived code flow chart per engine, `docs/flowcharts/<engine>_flow.svg|png` + `index.html` (64 charts). First pass: calls through module aliases (e.g. `_C.X`) are not yet drawn as arrows to engine.constants.

### 2026-11-26 · engine 3 · `t32_nilpotency` (0.110)
- Code: added `ones`, `trace_laplacian` (Δ(w) = w·𝟏), `square_class`, `radical_census`; registry equation `radical_census`. Primitives unchanged (verified: same 11/16 and 12/15 splits).
- Canonical maths brought in and re-measured, not copied: GF(2) square law x² ∈ {0, e₀} (128 / 128 at dim 8, exhaustive); Δ(w) = 0 ⟺ w² = 0 (exhaustive dim 2/4/8, 20,000 random words at dim 32, 0 mismatches); corrected lemma (𝟏 not an annihilator; supersedes the UDEO white-paper proof).
- Docs: wiki page, toolbox 37 regenerated, manifest (version, tool, Ainulindale pointer → wiki 78), Ainulindale wiki 78 §5, notebook 17 extended and re-executed clean. Tests: `tests/test_t32_nilpotency.py` (9). No d* use in this engine.
- Pending, in order: visuals (to be discussed with the author before any code), then the code flow chart, then the white paper.
- 2026-11-26 · `t32_nilpotency` visuals (author approved all four; no flow chart yet): `gallery/t32_nilpotency/` = index + four `canvas2d_*` pages (square-law 128 | 128 grid at d = 2/4/8/16; the detector Δ(w) = w·𝟏 with a live 20,000-word test; primes → Hyperwebster address → 32-bit word, with the chance baseline beside the count; the zero-divisor pair matrix). Data baked by `build_data.py` from the Python engine; every page self-checks its JS port against it on load. The self-check caught a real fault on first run (big integers in the baked JSON lost precision; addresses now baked as strings). Measured while building: the algebra is commutative at d = 2, 4, 8 (my draft text said otherwise; corrected, tested). Launch: `gallery/t32_nilpotency/serve_gallery.sh`.
- 2026-11-26 · `t32_nilpotency` 0.120 (propagation turned up context, so the engine was updated again, as the process intends): the repository-wide sweep found that the "70 % baseline" for the gap primes was an observed rate, not chance. Added `nilpotency_window`, `matched_prime_control` and the registry equation `nilpotency_control`; 14 tests. Measured: random words 49.6 % nilpotent; Hyperwebster words of 2..100000 49.9 % (primes 49.1 %, composites 50.0 %); the prime excess lives in two-digit numbers (17/21 vs 29/69); prime-matched P(5 of 5) = 0.127. Propagated to Ainulindale wiki 78 §6 and ledger X-60…X-62, FermatMonster, TuringStack and FourthAgePapers/CryptoVulnerability (`sha1_demonstration.md` still said "global annihilator" and "zero-ideal"), GenerationalLineage (name collision), the gallery (control on the primes page, an About panel on every page), the central index, and `.github/workflows/docs.yml` (the gallery and the flow charts are now published; `docs/api` regenerated). Flow chart: `tools/flowchart.py` now lays charts out left to right by call depth; `docs/flowcharts/t32_nilpotency_flow.svg` is the final chart for this engine (others first-pass). Paper: `paper/make_paper.py` draft 2 adds §3.2 (`constants`) and §3.3 (`t32_nilpotency`).
- Proposed, not built (visuals are discussed first): a fifth page, primes against composites by decimal length with the two-digit table of 90 numbers, to show where the excess lives.
