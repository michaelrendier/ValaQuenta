"""
ValaQuenta.modules.witches_hat.tools
====================================
THE WITCH'S HAT ENGINE.  Module Tools (EquationModule registry contract: formulary(), run(), viewer_data(), shell_commands()).

Version: 0.1
"""
from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation
from . import maths as M


class WitchesHatModule(EquationModule):
    """The Witch's Hat engine."""

    @property
    def name(self): return "witches_hat"

    @property
    def display_name(self): return "The Witch's Hat Engine (virtual brim, hat potential, paths of action)"

    @property
    def version(self): return "0.1"

    @property
    def description(self):
        return ("Static snapshots of the Witch's Hat: the hat potential (the Standard-Model Higgs quartic, a family of exponents, the "
                "fermion exchange hole, the boson bunching well, the difference of Gaussians), the brim, and the classical paths of "
                "action from the brim, with size, depth, energy and aim adjustable; the focal resolution, the defocus cone, the energy "
                "regimes; the zeta pair correlation against the 1-D fermion kernel. Returns plain data: rendering is done elsewhere.")

    @property
    def confidence_floor(self): return "THEORETICAL"

    @property
    def process_description(self):
        return "Builds a snapshot of one hat and its path bundle and measures the focus."

    def formulary(self) -> List[Equation]:
        def eq(name, display, latex, radian, conf, params, fn, process):
            return Equation(name=name, display=display, latex=latex, radian_form=radian, confidence=conf, code_verified=True,
                            params=params, compute=fn, display_options=["text"], process=process)
        return [
            eq("verify", "VERIFY: closed form and Standard-Model numbers", r"r_{min}=\sqrt{\sin\psi}\,((n-2)/n)^{1/4}", "small-angle closed form at E = 0", "ESTABLISHED", [],
               lambda: M.verify(), "Checks the focus closed form and returns the Higgs-hat numbers."),
            eq("snapshot", "SNAPSHOT: hat, brim, path bundle", r"V(r),\ W=\int\sqrt{2(E-V)}\,ds", "size, depth, shape, energy and aim are parameters", "THEORETICAL",
               ["shape", "n", "size", "depth", "E", "aim", "spread"],
               lambda shape="quartic", n=4.0, size=1.0, depth=1.0, E=0.0, aim=0.0, spread=0.3: M.snapshot(shape, n, size, depth, E, aim, spread),
               "A static snapshot as plain data."),
            eq("focus", "FOCUS: resolution of the bundle", r"\mathrm{median}\,r_{min}", "smaller is tighter", "ESTABLISHED", ["shape", "n", "E"],
               lambda shape="quartic", n=4.0, E=0.0: M.focus_resolution(shape, n, E), "Median closest approach, units of the brim radius."),
            eq("defocus", "DEFOCUS: the ring caustic against the aim offset", r"r_{ring}(\delta)", "zero only at aim 0 with E = 0", "ESTABLISHED", ["shape", "n", "E"],
               lambda shape="quartic", n=4.0, E=0.0: M.defocus_curve(shape, n, E), "The hollow-cone radius against aim."),
            eq("regimes", "ENERGY REGIMES: reflected, point, through", r"E\ \lessgtr\ V(0)", "the point focus is the separatrix", "ESTABLISHED", ["shape", "n"],
               lambda shape="quartic", n=4.0: M.energy_regimes(shape, n), "Radial rays at energies below, at and above the hilltop."),
            eq("shapes", "SHAPES: resolution of every hat", r"V=-g_F(r)", "the exchange hole as a hat", "THEORETICAL", [], lambda: M.shape_table(),
               "Focus resolution and the matching quartic exponent for each shape."),
            eq("compare", "COMPARE: Standard Model and VAPMIP Lagrangians", r"V_{SM}\ \text{vs}\ V_{vap}=-((1/\varphi)L_{bias}+L_{coup})", "kept separate, compared after", "THEORETICAL", [],
               lambda: M.compare(), "Both hats in their own units and in the normalised chart; the recorded sign and vev inconsistencies of the coded VAPMIP bias term."),
            eq("vap_snapshot", "VAPMIP SNAPSHOT: the monad Lagrangian's hat and paths", r"V_{vap}(\beta)", "g psi tilts the hat toward the information", "THEORETICAL", ["g", "psi_x", "psi_y"],
               lambda g=0.2, psi_x=1.0, psi_y=0.0: M.snapshot_plane(M.lagrangian_vap(g=g, psi=(psi_x, psi_y))), "Plain-data snapshot on the beta-plane."),
            eq("l_io", "L_(I|O) as the action of the actual path", r"W=\int p\,dq", "stationary: almost independent of the launch angle", "THEORETICAL", ["model"],
               lambda model="sm": M.l_io_action(M.lagrangian_sm() if model == "sm" else M.lagrangian_vap()), "Action to the closest approach against the aim offset."),
            eq("sm_hat", "STANDARD MODEL HAT", r"V=-\mu^2h^2/2+\lambda h^4/4", "m_h = 125.25, v = 246.22 GeV", "ESTABLISHED", [], lambda: M.sm_hat(),
               "The Higgs-sector numbers."),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eqs = {e.name: e for e in self.formulary()}
        if equation_name not in eqs:
            raise KeyError(f"witches_hat has no equation '{equation_name}'")
        eq = eqs[equation_name]
        result = eq.compute(**{k: v for k, v in params.items() if k in eq.params}) if params else eq.compute()
        return {"result": result, "equation": eq, "params": params}

    def viewer_data(self, equation_name: str, params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        out = self.run(equation_name, params)
        return {"mode": display_mode, "equation": equation_name, "text": repr(out["result"])[:4000]}

    def shell_commands(self) -> Dict[str, Any]:
        return {"hat_snapshot": M.snapshot, "hat_focus": M.focus_resolution, "hat_defocus": M.defocus_curve, "hat_regimes": M.energy_regimes,
                "hat_shapes": M.shape_table, "hat_compare": M.compare, "hat_l_io": M.l_io_action, "hat_snapshot_plane": M.snapshot_plane, "hat_sm": M.sm_hat, "hat_verify": M.verify}
