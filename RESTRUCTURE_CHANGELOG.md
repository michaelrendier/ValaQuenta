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
