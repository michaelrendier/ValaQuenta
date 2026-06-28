"""
ainulindale_engine.modules.inversion.tools
============================================
Inside-Out Inversion Engine — Module Tools

Implements the EquationModule registry contract.
Provides: formulary, run(), viewer_data(), shell_commands()

Display modes supported:
    complex_plane   — (r, theta) polar plot of inversion trajectory
    3d_cartesian    — 3D flow from r=1 to phi attractor
    text            — structured text output (always available)

Version: 0.111
"""

import math
from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from ...engine import constants as C
from .maths import InversionMap, RecursionAttractor, GradientFlow, get_observer


class InversionModule(EquationModule):
    """
    Inside-Out Inversion Engine module.

    Contributes the (I|O) map and all derived quantities to the
    Ainulindale Derivation Engine.
    """

    # ── Identity ─────────────────────────────────────────────────────────────

    @property
    def name(self):
        return "inversion"

    @property
    def display_name(self):
        return "Inside-Out Inversion Engine  (I|O)"

    @property
    def version(self):
        return "0.111"

    @property
    def description(self):
        return (
            "The (I|O) inversion map J_N: (r, theta) -> (1/r, theta + pi/2). "
            "The 2-stroke engine of the SMNNIP framework: compression stroke "
            "(r -> 1/r) and expansion stroke (1/r -> r). Unifies Schwarzschild, "
            "Hawking, Dirac sea, and Ptolemy inversion as the same map at "
            "different recursion depths. Fixed point r=1 is the horizon. "
            "Recursion attractor is phi. The sedenion is where the expansion "
            "stroke fails: top dead center, one-way ratchet."
        )

    @property
    def confidence_floor(self):
        return "ESTABLISHED"

    # ── Formulary ─────────────────────────────────────────────────────────────

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='inversion_map',
                display='(I|O) Inversion Map J_N',
                latex=r'J_N: (r, \theta) \mapsto (1/r,\; \theta + \pi/2)',
                radian_form='J_N(r, theta) = (1/r, theta + pi/2)  [theta in radians]',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['r', 'theta_rad'],
                compute=lambda r, theta_rad: InversionMap().apply(r, theta_rad),
                display_options=['complex_plane', '3d_cartesian', 'text'],
            ),
            Equation(
                name='involution_check',
                display='(I|O) Involution: J_N applied twice',
                latex=r'J_N \circ J_N:\; r \mapsto r \quad (\theta \mapsto \theta + \pi)',
                radian_form='J_N(J_N(r, theta)) -> (r, theta + pi)',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['r', 'theta_rad'],
                compute=lambda r, theta_rad: InversionMap().is_involution(r, theta_rad),
                display_options=['text'],
            ),
            Equation(
                name='gradient_flow',
                display='Gradient flow: r=1 to phi attractor',
                latex=r'r_{n+1} = r_n - \hbar_{NN} \cdot \nabla V(r_n)',
                radian_form='r_{n+1} = r_n - hbar_NN * (r_n - 1/r_n)',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['r0', 'max_steps'],
                compute=lambda r0, max_steps=1000: GradientFlow().flow(r0, max_steps),
                display_options=['complex_plane', '3d_cartesian', 'text'],
            ),
            Equation(
                name='phi_crossing_step',
                display='phi-crossing step = H/4 = (pi/2) hbar_NN',
                latex=r'\Delta r|_\phi = H_{NN}/4 = (\pi/2)\,\hbar_{NN}',
                radian_form='step = (pi/2) * hbar_NN  [radian-primary form is exact]',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: RecursionAttractor().phi_crossing_step(),
                display_options=['text'],
            ),
            Equation(
                name='d_star_gap',
                display='d* x ln(10) vs OMEGA_ZS  [OPEN — gap = 0.00070]',
                latex=r'd^* \times \ln(10) \approx \Omega_{\zeta\Sigma} \quad \text{gap: } 0.00070',
                radian_form='d* x ln(10) = 0.56644  vs  OMEGA_ZS = 0.56714',
                confidence='OPEN',
                code_verified=True,
                params=[],
                compute=lambda: RecursionAttractor().d_star_gap(),
                display_options=['text'],
            ),
            Equation(
                name='four_horizons',
                display='(I|O) unifies four physical horizons',
                latex=r'J_N \text{ at depth } d: \text{Schwarzschild, Hawking, Dirac, Ptolemy}',
                radian_form='Four instances of J_N at different recursion depths',
                confidence='THEORETICAL',
                code_verified=False,
                params=[],
                compute=lambda: InversionMap().four_horizons(),
                display_options=['text'],
            ),
        ]

    # ── Run ──────────────────────────────────────────────────────────────────

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a named equation."""
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not found in {self.name} module")
        result = eq.compute(**params) if params else eq.compute()
        return {
            'equation': eq,
            'params':   params,
            'result':   result,
            'module':   self.name,
        }

    # ── Viewer data ───────────────────────────────────────────────────────────

    def viewer_data(self, equation_name: str,
                    params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        """
        Return data formatted for a specific viewer mode.
        Currently prepares data structures; renderer lives in the viewer layer.
        """
        result = self.run(equation_name, params)

        if display_mode == 'text':
            return {'text': self._format_text(equation_name, result)}

        elif display_mode == 'complex_plane':
            return self._complex_plane_data(equation_name, params, result)

        elif display_mode == '3d_cartesian':
            return self._cartesian_3d_data(equation_name, params, result)

        else:
            return {'text': self._format_text(equation_name, result),
                    'note': f'Display mode {display_mode} not yet implemented for this equation'}

    def _format_text(self, equation_name: str, result: Dict) -> str:
        eq = result['equation']
        lines = [
            f"  {eq.display}",
            f"  Status: {eq.confidence}  |  Code-verified: {eq.code_verified}",
            f"  Radian form: {eq.radian_form}",
            f"  Result: {result['result']}",
        ]
        return "\n".join(lines)

    def _complex_plane_data(self, equation_name, params, result) -> Dict:
        """Prepare complex plane (r, theta polar) plot data."""
        if equation_name == 'inversion_map':
            r = params.get('r', 2.0)
            theta = params.get('theta_rad', 0.0)
            traj = InversionMap().apply_n(r, theta, 8)
            # Convert polar to Cartesian for plotting
            points = [(ri * math.cos(ti), ri * math.sin(ti)) for ri, ti in traj]
            return {
                'type':        'polar_trajectory',
                'trajectory':  traj,
                'cartesian':   points,
                'fixed_point': (1.0, 0.0),
                'phi':         (C.PHI, 0.0),
                'domain':      (C.A_PI, C.OMEGA_ZS),
            }
        elif equation_name == 'gradient_flow':
            flow = result['result']
            traj = [(r, 0.0) for r in flow.get('trajectory', [])]
            points = [(r, 0.0) for r in flow.get('trajectory', [])]
            return {
                'type':        'flow_trajectory',
                'trajectory':  traj,
                'cartesian':   points,
                'converged':   flow.get('converged'),
                'target_phi':  C.PHI,
            }
        return {'type': 'unsupported', 'equation': equation_name}

    def _cartesian_3d_data(self, equation_name, params, result) -> Dict:
        """Prepare 3D Cartesian data for VisPy renderer."""
        if equation_name == 'gradient_flow':
            flow = result['result']
            traj = flow.get('trajectory', [])
            # Map to 3D: x=step, y=r, z=|r - phi| (error from attractor)
            points_3d = [
                (float(i), r, abs(r - C.PHI))
                for i, r in enumerate(traj)
            ]
            return {
                'type':     '3d_flow',
                'points':   points_3d,
                'target':   (len(traj), C.PHI, 0.0),
                'axes':     ('step', 'r', '|r - phi|'),
            }
        return {'type': 'unsupported', 'equation': equation_name}

    # ── Shell commands ────────────────────────────────────────────────────────

    def shell_commands(self) -> Dict[str, Any]:
        """Commands available in the QTermWidget shell."""
        return {
            'io':        lambda r=2.0, t=0.0: InversionMap().apply(r, t),
            'flow':      lambda r0=1.0: GradientFlow().flow(r0),
            'phi_step':  lambda: RecursionAttractor().phi_crossing_step(),
            'gap':       lambda: RecursionAttractor().d_star_gap(),
            'observer':  lambda: get_observer(),
            'horizons':  lambda: InversionMap().four_horizons(),
        }

    # ── Registration hook ────────────────────────────────────────────────────

    def on_register(self, registry) -> None:
        observer = get_observer()
        assert observer.is_in_domain(C.D_STAR), \
            f"d* = {C.D_STAR} outside BK domain [{C.A_PI}, {C.OMEGA_ZS}]"
