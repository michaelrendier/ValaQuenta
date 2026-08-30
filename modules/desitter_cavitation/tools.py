"""
ValaQuenta.modules.desitter_cavitation.tools
============================================
EquationModule wrapper for the De Sitter Cavitation engine.

Version: 0.100 — 2026-08-30
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation
from .maths import (
    kretschmann_core, kretschmann_core_closed, kretschmann_schwarzschild,
    kretschmann_ratio_planck, planck_mass_crossover,
    r_schwarzschild, L_desitter, tau_interior, H_desitter,
    T_hawking, T_desitter, t_evaporation, t_bounce_exterior, echo_delay,
    stiff_matter_ceiling, core_energy_density, reheating_reaches_qgp,
    energy_partition, no_singularity_check, mass_class_table,
    cosmic_cavitation_budget, full_desitter_cavitation,
    M_SUN,
)


class DeSitterCavitationModule(EquationModule):
    """
    No Singularity — the Abrikosov-Vortex Core and De Sitter Cavitation
    over a Black Hole's Life.  Calculation, not simulation.
    """

    @property
    def name(self) -> str:
        return 'desitter_cavitation'

    @property
    def display_name(self) -> str:
        return ('De Sitter Cavitation Engine — No Singularity: the '
                'Abrikosov-Vortex Core')

    @property
    def version(self) -> str:
        return '0.100'

    @property
    def description(self) -> str:
        return (
            'The black-hole interior is a finite, sub-Planckian de Sitter '
            'core — the Abrikosov vortex core made gravitational: the '
            'condensate goes to zero (a Riemann zero, winding 1) while '
            'density, pressure and curvature stay finite. HOLCUS: the '
            'maximum curvature is the de Sitter Kretschmann scalar at '
            'L_dS = r_s, K_core(M) = (3/2) c^8 / (G^4 M^4) — mass-dependent, '
            'M^-4, sub-Planckian for every M > (3/2)^(1/4) m_Pl, with a '
            'ringdown-echo delay ~ r_s/c as its observational shadow. The '
            'core releases stiff space (Lambda-signed) and stiff matter '
            '(radiative) over the hole\'s life and unwraps at evaporation — '
            'the De Sitter Cavitation. Falsifier: a divergent core '
            'curvature, or one pinned to K_Planck independent of M.'
        )

    @property
    def confidence_floor(self) -> str:
        return 'THEORETICAL'

    # ── formulary ───────────────────────────────────────────────────────────

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                'full_desitter_cavitation',
                'The whole engine: Holcus + no-singularity check + mass-class '
                'table + partition + cosmic budget',
                r'K_{\rm core}(M)=\dfrac{24}{r_s^4}=\dfrac{3}{2}\dfrac{c^8}{G^4M^4}',
                'one radian of de Sitter expansion phase: tau = 1/H_dS = r_s/c',
                'THEORETICAL', True, [],
                lambda: full_desitter_cavitation(), ['text'],
            ),
            Equation(
                'kretschmann_core',
                'HOLCUS — core curvature is the de Sitter Kretschmann at L_dS = r_s',
                r'R_{abcd}R^{abcd}\big|_{\rm core}=24/L_{\rm dS}^4,\;L_{\rm dS}=r_s',
                'K = 24 / (one radian of curvature radius)^4; radius = r_s',
                'ESTABLISHED', True, ['M_kg'],
                lambda M_kg: {
                    'M_kg': M_kg,
                    'K_core_m^-4': kretschmann_core(M_kg),
                    'K_core_closed_form': kretschmann_core_closed(M_kg),
                    'K_core_over_K_Planck': kretschmann_ratio_planck(M_kg),
                    'r_s_m': r_schwarzschild(M_kg),
                    'L_desitter_m': L_desitter(M_kg),
                    'closed_form_matches': abs(
                        kretschmann_core(M_kg) - kretschmann_core_closed(M_kg)
                    ) <= 1e-6 * kretschmann_core(M_kg),
                }, ['text'],
            ),
            Equation(
                'no_singularity_check',
                'Consistency scorecard: finite, M^-4, sub-Planckian; '
                'Schwarzschild K->inf is the denied artifact',
                r'K_{\rm core}<\infty,\;K\propto M^{-4},\;K_{\rm core}<K_{\rm Pl}\;(M>m_{\rm Pl})',
                'finite curvature at every scale; no radian of the metric runs to infinity',
                'THEORETICAL', True, [],
                lambda: no_singularity_check(), ['text'],
            ),
            Equation(
                'mass_class_table',
                'Engineering table: kugelblitz / stellar / IMBH / SMBH — '
                'r_s, tau_interior, T_H, t_evap, bounce, K_core, echo',
                r'\{r_s,\,\tau_{\rm int}=r_s/c,\,T_H,\,t_{\rm evap},\,K_{\rm core}\}(M)',
                'per class: tau_interior in radians of expansion phase',
                'ESTABLISHED', True, [],
                lambda: mass_class_table(), ['text'],
            ),
            Equation(
                'interior_timescales',
                'Interior BANG time, de Sitter / Hawking temperatures, '
                'exterior bounce, ringdown echo',
                r'\tau=r_s/c,\;T_{\rm dS}=2T_H,\;\Delta t_{\rm echo}\sim(2r_s/c)\ln(r_s/\ell_{\rm Pl})',
                'tau = 1 / H_dS  (one radian of expansion)',
                'THEORETICAL', True, ['M_kg'],
                lambda M_kg: {
                    'M_kg': M_kg,
                    'tau_interior_s': tau_interior(M_kg),
                    'H_desitter_s^-1': H_desitter(M_kg),
                    'T_hawking_K': T_hawking(M_kg),
                    'T_desitter_K': T_desitter(M_kg),
                    'T_desitter_over_T_hawking': T_desitter(M_kg) / T_hawking(M_kg),
                    't_evaporation_s': t_evaporation(M_kg),
                    't_bounce_exterior_s': t_bounce_exterior(M_kg),
                    'echo_delay_s': echo_delay(M_kg),
                }, ['text'],
            ),
            Equation(
                'energy_partition',
                'SECONDARY — stiff-space vs stiff-matter release; default '
                'split 1 - d* : d*',
                r'E_{\rm space}/E_{\rm tot}=1-d^\*,\;E_{\rm matter}/E_{\rm tot}=d^\*',
                'partition of the rest-energy phase; d* is the boundary radian',
                'CONJECTURE', True, ['M_kg'],
                lambda M_kg, space_fraction=None: energy_partition(M_kg, space_fraction),
                ['text'],
            ),
            Equation(
                'stiff_matter_ceiling',
                'The incompressibility ceiling: p = rho c^2 (Zel\'dovich), '
                'sound speed = c',
                r'p=\rho c^2,\;c_s=c\;\text{(stiffest causal EoS)}',
                'sound cone opens to exactly one radian of the light cone',
                'ESTABLISHED', True, [],
                lambda: stiff_matter_ceiling(), ['text'],
            ),
            Equation(
                'cosmic_cavitation_budget',
                'SECONDARY — naive Omega_cav = Omega_BH (1 - d*) vs Omega_Lambda; '
                'expected to fall short (dark-flow, not dark-energy magnitude)',
                r'\Omega_{\rm cav}\approx\Omega_{\rm BH}(1-d^\*)\;\lessgtr\;\Omega_\Lambda',
                'accumulated stiff-space phase from the black-hole population',
                'CONJECTURE', True, [],
                lambda omega_bh=1.0e-5, space_fraction=None:
                    cosmic_cavitation_budget(omega_bh, space_fraction), ['text'],
            ),
        ]

    # ── run / viewer ────────────────────────────────────────────────────────

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"'{equation_name}' not in desitter_cavitation")
        result = eq.compute(**params) if params else eq.compute()
        return {'result': result, 'equation': eq, 'params': params}

    def viewer_data(self, equation_name: str, params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        out = self.run(equation_name, params)
        return {'mode': display_mode, 'module': self.name,
                'equation': equation_name, 'data': out['result']}

    def shell_commands(self) -> Dict[str, Any]:
        return {
            'dsc_table':  lambda: mass_class_table(),
            'dsc_holcus': lambda M=10 * M_SUN: {
                'K_core_m^-4': kretschmann_core(M),
                'K_over_K_Planck': kretschmann_ratio_planck(M),
            },
            'dsc_check':  lambda: no_singularity_check(),
        }
