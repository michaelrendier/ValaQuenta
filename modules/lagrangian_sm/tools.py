"""
ValaQuenta.modules.lagrangian_sm.tools
======================================
L_SM: THE STANDARD MODEL LAGRANGIAN ENGINE.  Module Tools (EquationModule registry contract: formulary(), run(), viewer_data(), shell_commands()).

Version: 0.1
"""
from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation
from . import maths as S
from . import compare as C


class LagrangianSMModule(EquationModule):
    """The Standard Model Lagrangian engine."""

    @property
    def name(self): return "lagrangian_sm"

    @property
    def display_name(self): return "L_SM: the Standard Model Lagrangian"

    @property
    def version(self): return "0.1"

    @property
    def description(self):
        return ("The Standard Model of particle physics as an engine: field content and gauge quantum numbers, anomaly cancellation, SU(2) and SU(3) "
                "structure constants, the symbolic derivation of the electroweak boson masses and the Higgs potential expansion, the count of "
                "independent parameters (19, 26, 28), tree-level relations against the PDG tables, CKM and PMNS mixing, Z couplings, one-loop "
                "running and the failure of gauge coupling unification, and a measured comparison of L_SM with the VAPMIP L_NN and with L_(I|O).")

    @property
    def confidence_floor(self): return "ESTABLISHED"

    @property
    def process_description(self):
        return "Builds the Standard Model Lagrangian from its gauge group and field content and checks it against measured numbers."

    def formulary(self) -> List[Equation]:
        def eq(name, display, formula, radian, conf, params, fn, process):
            return Equation(name=name, display=display, latex=formula, radian_form=radian, confidence=conf, code_verified=True,
                            params=params, compute=fn, display_options=["text"], process=process)
        return [
            eq("verify", "VERIFY: closure checks", "anomalies = 0, [T^a,T^b] = i f T, m_W² = g²v²/4", "all checks as numbers", "ESTABLISHED", [], lambda: S.verify(),
               "Anomalies, group closure, symbolic boson masses, parameter counts, CKM unitarity."),
            eq("fields", "FIELDS: content and degrees of freedom", "Q_L u_R d_R L_L e_R H", "(SU(3), SU(2), Y)", "ESTABLISHED", [],
               lambda: {"content": S.field_content(), "dof": S.degrees_of_freedom()}, "Quantum numbers and counts."),
            eq("anomalies", "ANOMALIES: why this content is consistent", "Σ Y³ = Σ T(R) Y = 0", "exact rational sums", "ESTABLISHED", [], lambda: S.anomaly_check(),
               "Gauge anomaly sums over one generation."),
            eq("hypercharges", "HYPERCHARGES: derived, not measured", "3Y_Q + Y_L = 0, 6Y_Q - 3Y_u - 3Y_d + 2Y_L - Y_e = 0", "given the multiplets and Y_H = 1/2", "ESTABLISHED", ["n_colours"],
               lambda n_colours=3: S.hypercharges_from_anomalies(n_colours), "Anomaly cancellation fixes every hypercharge."),
            eq("su5", "SU(5) EMBEDDING: where the anomaly cancellation comes from", "15 = 5-bar + 10, Y traceless", "A(10) + A(5-bar) = 0", "ESTABLISHED", [],
               lambda: S.su5_embedding(), "The one generation fills 5-bar + 10 exactly."),
            eq("groups", "GROUPS: SU(2), SU(3) structure constants", "[T^a,T^b] = i f^{abc} T^c", "Jacobi and Casimir residuals", "ESTABLISHED", [], lambda: S.group_checks(),
               "Closure, Jacobi and Casimir checks."),
            eq("parameters", "PARAMETERS: how many numbers L_SM has", "19 / 26 / 28", "counted from the Yukawa structure", "ESTABLISHED", ["neutrinos"],
               lambda neutrinos="massless": S.parameter_count(neutrinos), "Independent parameters of the most general renormalisable Lagrangian."),
            eq("ew_symbolic", "ELECTROWEAK MASSES, derived", "|D H|² → m_W², m_Z², 0", "sympy", "ESTABLISHED", [],
               lambda: {k: str(v) for k, v in S.ew_mass_matrix_symbolic().items() if k in ("m_W2", "m_Z2", "m_photon2", "quadratic_form")}, "Symbolic derivation from the covariant derivative."),
            eq("higgs_symbolic", "HIGGS POTENTIAL, expanded", "V(h) = λ v² h² + λ v h³ + λ/4 h⁴", "sympy", "ESTABLISHED", [],
               lambda: {"m_h2": str(S.higgs_potential_expansion()["m_h2"]), "coefficients": {k: str(v) for k, v in S.higgs_potential_expansion()["coefficients"].items()}},
               "Masses and self-couplings of the Higgs."),
            eq("higgs", "HIGGS SECTOR: numbers", "λ = m_h²/2v², μ² = λ v²", "from PDG m_h and G_F", "ESTABLISHED", ["m_h", "v"], lambda m_h=None, v=None: S.higgs_sector(m_h, v),
               "λ, μ², depth, couplings."),
            eq("ew_tree", "ELECTROWEAK TREE LEVEL", "m_W = g v/2, m_Z = √(g²+g'²) v/2", "against PDG", "ESTABLISHED", [], lambda: S.ew_tree(), "Tree relations and their loop-sized differences."),
            eq("yukawas", "YUKAWA COUPLINGS", "y = √2 m/v", "from PDG masses", "ESTABLISHED", [], lambda: S.yukawas(), "Charged-fermion Yukawas."),
            eq("ckm", "CKM and PMNS", "V†V = 1, J", "standard parametrisation", "ESTABLISHED", [],
               lambda: {"CKM_J": S.jarlskog(S.ckm_matrix()), "CKM_unitarity": S.unitarity_residual(S.ckm_matrix()), "PMNS_J": S.jarlskog(S.pmns_matrix())}, "Mixing and CP violation."),
            eq("zcouplings", "Z COUPLINGS", "g_V = T3 - 2Q sin²θ_W, g_A = T3", "per fermion", "ESTABLISHED", [], lambda: S.z_couplings(), "Neutral-current couplings."),
            eq("vertices", "VERTEX INVENTORY", "count of interaction types", "from the content", "ESTABLISHED", [], lambda: S.vertex_inventory(), "How many interaction types the broken Lagrangian has."),
            eq("running", "RUNNING and the failure to unify", "1/α_i(μ) = 1/α_i(M_Z) - b_i ln(μ/M_Z)/2π", "one loop", "ESTABLISHED", [], lambda: S.gauge_crossings(),
               "Scales where pairs of couplings meet; the spread is the result."),
            eq("compare", "COMPARE: L_SM, L_NN, L_(I|O), L_dynamic", "measured exponents and identities", "scaling by doubling the fields", "ESTABLISHED", [],
               lambda: C.comparison_table(), "The Lagrangians side by side, measured on the code."),
            eq("exponents", "COMPARE: degree of each term", "term ~ amplitude^n", "SM vs coded L_NN", "ESTABLISHED", [], lambda: C.measured_exponents(), "Which interaction each term is."),
            eq("loops", "WHAT EACH PARTICLE DOES TO THE HAT", "V_i = n_i m_i⁴/64π² [ln(m_i²/μ²) - c_i]", "Coleman-Weinberg, per particle", "ESTABLISHED", [],
               lambda: {k: float(v[0]) for k, v in S.coleman_weinberg(__import__("numpy").array([S.fermi_vev()])).items()}, "Each particle's one-loop term at h = v, in GeV⁴."),
            eq("hat_temperature", "THE HAT AGAINST TEMPERATURE", "V(h,T) = D(T²-T0²)h² - E T h³ + λ_T h⁴/4", "high-T expansion, valid above about 100 GeV", "ESTABLISHED", ["T"],
               lambda T=140.0: S.finite_temperature_hat(T), "Brim radius and depth at temperature T."),
            eq("hat", "THE HAT, for the path-of-action tools", "V(h) as a model dict", "feeds witches_hat", "ESTABLISHED", [], lambda: {k: v for k, v in S.hat_model().items() if k != "V"},
               "The Standard-Model Higgs hat with this engine's parameters."),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eqs = {e.name: e for e in self.formulary()}
        if equation_name not in eqs:
            raise KeyError(f"lagrangian_sm has no equation '{equation_name}'")
        eq = eqs[equation_name]
        result = eq.compute(**{k: v for k, v in params.items() if k in eq.params}) if params else eq.compute()
        return {"result": result, "equation": eq, "params": params}

    def viewer_data(self, equation_name: str, params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        out = self.run(equation_name, params)
        return {"mode": display_mode, "equation": equation_name, "text": repr(out["result"])[:4000]}

    def shell_commands(self) -> Dict[str, Any]:
        return {"sm_verify": S.verify, "sm_fields": S.field_content, "sm_anomalies": S.anomaly_check, "sm_groups": S.group_checks, "sm_parameters": S.parameter_count,
                "sm_higgs": S.higgs_sector, "sm_ew_tree": S.ew_tree, "sm_yukawas": S.yukawas, "sm_ckm": S.ckm_matrix, "sm_running": S.gauge_crossings,
                "sm_loops": S.coleman_weinberg, "sm_hat_temperature": S.finite_temperature_hat, "sm_compare": C.comparison_table, "sm_exponents": C.measured_exponents, "sm_hat": S.hat_model}
