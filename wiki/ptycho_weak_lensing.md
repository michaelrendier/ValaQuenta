# Engine: Ptycho-Weak-Lensing — shear, mass map, pointings, polarization

**Module:** `modules/ptycho_weak_lensing/` (`maths.py`, `tools.py`, `manifest.json`)
**Class:** `PtychoWeakLensingModule`
**Version:** 0.1 (2026-11-12)
**Confidence floor:** THEORETICAL (status label `THEORETICAL:CALCULATED`; the lensing algebra itself is ESTABLISHED)
**Notebook:** [notebooks/engines/21_ptycho_weak_lensing.ipynb](../notebooks/engines/21_ptycho_weak_lensing.ipynb) · **Proof locale:** `engine/proof_locale/ptycho_weak_lensing.json` · **Ainulindale:** `wiki/132_ptycho_weak_lensing.md`
**Tests:** `tests/test_ptycho_weak_lensing.py` (7)

**Claim.** Weak lensing is a *direct linear inversion of a spin-2 field* (no lost phase: a galaxy shape carries an orientation, so the shear's phase 2φ is measured). Ptychography enters in two places: (1) overlapping **pointings** are probe windows constraining one real field κ — the object constraint is "B-mode = 0" — and the update is ePIE/Kaczmarz; (2) the **intensity-only** variant (|γ| kept, orientation lost) is the genuine phase-retrieval case. Polarization Q+iU is a second spin-2 field through the same E/B operator.

## Mechanism (ESTABLISHED)
∇²ψ = 2κ · γ₁ = ½(ψ₁₁−ψ₂₂), γ₂ = ψ₁₂ · γ̂ = Dκ̂, κ̂ = D*γ̂, D = (k₁²−k₂²+2ik₁k₂)/|k|² (|D| = 1, D(0) := 0) · g = γ/(1−κ) · ε = (ε_s+g)/(1+g*ε_s) · mass-sheet κ → λκ+(1−λ) leaves g unchanged.

## What the engine computes (`formulary`)
`verify` · `forward` (NFW halo → shear profile) · `reconstruct` (Kaiser–Squires + reduced-shear iteration) · `null_tests` (45° rotation, shuffle, B floor) · `calibrate` ((m, c)) · `ptycho` (pointings with gaps) · `modulus` (intensity-only GS) · `polarization` (Q+iU E/B) · `efficiency` (D_ls/D_s, Σ_cr, flat ΛCDM).

## Measured (synthetic merger, 128², NFW pair; all :CALCULATED)
| check | result |
|---|---|
| Gaussian halo γ_t = κ̄(<r) − κ | max error 1.0e-3; γ_× rms 6e-6 |
| KS round trip (mass sheet removed) | 1.5e-4; B-mode 1.1e-4 |
| mass sheet invisible to γ | 4e-16 |
| rotation null | κ_E loses the lens, κ_B holds it (test) |
| potential-born Q+iU | pure E (|B|/|E| 2.8e-5) |
| ptychography, density 12, 3 of 9 pointings missing (covered area) | corr 0.923 vs naive 0.864; rms 0.0174 vs 0.0224 |
| ptychography, density 3, same gaps | corr 0.825 vs naive 0.701 |
| full coverage | **same** as naive (0.926/0.926 at density 12) — one fixed point; at density 3 it is slightly worse (0.776 vs 0.795) |
| modulus-only retrieval | data residual → 5e-4 from every start, but κ recovered only from an informative start (corr 0.80), global sign undetermined, flat/random starts stall — **OPEN** |

## Honest limits
Synthetic data only; no real catalogue yet. The ptychographic gain is a gap-filling/edge-leakage gain from the B = 0 constraint, not new information at full coverage. The modulus variant is not solved. Shape measurement (PSF, calibration bias), photo-z, cluster-member contamination and intrinsic alignments are not modelled. GR does not rotate polarization in the local frame, so Q+iU is an independent probe, not a lensing signal.

## Next
Real-data control (Frontier-Fields / UNCOVER-MARS / Clowe maps), multi-band efficiencies on real source catalogues, a multi-window modulus ptychography (the OPEN item), and a polarization–shear correlator on a real target.
