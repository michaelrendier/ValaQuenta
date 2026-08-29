"""
ainulindale_engine.modules.add_scale_sign.tools
===============================================
THE ADD:SCALE:SIGN DATATYPE -- Module Tools (EquationModule registry contract).

Surfaces the datatype's equation parts, the generalized-equation word, the
fold, the orthogonal Smith-chart read-out and the firing-order (camshaft)
defect. See maths.py for the datatype itself.

Version: 0.1
"""
from typing import Any, Dict, List

from ...engine.registry import EquationModule, Equation
from .maths import ASS, ASSWord, CAMSHAFT, compose


def _round_trip(add=3.0, scale=2.5, sign=-1) -> Dict[str, Any]:
    T = ASS(add, scale, sign)
    xs = [-2.0, 0.0, 1.0, 7.5]
    back = [(~T)(T(x)) for x in xs]
    return {"element": str(T), "x": xs, "(~T∘T)(x)": back,
            "exact": all(abs(a - b) < 1e-12 for a, b in zip(xs, back))}


def _camshaft_defect(add=4.0, scale=3.0, sign=1) -> Dict[str, Any]:
    T = ASS(add, scale, sign)
    w = T.lineage("chrono")
    return {"element": str(T), "u_total": w.u_total(),
            "Σ u_parts": w.u_sum_of_parts(), "firing_defect": w.firing_defect(),
            "order_matters": not w.additive(), "camshaft": CAMSHAFT}


def _chart(add=1.5, scale=4.0, sign=-1) -> Dict[str, Any]:
    return ASS(add, scale, sign).to_smith()


def _two_orderings(steps=((0.0, 8.0, 1), (2.0, 1.0, 1), (0.0, 0.5, -1))) -> Dict[str, Any]:
    T = compose(*[ASS(a, s, g) for a, s, g in steps])
    return {"chrono": str(T.lineage("chrono")), "zeta": str(T.lineage("zeta")),
            "same_element": str(T)}


class AddScaleSignModule(EquationModule):
    """THE ADD:SCALE:SIGN DATATYPE -- the tier-0 floor as a manipulable type."""

    @property
    def name(self):
        return "add_scale_sign"

    @property
    def display_name(self):
        return "ADD:SCALE:SIGN (the tier-0 datatype)"

    @property
    def version(self):
        return "0.1"

    @property
    def description(self):
        return (
            "A value type for elements of Aff(1,ℝ) = ADD ⋊ (SCALE × SIGN), "
            "x ↦ sign·scale·x + add. Compose with @, invert with ~, take "
            "residuals (strip one generator, keep the rest), decompose into "
            "an ASSWord. Each generator carries its equation part: ADD → a, "
            "SCALE → ln s, SIGN → g; the word is u = g·ln s + a and the fold "
            "is Γ = tanh(u/2). Read-out on the orthogonal Smith charts "
            "(Γ_SCALE, Γ_ADD, parity). Firing order is recorded — the "
            "three-phase camshaft SIGN→SCALE→ADD — and its defect "
            "(u_total − Σ u_parts) is non-zero exactly when [SCALE, ADD] = "
            "ADD bites. No sedenion here; order matters at THIS tier."
        )

    @property
    def confidence_floor(self):
        return "ESTABLISHED"

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name="round_trip",
                display="THE RETURN PATH: (~T ∘ T)(x) = x, exactly",
                latex=r"T^{-1}(a,s,g) = (-g\,a/s,\ 1/s,\ g)",
                radian_form="forward = @, backward = ~; the record reverses with it",
                confidence="ESTABLISHED", code_verified=True, params=[],
                compute=_round_trip, display_options=["text"],
            ),
            Equation(
                name="equation_parts",
                display="EACH GENERATOR'S EQUATION PART  (ADD→a, SCALE→ln s, SIGN→g)",
                latex=r"u = g\cdot\ln s + a,\qquad \Gamma = \tanh(u/2)",
                radian_form="the contribution of one ASS element to the generalized-equation word",
                confidence="ESTABLISHED", code_verified=True, params=["add", "scale", "sign"],
                compute=lambda add, scale, sign: ASS(add, scale, sign).equation_parts(),
                display_options=["text"],
            ),
            Equation(
                name="fold",
                display="THE FOLD:  Γ = tanh(u/2),  u = g·ln s + a",
                latex=r"\Gamma = \tanh\!\big(\tfrac12(g\ln s + a)\big)",
                radian_form="ground state a=0,s=1,g=+1 ⇒ u=0 ⇒ Γ=0 (the now)",
                confidence="ESTABLISHED", code_verified=True, params=["add", "scale", "sign"],
                compute=lambda add, scale, sign: {"u": ASS(add, scale, sign).u(),
                                                  "Γ": ASS(add, scale, sign).gamma()},
                display_options=["text"],
            ),
            Equation(
                name="orthogonal_charts",
                display="THE ORTHOGONAL SMITH CHARTS:  Γ_SCALE ⟂ Γ_ADD, parity g",
                latex=r"\Gamma_{\rm SCALE}=\tanh(\tfrac12\ln s),\ \ \Gamma_{\rm ADD}=\tanh(\tfrac12 a)",
                radian_form="multiplicative ring ⟂ additive ring; SIGN picks the sheet",
                confidence="ESTABLISHED", code_verified=True, params=["add", "scale", "sign"],
                compute=_chart, display_options=["text"],
            ),
            Equation(
                name="camshaft_defect",
                display="FIRING ORDER:  u_total − Σ u_parts  (non-zero ⇔ [SCALE,ADD]=ADD)",
                latex=r"[\mathrm{SCALE},\mathrm{ADD}] = \mathrm{ADD}",
                radian_form="the three-phase camshaft SIGN→SCALE→ADD; the defect is this datatype's ψ(x)−x",
                confidence="ESTABLISHED", code_verified=True, params=["add", "scale", "sign"],
                compute=_camshaft_defect, display_options=["text"],
            ),
            Equation(
                name="two_orderings",
                display="GENERATIONAL LINEAGE:  chrono ordering  vs  zeta ordering",
                latex=r"\text{chrono: as fired}\quad\text{zeta: by }|u_k|\downarrow",
                radian_form="two orderings of one recorded word; their departure is the datatype's ψ(x)−x",
                confidence="ESTABLISHED", code_verified=True, params=[],
                compute=_two_orderings, display_options=["text"],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not found in {self.name} module")
        result = eq.compute(**params) if params else eq.compute()
        return {"equation": eq, "params": params, "result": result, "module": self.name}

    def viewer_data(self, equation_name: str, params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        return {"text": self._format_text(self.run(equation_name, params))}

    def _format_text(self, result: Dict) -> str:
        eq, r = result["equation"], result["result"]
        if isinstance(r, dict):
            body = "\n".join(f"      {k:<24} {v}" for k, v in r.items()
                             if not isinstance(v, (list, dict)))
            summary = "\n" + body
        else:
            summary = r
        return (f"  {eq.display}\n"
                f"  Status: {eq.confidence}  |  Code-verified: {eq.code_verified}\n"
                f"  Notation: {eq.radian_form}\n"
                f"  Result: {summary}")

    def shell_commands(self) -> Dict[str, Any]:
        return {
            "ass":      lambda add, scale, sign: ASS(add, scale, sign),
            "apply":    lambda add, scale, sign, x: ASS(add, scale, sign)(x),
            "compose":  lambda *els: compose(*els),
            "inv":      lambda add, scale, sign: ~ASS(add, scale, sign),
            "residual": lambda add, scale, sign, without: ASS(add, scale, sign).residual(without),
            "word":     lambda add, scale, sign: str(ASS(add, scale, sign).lineage("chrono")),
            "smith":    lambda add, scale, sign: ASS(add, scale, sign).to_smith()["notation"],
            "camshaft": lambda: CAMSHAFT,
            "roundtrip": _round_trip,
            "defect":   _camshaft_defect,
        }

    def on_register(self, registry) -> None:
        pass
