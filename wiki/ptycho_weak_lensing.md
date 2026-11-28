# Engine: Ptycho-Weak-Lensing — shear, mass map, pointings, polarization

**Module:** `modules/ptycho_weak_lensing/` (`maths.py`, `shapes.py`, `tools.py`, `manifest.json`)
**Class:** `PtychoWeakLensingModule`
**Version:** 0.2 (0.1: 2026-11-12; 0.2: 2026-11-28, the pixel pipeline)
**Confidence floor:** THEORETICAL (status label `THEORETICAL:CALCULATED`; the lensing algebra itself is ESTABLISHED)
**Notebook:** [notebooks/engines/21_ptycho_weak_lensing.ipynb](../notebooks/engines/21_ptycho_weak_lensing.ipynb) · **Proof locale:** `engine/proof_locale/ptycho_weak_lensing.json` · **Ainulindale:** `wiki/132_ptycho_weak_lensing.md`
**Tests:** `tests/test_ptycho_weak_lensing.py` (7), `tests/test_ptycho_weak_lensing_shapes.py` (11)

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

## The pixel pipeline (version 0.2, `shapes.py`, 2026-11-28)
Cody, 2026-11-27: the ptychography is an attempt to map the dark matter, so weak lensing is required, and where a target has no weak-lensing catalogue we build our own. The catalogue-level engine above assumed the galaxy ellipticities; `shapes.py` is the step from **pixels to shear**, with the point-spread function (PSF) forward-modelled and not subtracted:

| step | function | what it does |
|---|---|---|
| the PSF from stars | `psf_fit_polynomial`, `psf_at` | each pixel of the star stamps is a polynomial of (x, y), order 0–3; evaluated anywhere, unit sum. A shipped PSF file (Euclid) or a modelled one (JWST) goes in through the same interface |
| a shape | `fit_shape` | an elliptical Gaussian convolved with the local PSF is fitted to the stamp (noise-weighted least squares); (ε₁, ε₂) and a Jacobian error come out, in the engine's convention ε = (a−b)/(a+b)·e²ⁱᵠ |
| a catalogue | `measure_image` | measures every galaxy of a square image and returns the dict `mock_catalogue` returns, so `ks_map` takes it unchanged |
| simulation | `simulate_stamp`, `render_field` | a galaxy (exponential or Gaussian) with intrinsic ε_s, sheared by g through `apply_shear`, convolved with the PSF, plus noise; or a whole field from a catalogue |
| calibration | `rotated_pair_shear`, `calibrate_shear_from_pixels` | each intrinsic shape is paired with its 90° twin so the shape noise cancels; (m, c) from simulations at known shears |
| diagnostics | `psf_leakage`, `shear_estimate`, `isolated_subset` | the PSF leakage α of galaxy on PSF ellipticity; the weighted mean ε as ĝ; thinning of crowded fields (no deblending here) |

**Measured (:CALCULATED, `verify_shapes`, equation `pixel_shapes`, `pixel_field`):** a PSF with ε₁ = 0.10 fakes a mean ε₁ = +0.040 in zero-shear galaxies when ignored and −0.0007 when forward-modelled; a position-dependent PSF recovered from 40 stars to 0.4% of its peak; an exponential disc fitted by a Gaussian underestimates the shear: m = −0.07 ± 0.015 (the bias is measured, not assumed, and is what the calibration is for); an isolated-galaxy field through an anisotropic PSF and noise gives ε₁ correlation 0.999 with the input and slope 0.93, rms difference 0.02.

**What it explains.** The Pillars of Creation shear check (BulletCluster, 2026-11-20) found 54% of objects aligned along the mosaic's pixel axis: the signature of uncorrected PSF and detector anisotropy. `BulletCluster/scaffolds/overlays/shear_measure.py` takes simple second moments without a PSF; this module is the correction route, not yet wired in.

**What is still to build (named, not hidden).** Detection and deblending (a blended galaxy is one object here: crowded fields must be thinned or deblended upstream); multi-exposure joint fitting (a stack hides the per-exposure PSF and detector orientation, so the inputs should be per-exposure frames: Euclid VIS stacked frames ship a PSF file, JWST `cal` frames need a PSF model); source selection by colour or redshift; intrinsic alignments; the survey-dependent additive terms; and a non-Gaussian galaxy model (a Sérsic or bulge+disc fit would shrink m). The real-data control is the Bullet Cluster against the published Lenstool model (z = 5.6 direction agreement already measured).

## Next
Real-data control (Frontier-Fields / UNCOVER-MARS / Clowe maps), multi-band efficiencies on real source catalogues, a multi-window modulus ptychography (the OPEN item), and a polarization–shear correlator on a real target.
