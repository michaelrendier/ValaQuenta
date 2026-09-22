"""
ainulindale_engine.modules.prime_gauge_field.maths
=====================================================
THE PRIME GAUGE FIELD -- the Weyl-shaped local-scale connection Gamma's own
Schwarzian-zero result did NOT test.

ORIGIN. `.claude/scratchpad/2026-09-21_smith_apollonian_uft_probe/` tested
whether Smith's map Gamma(s)=(s-1)/(s+1) (GenerationalLineage/engine/
toolsets/scale.py) carries classical gauge curvature, and found the
Schwarzian derivative of Gamma exactly zero. That result is correct and
narrower than it looks: it tested a single, FIXED, GLOBAL Mobius map.
"Gauge" is Weyl's own word (1918, Sitzungsberichte der Koeniglich
Preussischen Akademie der Wissenschaften, 465-480) -- he tried to unify
gravity and electromagnetism by making SCALE itself a LOCAL, position-
dependent freedom (Eichinvarianz) rather than a fixed global constant, and
the curvature of THAT connection was the first "gauge curvature" ever
written down. A single global map was never going to carry it, by
construction -- that is not evidence the local question is closed.

THIS MODULE runs the local question. Two candidate connections, both
built directly from Gamma (no new machinery invented beyond it):

    log_potential_curvature(s)  --  A = grad(log|Gamma|)
        Forced to zero for ANY holomorphic scalar (Poincare lemma,
        d(d f) = 0 identically) -- this is the GENERAL reason the
        Schwarzian check found nothing, not a property special to Gamma.
        Included here so the contrast is visible in one place.

    curvature(s)  --  A = (Re(Gamma(s)), Im(Gamma(s))), read directly as
        an R^2-valued connection, NOT as a gradient of anything.
        Closed form (Cauchy-Riemann): F(s) = 2*Im(dGamma/ds) -- verified
        against a finite-difference numeric derivative before being
        trusted (see verify()). NONZERO in general.

THE PRE-REGISTERED PREDICTION (FastInverse/README.md, stated before this
module was built): the connection's flat locus is the trivial/identity
member of the SCALE family -- where the local gauge freedom does no
work. Found: F(s)=0 exactly on two loci, closed form, both checked --
the real axis (t=0, where Gamma is real-valued: the phase/rotation
freedom the connection is built from is doing nothing there -- one
honest reading of "trivial") AND the vertical line sigma=-1 (through
Gamma's own pole -- NOT anticipated by the pre-registration). Reported
as a PARTIAL match, honestly: the real-axis locus is consistent with the
prediction; the pole-line locus is a genuine new feature the prediction
did not name and should not be read as if it had.

stdlib only (cmath). Exact closed forms; finite-difference used only to
cross-check them, never as the production computation.
"""
from __future__ import annotations

import cmath
import random
from typing import Any, Dict, List, Tuple


# ── the established object this engine is built on, re-derived not copied ──
def gamma(s: complex) -> complex:
    """Smith's map. ESTABLISHED, GenerationalLineage/engine/toolsets/scale.py."""
    return (s - 1) / (s + 1)


def dgamma(s: complex) -> complex:
    """d(Gamma)/ds = 2/(s+1)^2, exact -- matches scale.py's own
    local_scale_factor = |dGamma/ds|, re-derived independently this
    session and confirmed to agree exactly."""
    return 2 / (s + 1) ** 2


# ── candidate connection 1: the gradient reading -- provably always flat ──
def log_potential_curvature(s: complex, h: float = 1e-5) -> float:
    """A = grad(log|Gamma|). Curl of a gradient is zero for ANY scalar,
    always -- this function exists to make that structural fact visible
    and checkable in code, not because a nonzero result is possible."""
    def logmag(z: complex) -> float:
        return cmath.log(abs(gamma(z))).real

    def Ax(z: complex) -> float:
        return (logmag(z + h) - logmag(z - h)) / (2 * h)

    def Ay(z: complex) -> float:
        return (logmag(z + 1j * h) - logmag(z - 1j * h)) / (2 * h)

    Ay_x = (Ay(s + h) - Ay(s - h)) / (2 * h)
    Ax_y = (Ax(s + 1j * h) - Ax(s - 1j * h)) / (2 * h)
    return Ay_x - Ax_y


# ── candidate connection 2: Gamma itself, read as a 1-form -- the real test ──
def connection(s: complex) -> Tuple[float, float]:
    """A(s) = (Re(Gamma(s)), Im(Gamma(s))) -- Gamma read as an R^2-valued
    connection, not as a C-valued holomorphic function collapsed to one
    scalar. This is the reading that can carry curvature."""
    g = gamma(s)
    return g.real, g.imag


def curvature(s: complex) -> float:
    """F(s) = dA_y/dx - dA_x/dy for A = connection(s). Closed form via
    Cauchy-Riemann (u_y = -v_x): F(s) = v_x - u_y = 2*v_x = 2*Im(dGamma/ds).
    Exact; verify() checks it against curvature_numeric()."""
    return 2 * dgamma(s).imag


def curvature_numeric(s: complex, h: float = 1e-5) -> float:
    """Finite-difference cross-check of curvature() -- the honesty check,
    never the production path."""
    def u(z: complex) -> float:
        return gamma(z).real

    def v(z: complex) -> float:
        return gamma(z).imag

    vx = (v(s + h) - v(s - h)) / (2 * h)
    uy = (u(s + 1j * h) - u(s - 1j * h)) / (2 * h)
    return vx - uy


# ── the pre-registered prediction, checked exactly ─────────────────────────
def zero_locus_predicate(s: complex, tol: float = 1e-9) -> Dict[str, Any]:
    """Closed-form zero locus of curvature(): the real axis (t=0) or the
    vertical line sigma=-1 (through Gamma's pole). Compares the predicted
    locus against the measured one at a single point."""
    on_real_axis = abs(s.imag) < tol
    on_pole_line = abs(s.real + 1) < tol
    predicted_zero = on_real_axis or on_pole_line
    actual_zero = abs(curvature(s)) < 1e-6
    return {
        "s": s, "on_real_axis": on_real_axis, "on_pole_line": on_pole_line,
        "predicted_zero": predicted_zero, "actual_zero": actual_zero,
        "match": predicted_zero == actual_zero,
    }


def prediction_check(n_samples: int = 2000, seed: int = 0) -> Dict[str, Any]:
    """Sweeps random points, not just the two loci picked to look good --
    the honest test of whether the closed-form zero locus is complete."""
    rng = random.Random(seed)
    mismatches: List[Tuple[complex, Dict[str, Any]]] = []
    for _ in range(n_samples):
        s = complex(rng.uniform(-6, 6), rng.uniform(-6, 6))
        if abs(s + 1) < 1e-6:
            continue
        r = zero_locus_predicate(s)
        if not r["match"]:
            mismatches.append((s, r))
    return {
        "n_samples": n_samples, "n_mismatches": len(mismatches),
        "all_match": len(mismatches) == 0, "mismatches": mismatches[:5],
    }


def verify() -> Dict[str, Any]:
    """Self-check, three independent claims:
    1) curvature() (closed form) matches curvature_numeric() (finite
       difference) -- the closed form is trustworthy.
    2) log_potential_curvature() is ~zero everywhere tested -- the
       gradient reading really is structurally flat, not flat by luck.
    3) The zero-locus prediction matches on 2000 random points, not just
       the two lines it was derived from."""
    rng = random.Random(1)
    max_err = 0.0
    max_log_curv = 0.0
    n = 0
    for _ in range(200):
        s = complex(rng.uniform(-5, 5), rng.uniform(-5, 5))
        if abs(s + 1) < 0.05:
            continue
        n += 1
        c = curvature(s)
        cn = curvature_numeric(s)
        max_err = max(max_err, abs(c - cn))
        max_log_curv = max(max_log_curv, abs(log_potential_curvature(s)))
    pred = prediction_check(2000)
    ok = (max_err < 1e-3) and (max_log_curv < 1e-2) and pred["all_match"]
    return {
        "ok": ok,
        "n_checked": n,
        "closed_form_vs_numeric_max_err": max_err,
        "log_potential_curvature_max": max_log_curv,
        "zero_locus_prediction_all_match": pred["all_match"],
        "zero_locus_n_mismatches": pred["n_mismatches"],
    }


def report(s: complex) -> Dict[str, Any]:
    """One point, full readout -- Gamma, its connection, both candidate
    curvatures, and the zero-locus check."""
    g = gamma(s)
    return {
        "s": s, "Gamma": g, "|Gamma|": abs(g),
        "connection": connection(s),
        "curvature": curvature(s),
        "log_potential_curvature": log_potential_curvature(s),
        "zero_locus": zero_locus_predicate(s),
    }


if __name__ == "__main__":
    for s in [0.3 + 0.7j, 2 - 1j, -0.5 + 2j, 3 + 0j, -1 + 2j, 0.5 + 0.1j]:
        r = report(s)
        print(f"s={s}: Gamma={r['Gamma']:.4f}  curvature={r['curvature']:.6f}  "
              f"log_potential_curvature={r['log_potential_curvature']:.2e}  "
              f"zero_locus_match={r['zero_locus']['match']}")
    print()
    print("verify():", verify())
