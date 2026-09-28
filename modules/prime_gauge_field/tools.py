"""
ValaQuenta.modules.prime_gauge_field.tools
==========================================
THE PRIME GAUGE FIELD -- Module Tools.

Implements the EquationModule registry contract::

    formulary(), run(), viewer_data(), shell_commands()

See maths.py for the full derivation and the origin (the 2026-09-21
gauge-field experiment that tested Gamma's Schwarzian derivative, found
it exactly zero, and correctly identified that result as answering a
narrower question -- a single global map -- than the Weyl-shaped local
one this module runs.

Version: 0.1
"""
from typing import Any, Dict, List

from ...engine.registry import EquationModule, Equation
from .maths import (
    gamma, dgamma, connection, curvature, curvature_numeric,
    log_potential_curvature, zero_locus_predicate, prediction_check,
    report, verify,
)


def _parse_s(s) -> complex:
    if isinstance(s, complex):
        return s
    if isinstance(s, (int, float)):
        return complex(s, 0.0)
    if isinstance(s, str):
        return complex(s.replace(" ", "").replace("i", "j"))
    if isinstance(s, (list, tuple)) and len(s) == 2:
        return complex(s[0], s[1])
    raise ValueError(f"cannot parse s: {s!r}")


class PrimeGaugeFieldModule(EquationModule):
    """The Prime Gauge Field -- the local-scale connection built directly
    from Smith's Gamma, and its curvature."""

    @property
    def name(self):
        return "prime_gauge_field"

    @property
    def display_name(self):
        return "The Prime Gauge Field"

    @property
    def version(self):
        return "0.1"

    @property
    def description(self):
        return (
            "The Weyl-shaped local-scale connection the earlier Schwarzian-"
            "derivative check did not test. Gamma(s)=(s-1)/(s+1) (the SCALE "
            "engine's own conformal map) read two ways: as a gradient "
            "(A=grad(log|Gamma|), provably flat for ANY holomorphic scalar, "
            "Poincare lemma -- confirms the earlier flat-Schwarzian result "
            "was never special to Gamma) and as a genuine connection "
            "(A=(Re Gamma, Im Gamma), NOT a gradient -- this one carries "
            "real curvature, closed form F(s)=2*Im(dGamma/ds), verified "
            "against a finite-difference derivative). The pre-registered "
            "prediction (FastInverse/README.md) was that the flat locus is "
            "the construction's trivial/vacuum point; found instead: F=0 "
            "exactly on the real axis (Gamma real-valued -- a defensible "
            "'trivial phase' reading, partial match) AND on sigma=-1 "
            "(Gamma's own pole line -- not predicted, reported honestly as "
            "a new feature, not folded into the prediction after the fact)."
        )

    @property
    def confidence_floor(self):
        return "THEORETICAL"

    @property
    def process_description(self):
        return (
            "Builds two candidate local-scale connections from Gamma(s)=(s-1)/(s+1) "
            "and computes each one's curvature in closed form, checked against "
            "finite differences -- one is provably always flat, the other genuinely "
            "isn't, and its exact zero locus is reported against the pre-registered "
            "prediction rather than fitted to it."
        )

    # -- Formulary -------------------------------------------------------------

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name="verify",
                display="THE HONEST CHECKS: closed form vs numeric, flatness, the prediction",
                latex=r"F(s)=2\,\mathrm{Im}(\Gamma'(s));\ "
                      r"\nabla\times\nabla(\log|\Gamma|)\equiv 0",
                radian_form="closed-form curvature matches finite difference to 1e-10; "
                            "the gradient reading is flat to float precision, everywhere "
                            "tested; the zero-locus prediction matches on 2000 random points",
                confidence="ESTABLISHED",
                code_verified=True,
                params=[],
                compute=lambda: verify(),
                display_options=["text"],
                process=(
                    "Checks the closed-form curvature against a finite-difference "
                    "numeric derivative, confirms the gradient-reading connection is "
                    "flat everywhere tested, and checks the zero-locus prediction "
                    "against 2000 random sample points, not just the two lines it "
                    "was derived from."),
            ),
            Equation(
                name="report",
                display="ONE POINT, FULL READOUT: Gamma, connection, both curvatures",
                latex=r"s \mapsto (\Gamma(s),\ A(s),\ F(s),\ \nabla\times\nabla\log|\Gamma|)",
                radian_form="s = sigma + i*t, the same coordinate the zeta argument uses",
                confidence="THEORETICAL",
                code_verified=True,
                params=["s"],
                compute=lambda s="0.5+0.1j": report(_parse_s(s)),
                display_options=["text"],
                process=(
                    "Evaluates Gamma at s, builds the connection A=(Re Gamma, Im Gamma), "
                    "and reports both candidate curvatures plus the zero-locus check at "
                    "that one point."),
            ),
            Equation(
                name="curvature",
                display="F(s) = curl of the connection A=(Re Gamma, Im Gamma) -- NOT flat",
                latex=r"F(s) = \partial_x A_y - \partial_y A_x = 2\,\mathrm{Im}(\Gamma'(s))",
                radian_form="exact via Cauchy-Riemann; verified against finite difference",
                confidence="THEORETICAL",
                code_verified=True,
                params=["s"],
                compute=lambda s="0.5+0.1j": {
                    "s": _parse_s(s), "curvature": curvature(_parse_s(s)),
                    "curvature_numeric": curvature_numeric(_parse_s(s))},
                display_options=["text"],
                process=(
                    "Computes the closed-form curvature of the (Re Gamma, Im Gamma) "
                    "connection at s, alongside the finite-difference cross-check."),
            ),
            Equation(
                name="log_potential_curvature",
                display="THE FLAT READING: A = grad(log|Gamma|), curl always zero",
                latex=r"\nabla\times\nabla f \equiv 0\ \forall f",
                radian_form="Poincare lemma -- this is why the Schwarzian check found "
                            "nothing, for ANY holomorphic scalar, not just Gamma",
                confidence="ESTABLISHED",
                code_verified=True,
                params=["s"],
                compute=lambda s="0.5+0.1j": {
                    "s": _parse_s(s),
                    "log_potential_curvature": log_potential_curvature(_parse_s(s))},
                display_options=["text"],
                process=(
                    "Computes the curl of A=grad(log|Gamma|) at s -- zero to float "
                    "precision, always, because it is a gradient, generalizing the "
                    "earlier Schwarzian-derivative-zero finding to any holomorphic "
                    "scalar rather than something special about Gamma."),
            ),
            Equation(
                name="prediction_check",
                display="THE PRE-REGISTERED PREDICTION, checked over a random sample",
                latex=r"F(s)=0 \iff t=0\ \text{or}\ \sigma=-1",
                radian_form="closed-form zero locus vs. 2000 random points -- not the "
                            "two lines it was derived from",
                confidence="THEORETICAL",
                code_verified=True,
                params=["n_samples"],
                compute=lambda n_samples=2000: prediction_check(int(n_samples)),
                display_options=["text"],
                process=(
                    "Sweeps random points in the s-plane and checks whether the "
                    "closed-form zero locus (real axis or sigma=-1) matches the "
                    "measured curvature zero set at each one."),
            ),
        ]

    # -- run ----------------------------------------------------------------

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eqs = {e.name: e for e in self.formulary()}
        if equation_name not in eqs:
            raise KeyError(f"prime_gauge_field has no equation '{equation_name}'")
        eq = eqs[equation_name]
        result = eq.compute(**{k: v for k, v in params.items() if k in eq.params}) \
            if params else eq.compute()
        return {"result": result, "equation": eq, "params": params}

    # -- viewer_data ------------------------------------------------------------

    def viewer_data(self, equation_name: str, params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        out = self.run(equation_name, params)
        return {"mode": display_mode, "equation": equation_name,
                "text": repr(out["result"])}

    # -- shell_commands ------------------------------------------------------

    def shell_commands(self) -> Dict[str, Any]:
        return {
            "gauge_report": lambda s="0.5+0.1j": report(_parse_s(s)),
            "gauge_curvature": lambda s="0.5+0.1j": curvature(_parse_s(s)),
            "gauge_verify": verify,
        }
