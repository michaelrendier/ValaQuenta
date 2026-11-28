# Propagation ledger

Every downstream file ValaQuenta's tools changed or skipped. Working tree only; nothing committed from here.

- 2026-11-25 `h_rb_hat` d*-block applied to Ainulindale/PROVENANCE.md
- 2026-11-25 `h_rb_hat` d*-block applied to Ainulindale/wiki/18_fermat_lattice.md
- 2026-11-25 `h_rb_hat` d*-block applied to Ainulindale/wiki/131_riemann_canonical_maths.md
- 2026-11-25 `h_rb_hat` d*-block applied to Ainulindale/wiki/123_sigma_rb_mass_gap_calibration.md
- 2026-11-25 `h_rb_hat` d*-block applied to Ainulindale/wiki/14_redblue_hamiltonian.md
- 2026-11-25 `h_rb_hat` d*-block applied to Ainulindale/wiki/70_precession_stroke_oblique_crank_trine.md
- 2026-11-25 `h_rb_hat` d*-block applied to Ainulindale/AgeThird/D-CS_Memory_Edit_TODO.md
- 2026-11-25 `h_rb_hat` d*-block applied to Ainulindale/AgeThird/VAPMIP_Paper.md
- 2026-11-25 `h_rb_hat` d*-block applied to FourthAgePapers/EquationSpace/06_results_facets.md
- 2026-11-25 `h_rb_hat` d*-block applied to GenerationalLineage/wiki/Concepts-What-It-Was-Built-To-Do.md
- 2026-11-25 `h_rb_hat` d*-block applied to PtolemyDesktop/MONAD.md
- 2026-11-25 `h_rb_hat` d*-block applied to PtolemyDesktop/wiki/RedBlueHamiltonian.md
- 2026-11-25 `h_rb_hat` d*-block applied to RiemannHypothesisProof/docs/RIEMANN_CANONICAL_MATHS.md

## 2026-11-26 · `t32_nilpotency` 0.110 / 0.120 (engine 3) — propagated by hand (the d*-block tool does not apply: the engine does not use d*)
- `FourthAgePapers/FermatMonster/engine/fermat_monster_engine.py`: `t32_nilpotency_check` now reports `random_word_baseline_pct` and `gap_primes_prime_matched_control` (imports `matched_prime_control`).
- `TuringStack/sha1_demonstration.md`, `FourthAgePapers/CryptoVulnerability/sha1_demonstration.md`: "global annihilator" and "closed zero-ideal" corrected to the null subalgebra / detector statement, retraction kept in the text.
- `TuringStack/sha256_iv_zero_divisor_demo.py` (comments), `TuringStack/fermat_sedenion_test.py`, `FourthAgePapers/CryptoVulnerability/fermat_sedenion_test.py`: pointer to the maintained copy.
- `GenerationalLineage/engine/toolsets/t32_nilpotency.py`, `wiki/T32-Nilpotency.md`: name-collision note (path nilpotent vs word nilpotent).
- `Ainulindale/wiki/78_t32_nilpotency.md` (§5, §6), `01_overview.md` (version), `135_engine_findings_ledger.md` (X-60, X-61, X-62).
- Checked, no change needed: `SedenionSpectralRelativity` (no use), `RiemannHypothesisProof` (names only), `PtolemyDesktop` (no use of the engine), `VAPMIP` Tuning-the-Engine 19 (never edited; X-60 is its correction), `ContextPlease` hist_wiki (archives).
- Galleries: `gallery/t32_nilpotency/` registered in the central index (`ContextPlease/claude/galleries/build_index.py`, `michaelrendier.github.io/index.html`); `.github/workflows/docs.yml` now copies the gallery and the flow charts into the published site.

## 2026-11-27 · `hypergon_constructibility` 0.200 and `bell_curve` 1.2 (n-ball / Gamma)
- `Ainulindale`: wiki 77 (§3 note, new §6 Niemeier gap), ledger X-64 to X-67, `TODO.md` and wiki 138 (n* computed; BAO reading stays THEORETICAL).
- `FourthAgePapers/FermatMonster/engine/fermat_monster_engine.py`: the proof text in `fermat_n_shape_map` replaced by the four-line proof; status of the N-shape reading stated.
- Gamma / n-ball pointer added to the wiki pages of the ValaQuenta engines that use Gamma: `circle_atlas`, `prime_gauge_field`, `add_scale_sign`, `pi_derivations`, `singularity_null`, `tier7_cosmos`, `relativity`, `zeta_uns_path` (and the full section in `bell_curve`).
- Galleries: `gallery/hypergon_constructibility/` in the central index (`ContextPlease/claude/galleries/build_index.py`) and in `.github/workflows/docs.yml`.
- Not yet touched, by design: the `RiemannHypothesisProof` TODO "N-shape peak vs n* = 5.257" (now answered as a computed value; the algebraic connection is still to be derived), `FourthAgePapers/NBallTransformer` (no text to update; notebooks only), `GenerationalLineage` and the other repositories that call Gamma in their own code (the pointer is the engine in ValaQuenta).

## 2026-11-27 · `box_kite` 0.3 (the labelled group)
- `Ainulindale`: wiki 84 (the group sentence), ledger X-68.
- Checked, no change needed: every other mention of PSL(2,7) in the active repositories uses it as Aut(Fano) = GL(3,2), which remains correct (it is the quotient). Not edited, by design: the verbatim engine snapshots under `FourthAgePapers/ScalarContextPropagation/repo_appendix/box_kite_engine/` and `VAPMIP/FourthAgePaper/...` (appendix copies), and Tuning-the-Engine 25 (never edited); they still carry the earlier sentence.

## 2026-11-27 · `box_kite` 0.4 (visuals, the split result)
- `Ainulindale`: ledger X-69 (non-split; associator octonion block not flat); wiki 84 gains a pointer to the gallery.
- Galleries: `gallery/box_kite/` in the central index (`ContextPlease/claude/galleries/build_index.py`, port 8793) and in `.github/workflows/docs.yml`.
- Still not edited, by design: the verbatim engine snapshots (`ScalarContextPropagation/repo_appendix/box_kite_engine/`, VAPMIP appendix copy) and Tuning-the-Engine; the 0.3 sentence in them stands as a dated snapshot.

## 2026-11-27 · `add_scale_sign` 0.2 (exact inverse)
- `GenerationalLineage/engine/add_scale_sign.py`: same `__invert__` fix (Fractions stay Fractions); its 179 tests pass.
- `Ainulindale`: ledger X-70.
- Checked by `tools/propagate.py`: the other downstream mentions (wiki 107, 95, SFR wiki, VAPMIP Ring-Circle-Operators) describe the datatype and do not quote the manifest's exactness claim; not edited. Verbatim snapshots and Tuning-the-Engine are not edited, by design.

## 2026-11-27 · `add_scale_sign` 0.3 (visuals, quadrant labels)
- `Ainulindale`: ledger X-71; wiki 107 gains a pointer to the gallery.
- Galleries: `gallery/add_scale_sign/` in the central index (`ContextPlease/claude/galleries/build_index.py`, port 8794) and in `.github/workflows/docs.yml`.
- `GenerationalLineage/engine/add_scale_sign.py` has no `to_smith`, so the quadrant fix does not apply there (checked by grep).

## 2026-11-27 · `bracketing_firing_order` 0.2 (the four orderings)
- `GenerationalLineage/engine/bracketing_firing_order.py` (+ `tests/test_firing_plans.py`, `wiki/Firing-Plans.md`): A–D, `mode_counts`, `evolve_operator`, `evolve_value`.
- `SedenionSpectralRelativity/firing_plan.py` is the origin and is not edited; the engine of record is now `ValaQuenta/modules/bracketing_firing_order`.
