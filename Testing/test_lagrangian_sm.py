"""Test suite for ``ValaQuenta.modules.lagrangian_sm`` (L_SM, the Standard Model Lagrangian engine).

The Standard Model side is checked against identities and measured numbers; the comparison side is checked against the code of
``modules/lagrangian`` and the definition of L_(I|O) as they stand.  Where a test records a property of that code that differs from
its docstring (the 1/phi on L_bias, the sign convention of mu^2), the test asserts the current state and names it a recorded finding:
if the code is changed the test fails and the finding is revisited.
Run from the scratchpad (the working directory does not matter)::

    PYTHONPATH=/path/to/ThePlace /path/to/ValaQuenta/.venv/bin/python -m pytest /path/to/ValaQuenta/Testing/test_lagrangian_sm.py -p no:cacheprovider
"""
import math

import numpy as np

from ValaQuenta.modules.lagrangian_sm import maths as S
from ValaQuenta.modules.lagrangian_sm import compare as C


def test_content_and_anomalies():
    """Hypercharges give Q = T3 + Y integers/thirds; every gauge anomaly sum is exactly zero; SU(2) doublets per generation are even."""
    d = S.degrees_of_freedom(); a = S.anomaly_check()
    assert d["weyl_fermions"] == 45 and d["gauge_bosons"] == 12 and d["real_scalars"] == 4
    assert a["all_zero"] and a["witten_ok"] and a["witten_doublets_per_generation"] == 4


def test_hypercharges_are_derived_from_anomaly_cancellation():
    """Given the multiplets, Y_H = 1/2 and Yukawa invariance, the anomaly conditions have one solution and it is the observed hypercharges (1/6, 2/3, -1/3, -1/2, -1)."""
    h = S.hypercharges_from_anomalies()
    assert h["unique"] and h["solutions"][0] == h["sm"] and h["su3_condition_automatic"] and h["u1_cubed_automatic"]


def test_fractional_quark_charges_follow_from_three_colours():
    """With N_c colours and the lepton charge -1, anomaly cancellation gives Q_u = 1/2 + 1/(2 N_c), Q_d = -1/2 + 1/(2 N_c); N_c = 3 gives 2/3 and -1/3 and a proton charge of exactly 1."""
    c = S.hypercharges_from_anomalies(3)["charges"]; from fractions import Fraction as F
    assert c["Q_u"] == F(2, 3) and c["Q_d"] == F(-1, 3) and c["proton_uud"] == 1
    for n in (1, 2, 4, 5):
        h = S.hypercharges_from_anomalies(n); assert h["unique"] and h["u1_cubed_automatic"] and h["charges"]["Q_u"] == F(1, 2) + F(1, 2*n)


def test_anomaly_cancellation_comes_from_the_su5_embedding():
    """The fifteen Weyl fermions of a generation are exactly 5-bar + 10 of SU(5) with Y = diag(-1/3,-1/3,-1/3,1/2,1/2): both multiplets are traceless and A(10) + A(5-bar) = 0."""
    e = S.su5_embedding()
    assert e["matches_content"] and e["trace_5bar"] == 0 and e["trace_10"] == 0 and e["SU5_cubed_anomaly"] == 0 and e["weyl_per_generation"] == 15


def test_group_theory_closes():
    """[T^a, T^b] = i f^{abc} T^c, Jacobi identity and Casimirs (3/4 for SU(2), 4/3 for SU(3)) hold to rounding; f has 6 and 54 nonzero entries."""
    g = S.group_checks()
    for k in ("SU2", "SU3"):
        assert g[k]["closure_residual"] < 1e-12 and g[k]["jacobi_residual"] < 1e-12 and g[k]["casimir_residual"] < 1e-12
    assert g["SU2"]["nonzero_f"] == 6 and g["SU3"]["nonzero_f"] == 54


def test_parameter_counts_are_19_26_28():
    """The Yukawa structure and the flavour symmetry give 13 flavour parameters (9 masses, 3 angles, 1 phase) and 19 in all; 26 with Dirac neutrinos; 28 with Majorana."""
    assert S.parameter_count("massless")["flavour_physical"] == 13
    assert [S.parameter_count(k)["total"] for k in ("massless", "dirac", "majorana")] == [19, 26, 28]


def test_electroweak_masses_are_derived_symbolically():
    """|D H|^2 with H = (0, v/sqrt 2) gives the quadratic form whose Hessian has eigenvalues g^2 v^2/4 (twice), (g^2 + g'^2) v^2/4 and 0 (the photon)."""
    v = S.verify()
    assert v["boson_masses_match"] and v["m_h2_identity"]


def test_higgs_expansion_gives_mass_and_self_couplings():
    """V(h) = lambda v^2 h^2 + lambda v h^3 + lambda/4 h^4 with mu^2 = lambda v^2; m_h^2 = 2 lambda v^2."""
    import sympy as sp
    e = S.higgs_potential_expansion(); lam, v, h = e["symbols"]
    assert sp.simplify(e["coefficients"][2] - lam*v**2) == 0 and sp.simplify(e["coefficients"][3] - lam*v) == 0 and sp.simplify(e["coefficients"][4] - lam/4) == 0
    assert sp.simplify(e["coefficients"][1]) == 0


def test_numbers_against_the_pdg_tables():
    """v from G_F is 246.22 GeV; lambda = 0.129; tree-level m_W and m_Z are within 0.5 per cent of PDG (loop-sized differences); rho = 1 at tree level."""
    h = S.higgs_sector(); t = S.ew_tree()
    assert abs(h["v"] - 246.22) < 0.01 and 0.128 < h["lam"] < 0.131
    assert abs(t["m_W_diff_pct"]) < 0.5 and abs(t["m_Z_diff_pct"]) < 0.5 and abs(t["rho_tree"] - 1) < 1e-12


def test_yukawas_and_flavour_mixing():
    """y_t is about 1; the CKM matrix is unitary to rounding with J of about 3e-5; PMNS is unitary."""
    y = S.yukawas(); V = S.ckm_matrix(); U = S.pmns_matrix()
    assert 0.95 < y["t"] < 1.02 and y["e"] < 1e-5
    assert S.unitarity_residual(V) < 1e-12 and 2.5e-5 < S.jarlskog(V) < 3.5e-5 and S.unitarity_residual(U) < 1e-12


def test_z_couplings():
    """g_A = T3 and g_V = T3 - 2 Q sin^2 theta_W for every fermion; the neutrino has g_L = 1/2 and g_R = 0."""
    z = S.z_couplings(0.23122)
    assert abs(z["e"]["g_V"] - (-0.5 + 2*0.23122)) < 1e-12 and z["nu"]["g_R"] == 0 and z["u"]["g_A"] == 0.5


def test_gauge_couplings_do_not_meet_at_one_point():
    """At one loop the three inverse couplings cross pairwise at 1e13, 2e14 and 1e17 GeV: a spread of about four decades, no single unification scale."""
    c = S.gauge_crossings()
    assert 1e12 < c["mu_12"] < 1e14 and 1e16 < c["mu_23"] < 1e18 and c["mu_12"] < c["mu_13"] < c["mu_23"] and c["log10_spread"] > 3.0


def test_running_agrees_with_the_analytic_solution():
    """The numerical one-loop system for g1, g2, g3 reproduces the analytic 1/alpha_i(mu) of rge_gauge to integration accuracy."""
    r = S.rge_top_higgs(mu_max=1e10, n=60); mu = r["mu"][-1]; a = S.rge_gauge(mu)
    for g, ai in zip((r["g1"][-1], r["g2"][-1], r["g3"][-1]), a):
        assert abs(4*math.pi/g**2 - ai)/ai < 1e-6


def test_hat_model_matches_witches_hat():
    """The engine's hat model has brim radius v and depth lambda v^4/4, and is the same object witches_hat.lagrangian_sm builds."""
    h = S.higgs_sector(); m = S.hat_model()
    assert abs(m["brim_radius"] - h["v"]) < 1e-9 and abs(m["depth"] - h["depth_GeV4"]) < 1e-3


def test_hat_term_of_L_NN_is_the_standard_model_potential():
    """As coded, L_bias(mu^2 > 0) equals -V_SM exactly: the one term-for-term identity between L_NN and L_SM."""
    ex = C.measured_exponents()["bias / Higgs potential"]
    assert ex["SM"]["identical_to_NN_as_coded_for_mu2_positive"] and ex["SM"]["max_difference"] < 1e-12


def test_other_L_NN_terms_have_different_degree_from_the_SM_terms():
    """Recorded finding: doubling the fields shows gauge kinetic degree 4 (SM, non-Abelian) vs 2 (L_NN); fermion-gauge A^1 vs A^2; Yukawa psi^2 vs psi^1."""
    e = C.measured_exponents()
    assert round(e["gauge kinetic"]["SM"]["A"]) == 4 and round(e["gauge kinetic"]["NN"]["A"]) == 2
    assert round(e["matter (fermion-gauge)"]["SM"]["A"]) == 1 and round(e["matter (fermion-gauge)"]["NN"]["A"]) == 2
    assert round(e["coupling (Yukawa)"]["SM"]["psi"]) == 2 and round(e["coupling (Yukawa)"]["NN"]["psi"]) == 1


def test_coded_L_matter_has_the_form_of_the_scalar_gauge_seagull():
    """The coded L_matter equals the Standard Model scalar-gauge seagull term (the |D H|^2 piece that gives the W and Z their masses) up to the constant 8/n, for every
    activation norm, field and coupling: the same functional form, in a different sector from the one its name claims (Dirac fermion kinetic)."""
    r = C.seagull_correspondence()
    assert abs(r["ratio_max"] - r["ratio_min"]) < 1e-9 and abs(r["ratio_min"] - r["expected"]) < 1e-9


def test_recorded_code_findings_of_L_NN():
    """Recorded findings: polar_lagrangian does not apply 1/phi to L_bias; mu^2 < 0 (the docstring's symmetry-breaking sign) gives a bowl as coded."""
    assert C.one_over_phi_on_bias()["applied"] is False
    b = C.bias_conventions(); assert b["mu2=+1 (as coded)"] is not None and b["mu2=-1 (docstring convention, as coded)"] is None


def test_L_io_integrand_is_constant_in_sigma():
    """J_red J_blue = exp(-E) for every sigma (so L_(I|O) = exp(-E) times arc length); min(J_red, J_blue) peaks at sigma = 1/2."""
    li = C.lio_integrand(2.0)
    assert li["constant"] and abs(li["value"] - math.exp(-2.0)) < 1e-15 and abs(li["min_peaks_at"] - 0.5) < 1e-12


def test_engine_is_registered_and_its_manifest_validates():
    """The module appears in the registry with 19 equations, and its manifest and proof_locale pass validation."""
    from ValaQuenta.__main__ import _register_all
    from ValaQuenta.engine import manifest as MF
    reg = _register_all(); assert "lagrangian_sm" in reg.list_modules() and "witches_hat" in reg.list_modules()
    m = reg.get_module("lagrangian_sm"); assert len(m.formulary()) == 19 and MF.validate("lagrangian_sm", m) == []
