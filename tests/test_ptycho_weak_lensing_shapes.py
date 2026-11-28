"""The pixel pipeline of the Ptycho-Weak-Lensing engine (shapes.py): PSF from stars, PSF-corrected shapes, simulation, calibration, and the hand-off to ks_map."""
import numpy as np
import pytest
from scipy.spatial import cKDTree

from ValaQuenta.modules.ptycho_weak_lensing import maths as M
from ValaQuenta.modules.ptycho_weak_lensing import shapes as S


def test_shape_matrix_is_area_preserving_and_has_the_right_axis_ratio():
    for e1, e2 in ((0.0, 0.0), (0.3, 0.0), (0.1, -0.4)):
        A = S.shape_matrix(e1, e2)
        assert np.linalg.det(A) == pytest.approx(1.0)
        ev = np.linalg.eigvalsh(A)
        q = ev.min() / ev.max()                                  # axis ratio b/a = (1-|e|)/(1+|e|)
        assert q == pytest.approx((1 - np.hypot(e1, e2)) / (1 + np.hypot(e1, e2)))


def test_gaussian_profile_has_the_requested_flux_and_ellipticity():
    X, Y = S.stamp_grid(41)
    img = S.gaussian_profile(X, Y, 3.0, 0.0, 0.0, 3.0, 0.25, 0.1)
    assert img.sum() == pytest.approx(3.0, rel=1e-3)
    qxx, qyy, qxy = (np.sum(img * X * X), np.sum(img * Y * Y), np.sum(img * X * Y))
    chi = complex(qxx - qyy, 2 * qxy) / (qxx + qyy)               # distortion χ = 2ε/(1+|ε|²)
    eps = chi / (1 + np.sqrt(1 - abs(chi) ** 2))
    assert eps == pytest.approx(complex(0.25, 0.1), abs=2e-3)


def test_the_ellipticity_convention_matches_maths_apply_shear():
    """A circular source sheared by g has ε = g; an elliptical one follows (ε_s + g)/(1 + g* ε_s)."""
    es, g = 0.2 + 0.1j, 0.05 - 0.03j
    e = complex(M.apply_shear(np.array([es]), np.array([g]))[0])
    assert e == pytest.approx((es + g) / (1 + np.conj(g) * es))
    assert complex(M.apply_shear(np.array([0j]), np.array([g]))[0]) == pytest.approx(g)


def test_a_position_dependent_psf_is_recovered_from_stars():
    rng = np.random.default_rng(0)
    pos = rng.uniform(0, 100, (40, 2))
    stars = [S.psf_gaussian(25, 1.6, 0.02 + 0.0006 * x, -0.0004 * y) + rng.normal(0, 2e-4, (25, 25)) for x, y in pos]
    model = S.psf_fit_polynomial(pos, stars, order=1)
    truth = S.psf_gaussian(25, 1.6, 0.02 + 0.0006 * 77, -0.0004 * 12)
    assert np.abs(S.psf_at(model, 77, 12) - truth).max() / truth.max() < 0.02
    assert S.psf_at(model, 77, 12).sum() == pytest.approx(1.0)


def test_ignoring_an_anisotropic_psf_fakes_a_shear_and_the_forward_model_removes_it():
    rng = np.random.default_rng(1)
    psf = S.psf_gaussian(25, 1.8, 0.10, 0.0)
    delta = np.zeros((25, 25)); delta[12, 12] = 1.0
    naive, corr = [], []
    for _ in range(30):
        es = complex(rng.normal(0, 0.2), rng.normal(0, 0.2))
        pr = []
        for s in (es, -es):
            st, nz, _ = S.simulate_stamp(0j, s, psf, 40.0, 2.5, 1.0, "gauss", rng, size=25)
            a, b = S.fit_shape(st, delta, nz), S.fit_shape(st, psf, nz)
            pr.append((complex(a["e1"], a["e2"]), complex(b["e1"], b["e2"])))
        naive.append(0.5 * (pr[0][0] + pr[1][0])); corr.append(0.5 * (pr[0][1] + pr[1][1]))
    assert np.mean(np.real(naive)) > 0.02                         # PSF ε₁ = 0.10 leaks into the zero-shear galaxies
    assert abs(np.mean(np.real(corr))) < 0.01                     # forward-modelled: gone


def test_a_known_shear_is_recovered_for_a_gaussian_truth_with_the_gaussian_model():
    psf = S.psf_gaussian(25, 1.8, 0.05, 0.0)
    g = 0.06 - 0.03j
    e, err = S.rotated_pair_shear(g, psf, n_pairs=25, peak_snr=40.0, profile="gauss", rng=np.random.default_rng(2))
    assert abs(e - g) < max(4 * err, 0.01)


def test_calibration_measures_the_model_bias_and_correcting_it_recovers_an_independent_shear():
    psf = S.psf_gaussian(25, 1.8, 0.0, 0.0)
    cal = S.calibrate_shear_from_pixels(psf, g_values=(-0.05, 0.05), n_pairs=25, peak_snr=40.0, profile="exp", rng=np.random.default_rng(3))
    assert -0.25 < cal["m"] < 0.0                                 # a Gaussian model underestimates an exponential disc's shear
    g = 0.05
    e, err = S.rotated_pair_shear(complex(g, 0), psf, n_pairs=25, peak_snr=40.0, profile="exp", rng=np.random.default_rng(4))
    corrected = (e.real - cal["c1"]) / (1 + cal["m"])
    assert abs(corrected - g) < 4 * np.hypot(err, cal["m_err"] * g) + 0.005


def test_the_measured_catalogue_goes_into_ks_map_and_agrees_with_the_truth_ellipticities():
    rng = np.random.default_rng(5)
    n = 192
    kt = M.merging_cluster(n)
    cat = S.isolated_subset(M.mock_catalogue(kt, 0.02, sigma_e=0.26, rng=rng), 20.0)
    psf = S.psf_gaussian(25, 1.8, 0.08, 0.03)
    img, nz = S.render_field(cat, psf, 30.0, rng=rng)
    m = S.measure_image(img, np.c_[cat["x"], cat["y"]], psf, nz, size=25)
    assert m["ok"] > 20 and set(("x", "y", "e", "n", "dx", "sigma_e", "w")) <= set(m)
    d, j = cKDTree(np.c_[cat["x"], cat["y"]]).query(np.c_[m["x"], m["y"]])
    assert d.max() < 1e-9
    et = cat["e"][j]
    assert np.corrcoef(et.real, m["e"].real)[0, 1] > 0.98 and np.corrcoef(et.imag, m["e"].imag)[0, 1] > 0.98
    kE, kB = M.ks_map(m, 4.0)                                      # the dict is what maths.ks_map takes
    assert kE.shape == (n, n) and np.isfinite(kE).all()


def test_isolated_subset_thins_a_crowded_field_and_measure_image_refuses_a_non_square_image():
    cat = {"x": np.array([10.0, 12.0, 40.0]), "y": np.array([10.0, 10.0, 40.0]), "e": np.zeros(3, complex), "n": 64}
    assert len(S.isolated_subset(cat, 5.0)["x"]) == 2
    with pytest.raises(ValueError):
        S.measure_image(np.zeros((32, 48)), [(10, 10)], S.psf_gaussian(9, 1.5), 1.0, size=9)


def test_psf_leakage_finds_an_injected_leak_and_zero_without_one():
    rng = np.random.default_rng(6)
    ep = rng.normal(0, 0.05, 500) + 1j * rng.normal(0, 0.05, 500)
    eg = 0.1 * ep + rng.normal(0, 0.02, 500) + 1j * rng.normal(0, 0.02, 500)
    a, err = S.psf_leakage(eg, ep)
    assert a == pytest.approx(0.1, abs=4 * err)
    a0, err0 = S.psf_leakage(rng.normal(0, 0.02, 500) + 1j * rng.normal(0, 0.02, 500), ep)
    assert abs(a0) < 4 * err0


def test_shear_estimate_is_the_weighted_mean():
    g, err = S.shear_estimate(np.array([0.1 + 0j, 0.3 + 0j]), np.array([1.0, 1.0]))
    assert g == pytest.approx(0.2) and err > 0
