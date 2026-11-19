# SPDX-License-Identifier: GPL-3.0-only
r"""
ValaQuenta.modules.lagrangian_sm.compare
========================================
L_SM against L_NN (VAPMIP, ``modules/lagrangian``) and L_(I|O) / L_dynamic (``modules/l_io_photon_path``, Ainulindale wiki 52, 63, 64):
what is the same, what differs, measured on the code as it stands.  Nothing is argued here that a number below does not show.

The comparison is by SCALING: each term of each Lagrangian is evaluated at a field configuration and again with one field doubled, and
the exponent n in  term ~ amplitude^n  is read off.  Two terms with the same structure have the same exponent; the Standard Model terms
are polynomials of fixed degree in the fields (renormalisable: degree <= 4), and the exponent identifies the interaction.

Layers
------
ESTABLISHED   the Standard Model side (the exponents follow from the Lagrangian as written); the code reading of ``modules/lagrangian``.
INTERPRETATION  the summary table: what the measured exponents say about the claimed term-for-term correspondence.
"""
from __future__ import annotations
import math
import numpy as np

from . import maths as S

PHI = (1 + math.sqrt(5))/2


def _exponent(f, x: float = 1.0, k: float = 2.0) -> float:
    """Return n in f(k x) = k^n f(x) from two evaluations.

    :param f: function of a scalar amplitude.
    :param x: base amplitude.
    :param k: scale factor.
    :returns: the exponent.
    :rtype: float
    """
    a, b = f(x), f(k*x)
    return math.log(abs(b)/abs(a))/math.log(k) if a != 0 and b != 0 else float("nan")


# ------------------------------------------------------------------ the Standard Model terms on static fields
def _eta() -> np.ndarray:
    return np.diag([1.0, -1.0, -1.0, -1.0])


def sm_gauge_static(A: np.ndarray, g: float) -> float:
    """-1/4 F^a_{mu nu} F^{a mu nu} for a spatially and temporally constant SU(2) field: F^a_{mu nu} = g eps^{abc} A^b_mu A^c_nu.

    :param A: array ``(4, 3)``, A[mu, a].
    :param g: gauge coupling.
    :returns: the Lagrangian density.
    :rtype: float
    """
    eps = S.structure_constants(S.su2_generators()); eta = _eta()
    F = g*np.einsum("abc,mb,nc->mna", eps, A, A)
    return float(-0.25*np.einsum("mna,mr,ns,rsa->", F, eta, eta, F))


def sm_fermion_gauge(psi: np.ndarray, A: np.ndarray, g: float) -> float:
    """The fermion-gauge interaction g psibar gamma^mu T^a psi A^a_mu from i psibar gamma^mu D_mu psi, for an abelian field A_mu and a Dirac spinor.

    :param psi: complex 4-spinor.
    :param A: real 4-vector A_mu.
    :param g: coupling.
    :returns: the real part of g psibar gamma^mu psi A_mu.
    :rtype: float
    """
    I2, Z = np.eye(2), np.zeros((2, 2)); sx = np.array([[0, 1], [1, 0]]); sy = np.array([[0, -1j], [1j, 0]]); sz = np.array([[1, 0], [0, -1]])
    g0 = np.block([[I2, Z], [Z, -I2]]); gs = [np.block([[Z, s], [-s, Z]]) for s in (sx, sy, sz)]; gam = [g0] + gs
    bar = psi.conj()@g0; eta = _eta(); cur = [bar@gam[m]@psi for m in range(4)]
    return float(np.real(g*sum(eta[m, m]*cur[m]*A[m] for m in range(4))))


def sm_yukawa(psi_L: complex, psi_R: complex, h: float, y: float) -> float:
    """-y (psibar_L H psi_R + h.c.) for one fermion pair and a real Higgs value H = h/sqrt 2: -(y h/sqrt 2) 2 Re(conj(psi_L) psi_R).

    :param psi_L: left-handed amplitude.
    :param psi_R: right-handed amplitude.
    :param h: real Higgs field value.
    :param y: Yukawa coupling.
    :returns: the Lagrangian density.
    :rtype: float
    """
    return float(-(y*h/math.sqrt(2))*2*np.real(np.conj(psi_L)*psi_R))


def sm_higgs_potential_term(rho: float, mu2: float, lam: float) -> float:
    """-V(H) for H†H = rho^2/2: 1/2 mu^2 rho^2 - 1/4 lambda rho^4.

    :param rho: the radial Higgs field.
    :param mu2: mu^2.
    :param lam: lambda.
    :returns: -V.
    :rtype: float
    """
    return 0.5*mu2*rho**2 - 0.25*lam*rho**4


# ------------------------------------------------------------------ L_NN as coded
def lnn_terms(amp: float = 1.0, g: float = 0.05, mu_sq: float = 1.0, lam: float = 0.5, psi_amp: float = 1.0, beta_amp: float = 1.0) -> dict:
    """Evaluate the four coded L_NN terms (``modules/lagrangian/maths.py``) at amplitude-scaled fields.

    :param amp: scale of the gauge field A.
    :param g: gauge coupling.
    :param mu_sq: mu^2 as the code takes it.
    :param lam: lambda.
    :param psi_amp: scale of the activation norms.
    :param beta_amp: scale of the bias field.
    :returns: dict ``kinetic``, ``matter``, ``bias``, ``coupling``.
    :rtype: dict
    """
    from ..lagrangian import maths as N
    A = [0.3*amp, 0.5*amp, 0.2*amp]; psi = [0.7*psi_amp, 0.4*psi_amp]; beta = [0.6*beta_amp, 0.5*beta_amp]
    return {"kinetic": N.L_kinetic(A, g, N.ALG_H), "matter": N.L_matter(psi, A, g, 0.1, N.ALG_H), "bias": N.L_bias(beta, mu_sq, lam), "coupling": N.L_coupling(psi, beta, g)}


def measured_exponents() -> dict:
    """The degree of each term in the field amplitudes, measured: Standard Model against the coded L_NN.

    :returns: dict term -> ``{'SM': {...}, 'NN': {...}}`` with exponents in the named fields.
    :rtype: dict
    """
    g, th = 0.65, np.array([0.3, 0.5, 0.2])
    def smA(a): A = np.zeros((4, 3)); A[1] = a*th; A[2] = a*np.array([0.2, -0.4, 0.1]); return sm_gauge_static(A, g)
    rng = np.random.default_rng(1); psi = rng.normal(size=4) + 1j*rng.normal(size=4)
    out = {
        "gauge kinetic": {"SM": {"A": _exponent(smA)}, "NN": {"A": _exponent(lambda a: lnn_terms(amp=a)["kinetic"])}},
        "matter (fermion-gauge)": {"SM": {"psi": _exponent(lambda p: sm_fermion_gauge(p*psi, np.array([0.2, 0.3, -0.1, 0.4]), g)),
                                          "A": _exponent(lambda a: sm_fermion_gauge(psi, a*np.array([0.2, 0.3, -0.1, 0.4]), g))},
                                   "NN": {"psi": _exponent(lambda p: lnn_terms(psi_amp=p)["matter"]), "A": _exponent(lambda a: lnn_terms(amp=a)["matter"])}},
        "bias / Higgs potential": {"SM": {"field": None}, "NN": {"beta": None}},
        "coupling (Yukawa)": {"SM": {"psi": _exponent(lambda p: sm_yukawa(p*(0.7 + 0.2j), p*(0.4 - 0.1j), 1.3, 0.9)), "h": _exponent(lambda h: sm_yukawa(0.7 + 0.2j, 0.4 - 0.1j, h, 0.9))},
                              "NN": {"psi": _exponent(lambda p: lnn_terms(psi_amp=p)["coupling"]), "beta": _exponent(lambda b: lnn_terms(beta_amp=b)["coupling"])}},
    }
    # the hat term is a polynomial: read the degrees by fitting beta^2 and beta^4 coefficients, not a single exponent
    mu2, lam = 1.0, 0.5; xs = np.array([0.3, 0.5, 0.7, 0.9])
    sm = np.array([sm_higgs_potential_term(x, mu2, lam) for x in xs]); nn = np.array([lnn_terms(mu_sq=mu2, lam=lam, beta_amp=x/math.hypot(0.6, 0.5))["bias"] for x in xs])
    out["bias / Higgs potential"]["SM"] = {"identical_to_NN_as_coded_for_mu2_positive": bool(np.allclose(sm, nn, atol=1e-12)), "max_difference": float(np.abs(sm - nn).max())}
    out["bias / Higgs potential"]["NN"] = {"same_numbers": bool(np.allclose(sm, nn, atol=1e-12))}
    return out


def bias_conventions() -> dict:
    """The sign convention of L_bias in the code against the docstring, and the hat or bowl that results.

    As coded, L_bias = 1/2 mu^2 b^2 - 1/4 lambda b^4, so the potential V = -L_bias = -1/2 mu^2 b^2 + 1/4 lambda b^4: a hat for mu^2 > 0.
    The docstring and the wiki say mu^2 < 0 breaks the symmetry; with that sign the coded potential is a bowl.

    :returns: dict with the brim radius (or None) for mu^2 = +1 and -1.
    :rtype: dict
    """
    def brim(mu2, lam=0.5):
        a, b = -0.5*mu2, 0.25*lam
        return math.sqrt(-a/(2*b)) if a < 0 < b else None
    return {"mu2=+1 (as coded)": brim(1.0), "mu2=-1 (docstring convention, as coded)": brim(-1.0),
            "reading": "hat for mu^2 > 0; the docstring's mu^2 < 0 gives a bowl, no brim"}


def one_over_phi_on_bias() -> dict:
    """Whether polar_lagrangian applies the 1/phi to L_bias, as the docstring and wiki 04 write (1/phi) L_bias.

    :returns: dict with the integrand, the integrand with 1/phi applied, and ``applied`` (bool).
    :rtype: dict
    """
    from ..lagrangian import maths as N
    st = N.FieldState(psi=[0.7, 0.4], A=[0.3, 0.5, 0.2], beta=[0.6, 0.5], algebra=N.ALG_H, layer=3, g_coup=0.05, mu_sq=1.0, lam=0.5)
    r = N.polar_lagrangian(st); with_phi = r["kinetic"] + r["matter"] + r["bias"]/PHI + r["coupling"]
    return {"integrand": r["integrand"], "integrand_with_1_over_phi_on_bias": with_phi, "applied": abs(r["integrand"] - with_phi) < 1e-14, "bias_term": r["bias"]}


def seagull_correspondence(trials: int = 200, seed: int = 0) -> dict:
    """Compare the coded L_matter with the scalar-gauge 'seagull' term of the Standard Model, g^2 psi^2 A^2 / 8 per gauge component, which is the piece of |D H|^2 that gives
    the W and Z their masses (the quadratic form derived in ``maths.ew_mass_matrix_symbolic``).  For equal activation norms p the two have the same functional form, so their ratio
    is a constant (8/n) for every p, A and g.

    :param trials: number of random draws.
    :param seed: random seed.
    :returns: dict ``ratio_min``, ``ratio_max`` (equal when the form is identical) and ``expected`` (8/n).
    :rtype: dict
    """
    from ..lagrangian import maths as N
    rng = np.random.default_rng(seed); n = N.N_GEN[N.ALG_H]; rs = []
    for _ in range(trials):
        p = rng.uniform(0.2, 2.0); g = rng.uniform(0.01, 1.0); a = rng.normal(size=n); A = list(a)
        lnn = N.L_matter([p]*n, A, g, 0.1, N.ALG_H); sm = (g*g*p*p/8)*float(np.sum(a*a)); rs.append(lnn/sm)
    return {"ratio_min": min(rs), "ratio_max": max(rs), "expected": 8.0/n, "n_components": n}


# ------------------------------------------------------------------ L_(I|O): the integrand
def lio_integrand(E: float = 1.0, n: int = 11) -> dict:
    """J_red(sigma) J_blue(sigma) for L_(I|O) = integral J_red J_blue ds with J_red = exp(-(1-sigma)E), J_blue = exp(-sigma E).

    The product is exp(-E) for every sigma: the integrand does not depend on where on the path you are, so L_(I|O) = exp(-E) times the arc length.
    (Ainulindale wiki 64 section 2; the original L_dynamic of 2026-06-12 is described as having locally more and less action along the path.)

    :param E: the energy in the exponents.
    :param n: number of sigma samples in [0, 1].
    :returns: dict ``sigma``, ``product``, ``constant`` (bool), ``value`` (exp(-E)), ``min_over_sigma`` (peaks at sigma = 1/2).
    :rtype: dict
    """
    s = np.linspace(0, 1, n); jr = np.exp(-(1 - s)*E); jb = np.exp(-s*E); p = jr*jb; m = np.minimum(jr, jb)
    return {"sigma": s, "product": p, "constant": bool(np.allclose(p, p[0])), "value": math.exp(-E), "min_J": m, "min_peaks_at": float(s[int(np.argmax(m))])}


# ------------------------------------------------------------------ the summary
def parameters_NN() -> dict:
    """The adjustable quantities that the coded L_NN actually takes (FieldState and polar_lagrangian), against the Standard Model's 19.

    :returns: dict with the names and the count.
    :rtype: dict
    """
    names = ["g_coup", "hbar_nn", "mu_sq", "lam", "vev (declared; not used by polar_lagrangian)", "layer", "total_layers", "algebra", "phi (constant 1/phi in L_coup)"]
    return {"names": names, "count_free_numbers": 4, "note": "four numbers enter polar_lagrangian: g, hbar_NN, mu^2, lambda (plus the integer layer and the algebra stratum)."}


def comparison_table() -> list:
    """The three/four Lagrangians side by side: what each is, its status, its measured properties.  Plain data.

    :returns: list of dict rows.
    :rtype: list
    """
    ex = measured_exponents(); bc = bias_conventions(); ph = one_over_phi_on_bias(); li = lio_integrand()
    return [
        {"name": "L_SM", "role": "the measured theory of the fundamental interactions", "form": "L_gauge + L_fermion + L_Higgs + L_Yukawa",
         "gauge_group": "SU(3)×SU(2)×U(1), non-Abelian structure constants", "free_parameters": S.parameter_count("massless")["total"],
         "status": "ESTABLISHED (form from symmetry + content + renormalisability; numbers measured)"},
        {"name": "L_NN / L_vap (VAPMIP, SMNNIP)", "role": "information propagation; claimed term-for-term isomorphic to L_SM",
         "form": "(2/π)∮[L_kin + L_mat + (1/φ)L_bias + L_coup] r dr dθ", "gauge_group": "ℝ,ℂ,ℍ,𝕆 strata; Abelian single layer as coded",
         "free_parameters": parameters_NN()["count_free_numbers"], "status": "THEORETICAL",
         "measured": {"degree_of_gauge_kinetic": ex["gauge kinetic"], "degree_of_matter": ex["matter (fermion-gauge)"], "degree_of_coupling": ex["coupling (Yukawa)"],
                      "bias_term_equals_SM_hat": ex["bias / Higgs potential"], "bias_conventions": bc, "one_over_phi_applied_to_bias": ph["applied"]}},
        {"name": "L_(I|O)  (the Pathway; deprecated alias L_dynamic)", "role": "the path actually travelled; the third operator",
         "form": "∫_path J_red · J_blue ds", "gauge_group": "none (a functional on paths)", "free_parameters": 1, "status": "CONJECTURE (definition); algebra ESTABLISHED",
         "measured": {"integrand_is_constant_in_sigma": li["constant"], "value": li["value"], "min_J_peaks_at": li["min_peaks_at"]}},
        {"name": "L_dynamic (original, 2026-06-12; Ainulindale wiki 51 'The Dynamic Geodesic')", "role": "the truest trajectory through a field of varying momentum; the slingshot term L_sling ~ v dg/dt",
         "form": "L_standard + ∫ J_red · d(J_blue)/dt dλ  (the standard Lagrangian plus a coupling of forward momentum to the changing potential, in real time)",
         "gauge_group": "none (a time-dependent background)", "free_parameters": None,
         "status": "CONJECTURE; its established home is mechanics in a time-dependent potential, dE/dt = dV/dt at fixed q (measured: witches_hat.action.moving_hat_exchange). Wiki 52 §3 (same day) describes it in words and lists 'define L_dynamic formally' as open; the rename to L_(I|O) on 2026-06-17 dropped L_standard and the time derivative."},
    ]
