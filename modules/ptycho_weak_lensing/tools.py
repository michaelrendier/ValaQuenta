"""
ValaQuenta.modules.ptycho_weak_lensing.tools
============================================
THE PTYCHO-WEAK-LENSING ENGINE.  Module Tools (EquationModule registry contract:
formulary(), run(), viewer_data(), shell_commands()).

Weak lensing is a direct linear inversion of a spin-2 field (no lost phase); ptychography enters through the
overlapping pointings (probe windows) that jointly constrain one real field κ, and through the intensity-only
variant where the orientation of the shear is lost.  Polarization (Q+iU) is a second, separate spin-2 field
that goes through the same E/B machinery.

Version: 0.2 (adds the pixel pipeline: PSF from stars, PSF-corrected shapes, simulation and calibration; see shapes.py)
"""
from typing import Dict, List, Any
import numpy as np

from ...engine.registry import EquationModule, Equation
from . import maths as M
from . import shapes as SH


def _s(x):
    return float(x) if isinstance(x, (np.floating, float, int)) else x


def _forward(kappa_s=0.18, r_s=10.0, n=128):
    k = M.nfw_kappa((n, n), (n / 2, n / 2), kappa_s, r_s, 1.0, r_cut=0.45 * n)
    g = M.kappa_to_gamma(k); gt, gx, r = M.tangential_cross(g, (n / 2, n / 2)); mu = M.magnification(k, g)
    edges = np.array([2, 5, 10, 20, 40]); prof = M.radial_profile(gt, r, edges)
    return {"kappa_peak": float(k.max()), "gamma_t_profile_r=2,5,10,20,40": [round(float(v), 5) for v in prof],
            "gamma_x_rms": float(np.sqrt(np.mean(gx[(r > 3) & (r < 40)] ** 2))), "max_magnification": float(np.nanmax(np.abs(mu)))}


def _reconstruct(n_per_pix=12.0, smooth=2.0, seed=1):
    n = 128; kt = M.merging_cluster(n); rng = np.random.default_rng(seed)
    cat = M.mock_catalogue(kt, n_per_pix, rng=rng); kE, kB = M.ks_map(cat, smooth)
    r = M.compare_maps(kt, kE); r["B_mode_rms"] = float(np.sqrt(np.mean(kB ** 2))); r["N_galaxies"] = len(cat["e"]); return r


def _null_tests(n_per_pix=12.0, smooth=2.0, seed=1):
    n = 128; kt = M.merging_cluster(n); rng = np.random.default_rng(seed); cat = M.mock_catalogue(kt, n_per_pix, rng=rng)
    kE, kB = M.ks_map(cat, smooth); kE45, kB45 = M.ks_map(M.rotate45(cat), smooth); kEs, _ = M.ks_map(M.shuffle_orientation(cat), smooth)
    return {"signal corr": M.compare_maps(kt, kE)["corr"], "rot45: corr of κ_E with truth": M.compare_maps(kt, kE45)["corr"],
            "rot45: κ_B recovers the lens": M.compare_maps(kt, kB45)["corr"], "shuffled orientation: corr": M.compare_maps(kt, kEs)["corr"],
            "B-mode rms (should be at the noise floor)": float(np.sqrt(np.mean(kB ** 2))), "noise floor rms": float(np.sqrt(np.mean(kEs ** 2)))}


def _pixel_shapes(seed=3):
    return SH.verify_shapes(seed)


def _pixel_field(n=192, density=0.02, min_sep=20.0, seed=5):
    rng = np.random.default_rng(seed); kt = M.merging_cluster(n)
    cat = SH.isolated_subset(M.mock_catalogue(kt, density, sigma_e=0.26, rng=rng), min_sep)
    psf = SH.psf_gaussian(25, 1.8, 0.08, 0.03); img, nz = SH.render_field(cat, psf, 30.0, rng=rng)
    m = SH.measure_image(img, np.c_[cat["x"], cat["y"]], psf, nz, size=25)
    from scipy.spatial import cKDTree
    d, j = cKDTree(np.c_[cat["x"], cat["y"]]).query(np.c_[m["x"], m["y"]]); et = cat["e"][j]
    return {"isolated galaxies": len(cat["e"]), "fits accepted": m["ok"],
            "corr(ε₁ measured, true)": float(np.corrcoef(et.real, m["e"].real)[0, 1]), "slope ε₁ (Gaussian model, exponential truth)": float(np.polyfit(et.real, m["e"].real, 1)[0]),
            "rms difference per component": float(np.sqrt(np.mean(np.abs(et - m["e"]) ** 2) / 2))}


def _ptycho(n_per_pix=12.0, gaps=(1, 4, 6), n_iter=60, tile=48, step=40, seed=2):
    n = 128; kt = M.merging_cluster(n); W = M.tile_windows(n, tile, step, taper=6)
    data = M.simulate_pointings(kt, W, n_per_pix, seed=seed, skip=tuple(gaps))
    cov = sum(d["count"] for d in data) > 0.05 * n_per_pix
    kn, _ = M.naive_mosaic(data); kp, hist, bl = M.ptycho_reconstruct(data, n_iter=n_iter)
    return {"pointings": len(W), "observed": len(data), "covered fraction": float(cov.mean()),
            "naive mosaic (corr, rms)": (M.compare_maps(kt, M.gauss_smooth(kn, 1.0), cov)["corr"], M.compare_maps(kt, M.gauss_smooth(kn, 1.0), cov)["rms"]),
            "ptychographic (corr, rms)": (M.compare_maps(kt, kp, cov)["corr"], M.compare_maps(kt, kp, cov)["rms"]),
            "chi2 first/last": (hist[0], hist[-1]), "overlap error": M.overlap_error(data), "B-mode leak rms": bl}


def _modulus(n_iter=300):
    n = 128; kt = M.merging_cluster(n); mod = np.abs(M.kappa_to_gamma(kt)); out = {}
    for name, k0 in (("start = |gamma|", mod), ("start = flat +0.05", np.full((n, n), 0.05)), ("start = random", np.random.default_rng(1).normal(0, 0.1, (n, n)))):
        k, res = M.modulus_ptycho(mod, k0, n_iter=n_iter); out[name] = {"corr(kappa)": M.compare_maps(kt, k)["corr"], "corr(-kappa)": M.compare_maps(-kt, k)["corr"], "data residual": res[-1]}
    return out


def _polarization(seed=1):
    n = 128; rng = np.random.default_rng(seed); kt = M.merging_cluster(n)
    phi = M.gauss_smooth(rng.normal(size=(n, n)), 6.0); Q = M.polarization_from_potential(phi)
    E, B = M.eb_decompose(Q); g = M.kappa_to_gamma(kt); Eg, Bg = M.eb_decompose(g)
    return {"pol E/B rms (potential-born)": float(np.sqrt(np.mean(B ** 2)) / np.sqrt(np.mean(E ** 2))),
            "shear E/B rms (lens)": float(np.sqrt(np.mean(Bg ** 2)) / np.sqrt(np.mean(Eg ** 2))),
            "corr(shear E, polarization E) independent fields": M.field_correlation(Eg, E)}


class PtychoWeakLensingModule(EquationModule):
    """The Ptycho-Weak-Lensing engine."""

    @property
    def name(self): return "ptycho_weak_lensing"

    @property
    def display_name(self): return "Ptycho-Weak-Lensing (shear, mass map, pointings, polarization)"

    @property
    def version(self): return "0.2"

    @property
    def description(self):
        return ("Weak gravitational lensing as a spin-2 inverse problem. Forward: kappa -> psi -> gamma -> g -> epsilon -> galaxy catalogue "
                "(NFW / Gaussian halos, flat LCDM efficiency). Inverse: Kaiser-Squires with the reduced-shear iteration, E/B decomposition, "
                "the 45-degree rotation and shuffle nulls, shear calibration (m, c). Ptychographic part: overlapping pointings are the probe "
                "windows, the object is one real field kappa with B = 0, the iteration is ePIE/Kaczmarz over pointings; an intensity-only "
                "(modulus) Gerchberg-Saxton variant is the genuine phase-retrieval case. Polarization (Q+iU) is a second spin-2 field through "
                "the same E/B machinery. Built so a calculated mass map can be matched against published shear / DM maps as a control.")

    @property
    def confidence_floor(self): return "THEORETICAL"

    @property
    def process_description(self):
        return ("Simulates a lens, observes it through overlapping pointings with shape noise, recovers the mass map by Kaiser-Squires and by "
                "a ptychographic iteration, and checks it against E/B, rotation, calibration and overlap nulls.")

    def formulary(self) -> List[Equation]:
        def eq(name, display, latex, radian, conf, params, fn, process):
            return Equation(name=name, display=display, latex=latex, radian_form=radian, confidence=conf, code_verified=True,
                            params=params, compute=fn, display_options=["text"], process=process)
        return [
            eq("verify", "THE HONEST CHECKS: |D|=1, Gaussian halo gamma_t, KS round trip, mass sheet, pure-E polarization, calibration",
               r"|D|{=}1;\ \gamma_t=\bar\kappa(<r)-\kappa;\ \hat\kappa=D^*\hat\gamma", "all derived; a mismatch is a bug, not a result",
               "ESTABLISHED", [], lambda: M.verify(), "Runs the exact self-checks of the lensing algebra against closed-form results."),
            eq("forward", "FORWARD: NFW halo -> shear profile, magnification",
               r"\nabla^2\psi=2\kappa;\ \gamma=D\kappa", "gamma_x = 0 for an axisymmetric halo", "ESTABLISHED", ["kappa_s", "r_s", "n"],
               lambda kappa_s=0.18, r_s=10.0, n=128: _forward(kappa_s, r_s, n), "Builds the projected NFW convergence and returns its tangential shear profile."),
            eq("reconstruct", "INVERSE: mock catalogue -> Kaiser-Squires mass map vs truth",
               r"\hat\kappa_E+i\hat\kappa_B=D^*\hat\gamma", "mass-sheet degeneracy: the mean of kappa is not measured", "ESTABLISHED",
               ["n_per_pix", "smooth", "seed"], lambda n_per_pix=12.0, smooth=2.0, seed=1: _reconstruct(n_per_pix, smooth, seed),
               "Draws shape-noise-limited galaxies from a synthetic merger, inverts, reports correlation and B-mode leak."),
            eq("null_tests", "CONTROLS: rotate 45 degrees, shuffle orientations, B-mode floor", r"\epsilon\to i\epsilon\Rightarrow\kappa_E\leftrightarrow\kappa_B",
               "a real lens signal moves to the B channel under a 45 degree rotation and vanishes under shuffling", "ESTABLISHED",
               ["n_per_pix", "smooth", "seed"], lambda n_per_pix=12.0, smooth=2.0, seed=1: _null_tests(n_per_pix, smooth, seed),
               "Applies the standard null tests to one catalogue and reports each channel against the noise floor."),
            eq("calibrate", "CALIBRATION: inject constant shear and (m, c), recover",
               r"\epsilon_{meas}=(1+m)\epsilon+c", "statistical error sets the smallest detectable m", "ESTABLISHED", [],
               lambda: M.calibrate_shear(), "Recovers a known multiplicative shear bias from a catalogue of random galaxies."),
            eq("pixel_shapes", "FROM PIXELS: PSF from stars, PSF forward-modelled, shear calibration (exponential truth, Gaussian model)",
               r"\epsilon_{meas}=(1+m)\,g+c;\ \text{PSF}\otimes\text{Gaussian}(\epsilon)\ \text{fitted}", "ignoring an anisotropic PSF fakes a shear; the model-bias m is measured by simulation, not assumed",
               "THEORETICAL", ["seed"], lambda seed=3: _pixel_shapes(seed),
               "Fits a polynomial PSF to simulated stars, measures zero-shear galaxies with and without the PSF, and calibrates the estimator with rotated-pair simulations."),
            eq("pixel_field", "FROM PIXELS: render a lensed field, measure every shape with the PSF, compare with the truth",
               r"\hat\epsilon\to\text{catalogue}\to\mathrm{KS}", "the output catalogue is the dict ks_map takes; crowded fields must be thinned or deblended first",
               "THEORETICAL", ["n", "density", "min_sep", "seed"],
               lambda n=192, density=0.02, min_sep=20.0, seed=5: _pixel_field(n, density, min_sep, seed),
               "Renders isolated galaxies of a synthetic cluster through an anisotropic PSF with noise, measures them, and compares with the input ellipticities."),
            eq("ptycho", "PTYCHOGRAPHY: overlapping pointings (with gaps) -> kappa, vs the naive mosaic",
               r"\kappa\leftarrow\kappa+\alpha\,\mathrm{Re}[D^*M_j(\epsilon_j-\eta_jD\kappa)]/\eta_j",
               "full coverage: same fixed point as KS; with gaps the B=0 object constraint fills the holes", "THEORETICAL",
               ["n_per_pix", "gaps", "n_iter", "tile", "step", "seed"],
               lambda n_per_pix=12.0, gaps=(1, 4, 6), n_iter=60, tile=48, step=40, seed=2: _ptycho(n_per_pix, gaps, n_iter, tile, step, seed),
               "Observes the synthetic cluster through overlapping pointings, reconstructs by ePIE/Kaczmarz, compares with naive stacking on the covered area."),
            eq("modulus", "INTENSITY-ONLY: recover kappa from |gamma| alone (Gerchberg-Saxton)",
               r"\kappa\to\gamma=D\kappa\to|\gamma|\ \text{imposed}\to\kappa=\mathrm{Re}\,D^*\gamma", "global sign of kappa is not determined; uninformed starts stall",
               "THEORETICAL", ["n_iter"], lambda n_iter=300: _modulus(n_iter), "Phase retrieval of the lens from the shear modulus with different starting guesses."),
            eq("polarization", "SECOND FIELD: Q+iU through the same E/B machinery; correlation with shear",
               r"Q+iU=D\,\nabla^2\phi/(-2)", "a potential-born polarization field is pure E; independent of the lens", "THEORETICAL", ["seed"],
               lambda seed=1: _polarization(seed), "Builds a potential-born spin-2 polarization field, takes its E/B, and correlates it with the shear E-mode."),
            eq("efficiency", "SOURCE REDSHIFT: beta = D_ls/D_s and Sigma_crit (flat LCDM)",
               r"\beta=D_{ls}/D_s;\ \Sigma_{cr}=c^2D_s/(4\pi G D_l D_{ls})", "kappa and gamma scale with beta", "ESTABLISHED", ["z_l", "z_s"],
               lambda z_l=0.3, z_s=1.0: {"beta": M.lensing_efficiency(z_l, z_s), "sigma_crit_Msun_per_Mpc2": M.sigma_crit(z_l, z_s)},
               "Returns the lensing efficiency of a source plane behind a lens."),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eqs = {e.name: e for e in self.formulary()}
        if equation_name not in eqs:
            raise KeyError(f"ptycho_weak_lensing has no equation '{equation_name}'")
        eq = eqs[equation_name]
        result = eq.compute(**{k: v for k, v in params.items() if k in eq.params}) if params else eq.compute()
        return {"result": result, "equation": eq, "params": params}

    def viewer_data(self, equation_name: str, params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        out = self.run(equation_name, params)
        return {"mode": display_mode, "equation": equation_name, "text": repr(out["result"])}

    def shell_commands(self) -> Dict[str, Any]:
        return {"lens_verify": M.verify, "lens_ptycho": _ptycho, "lens_reconstruct": _reconstruct, "lens_nulls": _null_tests}
