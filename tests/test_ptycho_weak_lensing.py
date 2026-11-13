"""The Ptycho-Weak-Lensing engine: spin-2 kernel, closed-form halo, KS round trip, nulls, calibration, ptychographic gaps, polarization."""
import numpy as np
import pytest

from ValaQuenta.modules.ptycho_weak_lensing import maths as M


def test_verify_checks():
    v = M.verify()
    assert v["|D| = 1 for k ≠ 0"] is True
    assert v["Gaussian halo: γ_t = κ̄(<r) − κ (max |err|)"] < 3e-3
    assert v["cross component γ_× ≈ 0 (rms)"] < 1e-4
    assert v["KS round trip, κ_E error after removing the mass sheet (rms)"] < 1e-3
    assert v["round trip B-mode (rms)"] < 1e-3
    assert v["mass-sheet: γ blind to a constant added to κ (max |Δγ|, unpadded)"] < 1e-12
    assert v["potential-born polarization is pure E (|B|/|E| rms)"] < 1e-3
    assert abs(v["calibration: (m recovered − m injected) in sigma"]) < 4


def test_nfw_centre_and_one():
    k = M.nfw_kappa((65, 65), (32, 32), 0.2, 10.0)
    assert k[32, 32 + 10] == pytest.approx(2 * 0.2 / 3, rel=1e-3)      # x = 1
    assert k[32, 33] > k[32, 40] > k[32, 62]                            # monotone in r


def test_efficiency_and_sigma_crit():
    assert M.lensing_efficiency(0.3, 0.2) == 0.0
    assert 0 < M.lensing_efficiency(0.3, 0.8) < M.lensing_efficiency(0.3, 2.0) < 1
    assert M.sigma_crit(0.3, 1.0) > 0


def test_rotation_null_moves_lens_to_B():
    n = 96; kt = M.merging_cluster(n); cat = M.mock_catalogue(kt, 12.0, rng=np.random.default_rng(1))
    kE, kB = M.ks_map(cat, 2.0); kE45, kB45 = M.ks_map(M.rotate45(cat), 2.0)
    assert M.compare_maps(kt, kE)["corr"] > 0.7
    assert abs(M.compare_maps(kt, kE45)["corr"]) < 0.3
    assert M.compare_maps(kt, kB45)["corr"] > 0.6


def test_ptycho_fills_gaps_better_than_naive():
    n = 128; kt = M.merging_cluster(n); W = M.tile_windows(n, 48, 40, taper=6)
    data = M.simulate_pointings(kt, W, 12.0, seed=2, skip=(1, 4, 6))
    cov = sum(d["count"] for d in data) > 0.6
    kn, _ = M.naive_mosaic(data); kp, hist, _ = M.ptycho_reconstruct(data, n_iter=40)
    cn = M.compare_maps(kt, M.gauss_smooth(kn, 1.0), cov); cp = M.compare_maps(kt, kp, cov)
    assert hist[-1] < hist[0]
    assert cp["corr"] > cn["corr"] + 0.02 and cp["rms"] < cn["rms"]


def test_modulus_sign_ambiguity():
    n = 96; kt = M.merging_cluster(n); mod = np.abs(M.kappa_to_gamma(kt))
    k, res = M.modulus_ptycho(mod, mod.copy(), n_iter=150)
    assert res[-1] < res[0]
    c = M.compare_maps(kt, k)["corr"]; assert abs(c) > 0.6          # the global sign is not determined by |γ|
    k2, _ = M.modulus_ptycho(mod, -mod, n_iter=150); assert M.compare_maps(kt, k)["corr"] == pytest.approx(-M.compare_maps(kt, k2)["corr"], abs=1e-6)


def test_registered_module_runs():
    from ValaQuenta.modules.ptycho_weak_lensing import PtychoWeakLensingModule
    m = PtychoWeakLensingModule(); assert m.name == "ptycho_weak_lensing"
    r = m.run("verify", {})["result"]; assert r["|D| = 1 for k ≠ 0"] is True
    assert {e.name for e in m.formulary()} >= {"verify", "forward", "reconstruct", "null_tests", "calibrate", "ptycho", "modulus", "polarization", "efficiency"}
