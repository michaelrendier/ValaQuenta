# Engine: L_(I|O) Photon Path — GR Lensing as the Boundary-Crossing Template

**File:** `modules/l_io_photon_path/maths.py`
**Class:** `LIOPhotonPathModule`
**Claim:** `L_(I|O) - L := -psi(theta)` — the real (curved-metric) light-travel-time functional differs from the flat-space one by exactly the lensing potential. Established weak-lensing GR (Kaiser & Squires 1993 shear inversion, exact FFT Poisson solve) — not a new operator, named to match `Ainulindale/wiki/52`'s language. Zero fitted parameters anywhere in the pipeline.

---

## Origin

`Ainulindale/wiki/52` defined L_(I|O) philosophically: "Photons are not undisturbed paths... The light's path was not clean. The path was L_(I|O)." Two formal targets were left open there: (1) define L_(I|O) formally, distinguishing it from L (stationary action); (4) formalize light bending within L_(I|O). This module answers both using established GR rather than new formalism — the hypothesis that L_(I|O) is not a different operator from L at all, just L computed honestly with the real (curved) metric, sourced by real mass.

## The Mechanism

```
1. kaiser_squires_kappa: kappa_hat(k) = D*(k) . gamma_hat(k)   (exact, Kaiser & Squires 1993 eq 2.2)
2. lensing_potential:    nabla^2 psi = 2 kappa -> psi_hat(k) = -2 kappa_hat(k)/|k|^2   (exact FFT Poisson solve)
3. deflection_field:     alpha = grad(psi)                     (unit conversion only)
4. trace_photon:         beta = theta - alpha(theta)           (lens equation)
5. l_io_deficit:         L_(I|O) - L := -psi(theta)             (Fermat potential term)
```

`theta` = apparent (observed) position, the clean-path endpoint an undeflected photon would trace. `beta` = the true source position implied by the actual bent path. The deviation is computed from real shear data, not asserted.

A boundary-condition fix (`bounded_lensing_pipeline`) tapers the real (non-periodic) field to zero at its edges (Tukey window) and zero-pads before the FFT, then crops after — plain FFT treats input as periodic, and without this the forced wraparound discontinuity injected spurious ~700–1700 arcsec deflections. Fixed as a real bug, not a fit: nothing is adjusted toward an expected outcome, the correction only removes an artifact of assuming periodicity a single finite frame doesn't have.

## Results (real Bullet Cluster JWST F444W shear, BIN=32)

```
deflection_mag:   mean=0.4054″  std=0.1880″  max=1.0802″  median=0.3962″
L_(I|O) - L:      mean=-14.42″  std=14.05″   min=-51.42″  max=23.69″  median=-16.32″
grid_shape: [78, 176]   pixel_scale (coarse): 1.9288″
```
Cited from `BulletCluster/optical/jwst/prepped/l_io/l_io_deficit.json` — not re-derived here, that file is the actual measurement. No quantitative polarization-prediction match is claimed alongside this; that's a separate, qualitative overlay elsewhere, not conflated with this result.

## Boundary Role (2026-07-21)

(I|O)_RB (renamed from H_hat_RB) defines *where* a boundary/degenerate locus is — the zero-divisor crossing, corrected this session to be the **origin** a pathway is measured outward from, not an endpoint (see `project_holcus_zero_divisors_quote` memory). This module is the general template for *how* you actually cross such a boundary once it's defined: `kaiser_squires_kappa`'s `kappa_hat[0,0] = 0.0` is not a lensing-specific special case, it's the reusable pattern — at a transform's own degenerate point, neither let the direct formula blow up (`1/|k|^2 → ∞`) nor silently exclude it; assign the value explicitly, by a stated convention, and say why (here: the mean isn't observable from shear alone). That's interpretive framing laid on top of established GR math — it doesn't change any equation above.

## CONJECTURE, explicitly not established — the zeta-pole category match

Raised and fought over directly (2026-07-21): the Riemann zeta function's simple pole at s=1 (`zeta(s) ~ 1/(s-1) + gamma`, a finite residue extracted at the divergent point) and its functional equation (`zeta(s) = 2^s pi^(s-1) sin(pi s/2) Gamma(1-s) zeta(1-s)`, an s↔1-s involution fixed at Re(s)=1/2) are the *same category* of construction as this module's k=0-zeroing and theta/beta pair — both regularize a transform at its own singular point by explicit convention, both are involution-shaped with a fixed locus. That is a structural resonance, checked and stated plainly. It is **not** a claim that zeta(s) is derivable as a parameter setting of `kaiser_squires_kappa`/`lensing_potential`'s actual functional form — that derivation does not exist. Flagged so it isn't lost, not asserted as solved.

## What This Is, and Isn't

**Is:** established weak-lensing GR, zero fitted parameters, already run against real Bullet Cluster JWST shear with the cited result above. The k=0-zeroing convention is a genuine, reusable template for handling a degenerate/singular point of any transform by explicit assignment rather than blowup or omission — already reused conceptually this session for the prime-factor-path question and the Noether-Information-into-the-sedenion-shell gap.

**Isn't:** a claim that gravitational lensing and the zero-divisor locus are the same physical mechanism — the boundary-crossing role is an interpretive layer on established GR, the usual ESTABLISHED-math-plus-THEORETICAL-reading pattern used throughout this codebase. The zeta-function connection is explicitly CONJECTURE-tier.

See also: `Ainulindale/wiki/82_l_io_photon_path.md` (cross-repo companion page), `notebooks/core/18_l_io_photon_path.ipynb`.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| L_(I|O) as the boundary-crossing template (photon path) | the L_(I|O) traversal through the (I|O) boundary | 1 · SIGN | MINGLING | DEFINITIONAL | **FLAGGED** — deficit: the GR boundary-template application (L_(I|O) itself is classical conformal inversion; the hyper-application is the imported claim) |


Calibration: this verdict agrees with the page's stated status (**THEORETICAL**).
