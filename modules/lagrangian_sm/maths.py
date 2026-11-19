# SPDX-License-Identifier: GPL-3.0-only
r"""
ValaQuenta.modules.lagrangian_sm.maths
======================================
L_SM: THE STANDARD MODEL OF PARTICLE PHYSICS LAGRANGIAN, as an engine.  Built from the textbook construction and nothing else:
choose the gauge group and the field content, write the most general renormalisable gauge-invariant Lagrangian, break the electroweak
symmetry with the Higgs doublet.  The engine computes what that construction gives and checks it against measured numbers.  It uses
no framework constant and no value fitted to anything of the author's.

    L_SM = L_gauge + L_fermion + L_Higgs + L_Yukawa   (+ L_gauge-fixing + L_ghost for quantisation; + theta terms)

    L_gauge    = -1/4 G^A_{mu nu} G^{A mu nu} - 1/4 W^a_{mu nu} W^{a mu nu} - 1/4 B_{mu nu} B^{mu nu}
    L_fermion  = sum_psi  psibar i gamma^mu D_mu psi            over Q_L, u_R, d_R, L_L, e_R, three generations
    L_Higgs    = (D_mu H)^dagger (D^mu H) - V(H),   V = -mu^2 H^dagger H + lambda (H^dagger H)^2
    L_Yukawa   = - Y_u Qbar_L H~ u_R - Y_d Qbar_L H d_R - Y_e Lbar_L H e_R + h.c.
    D_mu       = d_mu - i g_s T^A G^A_mu - i g T^a W^a_mu - i g' Y B_mu

Layers
------
ESTABLISHED  everything in this file that is a theorem of group theory or algebra (structure constants, Jacobi identity, anomaly sums,
             the symbolic boson-mass derivation, the Yukawa counting of independent parameters, CKM unitarity), the tree-level
             relations of the broken theory (m_W, m_Z, couplings of the Z and W, couplings of the Higgs), the one-loop beta functions
             (Machacek-Vaughn), and the measured inputs, which carry their source in ``INPUTS``.
INTERPRETATION  where the file says what is derived and what is measured: the FORM of L_SM follows from the gauge group, the field
             content and renormalisability; the NUMBERS (the 19 parameters) and the choice of group and content are measured.
Nothing here is THEORETICAL in the author's sense: this engine is the control against which the other Lagrangians are compared.

Units: GeV, natural units (hbar = c = 1), couplings dimensionless, V in GeV^4.
"""
from __future__ import annotations
import math
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

# ------------------------------------------------------------------ measured inputs, with sources
INPUTS = {
    "alpha_em_inv_MZ": (127.951, 0.009, "PDG Review of Particle Physics, MSbar alpha(M_Z)^-1"),
    "sin2_thetaW_MSbar_MZ": (0.23122, 0.00003, "PDG Review, electroweak model, MSbar sin^2 theta_W(M_Z)"),
    "alpha_s_MZ": (0.1180, 0.0009, "PDG Review, QCD, alpha_s(M_Z)"),
    "G_F": (1.1663788e-5, 6e-12, "PDG Review, Fermi constant from the muon lifetime, GeV^-2"),
    "ckm": {"s12": 0.22501, "s23": 0.04183, "s13": 0.003732, "delta": 1.147, "source": "PDG Review, CKM, standard parametrisation"},
    "pmns": {"s12sq": 0.307, "s23sq": 0.546, "s13sq": 0.0220, "delta": 3.44, "source": "NuFIT 5.x global fit, normal ordering (radians for delta)"},
    "note": "Values typed from the PDG/NuFIT reviews; masses are read from the installed `particle` package (PDG tables). "
            "Verify against the live PDG before quoting in a paper.",
}


def pdg_mass(name: str):
    """Mass and symmetric uncertainty in GeV from the installed PDG tables (``particle``).

    :param name: PDG particle name, e.g. ``'W+'``, ``'Z0'``, ``'H0'``, ``'t'``, ``'tau-'``.
    :returns: ``(mass_GeV, uncertainty_GeV)``.
    :rtype: tuple
    """
    from particle import Particle
    p = Particle.from_name(name)
    return p.mass/1000.0, 0.5*((p.mass_upper or 0) + (p.mass_lower or 0))/1000.0


def pdg_masses() -> dict:
    """The nine charged-fermion masses, W, Z and Higgs, GeV, from the PDG tables.

    :returns: dict name -> (mass, uncertainty).
    :rtype: dict
    """
    names = {"u": "u", "d": "d", "s": "s", "c": "c", "b": "b", "t": "t", "e": "e-", "mu": "mu-", "tau": "tau-", "W": "W+", "Z": "Z0", "H": "H0"}
    return {k: pdg_mass(v) for k, v in names.items()}


# ------------------------------------------------------------------ field content (ESTABLISHED, as observed)
def field_content() -> list:
    """The fermion and scalar content of the Standard Model, one generation, with gauge quantum numbers.

    Each entry: ``name``, ``su3`` (dimension of the SU(3) representation), ``su2`` (dimension of the SU(2) representation),
    ``Y`` (hypercharge, Q = T3 + Y, as a Fraction), ``chirality`` (``'L'``, ``'R'`` or ``'scalar'``), ``generations``.

    :returns: list of dicts.
    :rtype: list
    """
    return [
        {"name": "Q_L", "su3": 3, "su2": 2, "Y": Fr(1, 6), "chirality": "L", "generations": 3},
        {"name": "u_R", "su3": 3, "su2": 1, "Y": Fr(2, 3), "chirality": "R", "generations": 3},
        {"name": "d_R", "su3": 3, "su2": 1, "Y": Fr(-1, 3), "chirality": "R", "generations": 3},
        {"name": "L_L", "su3": 1, "su2": 2, "Y": Fr(-1, 2), "chirality": "L", "generations": 3},
        {"name": "e_R", "su3": 1, "su2": 1, "Y": Fr(-1), "chirality": "R", "generations": 3},
        {"name": "H", "su3": 1, "su2": 2, "Y": Fr(1, 2), "chirality": "scalar", "generations": 1},
    ]


def degrees_of_freedom() -> dict:
    """Count the fields: Weyl fermions, real scalars, gauge bosons, and the on-shell degrees of freedom they carry.

    :returns: dict with ``weyl_fermions``, ``real_scalars``, ``gauge_bosons`` (12), ``gauge_on_shell_unbroken`` (24).
    :rtype: dict
    """
    weyl = sum(f["su3"]*f["su2"]*f["generations"] for f in field_content() if f["chirality"] != "scalar")
    return {"weyl_fermions": weyl, "real_scalars": 2*2, "gauge_bosons": 8 + 3 + 1, "gauge_on_shell_unbroken": 2*(8 + 3 + 1)}


def anomaly_check() -> dict:
    """Gauge anomaly sums over one generation of left-handed Weyl fermions (right-handed fields enter as conjugates, Y -> -Y).

    The theory is consistent only if every sum vanishes; they do, exactly (rational arithmetic).

    :returns: dict of the sums ``U1^3``, ``SU3^2 U1``, ``SU2^2 U1``, ``grav^2 U1`` (each Fraction 0) and the Witten parity of SU(2) doublets.
    :rtype: dict
    """
    weyl = []
    for f in field_content():
        if f["chirality"] == "scalar": continue
        Y = f["Y"] if f["chirality"] == "L" else -f["Y"]
        c3, c2 = f["su3"], f["su2"]
        weyl.append((c3, c2, Y))
    t3 = lambda d: Fr(1, 2) if d == 3 else Fr(0)           # SU(3) index of the triplet (and antitriplet); singlet 0
    t2 = lambda d: Fr(1, 2) if d == 2 else Fr(0)
    u13 = sum(c3*c2*Y**3 for c3, c2, Y in weyl)
    su3u1 = sum(t3(c3)*c2*Y for c3, c2, Y in weyl)
    su2u1 = sum(t2(c2)*c3*Y for c3, c2, Y in weyl)
    grav = sum(c3*c2*Y for c3, c2, Y in weyl)
    doublets = sum(c3 for c3, c2, Y in weyl if c2 == 2)
    return {"U1^3": u13, "SU3^2 U1": su3u1, "SU2^2 U1": su2u1, "grav^2 U1": grav, "witten_doublets_per_generation": doublets,
            "witten_ok": doublets % 2 == 0, "all_zero": all(x == 0 for x in (u13, su3u1, su2u1, grav))}


def hypercharges_from_anomalies(n_colours: int = 3) -> dict:
    """Solve for the hypercharges: given the multiplets (Q_L, u_R, d_R, L_L, e_R), the Higgs doublet with Y_H = 1/2 (a normalisation) and Yukawa
    invariance (Y_u = Y_Q + Y_H, Y_d = Y_Q - Y_H, Y_e = Y_L - Y_H), the anomaly conditions fix every hypercharge.  This is DERIVED, not measured.
    With N_c colours the solution is Y_Q = 1/(2 N_c), Y_L = -1/2: the fractional quark charges are a consequence of N_c = 3 and the lepton charge.

    :param n_colours: number of colours N_c.
    :returns: ``{'solutions', 'unique', 'sm', 'su3_condition_automatic', 'u1_cubed_automatic', 'charges'}``; solutions hold Fractions; ``charges`` gives the electric charges of the right-handed u, d, e (T3 = 0, so Q = Y) and of the uud proton.
    :rtype: dict
    """
    YQ, YL = sp.symbols("YQ YL"); YH = sp.Rational(1, 2); Yu, Yd, Ye = YQ + YH, YQ - YH, YL - YH; N = n_colours
    su2 = N*YQ + YL; su3 = 2*YQ - Yu - Yd; grav = 2*N*YQ - N*Yu - N*Yd + 2*YL - Ye; cube = 2*N*YQ**3 - N*Yu**3 - N*Yd**3 + 2*YL**3 - Ye**3
    sol = sp.solve([su2, grav], [YQ, YL], dict=True)
    out = [{"Y_Q": Fr(str(s[YQ])), "Y_L": Fr(str(s[YL])), "Y_u": Fr(str(Yu.subs(s))), "Y_d": Fr(str(Yd.subs(s))), "Y_e": Fr(str(Ye.subs(s)))} for s in sol]
    return {"solutions": out, "unique": len(out) == 1, "sm": {"Y_Q": Fr(1, 6), "Y_L": Fr(-1, 2), "Y_u": Fr(2, 3), "Y_d": Fr(-1, 3), "Y_e": Fr(-1)},
            "su3_condition_automatic": sp.simplify(su3) == 0, "u1_cubed_automatic": all(sp.simplify(cube.subs(s)) == 0 for s in sol),
            "charges": {"Q_u": out[0]["Y_u"], "Q_d": out[0]["Y_d"], "Q_e": out[0]["Y_e"], "proton_uud": 2*out[0]["Y_u"] + out[0]["Y_d"]} if out else None}


def su5_embedding() -> dict:
    """The source of the anomaly cancellation: the fifteen Weyl fermions of one generation fill exactly the SU(5) representations 5-bar + 10, and the
    Standard-Model hypercharge is the traceless SU(5) generator diag(-1/3, -1/3, -1/3, 1/2, 1/2) acting on them.  Tracelessness inside each multiplet and the SU(5)
    anomaly coefficients A(10) = +1, A(5-bar) = -1 (A(antisymmetric 2-tensor of SU(N)) = N - 4, A(fundamental) = 1) then make every anomaly sum vanish.

    :returns: dict with the 5 and 10 hypercharges built from the generator, their traces, the SU(5)^3 anomaly sum, and whether they equal the content of ``field_content``.
    :rtype: dict
    """
    y5 = [Fr(-1, 3)]*3 + [Fr(1, 2)]*2                      # hypercharge generator on the 5 (d^c-bar... conj: see below); 5-bar is minus this
    y5bar = [-y for y in y5]
    y10 = [y5[i] + y5[j] for i in range(5) for j in range(i + 1, 5)]
    # left-handed Weyl content of one generation, conjugating the right-handed fields (Y -> -Y): d^c (3-bar,1,1/3), L (1,2,-1/2) | Q (3,2,1/6), u^c (3-bar,1,-2/3), e^c (1,1,1)
    content_5bar = sorted([Fr(1, 3)]*3 + [Fr(-1, 2)]*2); content_10 = sorted([Fr(1, 6)]*6 + [Fr(-2, 3)]*3 + [Fr(1)])
    N = 5; A_fund = 1; A_10 = N - 4
    return {"Y_5bar": sorted(y5bar), "Y_10": sorted(y10), "trace_5bar": sum(y5bar), "trace_10": sum(y10), "A_10": A_10, "A_5bar": -A_fund, "SU5_cubed_anomaly": A_10 - A_fund,
            "matches_content": sorted(y5bar) == content_5bar and sorted(y10) == content_10, "weyl_per_generation": len(y5bar) + len(y10),
            "note": "with a right-handed neutrino the 16 = 5-bar + 10 + 1 is one spinor of SO(10)"}


# ------------------------------------------------------------------ group theory: structure constants
def su2_generators() -> np.ndarray:
    """SU(2) generators T^a = sigma^a / 2, shape (3, 2, 2).

    :returns: complex array.
    :rtype: numpy.ndarray
    """
    s = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], complex)
    return s/2


def su3_generators() -> np.ndarray:
    """SU(3) generators T^A = lambda^A / 2 (Gell-Mann), shape (8, 3, 3).

    :returns: complex array.
    :rtype: numpy.ndarray
    """
    l = np.zeros((8, 3, 3), complex)
    l[0][0, 1] = l[0][1, 0] = 1
    l[1][0, 1] = -1j; l[1][1, 0] = 1j
    l[2][0, 0] = 1; l[2][1, 1] = -1
    l[3][0, 2] = l[3][2, 0] = 1
    l[4][0, 2] = -1j; l[4][2, 0] = 1j
    l[5][1, 2] = l[5][2, 1] = 1
    l[6][1, 2] = -1j; l[6][2, 1] = 1j
    l[7] = np.diag([1, 1, -2])/math.sqrt(3)
    return l/2


def structure_constants(T: np.ndarray) -> np.ndarray:
    """Real structure constants f^{abc} of a Lie algebra from its generators: [T^a, T^b] = i f^{abc} T^c, f^{abc} = -2i Tr([T^a, T^b] T^c)
    for generators normalised Tr(T^a T^b) = delta/2.

    :param T: generators, shape ``(n, d, d)``.
    :returns: real array ``(n, n, n)``.
    :rtype: numpy.ndarray
    """
    n = len(T); f = np.zeros((n, n, n))
    for a in range(n):
        for b in range(n):
            comm = T[a]@T[b] - T[b]@T[a]
            for c in range(n):
                f[a, b, c] = float(np.real(-2j*np.trace(comm@T[c])))
    return f


def group_checks() -> dict:
    """Closure, Jacobi identity and Casimir checks for SU(2) and SU(3).

    :returns: dict of maximum residuals and the Casimirs (3/4 for the SU(2) doublet, 4/3 for the SU(3) triplet).
    :rtype: dict
    """
    out = {}
    for name, T, casimir in (("SU2", su2_generators(), 0.75), ("SU3", su3_generators(), 4/3)):
        f = structure_constants(T); n = len(T); d = T.shape[1]; err = 0.0
        for a in range(n):
            for b in range(n):
                comm = T[a]@T[b] - T[b]@T[a]; rhs = sum(1j*f[a, b, c]*T[c] for c in range(n)); err = max(err, float(np.abs(comm - rhs).max()))
        jac = 0.0
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    for dd in range(n):
                        s = sum(f[a, b, e]*f[e, c, dd] + f[b, c, e]*f[e, a, dd] + f[c, a, e]*f[e, b, dd] for e in range(n)); jac = max(jac, abs(s))
        C2 = sum(T[a]@T[a] for a in range(n)); out[name] = {"generators": n, "closure_residual": err, "jacobi_residual": jac,
                                                              "casimir_residual": float(np.abs(C2 - casimir*np.eye(d)).max()), "nonzero_f": int(np.sum(np.abs(f) > 1e-12))}
    return out


# ------------------------------------------------------------------ parameter count (ESTABLISHED, counted from the content)
def parameter_count(neutrinos: str = "massless") -> dict:
    """Count the independent real parameters of the most general renormalisable L_SM from the Yukawa structure and the flavour symmetry.

    Complex 3x3 Yukawa matrices carry 2 n^2 real numbers each; the symmetry U(3)^k of the kinetic terms removes (generators of U(3)^k
    minus the generators that stay unbroken) of them.  Add the three gauge couplings, the two Higgs parameters and theta_QCD.

    :param neutrinos: ``'massless'`` (19 parameters), ``'dirac'`` (26) or ``'majorana'`` (28, Weinberg operator).
    :returns: dict with the pieces and ``total``.
    :rtype: dict
    :raises ValueError: for an unknown neutrino option.
    """
    n = 3; gauge, higgs, theta = 3, 2, 1
    if neutrinos == "massless": yuk = 3*2*n*n; gen = 5*n*n; unbroken = 4
    elif neutrinos == "dirac": yuk = 4*2*n*n; gen = 6*n*n; unbroken = 2
    elif neutrinos == "majorana": yuk = 3*2*n*n + n*(n + 1); gen = 5*n*n; unbroken = 1
    else: raise ValueError("neutrinos must be 'massless', 'dirac' or 'majorana'")
    flavour = yuk - (gen - unbroken)
    return {"neutrinos": neutrinos, "gauge_couplings": gauge, "higgs": higgs, "theta_QCD": theta, "yukawa_real": yuk, "flavour_generators": gen,
            "unbroken_generators": unbroken, "flavour_physical": flavour, "total": gauge + higgs + theta + flavour}


# ------------------------------------------------------------------ the Higgs sector, derived symbolically
def ew_mass_matrix_symbolic() -> dict:
    """Derive the electroweak boson masses from |D H|^2 with H = (0, v/sqrt 2): the quadratic form in (W1, W2, W3, B), its Hessian,
    and the eigenvalues (sympy).  Returns the expressions.

    :returns: ``{'quadratic_form', 'mass_matrix', 'eigenvalues': {...}, 'm_W2', 'm_Z2', 'm_photon2'}`` as sympy objects.
    :rtype: dict
    """
    g, gp, v = sp.symbols("g gp v", positive=True); W1, W2, W3, B = sp.symbols("W1 W2 W3 B", real=True)
    s = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.Matrix([[1, 0], [0, -1]])]
    A = g*(s[0]*W1 + s[1]*W2 + s[2]*W3)/2 + gp*sp.Rational(1, 2)*B*sp.eye(2)
    phi = sp.Matrix([0, v/sp.sqrt(2)]); vec = A*phi; Q = sp.simplify((vec.H*vec)[0])
    M = sp.hessian(Q, (W1, W2, W3, B)); ev = M.eigenvals()
    ev = {sp.simplify(k): m for k, m in ev.items()}
    return {"quadratic_form": Q, "mass_matrix": M, "eigenvalues": ev, "m_W2": g**2*v**2/4, "m_Z2": (g**2 + gp**2)*v**2/4, "m_photon2": sp.Integer(0),
            "symbols": (g, gp, v)}


def higgs_potential_expansion() -> dict:
    """Expand V(H) in the unitary gauge H = (0, (v + h)/sqrt 2) with mu^2 = lambda v^2: mass, cubic and quartic couplings of h (sympy).

    :returns: ``{'V', 'coefficients': {2, 3, 4}, 'm_h2'}`` where ``m_h2 = 2 lambda v^2``.
    :rtype: dict
    """
    lam, v, h = sp.symbols("lam v h", positive=True); mu2 = lam*v**2; hh = (v + h)**2/2
    V = sp.expand(-mu2*hh + lam*hh**2)
    c = {k: sp.simplify(V.coeff(h, k)) for k in range(0, 5)}
    return {"V": V, "coefficients": c, "m_h2": sp.simplify(2*c[2]), "symbols": (lam, v, h)}


def higgs_sector(m_h: float = None, v: float = None) -> dict:
    """Numerical Higgs sector from the measured mass and vev: lambda = m_h^2/(2 v^2), mu^2 = lambda v^2, depth, trilinear and quartic couplings.

    :param m_h: Higgs mass in GeV (default PDG).
    :param v: vev in GeV (default (sqrt(2) G_F)^(-1/2)).
    :returns: dict with ``lam``, ``mu2``, ``v``, ``m_h``, ``depth_GeV4`` = lambda v^4/4, ``trilinear`` = m_h^2/(2 v), ``quartic`` = lambda/4.
    :rtype: dict
    """
    m_h = pdg_mass("H0")[0] if m_h is None else m_h; v = fermi_vev() if v is None else v
    lam = m_h**2/(2*v**2)
    return {"m_h": m_h, "v": v, "lam": lam, "mu2": lam*v**2, "depth_GeV4": lam*v**4/4, "trilinear": m_h**2/(2*v), "quartic": lam/4}


def fermi_vev() -> float:
    """v = (sqrt(2) G_F)^(-1/2), GeV, from the measured Fermi constant.

    :returns: the vev (about 246.22 GeV).
    :rtype: float
    """
    return (math.sqrt(2)*INPUTS["G_F"][0])**-0.5


def ew_tree(alpha_inv: float = None, sin2w: float = None, v: float = None) -> dict:
    """Tree-level electroweak relations from alpha(M_Z), sin^2 theta_W and v: e, g, g', m_W, m_Z, rho, and the comparison with the measured masses.

    :param alpha_inv: 1/alpha(M_Z) (MSbar).
    :param sin2w: sin^2 theta_W (MSbar at M_Z).
    :param v: vev in GeV.
    :returns: dict; ``m_W_tree`` and ``m_Z_tree`` against ``m_W_pdg``, ``m_Z_pdg`` with the percentage differences (loop corrections).
    :rtype: dict
    """
    alpha_inv = INPUTS["alpha_em_inv_MZ"][0] if alpha_inv is None else alpha_inv; sin2w = INPUTS["sin2_thetaW_MSbar_MZ"][0] if sin2w is None else sin2w
    v = fermi_vev() if v is None else v
    e = math.sqrt(4*math.pi/alpha_inv); s = math.sqrt(sin2w); c = math.sqrt(1 - sin2w); g = e/s; gp = e/c
    mW, mZ = g*v/2, math.sqrt(g*g + gp*gp)*v/2; mWp, mZp = pdg_mass("W+")[0], pdg_mass("Z0")[0]
    return {"e": e, "g": g, "gp": gp, "m_W_tree": mW, "m_Z_tree": mZ, "rho_tree": (mW/(mZ*c))**2, "m_W_pdg": mWp, "m_Z_pdg": mZp,
            "m_W_diff_pct": 100*(mW - mWp)/mWp, "m_Z_diff_pct": 100*(mZ - mZp)/mZp}


def yukawas(v: float = None) -> dict:
    """Yukawa couplings of the charged fermions, y = sqrt(2) m / v, from the PDG masses.

    :param v: vev in GeV.
    :returns: dict name -> y.
    :rtype: dict
    """
    v = fermi_vev() if v is None else v; m = pdg_masses()
    return {k: math.sqrt(2)*m[k][0]/v for k in ("u", "d", "s", "c", "b", "t", "e", "mu", "tau")}


# ------------------------------------------------------------------ flavour mixing
def ckm_matrix(s12: float = None, s23: float = None, s13: float = None, delta: float = None) -> np.ndarray:
    """CKM matrix in the standard parametrisation (three angles, one phase).

    :param s12: sin theta_12 (default PDG).
    :param s23: sin theta_23.
    :param s13: sin theta_13.
    :param delta: CP phase in radians.
    :returns: complex 3x3 matrix.
    :rtype: numpy.ndarray
    """
    k = INPUTS["ckm"]; s12 = k["s12"] if s12 is None else s12; s23 = k["s23"] if s23 is None else s23; s13 = k["s13"] if s13 is None else s13
    d = k["delta"] if delta is None else delta; c12, c23, c13 = (math.sqrt(1 - x*x) for x in (s12, s23, s13)); e = np.exp(1j*d)
    return np.array([[c12*c13, s12*c13, s13/e], [-s12*c23 - c12*s23*s13*e, c12*c23 - s12*s23*s13*e, s23*c13], [s12*s23 - c12*c23*s13*e, -c12*s23 - s12*c23*s13*e, c23*c13]])


def pmns_matrix() -> np.ndarray:
    """PMNS matrix, same parametrisation, from the NuFIT angles in ``INPUTS`` (Dirac phase only).

    :returns: complex 3x3 matrix.
    :rtype: numpy.ndarray
    """
    p = INPUTS["pmns"]; return ckm_matrix(math.sqrt(p["s12sq"]), math.sqrt(p["s23sq"]), math.sqrt(p["s13sq"]), p["delta"])


def jarlskog(V: np.ndarray) -> float:
    """Rephasing-invariant CP-violation measure J = Im(V_us V_cb V*_ub V*_cs).

    :param V: a 3x3 mixing matrix.
    :returns: J.
    :rtype: float
    """
    return float(np.imag(V[0, 1]*V[1, 2]*np.conj(V[0, 2])*np.conj(V[1, 1])))


def unitarity_residual(V: np.ndarray) -> float:
    """max |V^dagger V - 1|.

    :param V: mixing matrix.
    :returns: the residual.
    :rtype: float
    """
    return float(np.abs(V.conj().T@V - np.eye(len(V))).max())


# ------------------------------------------------------------------ couplings of the Z, W and Higgs
def z_couplings(sin2w: float = None) -> dict:
    """Z couplings of every Dirac fermion: g_L = T3 - Q sin^2 theta_W, g_R = -Q sin^2 theta_W, g_V = T3 - 2Q sin^2, g_A = T3.

    :param sin2w: sin^2 theta_W.
    :returns: dict name -> dict of T3, Q, g_L, g_R, g_V, g_A.
    :rtype: dict
    """
    s = INPUTS["sin2_thetaW_MSbar_MZ"][0] if sin2w is None else sin2w
    rows = {"nu": (0.5, 0.0), "e": (-0.5, -1.0), "u": (0.5, 2/3), "d": (-0.5, -1/3)}; out = {}
    for k, (t3, q) in rows.items():
        out[k] = {"T3": t3, "Q": q, "g_L": t3 - q*s, "g_R": -q*s, "g_V": t3 - 2*q*s, "g_A": t3}
    return out


def vertex_inventory() -> dict:
    """Count the distinct interaction vertex types of the broken L_SM, from the content (no fitting, no free choice).

    :returns: dict with the numbers of bosonic, gauge-fermion, Yukawa and QCD vertex types, and the totals.
    :rtype: dict
    """
    bosonic_ew = ["hhh", "hhhh", "hWW", "hZZ", "hhWW", "hhZZ", "WWgamma", "WWZ", "WWgammagamma", "WWZgamma", "WWZZ", "WWWW"]
    charged = 9; neutral_z = 12; w_lepton = 3; w_quark = 9; yukawa = 9; qcd_quark = 6
    qcd = ["ggg", "gggg"]
    n_fermion_vertices = charged + neutral_z + w_lepton + w_quark + yukawa + qcd_quark
    return {"bosonic_electroweak": len(bosonic_ew), "bosonic_qcd": len(qcd), "photon_fermion": charged, "Z_fermion": neutral_z, "W_lepton": w_lepton,
            "W_quark_CKM_entries": w_quark, "Higgs_fermion": yukawa, "gluon_quark_flavours": qcd_quark, "total_vertex_types": len(bosonic_ew) + len(qcd) + n_fermion_vertices,
            "note": "per generation and colour structure; the components multiply these: 8 gluons, 3 colours, 3 generations."}


def term_inventory() -> list:
    """The terms of L_SM as written, each with the parameters it carries.  Plain data for display and for the comparison with L_NN.

    :returns: list of dicts ``{'sector', 'term', 'parameters', 'count'}``.
    :rtype: list
    """
    return [
        {"sector": "gauge", "term": "-1/4 G^A_{μν} G^{Aμν} - 1/4 W^a_{μν} W^{aμν} - 1/4 B_{μν} B^{μν}", "parameters": ["g_s", "g", "g'"], "count": 3},
        {"sector": "fermion", "term": "Σ ψ̄ i γ^μ D_μ ψ over Q_L u_R d_R L_L e_R × 3 generations", "parameters": [], "count": 0},
        {"sector": "Higgs", "term": "(D_μ H)† (D^μ H) - V(H),  V = -μ² H†H + λ (H†H)²", "parameters": ["μ²", "λ"], "count": 2},
        {"sector": "Yukawa", "term": "-Y_u Q̄ H̃ u - Y_d Q̄ H d - Y_e L̄ H e + h.c.", "parameters": ["9 masses", "3 CKM angles", "1 CKM phase"], "count": 13},
        {"sector": "topological", "term": "θ g_s²/(32π²) G^A_{μν} G̃^{Aμν}", "parameters": ["θ_QCD"], "count": 1},
    ]


# ------------------------------------------------------------------ one-loop running
_B_GAUGE = (41/10, -19/6, -7.0)


def gauge_initial() -> tuple:
    """Gauge couplings at M_Z in GUT normalisation: g1 = sqrt(5/3) g', g2, g3 = sqrt(4 pi alpha_s).

    :returns: ``(g1, g2, g3)``.
    :rtype: tuple
    """
    t = ew_tree(); return math.sqrt(5/3)*t["gp"], t["g"], math.sqrt(4*math.pi*INPUTS["alpha_s_MZ"][0])


def rge_gauge(mu: float, mu0: float = None) -> tuple:
    """One-loop running of the three gauge couplings (analytic): 1/alpha_i(mu) = 1/alpha_i(M_Z) - b_i/(2 pi) ln(mu/M_Z).

    :param mu: scale in GeV.
    :param mu0: reference scale (default M_Z from the PDG tables).
    :returns: ``(alpha1_inv, alpha2_inv, alpha3_inv)`` with GUT-normalised alpha1.
    :rtype: tuple
    """
    mu0 = pdg_mass("Z0")[0] if mu0 is None else mu0; g = gauge_initial(); t = math.log(mu/mu0)
    return tuple(4*math.pi/gi**2 - b/(2*math.pi)*t for gi, b in zip(g, _B_GAUGE))


def gauge_crossings() -> dict:
    """Scales where pairs of one-loop inverse couplings meet.  A single common point would be unification; the spread is the measured result.

    :returns: dict with ``mu_12``, ``mu_23``, ``mu_13`` in GeV and ``log10_spread``.
    :rtype: dict
    """
    g = gauge_initial(); a = [4*math.pi/x**2 for x in g]; M = pdg_mass("Z0")[0]; out = {}
    for (i, j), key in (((0, 1), "mu_12"), ((1, 2), "mu_23"), ((0, 2), "mu_13")):
        t = (a[i] - a[j])/((_B_GAUGE[i] - _B_GAUGE[j])/(2*math.pi)); out[key] = M*math.exp(t)
    ls = [math.log10(out[k]) for k in ("mu_12", "mu_23", "mu_13")]; out["log10_spread"] = max(ls) - min(ls); return out


def rge_top_higgs(mu_max: float = 1e19, n: int = 400) -> dict:
    """One-loop running of (g1, g2, g3, y_t, lambda) from M_Z, with the standard one-loop beta functions (V = lambda |H|^4).
    One loop is illustrative; the stability scale needs two-loop and threshold corrections.

    :param mu_max: upper scale in GeV.
    :param n: number of output points.
    :returns: ``{'mu', 'g1', 'g2', 'g3', 'yt', 'lam'}`` arrays and ``lambda_zero_scale`` (GeV, or None).
    :rtype: dict
    """
    from scipy.integrate import solve_ivp
    k = 1/(16*math.pi**2); M = pdg_mass("Z0")[0]; g1, g2, g3 = gauge_initial(); yt = math.sqrt(2)*162.5/fermi_vev(); lam = higgs_sector()["lam"]
    def f(t, y):
        a1, a2, a3, yy, l = y; gp2 = 3/5*a1**2
        return [k*41/10*a1**3, -k*19/6*a2**3, -k*7*a3**3,
                k*yy*(4.5*yy**2 - 8*a3**2 - 9/4*a2**2 - 17/20*a1**2),
                k*(24*l**2 - 6*yy**4 + 12*l*yy**2 - 3*l*(3*a2**2 + gp2) + 3/8*(2*a2**4 + (a2**2 + gp2)**2))]
    ts = np.linspace(0, math.log(mu_max/M), n); s = solve_ivp(f, (0, ts[-1]), [g1, g2, g3, yt, lam], t_eval=ts, rtol=1e-9, atol=1e-12)
    mu = M*np.exp(s.t); neg = np.where(s.y[4] < 0)[0]
    return {"mu": mu, "g1": s.y[0], "g2": s.y[1], "g3": s.y[2], "yt": s.y[3], "lam": s.y[4], "lambda_zero_scale": (float(mu[neg[0]]) if len(neg) else None)}


# ------------------------------------------------------------------ what each particle does to the hat
def particle_content_for_potential() -> list:
    """Field-dependent masses m_i(h) and degrees of freedom n_i (negative for fermions) of the particles that feed the one-loop effective potential of h.

    m_W = g h/2 (n = 6), m_Z = sqrt(g^2 + g'^2) h/2 (n = 3), fermions m_f = y_f h/sqrt 2 (n = -4 N_c: top, bottom, charm -12; tau -4).  Goldstones and the Higgs
    are handled in ``coleman_weinberg`` separately (their field-dependent masses go negative on the hilltop side).

    :returns: list of dicts ``name, n, c (the MSbar constant), slope`` where ``m_i(h) = slope * h``.
    :rtype: list
    """
    t = ew_tree(); y = yukawas()
    return [{"name": "W", "n": 6, "c": 5/6, "slope": t["g"]/2}, {"name": "Z", "n": 3, "c": 5/6, "slope": math.sqrt(t["g"]**2 + t["gp"]**2)/2},
            {"name": "top", "n": -12, "c": 3/2, "slope": y["t"]/math.sqrt(2)}, {"name": "bottom", "n": -12, "c": 3/2, "slope": y["b"]/math.sqrt(2)},
            {"name": "charm", "n": -12, "c": 3/2, "slope": y["c"]/math.sqrt(2)}, {"name": "tau", "n": -4, "c": 3/2, "slope": y["tau"]/math.sqrt(2)}]


def coleman_weinberg(h, mu: float = None) -> dict:
    """One-loop (MSbar) correction to the Higgs hat from each particle: V_i(h) = n_i m_i(h)^4 / (64 pi^2) [ln(m_i^2(h)/mu^2) - c_i], per particle and in total.

    ESTABLISHED (Coleman & Weinberg 1973).  The Higgs and Goldstone contributions use |m^2(h)| (their field-dependent masses go negative inside the brim) and are
    reported separately as ``'higgs+goldstones'``; they need resummation and are shown only to display the shape.  Each particle adds a term of the form h^4 ln h^2 with
    its own weight n_i m_i^4: bosons enter with n > 0 and fermions with n < 0, and the top dominates in magnitude (about 40 times the W). The sign of a given term at a given h depends
    on the logarithm, that is on mu: only the total, with the running of the tree parameters, is scale independent.

    :param h: array of field values in GeV.
    :param mu: renormalisation scale in GeV (default v).
    :returns: dict name -> array, plus ``'tree'`` and ``'sum_fermions_and_gauge'``.
    :rtype: dict
    """
    h = np.asarray(h, float); v = fermi_vev(); mu = v if mu is None else mu; hs = higgs_sector(); lam, mu2 = hs["lam"], hs["mu2"]; out = {}
    f = lambda m2, n, c: n*m2**2/(64*math.pi**2)*(np.log(np.maximum(np.abs(m2), 1e-12)/mu**2) - c)
    tot = np.zeros_like(h)
    for p in particle_content_for_potential():
        m2 = (p["slope"]*h)**2; out[p["name"]] = f(m2, p["n"], p["c"]); tot += out[p["name"]]
    out["higgs+goldstones"] = f(3*lam*h**2 - mu2, 1, 3/2) + f(lam*h**2 - mu2, 3, 3/2)
    out["tree"] = -0.5*mu2*h**2 + 0.25*lam*h**4; out["sum_fermions_and_gauge"] = tot
    return out


def finite_temperature_hat(T: float, h=None) -> dict:
    """The hat at temperature T in the standard high-temperature expansion of the one-loop potential (Dine et al. 1992; Quiros 1999):
    V(h, T) = D (T^2 - T0^2) h^2 - E T h^3 + lambda_T h^4 / 4, with D = (2 m_W^2 + m_Z^2 + 2 m_t^2)/(8 v^2), E = (2 m_W^3 + m_Z^3)/(4 pi v^3),
    T0^2 = (m_h^2 - 8 B v^2)/(4 D), B = 3 (2 m_W^4 + m_Z^4 - 4 m_t^4)/(64 pi^2 v^4).  ESTABLISHED as an approximation; it predicts a weak first-order transition
    at m_h = 125 GeV where lattice calculations find a smooth crossover (the one-loop expansion fails near T_c: infrared problems of the Higgs).
    VALIDITY: the expansion needs T well above the particle masses; below about 100 GeV the logarithm in lambda_T makes h_min exceed v (1.035 v at 50 GeV, an artifact).
    Use the zero-temperature hat there.

    :param T: temperature in GeV (T = 0 returns the zero-temperature hat).
    :param h: optional array of field values at which to tabulate V.
    :returns: dict ``D, E, T0, lam_T``, ``h_min`` (global minimum, the brim radius), ``depth`` = V(0) - V(h_min), and ``V`` when ``h`` is given.
    :rtype: dict
    """
    v = fermi_vev(); mW, mZ, mt = pdg_mass("W+")[0], pdg_mass("Z0")[0], pdg_mass("t")[0]; hs = higgs_sector(); lam = hs["lam"]
    D = (2*mW**2 + mZ**2 + 2*mt**2)/(8*v**2); E = (2*mW**3 + mZ**3)/(4*math.pi*v**3); B = 3*(2*mW**4 + mZ**4 - 4*mt**4)/(64*math.pi**2*v**4)
    T0 = math.sqrt((hs["m_h"]**2 - 8*B*v**2)/(4*D))
    if T <= 0:
        lamT = lam; V = (lambda x: -0.5*hs["mu2"]*x**2 + 0.25*lam*x**4)
    else:
        lnaB, lnaF = 5.4076, 2.6351
        lamT = lam - 3/(16*math.pi**2*v**4)*(2*mW**4*math.log(mW**2/(math.exp(lnaB)*T**2)) + mZ**4*math.log(mZ**2/(math.exp(lnaB)*T**2)) - 4*mt**4*math.log(mt**2/(math.exp(lnaF)*T**2)))
        V = (lambda x: D*(T**2 - T0**2)*x**2 - E*T*x**3 + 0.25*lamT*x**4)
    xs = np.linspace(0, 1.6*v, 4001); vs = V(xs); i = int(np.argmin(vs)); out = {"D": D, "E": E, "T0": T0, "lam_T": lamT, "h_min": float(xs[i]), "depth": float(vs[0] - vs[i])}
    if h is not None: out["V"] = V(np.asarray(h, float))
    return out


# ------------------------------------------------------------------ bridge to the hat potential
def hat_model() -> dict:
    """The Standard-Model Higgs hat as a model dict that the path-of-action tools accept (``witches_hat.maths.lagrangian_sm`` with this engine's lambda, mu^2).

    :returns: model dict with ``V``, ``brim_radius`` (= v), ``depth`` (= lambda v^4 / 4).
    :rtype: dict
    """
    from ..witches_hat import maths as W
    h = higgs_sector(); return W.lagrangian_sm(mu2=h["mu2"], lam=h["lam"])


def verify() -> dict:
    """Closure checks: anomalies cancel, group identities close, the symbolic masses match the tree relations, parameter counts are 19/26/28,
    the CKM matrix is unitary, the Higgs expansion gives m_h^2 = 2 lambda v^2.

    :returns: dict of booleans and residuals.
    :rtype: dict
    """
    an = anomaly_check(); gc = group_checks(); sy = ew_mass_matrix_symbolic(); g, gp, v = sy["symbols"]; ev = sorted(float(sp.N(k.subs({g: 0.65, gp: 0.36, v: 246.0}))) for k, m in sy["eigenvalues"].items() for _ in range(m))
    pe = [0.0, (0.65*246/2)**2, (0.65*246/2)**2, (0.65**2 + 0.36**2)*246**2/4]; ex = sp.simplify(higgs_potential_expansion()["m_h2"] - 2*higgs_potential_expansion()["symbols"][0]*higgs_potential_expansion()["symbols"][1]**2)
    return {"anomalies_cancel": an["all_zero"] and an["witten_ok"], "su2_closure": gc["SU2"]["closure_residual"], "su3_closure": gc["SU3"]["closure_residual"],
            "su3_jacobi": gc["SU3"]["jacobi_residual"], "boson_masses_match": bool(np.allclose(sorted(pe), ev, rtol=1e-9, atol=1e-6)),
            "parameters": (parameter_count("massless")["total"], parameter_count("dirac")["total"], parameter_count("majorana")["total"]),
            "ckm_unitarity": unitarity_residual(ckm_matrix()), "m_h2_identity": ex == 0}
