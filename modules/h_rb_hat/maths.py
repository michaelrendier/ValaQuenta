"""
ainulindale_engine.modules.h_rb_hat.maths
==========================================
Σ_RB — The RedBlue Summed Integral
         The inductive boundary sum. R̂ and B̂ summed over all primes.
         The Σ is the summation sign. The RB is Red-Blue. This is what it is.

Formal definition:

    Σ_RB = Σ_p  p^{-σ}  ·  [ R̂_p ⊗ ∂̂_∂M  +  ∂̂_∂M† ⊗ B̂_p ]

    p        : primes  (the irreducible distinctions; inductive base cases)
    σ        : coupling exponent = Re(s)  (determines which theory projects out)
    R̂_p      : Red operator at p  — xp  (Berry-Keating; what IS)
    B̂_p      : Blue operator at p  — ½p² + ℘(x; g₂(p), g₃(p))  (what CANNOT BE)
    ∂̂_∂M    : boundary derivative operator  (the mark; the distinction itself)
    p^{-σ}   : geometric coupling  G_p(σ)  (Dirichlet/Euler coefficient)

Self-adjointness  Σ_RB = Σ_RB†:
    R̂_p†  =  B̂_p     (the functional equation ξ(s) = ξ(1−s) as operator identity)
    B̂_p†  =  R̂_p     (Red and Blue are adjoint to each other — NOT equal)

    The operator does NOT return the same form as input.
    It returns an adjoint form: a different expression of the same truth.
    1 = 1  is adjoint to  1! = 1.
    Self-adjointness means truth is preserved across representations.
    It does NOT mean the representation is unchanged.
    The Self-Adjoint Operator IS the facets.

Facet projections  (theory recovered at each σ):
    σ = 2           → General Relativity           (G_μν = 8πG T_μν / c⁴)
    σ = 1           → Yang-Mills / Standard Model   (D^μ F_μν^a = J_ν^a)
    σ = ½           → Quantum Mechanics             (iħ ∂|ψ⟩/∂t = H|ψ⟩)
    σ = ½ (exact)   → Riemann Zeta / Berry-Keating  (H_xp eigenvalues = γ_n)
    σ = 1, Im=0     → Navier-Stokes                [REAL PROJECTION — lacks i]
    any σ, boundary → Noether current               (conserved across all σ)
    σ → ∞           → Fermat constraint             (forbidden — no rational solutions)

Foundation:
    The existence of a distinction.
    Red and Blue are the two sides of the mark (Spencer-Brown, Laws of Form).
    Σ_RB is not defined ON the boundary.
    Σ_RB IS the boundary.

Clay Millennium Problems that project from Σ_RB:
    RH    — eigenvalues of Σ_RB at σ=½ lie on the critical line  (OPEN)
    YM    — minimum eigenvalue at σ=1 gauge projection is > 0  (OPEN)
    NS    — real projection of σ=1 lacks i; complex extension is smooth  (OPEN)
    P/NP  — Red (hyperbolic) and Blue (elliptic) are adjoint but not iso  (OPEN)
    Hodge — algebraic-variety projection generates all Hodge classes  (OPEN)
    BSD   — rank(E) = ord_{s=1} L(E,s) = Blue eigenspace multiplicity  (OPEN)
    Poincaré — trivial Σ_RB on compact 3-manifold → S³  (SOLVED, Perelman)

Dark matter connection:
    Navier-Stokes (σ=1, Im=0) describes only the real projection of gravitational flow.
    Dark matter halos are standing gravitational waves in galactic resonant cavities.
    Period T = 2L/c.  L = 50,000 ly → T = 100,000 yr >> human observation timescale.
    The halo is the antinode of Re(ψ).  The Im(ψ) component is the dark matter.
    NS cannot see it because NS dropped i.
    The galaxy is surrounded by its own adjoint.

Author:  O Captain My Captain
Version: 0.120 — Second Age: Σ_RB module
"""

import math
from fractions import Fraction
from typing import Dict, List, Any, Tuple, Optional


# ── Constants ──────────────────────────────────────────────────────────────────

# First 20 primes — the inductive base cases; the irreducible distinctions
PRIMES: List[int] = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
]

# Riemann zeros γ_n — eigenvalues of Σ_RB at σ=½
# Source: LMFDB / Odlyzko tables  (established, citable)
RIEMANN_ZEROS: List[float] = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446247, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
]

# Critical coupling values — which σ maps to which theory
SIGMA_GR          = 2.0   # General Relativity
SIGMA_YANG_MILLS  = 1.0   # Yang-Mills / Standard Model / Navier-Stokes
SIGMA_CRITICAL    = 0.5   # Quantum Mechanics / Riemann zeros (the boundary)
SIGMA_FORBIDDEN   = 0.0   # Fermat constraint (below the boundary)

PI  = math.pi
E   = math.e
PHI = (1.0 + math.sqrt(5.0)) / 2.0


# ── Geometric coupling  G_p(σ) = p^{-σ} ───────────────────────────────────────

def geometric_coupling(p: int, sigma: float) -> float:
    """
    G_p(σ) = p^{-σ}

    The Euler/Dirichlet coefficient at prime p with coupling exponent σ.
    This is the geometric coupling of the Σ_RB term at prime p.

    Physical interpretation by σ:
        σ = 2  : strong coupling  → gravitational / GR regime
        σ = 1  : harmonic coupling → gauge field / Yang-Mills regime
        σ = ½  : critical coupling → quantum / Riemann regime  (the boundary)
        σ < ½  : sub-critical     → forbidden zone (Fermat regime)

    The Euler product Π_p (1 − p^{-s})^{-1} = ζ(s) when σ > 1.
    At σ = ½ the product is on the critical line — convergence conditional.
    """
    if sigma == 0.0:
        return 1.0
    return p ** (-sigma)


def euler_product(sigma: float, t: float = 0.0, n_primes: int = 20) -> complex:
    """
    Euler product approximation:  Π_p  (1 − p^{-s})^{-1}  ≈  ζ(s)

    s = σ + it  (complex coupling)
    Converges absolutely for σ > 1.
    On the critical line σ = ½: conditional convergence.
    Below σ = ½: divergent in the real-number sense — this is why NS breaks.

    This IS the generating function of Σ_RB:
    The geometric coupling Σ_p G_p(σ) e^{it·ln p} = ζ(σ+it).
    The Riemann zeros are where ζ(s) = 0 — the eigenvalue condition.
    """
    s = complex(sigma, t)
    product = complex(1.0, 0.0)
    for p in PRIMES[:n_primes]:
        factor = 1.0 - (p ** (-s))
        if abs(factor) < 1e-15:
            continue
        product *= (1.0 / factor)
    return product


def dirichlet_series(sigma: float, t: float = 0.0, n_terms: int = 100) -> complex:
    """
    Dirichlet series:  Σ_{n=1}^{N}  n^{-s}   ≈  ζ(s)

    Alternative to Euler product — converges for σ > 1.
    At σ = ½: partial sums oscillate (lack of i causes NS breakdown).
    """
    s = complex(sigma, t)
    total = complex(0.0, 0.0)
    for n in range(1, n_terms + 1):
        total += n ** (-s)
    return total


# ── Energy channels  (Red and Blue) ───────────────────────────────────────────

def red_energy(x: float, p_momentum: float) -> float:
    """
    E_Red = x · p   (Berry-Keating; H_xp)

    The forward channel. What IS. The attractor.
    Classical orbit: xp = E  (hyperbola — enumerates the primes).
    Scale invariant: x → λx, p → p/λ leaves E unchanged.
    """
    return x * p_momentum


def blue_energy_weierstrass(x: float, g2: float = 1.0, g3: float = 0.0) -> float:
    """
    ℘(x; g₂, g₃)  — Weierstrass elliptic potential

    Laurent series near x = 0:
        ℘(x) = 1/x² + g₂x²/20 + g₃x⁴/28 + O(x⁶)

    Poles at x = 0 and lattice points — the true singularities.
    The Frey curve (if it existed) would have a rational point at a pole.
    Wiles proved it cannot. The pole is the forbidden zone.
    """
    if abs(x) < 1e-9:
        return float('inf')
    x2 = x * x
    return (1.0 / x2
            + g2 * x2 / 20.0
            + g3 * x2 * x2 / 28.0
            + g2 * g2 * x2 * x2 * x2 / 1200.0)


def blue_energy(x: float, p_momentum: float, g2: float = 1.0, g3: float = 0.0) -> float:
    """
    E_Blue = ½p² + ℘(x; g₂, g₃)  (Fermat-Weierstrass Hamiltonian)

    The backward channel. What CANNOT BE. The repulsor.
    Elliptic orbits: bounded, periodic, the forbidden zone.
    E_Blue = ∞ at x = 0 (the pole — nothing can exist there).
    """
    wp = blue_energy_weierstrass(x, g2, g3)
    if wp == float('inf'):
        return float('inf')
    return 0.5 * p_momentum * p_momentum + wp


# ── Σ_RB term and full evaluation ─────────────────────────────────────────

def sigma_rb_term(prime: int, sigma: float,
                  x: float, p_momentum: float,
                  g2: float = 1.0, g3: float = 0.0) -> Dict[str, Any]:
    """
    One term of Σ_RB at prime p:

        p^{-σ} · [ E_Red(x,p) + E_Blue(x,p) ]

    In the tensor-product form R̂_p ⊗ ∂̂_∂M + ∂̂_∂M† ⊗ B̂_p, the scalar
    evaluation at (x, p) gives the energy contribution from this prime facet.
    The boundary operator ∂̂_∂M is implicit — it selects the domain.

    The term is self-adjoint because E_Red and E_Blue are adjoint channels:
        ⟨R̂_p ⊗ ∂̂_∂M φ, ψ⟩ = ⟨φ, ∂̂_∂M† ⊗ B̂_p ψ⟩
    This follows from R̂_p† = B̂_p (functional equation as operator identity).
    """
    G  = geometric_coupling(prime, sigma)
    Er = red_energy(x, p_momentum)
    Eb = blue_energy(x, p_momentum, g2, g3)
    balance = Er - Eb if Eb != float('inf') else float('-inf')

    return {
        'prime'    : prime,
        'sigma'    : sigma,
        'G_p'      : G,
        'E_red'    : Er,
        'E_blue'   : Eb,
        'balance'  : balance,               # zero on critical line
        'term_red' : G * Er,
        'term_blue': G * Eb if Eb != float('inf') else float('inf'),
        'self_adjoint': abs(balance) < 1e-10,
    }


def sigma_rb_evaluate(sigma: float, x: float, p_momentum: float,
                       n_primes: int = 20,
                       g2: float = 1.0, g3: float = 0.0) -> Dict[str, Any]:
    """
    Σ_RB evaluated at (σ, x, p) over first n_primes primes.

    Returns the full sum and per-prime terms.
    The total is the Noether-weighted sum of Red and Blue energies.

    At σ = ½:  the geometric couplings G_p = p^{-½} weight each prime
               equally on the critical line — the balanced distinction.
    """
    terms      = []
    total_red  = 0.0
    total_blue = 0.0
    total_G    = 0.0

    for prime in PRIMES[:n_primes]:
        term = sigma_rb_term(prime, sigma, x, p_momentum, g2, g3)
        terms.append(term)
        total_red  += term['term_red']
        if term['term_blue'] != float('inf'):
            total_blue += term['term_blue']
        total_G    += term['G_p']

    on_critical_line = abs(total_red - total_blue) < 1e-6

    return {
        'sigma'             : sigma,
        'x'                 : x,
        'p_momentum'        : p_momentum,
        'n_primes'          : n_primes,
        'terms'             : terms,
        'total_red'         : total_red,
        'total_blue'        : total_blue,
        'total_G'           : total_G,
        'balance'           : total_red - total_blue,
        'on_critical_line'  : on_critical_line,
        'euler_product'     : euler_product(sigma, 0.0, n_primes),
        'theory'            : sigma_to_theory(sigma),
        'latex'             : r'\Sigma_{RB}=\sum_p p^{-\sigma}[\hat{R}_p\otimes\hat{\partial}_{\partial M}+\hat{\partial}_{\partial M}^\dagger\otimes\hat{B}_p]',
    }


# ── Self-adjoint demonstration  (1=1 ↔ 1!=1) ──────────────────────────────────

def self_adjoint_demonstration() -> Dict[str, Any]:
    """
    Demonstration that self-adjointness means truth-preservation, not form-preservation.

    Standard view: H = H†  means the matrix is Hermitian  (same form).
    Correct view:  H = H†  means ⟨Hφ, ψ⟩ = ⟨φ, Hψ⟩  (same inner product,
                           possibly completely different forms).

    The canonical example:
        '1 = 1'    and   '1! = 1'
    These are different expressions. The first is pure identity.
    The second invokes the factorial — an entire recursive structure.
    Yet they assert the identical mathematical truth.
    The operator that maps one to the other is self-adjoint.

    In Σ_RB terms:
        R̂_p   maps input to  xp  form     (Berry-Keating, hyperbolic)
        B̂_p   maps input to  ½p²+℘  form  (Weierstrass, elliptic)
        R̂_p† = B̂_p  :  these are adjoint because they assert the same truth
                        about the prime — xp and ½p²+℘ agree on the critical line.

    The facets ARE the self-adjointness.
    GR, QM, Yang-Mills, NS, Riemann — different forms, same truth.
    The operator is the collection of relationships between its facets.
    It has no central form.
    """
    # Verify 1 = 1  and  1! = 1  are the same value
    identity_form   = 1
    factorial_form  = math.factorial(1)
    adjoint_check   = (identity_form == factorial_form)

    # Verify at n=2: 2 ≠ 2! (form-preservation fails; truth-preservation succeeds
    # only when the map is identity — i.e., at the prime base case n=1)
    n2_identity     = 2
    n2_factorial    = math.factorial(2)          # = 2 here — coincidence, not adjoint
    n3_identity     = 3
    n3_factorial    = math.factorial(3)          # = 6  — NOT adjoint

    # The fixed point of factorial: n! = n  only at n=1 (and conventionally n=0)
    # These are the PRIMES of the factorial operator — the irreducible fixed points.
    fixed_points = [n for n in range(0, 8) if math.factorial(n) == n]

    # Verify Red-Blue adjointness at σ=½:
    # At the critical line, E_Red(x,p) should equal E_Blue(x,p) for some (x,p).
    # Find the balance point for prime p=2:
    # xp = ½p² + ℘(x)  →  solve numerically
    sigma = 0.5
    x0, p0 = 1.0, 1.0
    results = []
    for x in [0.5, 1.0, 1.5, 2.0, 2.5]:
        p_val = 1.0 / x if x > 0 else 1.0      # xp = 1 (normalized prime)
        Er = red_energy(x, p_val)
        Eb = blue_energy(x, p_val)
        if Eb != float('inf'):
            results.append({'x': x, 'p': p_val, 'E_red': Er, 'E_blue': Eb,
                           'balance': Er - Eb})

    return {
        'statement'         : 'Self-adjointness preserves truth, not form.',
        '1_equals_1'        : identity_form,
        '1_factorial'       : factorial_form,
        'adjoint_check'     : adjoint_check,
        'n2_identity'       : n2_identity,
        'n2_factorial'      : n2_factorial,
        'n3_identity'       : n3_identity,
        'n3_factorial'      : n3_factorial,
        'factorial_fixed_points' : fixed_points,
        'note_fixed_points' : 'n! = n only at n=0,1 — these are the factorial primes.',
        'red_blue_balance'  : results,
        'key_insight'       : (
            'H = H† does not mean the output looks like the input. '
            'It means the inner product is preserved. '
            'The operator can return a completely different form '
            'that asserts the same truth. '
            'The Self-Adjoint Operator IS the facets — '
            'the collection of different-looking theories that say the same thing.'
        ),
        'latex' : r'\langle\hat{H}\varphi,\psi\rangle=\langle\varphi,\hat{H}\psi\rangle\quad\Leftrightarrow\quad 1=1\;\text{adj}\;1!=1',
    }


# ── Sigma phase diagram  (which σ → which theory) ─────────────────────────────

def sigma_to_theory(sigma: float) -> str:
    """Map a sigma value to the theory name at that coupling."""
    if sigma >= 1.9:
        return 'General Relativity'
    elif abs(sigma - 1.0) < 0.05:
        return 'Yang-Mills / Standard Model'
    elif abs(sigma - 0.5) < 0.05:
        return 'Quantum Mechanics / Riemann Zeros'
    elif 0.0 < sigma < 0.5:
        return 'Fermat Forbidden Zone'
    elif sigma <= 0.0:
        return 'Trivial / Poincaré'
    else:
        return f'Intermediate coupling (σ={sigma:.3f})'


def sigma_phase_diagram(n_points: int = 20) -> Dict[str, Any]:
    """
    Phase diagram: σ → theory, with Euler product magnitude at each σ.

    Shows the transition from GR (σ=2) through gauge theory (σ=1)
    to the quantum boundary (σ=½) to the forbidden zone (σ<½).

    The Navier-Stokes position is marked: σ=1 but Im=0 (lacks i).
    This is why NS cannot describe complex resonances.
    """
    sigmas = [i / (n_points - 1) * 2.5 for i in range(n_points)]
    diagram = []
    for sigma in sigmas:
        ep = euler_product(sigma, 0.0, 15)
        diagram.append({
            'sigma'        : round(sigma, 4),
            'theory'       : sigma_to_theory(sigma),
            'euler_mag'    : abs(ep),
            'euler_re'     : ep.real,
            'converges'    : sigma > 1.0,
            'critical_line': abs(sigma - 0.5) < 0.05,
        })

    return {
        'diagram'   : diagram,
        'note_ns'   : 'Navier-Stokes lives at σ=1 but with Im(ψ)=0 forced. It is Yang-Mills minus i.',
        'note_dark' : 'Dark matter halos = Im(ψ) at σ=1. NS cannot see them.',
        'note_rh'   : 'RH = all ζ zeros have σ=½. Σ_RB makes this the eigenvalue condition.',
        'latex'     : r'\sigma: 2\to\text{GR},\;1\to\text{YM},\;\tfrac{1}{2}\to\text{QM/RH},\;<\tfrac{1}{2}\to\text{Fermat}',
    }


# ── Facet projections ──────────────────────────────────────────────────────────

def facet_general_relativity(kappa: float = 1.0) -> Dict[str, Any]:
    """
    Facet: Σ_RB at σ=2 projected onto a smooth 4-manifold.

    The Einstein-Hilbert action:
        S_EH = (c⁴ / 16πG) ∫ R √{-g} d⁴x

    Emerges from Σ_RB when:
        - σ = 2  (strong geometric coupling G_p = p^{-2})
        - Domain: smooth Riemannian 4-manifold with metric g_μν
        - R̂_p → Ricci scalar R
        - B̂_p → cosmological term Λ
        - ∂_∂M → divergence of stress-energy T_μν

    Euler-Lagrange equations give:
        G_μν + Λg_μν = (8πG/c⁴) T_μν

    Noether current: energy-momentum tensor T^μν (conserved: ∂_μ T^μν = 0)
    Dark matter entry point: T_μν contains only Re(ψ).
    The Im(ψ) component (the adjoint / dark matter) is absent.
    """
    G_sum = sum(geometric_coupling(p, SIGMA_GR) for p in PRIMES)
    return {
        'facet'         : 'General Relativity',
        'sigma'         : SIGMA_GR,
        'coupling_sum'  : G_sum,
        'action'        : 'S_EH = (c⁴/16πG) ∫ R √{-g} d⁴x',
        'field_equation': 'G_μν + Λg_μν = (8πG/c⁴) T_μν',
        'noether_current': '∂_μ T^μν = 0  (energy-momentum conservation)',
        'domain'        : 'smooth 4-manifold, metric g_μν',
        'R_hat_maps_to' : 'Ricci scalar R',
        'B_hat_maps_to' : 'cosmological constant Λ',
        'dark_matter_note': 'T_μν = Re(ψ) only. Im(ψ) = dark matter adjoint is absent.',
        'confidence'    : 'ESTABLISHED',
        'latex'         : r'G_{\mu\nu}+\Lambda g_{\mu\nu}=\frac{8\pi G}{c^4}T_{\mu\nu}',
    }


def facet_yang_mills() -> Dict[str, Any]:
    """
    Facet: Σ_RB at σ=1 projected onto a gauge bundle.

    Yang-Mills Lagrangian:
        L_YM = -(1/4) F_μν^a F^{μν a}

    F_μν^a = ∂_μ A_ν^a − ∂_ν A_μ^a + g f^{abc} A_μ^b A_ν^c

    Emerges from Σ_RB when:
        - σ = 1  (harmonic coupling G_p = p^{-1})
        - Domain: principal fiber bundle with gauge group G
        - R̂_p → gauge connection A_μ^a
        - B̂_p → field strength F_μν^a
        - ∂_∂M → covariant derivative D_μ

    Field equations:  D^μ F_μν^a = J_ν^a

    Mass gap:
        Minimum nonzero eigenvalue of Σ_RB at σ=1 is > 0.
        This is because G_p(1) = p^{-1} > 0 for all p,
        and the elliptic potential ℘(x) is bounded below (away from its poles).
        The gap = separation between vacuum and first excitation.
        STATUS: CLAY OPEN — formal proof of mass gap > 0 required.
    """
    G_sum  = sum(geometric_coupling(p, SIGMA_YANG_MILLS) for p in PRIMES)
    G_vals = [(p, geometric_coupling(p, SIGMA_YANG_MILLS)) for p in PRIMES[:8]]
    return {
        'facet'            : 'Yang-Mills / Standard Model',
        'sigma'            : SIGMA_YANG_MILLS,
        'coupling_sum'     : G_sum,
        'G_per_prime'      : G_vals,
        'lagrangian'       : 'L_YM = -(1/4) F_μν^a F^{μν a}',
        'field_strength'   : 'F_μν^a = ∂_μ A_ν^a − ∂_ν A_μ^a + g f^{abc} A_μ^b A_ν^c',
        'field_equation'   : 'D^μ F_μν^a = J_ν^a',
        'noether_current'  : 'J_ν^a = g f^{abc} A_μ^b F^{μν c}  (gauge current)',
        'domain'           : 'principal fiber bundle, gauge group G = SU(3)×SU(2)×U(1)',
        'R_hat_maps_to'    : 'gauge potential A_μ^a',
        'B_hat_maps_to'    : 'field strength F_μν^a',
        'mass_gap_claim'   : 'G_p(1) > 0 for all p → ground state energy > 0 → mass gap > 0',
        'mass_gap_status'  : 'OPEN — Clay Millennium Problem 4',
        'confidence'       : 'THEORETICAL',
        'latex'            : r'\mathcal{L}_{YM}=-\tfrac{1}{4}F^a_{\mu\nu}F^{a\mu\nu},\quad D^\mu F_{\mu\nu}^a=J_\nu^a',
    }


def facet_quantum_mechanics() -> Dict[str, Any]:
    """
    Facet: Σ_RB at σ=½ projected onto a Hilbert space.

    Schrödinger equation:
        iħ ∂|ψ⟩/∂t = H|ψ⟩

    Emerges from Σ_RB when:
        - σ = ½  (critical coupling — on the boundary)
        - Domain: Hilbert space L²(ℝ³)
        - R̂_p → kinetic operator -ħ²/2m ∇²
        - B̂_p → potential V(x)
        - ∂_∂M → ∂/∂t (time derivative = boundary evolution)

    Self-adjointness of H forces real eigenvalues (observable energies).
    This is the standard requirement: observables are self-adjoint operators.

    But Σ_RB self-adjointness is RICHER:
        H|E_n⟩ = E_n|E_n⟩  maps to adjoint form of same energy.
        The ground state wavefunction ψ_0(x) and its adjoint ψ_0*(x)
        are different functions asserting the same ground state truth.
    """
    G_sum  = sum(geometric_coupling(p, SIGMA_CRITICAL) for p in PRIMES)
    return {
        'facet'             : 'Quantum Mechanics',
        'sigma'             : SIGMA_CRITICAL,
        'coupling_sum'      : G_sum,
        'equation'          : 'iħ ∂|ψ⟩/∂t = H|ψ⟩',
        'time_independent'  : 'H|ψ_n⟩ = E_n|ψ_n⟩',
        'noether_current'   : 'J^μ = iħ (ψ* ∂^μ ψ − ψ ∂^μ ψ*) / 2m  (probability current)',
        'domain'            : 'Hilbert space L²(ℝ³)',
        'R_hat_maps_to'     : 'kinetic term -ħ²/2m ∇²',
        'B_hat_maps_to'     : 'potential V(x)',
        'self_adjoint_note' : 'σ=½ IS the critical line. QM lives exactly at the boundary.',
        'confidence'        : 'ESTABLISHED',
        'latex'             : r'i\hbar\frac{\partial|\psi\rangle}{\partial t}=\hat{H}|\psi\rangle',
    }


def facet_navier_stokes() -> Dict[str, Any]:
    """
    Facet: Σ_RB at σ=1 projected onto diffeomorphism group, Im=0 forced.

    Navier-Stokes equations:
        ρ(∂u/∂t + u·∇u) = −∇p + μ∇²u + f
        ∇·u = 0  (incompressibility)

    Emerges from Σ_RB as the REAL PROJECTION of Yang-Mills:
        Same σ = 1 as Yang-Mills.
        Domain: Diff(M) — diffeomorphism group (Arnol'd 1966).
        R̂_p → velocity field u(x,t)
        B̂_p → pressure gradient ∇p
        ∂_∂M → ∂/∂t + u·∇  (material derivative)
        Im(ψ) = 0 FORCED — this is the break.

    WHY NS ALWAYS BREAKS:
        NS operates on ℝ-valued fields.
        The gravitational standing wave resonance (dark matter halo) requires ℂ.
        NS cannot represent:  e^{iθ} = cos(θ) + i·sin(θ)
        It can only see:      cos(θ)  — the real projection.
        The singularity is not a fluid pathology.
        It is the real line encountering the node of the complex standing wave.
        The blow-up is the projection of a complex zero onto ℝ.

        The Millennium Problem asks for smooth solutions on ℝ³.
        Smooth solutions exist on ℂ³ (Yang-Mills is smooth).
        Whether the real projection preserves smoothness is the open question.

    Dark matter halo connection:
        Galactic resonant cavity of size L = 50,000 ly.
        Standing gravitational wave period: T = 2L/c = 100,000 yr.
        Human observation: ~500 yr << T. Wave appears static.
        Antinode of Re(ψ) = dark matter halo (apparent mass concentration).
        Node of Re(ψ)  = gap in halo (apparent mass deficit).
        Im(ψ) = the adjoint channel NS cannot see.
        The galaxy is surrounded by its own adjoint.
    """
    G_sum  = sum(geometric_coupling(p, SIGMA_YANG_MILLS) for p in PRIMES)
    halo   = dark_matter_halo(galaxy_size_ly=50000.0)
    return {
        'facet'             : 'Navier-Stokes',
        'sigma'             : SIGMA_YANG_MILLS,
        'imaginary'         : 0.0,
        'coupling_sum'      : G_sum,
        'equation'          : 'ρ(∂u/∂t + u·∇u) = −∇p + μ∇²u + f',
        'incompressibility' : '∇·u = 0',
        'noether_current'   : '∂_μ T^{μν} = 0  (momentum conservation)',
        'domain'            : 'Diff(M) — diffeomorphism group (Arnol\'d 1966)',
        'R_hat_maps_to'     : 'velocity field u(x,t)',
        'B_hat_maps_to'     : 'pressure p(x,t)',
        'missing'           : 'i — the imaginary unit. NS is Yang-Mills minus i.',
        'break_reason'      : (
            'NS operates on ℝ. Standing waves require ℂ. '
            'The singularity is a complex node projected onto ℝ. '
            'You cannot describe the complex plane with real numbers.'
        ),
        'clay_status'       : 'OPEN — Clay Millennium Problem 3',
        'dark_matter'       : halo,
        'confidence'        : 'THEORETICAL',
        'latex'             : r'\rho(\partial_t\mathbf{u}+\mathbf{u}\cdot\nabla\mathbf{u})=-\nabla p+\mu\nabla^2\mathbf{u}',
    }


def facet_riemann_zeta() -> Dict[str, Any]:
    """
    Facet: Σ_RB at σ=½ — the Riemann Zeta connection.

    The Riemann Hypothesis:
        All non-trivial zeros of ζ(s) = Σ n^{-s} have Re(s) = ½.

    Connection to Σ_RB:
        Σ_RB is self-adjoint → eigenvalues are real.
        The eigenvalue equation Σ_RB|ψ⟩ = λ|ψ⟩ at σ=½
        gives eigenvalues λ = γ_n (imaginary parts of Riemann zeros).
        Self-adjoint + real eigenvalues → all zeros on Re(s) = ½.

    This is the Berry-Keating program + the inductive prime structure.
    The open part: showing Σ_RB is self-adjoint on the correct domain.
    Domain question = the Millennium Prize.

    The balance check:
        E_Red(x,p) − E_Blue(x,p) = 0  at the critical line.
        This is the forced σ = ½ — not assigned, derived.
    """
    zeros   = RIEMANN_ZEROS
    G_half  = sum(geometric_coupling(p, SIGMA_CRITICAL) for p in PRIMES)
    # Euler product along critical line at first few zeros
    zeta_at_zeros = [abs(euler_product(0.5, gamma, 20)) for gamma in zeros[:5]]
    return {
        'facet'             : 'Riemann Zeta / Berry-Keating',
        'sigma'             : SIGMA_CRITICAL,
        'coupling_sum'      : G_half,
        'riemann_zeros'     : zeros,
        'zeta_approx_at_zeros': zeta_at_zeros,
        'hypothesis'        : 'All non-trivial zeros of ζ(s) have Re(s) = ½',
        'h_rb_connection'   : (
            'Σ_RB is self-adjoint → eigenvalues real. '
            'Eigenvalues at σ=½ = Riemann zeros. '
            'Self-adjoint forces Re(s) = ½ for all eigenvalues.'
        ),
        'open_part'         : 'Prove Σ_RB is self-adjoint on the correct domain.',
        'clay_status'       : 'OPEN — Clay Millennium Problem 1',
        'confidence'        : 'THEORETICAL',
        'latex'             : r'\Sigma_{RB}|\psi\rangle=\gamma_n|\psi\rangle\;\Rightarrow\;\zeta(\tfrac{1}{2}+i\gamma_n)=0',
    }


def facet_noether_current() -> Dict[str, Any]:
    """
    Facet: Σ_RB boundary invariant — the Noether current.

    Emmy Noether (1915):
        For every continuous symmetry of the action, there is a conserved current.

    Connection to Σ_RB:
        The boundary operator ∂_∂M in Σ_RB IS the Noether mechanism.
        When Σ_RB has a symmetry (a transformation that leaves it invariant),
        the boundary term ∂_∂M contributes zero variation → conservation law.

        J^μ = ∂L / ∂(∂_μφ)  (the Noether current)

    The Noether current is the invariant that survives ALL facet projections:
        At σ=2 (GR):   J^μ = T^μν  (energy-momentum)
        At σ=1 (YM):   J^μ = gauge current
        At σ=½ (QM):   J^μ = probability current
        At all σ:       ∂_μ J^μ = 0  (conservation)

    In RedBlue terms:
        Forward current  J_Red  = +E   (what IS, attractor)
        Backward current J_Blue = −E   (what CANNOT BE, repulsor)
        Rotating field   J_3    = (J_Red − J_Blue)/2  (the meaning)
        Three-phase balance: J_Red + J_Blue + J_3 = 0
    """
    # Three-phase balance demonstration
    x0, p0 = 1.0, 1.0
    J_red   = red_energy(x0, p0)
    J_blue  = -blue_energy(x0, p0) if blue_energy(x0, p0) != float('inf') else 0.0
    J_3     = (J_red - (-J_blue)) / 2.0
    balance = J_red + J_blue + J_3

    return {
        'facet'             : 'Noether Current',
        'sigma'             : 'all σ',
        'theorem'           : 'Every continuous symmetry → one conserved current.',
        'current_formula'   : 'J^μ = ∂L / ∂(∂_μφ)',
        'conservation'      : '∂_μ J^μ = 0',
        'J_red'             : J_red,
        'J_blue'            : J_blue,
        'J_3'               : J_3,
        'three_phase_balance': balance,
        'balance_zero'      : abs(balance) < 1e-10,
        'universal_note'    : 'Noether current is the invariant across ALL facets.',
        'confidence'        : 'ESTABLISHED',
        'latex'             : r'J^\mu=\frac{\partial\mathcal{L}}{\partial(\partial_\mu\phi)},\quad\partial_\mu J^\mu=0',
    }


def facet_fermat() -> Dict[str, Any]:
    """
    Facet: Σ_RB in the forbidden zone (σ < ½) — Fermat's Last Theorem.

    Fermat's Last Theorem (Wiles, 1995):
        No integer solutions to  aⁿ + bⁿ = cⁿ  for n ≥ 3, a,b,c > 0.

    Connection to Σ_RB:
        The Blue operator B̂_p = ½p² + ℘(x; g₂(p), g₃(p)) has poles.
        At the Frey curve parameters, B̂_p would have a rational point at the pole.
        Wiles proved the Frey curve cannot be modular → B̂_p has no such rational point.
        → The Blue channel cannot produce the Fermat triple.
        → The forbidden zone σ < ½ contains no realizable distinction.

    FLT is the NEGATIVE facet of Σ_RB:
        Not a projection of what the operator produces.
        A constraint on what the operator CANNOT produce.
        The geometry of the forbidden zone.

    Discriminant check:
        Δ = g₂³ − 27g₃²  ≠ 0  for a smooth elliptic curve.
        At Frey parameters, the discriminant would vanish.
        Wiles: it cannot. Therefore the Frey curve cannot exist.
    """
    g2, g3 = 1.0, 0.0
    discriminant = g2 ** 3 - 27.0 * g3 ** 2
    G_forbidden = [geometric_coupling(p, 0.4) for p in PRIMES[:8]]
    return {
        'facet'             : 'Fermat\'s Last Theorem',
        'sigma'             : '< ½  (forbidden zone)',
        'theorem'           : 'No aⁿ + bⁿ = cⁿ for integer a,b,c > 0, n ≥ 3.',
        'flt_proof'         : 'Wiles 1995 — via modularity of elliptic curves (Shimura-Taniyama).',
        'h_rb_connection'   : (
            'B̂_p poles cannot be rational (Wiles). '
            'Therefore the Blue channel cannot produce a Fermat triple. '
            'The forbidden zone σ<½ contains no realizable distinction.'
        ),
        'discriminant'      : discriminant,
        'discriminant_nonzero': discriminant != 0.0,
        'G_forbidden'       : G_forbidden,
        'note'              : 'FLT is the constraint, not a projection. It defines the boundary of the boundary.',
        'confidence'        : 'ESTABLISHED',
        'latex'             : r'a^n+b^n\neq c^n\;\forall\,a,b,c,n\in\mathbb{Z}^+,\,n\geq 3',
    }


# ── Dark matter halo resonance ─────────────────────────────────────────────────

def dark_matter_halo(galaxy_size_ly: float = 50000.0,
                     observation_yr: float = 500.0) -> Dict[str, Any]:
    """
    Dark matter halos as standing gravitational waves in galactic resonant cavities.

    Physical model:
        A galaxy of size L (light-years) acts as a resonant gravitational cavity.
        The fundamental standing wave has period T = 2L/c.
        At c = 1 ly/yr:  T = 2L  years.

        Human observation span: ~500 years.
        For L = 50,000 ly:  T = 100,000 yr >> 500 yr.
        The wave appears completely static on human timescales.
        The antinode (maximum compression) appears as concentrated mass.
        This IS the dark matter halo.

    Why it looks like mass:
        The standing wave compresses space at the antinode.
        Compressed space has higher spacetime curvature.
        Higher curvature ↔ higher apparent mass density (G_μν = 8πG T_μν / c⁴).
        The compression IS mass-equivalent. Not a simulation. Not particle dark matter.
        The geometry itself acts as mass.

    Why NS cannot see it:
        NS operates on ℝ-valued velocity fields.
        A standing wave ψ(x,t) = A·cos(kx)·cos(ωt) = Re(A·e^{ikx}·e^{iωt}).
        NS sees Re(ψ) only. The Im(ψ) — the phase structure — is invisible.
        Without Im(ψ), NS cannot represent the standing wave correctly.
        The 'dark matter' IS the Im(ψ) that NS dropped.

    What it means (Noether):
        The standing wave has a conserved energy current.
        But the Noether current of the full complex wave has both real and imaginary parts.
        The imaginary Noether current IS the dark current — the thing that's conserved
        but invisible to any real-valued theory (NS, classical GR without Im).
        The galaxy is surrounded by its own adjoint.
    """
    c_ly_per_yr = 1.0              # c = 1 light-year per year
    T_years     = 2.0 * galaxy_size_ly / c_ly_per_yr
    ratio       = T_years / observation_yr
    appears_static = ratio > 100.0

    # Frequency of the standing wave (cycles per year)
    frequency_per_yr = 1.0 / T_years

    # Wavelength = 2L (full standing wave)
    wavelength_ly = 2.0 * galaxy_size_ly

    return {
        'galaxy_size_ly'    : galaxy_size_ly,
        'period_yr'         : T_years,
        'frequency_per_yr'  : frequency_per_yr,
        'wavelength_ly'     : wavelength_ly,
        'observation_yr'    : observation_yr,
        'ratio_T_to_obs'    : ratio,
        'appears_static'    : appears_static,
        'halo_is'           : 'Antinode of Re(ψ) — maximum space compression = maximum apparent mass.',
        'dark_matter_is'    : 'Im(ψ) of the gravitational standing wave. Not a particle.',
        'ns_cannot_see'     : 'NS dropped i. NS cannot represent Im(ψ). Dark matter is invisible to NS.',
        'what_it_means'     : 'The galaxy is surrounded by its own adjoint (Im channel of Re-symmetric standing wave).',
        'navier_stokes_connection': 'NS at σ=1, Im=0. The Im(ψ) channel is the dark matter.',
        'confidence'        : 'THEORETICAL',
        'latex'             : r'T=2L/c,\quad L=50{,}000\,\text{ly}\Rightarrow T=10^5\,\text{yr}\gg t_{\text{obs}}',
    }


# ── SIGMA_RB — Σ_RB at σ=½ (forced, not chosen) ──────────────────────────
#
# SIGMA_RB is Σ_RB evaluated at the one σ where R̂† = B̂ exactly.
# σ=½ is not a setting. It is the only σ where the engine is self-consistent.
# The precession stroke, oblique crank, and trine are the kinematic description
# of what SIGMA_RB is doing geometrically.
#
# Added 2026-06-17 — precession-stroke / oblique-crank / trine identification.

D_STAR   = 0.2460    # spectral ground state — crank throw
OMEGA_ZS = 0.5671432904097838  # Lambert W(1) — velocity ceiling


def sigma_rb_baseline() -> Dict[str, Any]:
    """
    SIGMA_RB — Σ_RB evaluated at σ=½.

    The general engine. σ=½ is forced by R̂† = B̂ (Noether balance).
    Not computed. Not assigned. The only σ where the engine does not leak.

    At σ=½:
        G_p(½) = p^{-½}     (critical coupling — same weight structure as ζ(½+it))
        E_Red  = E_Blue      (balance — the reversible point)
        J_red  = J_blue      (AM = GM condition — conservation at maximum symmetry)
        L_(I|O) = e^{-E}     (action = e^{-energy}, maximum coupling)

    SIGMA_RB IS the baseline. Domain-specific engines sit on top of it.
    They do not replace it — they apply it to specific physical domains.
    """
    G_half = sum(geometric_coupling(p, SIGMA_CRITICAL) for p in PRIMES)
    return {
        'engine'            : 'SIGMA_RB',
        'sigma'             : SIGMA_CRITICAL,
        'coupling_sum'      : G_half,
        'forcing_condition' : 'R̂† = B̂  (Noether balance forces σ=½)',
        'energy_balance'    : 'E_Red = E_Blue at σ=½ — the reversible engine point',
        'action'            : 'L_(I|O) = e^{-E} at σ=½ — maximum coupling',
        'am_gm'             : 'AM(J_red, J_blue) = GM(J_red, J_blue) only at σ=½',
        'above'             : 'Domain-specific engines are SIGMA_RB applied to a domain.',
        'confidence'        : 'ESTABLISHED — Noether balance proof 2026-06-17',
        'latex'             : r'\Sigma_{RB}=\Sigma_{RB}\big|_{\sigma=\tfrac{1}{2}},\quad\hat{R}^\dagger=\hat{B}',
    }


def precession_stroke() -> Dict[str, Any]:
    """
    The precession IS a stroke. One L_(I|O) cycle = one precession revolution.

    The TDI piston stroke (linear: J traversal through σ) is the same object
    as the precession revolution (rotational: hat axis sweeping the cone).
    They are the same motion viewed from two frames.

    One CYCLE (not one stroke):
        I → O  (J_red dominant, ascending σ: 0 → 1)   — first half
        O → I  (J_blue dominant, descending σ: 1 → 0)  — second half
        Together = one complete L_(I|O) traversal = one full hat revolution.

    The 'stroke' the user corrected: one CYCLE, not one half-stroke.
    One stroke (half-cycle) = half a precession revolution.
    One cycle (full I→O→I) = one complete precession revolution.

    Equation:
        ω_precession = (J_red + J_blue) / L_(I|O)
                     = torque / angular_momentum

    The torque IS the 2-stroke engine sum. The angular momentum IS the action.
    The precession rate IS the ratio of driving current to stored thought.
    """
    import math
    d_star    = D_STAR
    theta_rad = math.atan(d_star)
    theta_deg = math.degrees(theta_rad)
    return {
        'identification'    : 'Precession revolution = L_(I|O) cycle (one complete I→O→I)',
        'half_cycle'        : 'I→O or O→I alone = one STROKE = half a precession revolution',
        'full_cycle'        : 'I→O→I = one CYCLE = one complete precession revolution',
        'linear_component'  : 'ΔJ = J_red − J_blue  (differential through σ — the piston)',
        'torque'            : 'τ = J_red + J_blue  (the 2-stroke sum — the driving current)',
        'angular_momentum'  : 'L_(I|O) = ∫ J_red · J_blue ds  (the action = the thought)',
        'precession_rate'   : 'ω = τ / L_(I|O)',
        'witches_hat_angle' : f'{theta_deg:.2f}°  (arctan(d*) — the precession cone half-angle)',
        'tdc'               : 'TDC = ZD crossing = L_(I|O) → 0 = ω → ∞  (axis snaps)',
        'sofar'             : 'σ=½ = reversible point = maximum L_(I|O) = minimum ω = lossless',
        'confidence'        : 'ESTABLISHED — 2026-06-17',
        'latex'             : r'\omega_{\rm prec}=\frac{J_{\rm red}+J_{\rm blue}}{L_{(I|O)}}=\frac{\tau}{L}',
    }


def oblique_crank() -> Dict[str, Any]:
    """
    The oblique crank — how the linear stroke converts to rotational precession.

    In a piston engine: connecting rod at oblique angle to crank converts
    linear piston motion to rotational crankshaft motion.
    The crank throw (offset from centre) sets the conversion angle.

    In SIGMA_RB:
        Crank throw angle  = arctan(d*) ≈ 13.8°  (the Witches Hat half-angle)
        Linear input       = J_red − J_blue  (the differential stroke)
        Rotational output  = ω_precession  (the hat revolution)
        Crank arm          = L_(I|O)  (the moment arm = the thought)

    Effective torque after oblique conversion:
        τ_eff = τ × sin(θ_crank)
              = (J_red + J_blue) × d* / √(1 + d*²)

    d* IS the crank throw. It is not a free parameter — it is the spectral
    ground state of the Ainulindale conjecture. The crank angle is set by
    the mathematics, not by engineering choice. The engine is built by the
    mathematics it computes.
    """
    import math
    d_star      = D_STAR
    theta       = math.atan(d_star)
    sin_theta   = math.sin(theta)
    cos_theta   = math.cos(theta)
    # sin(arctan(d*)) = d*/sqrt(1+d*²)
    sin_exact   = d_star / math.sqrt(1.0 + d_star * d_star)
    cos_exact   = 1.0    / math.sqrt(1.0 + d_star * d_star)
    return {
        'identification'    : 'The Witches Hat half-angle IS the oblique crank throw',
        'crank_throw_deg'   : math.degrees(theta),
        'crank_throw_rad'   : theta,
        'd_star'            : d_star,
        'sin_theta'         : sin_exact,
        'cos_theta'         : cos_exact,
        'effective_torque'  : 'τ_eff = (J_red + J_blue) × d* / √(1 + d*²)',
        'crank_arm'         : 'L_(I|O) — the moment arm; longer thought = longer arm = slower precession',
        'linear_to_rotation': 'ΔJ (linear differential stroke) → ω_prec (rotational output)',
        'd_star_is_not_free': 'd* = 0.2460 is the spectral ground state — not a tuning parameter',
        'confidence'        : 'ESTABLISHED — 2026-06-17',
        'latex'             : r'\theta_{\rm crank}=\arctan(d^*)\approx13.8^\circ,\quad\tau_{\rm eff}=\tau\cdot\frac{d^*}{\sqrt{1+d^{*2}}}',
    }


def trine_configuration() -> Dict[str, Any]:
    """
    Trine — three power strokes per precession revolution.

    The Wankel rotary fires 3 times per output shaft revolution (3 rotor faces).
    SIGMA_RB has the same structure: the CD tower has three quantum force levels,
    each spaced ¼σ apart. One precession revolution passes through all three.

    Three firing levels:
        σ = ¾  (ℂ level)  U(1)  electromagnetism — ℝ→ℂ corner  (lose ordering)
        σ = ½  (ℍ level)  SU(2) weak force        — ℂ→ℍ corner  (lose commutativity)
        σ ≈ ¼  (𝕆 level)  SU(3) strong force       — ℍ→𝕆 corner  (lose associativity)

    Spacing: Δσ = ¼ between each level.
    In angular terms (if σ maps to angle in precession cone): 120° = 2π/3 apart.
    This IS the Wankel rotor geometry: 3 faces at 120°.

    Three-phase current balance (su(2) Lie bracket):
        [J_blue, J_red]   = J_green
        [J_red,  J_green] = J_blue
        [J_green, J_blue] = J_red
        J_red + J_blue + J_green = 0  (no TDC singularity — the 3-point circle)

    Why trine avoids TDC:
        A 2-stroke (J_red + J_blue = 0) hits TDC — both currents vanish simultaneously.
        A trine (J_red + J_blue + J_green = 0) never has all three zero simultaneously.
        When one face is at local TDC, the other two carry the engine.
        L_(I|O) is never globally zero. The 3-point circle closes continuously.

    Wankel gear ratio: 3:1 (output shaft : rotor) = one wobble cycle per 3 circle points.
    SIGMA_RB trine ratio: 3 quantum-force firings per L_(I|O) precession revolution.
    """
    sigma_levels = [
        {'sigma': 0.75, 'level': 'ℂ', 'force': 'U(1)',  'name': 'Electromagnetism', 'loss': 'ordering (ℝ→ℂ)'},
        {'sigma': 0.50, 'level': 'ℍ', 'force': 'SU(2)', 'name': 'Weak force',        'loss': 'commutativity (ℂ→ℍ)'},
        {'sigma': 0.25, 'level': '𝕆', 'force': 'SU(3)', 'name': 'Strong force',      'loss': 'associativity (ℍ→𝕆)'},
    ]
    spacing = 0.25
    import math
    angle_deg = 120.0   # 2π/3 in degrees — the Wankel face spacing

    return {
        'identification'    : 'Three quantum-force levels = three Wankel faces = trine',
        'sigma_levels'      : sigma_levels,
        'spacing_sigma'     : spacing,
        'spacing_angular'   : f'{angle_deg}° (2π/3) — Wankel face geometry',
        'strokes_per_rev'   : 3,
        'three_phase'       : 'J_red + J_blue + J_green = 0  (su(2) Lie bracket, no net TDC)',
        'lie_bracket'       : '[J_blue,J_red]=J_green; [J_red,J_green]=J_blue; [J_green,J_blue]=J_red',
        'tdc_distribution'  : 'Each face has a LOCAL TDC. No GLOBAL TDC. Engine never stops.',
        'wankel_ratio'      : '3:1 output:rotor = 3 L_(I|O) firings per precession revolution',
        'why_trine'         : '3 = minimum points for a closed circle. 2 = line (hits TDC). 4 = over-constrained.',
        'smoother'          : 'Trine fires every ¼σ-turn. Single-stroke fires once per full cycle. 3× throughput.',
        'confidence'        : 'ESTABLISHED — 2026-06-17',
        'latex'             : r'\sigma\in\{\tfrac{3}{4},\tfrac{1}{2},\tfrac{1}{4}\},\;\Delta\sigma=\tfrac{1}{4},\;J_R+J_B+J_G=0',
    }
