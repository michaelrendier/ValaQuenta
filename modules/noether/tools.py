"""
ainulindale_engine.modules.noether.tools
==========================================
NoetherModule — registry contract implementation.

Equations:
  1. conservation_diagnostic   full J^μ conservation check
  2. violation_scan            scan across algebra strata
  3. resonance_artifacts       oscillation detection
  4. blockchain_record         record to NoetherLedger
  5. blockchain_verify         verify ledger chain
  6. blockchain_summary        ledger summary

Version: 0.111
"""

import math
from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    ALG_R, ALG_C, ALG_H, ALG_O, ALG_NAME, ALG_GAUGE, N_GEN,
    activation_current, noether_violation, conservation_diagnostic,
    resonance_artifacts, conservation_status, get_ledger,
)


class NoetherModule(EquationModule):

    @property
    def name(self): return 'noether'

    @property
    def display_name(self): return 'Noether Currents  ∂_μJ^μ = 0'

    @property
    def version(self): return '0.111'

    @property
    def description(self):
        return (
            'Emmy Noether theorem applied to L_NN. Symmetry → conserved current. '
            'Violation = |∂_μJ^μ| — the training diagnostic with no GD analog. '
            'Blockchain ledger records every violation event. '
            'Resonance artifact detection identifies boundary oscillations.'
        )

    @property
    def confidence_floor(self): return 'THEORETICAL'

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='conservation_diagnostic',
                display='∂_μJ^μ — full Noether conservation check',
                latex=r'\partial_\mu J^\mu = 0 \quad J^a = g\sum_i|\Psi_i|^2',
                radian_form='J^a = g * sum |psi_i|^2  per generator a',
                confidence='THEORETICAL',
                code_verified=True,
                params=['psi_norms', 'g', 'algebra'],
                compute=None,
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='violation_scan',
                display='Violation scan across all algebra strata',
                latex=r'\Delta J^a\text{ across }{\mathbb R}\to{\mathbb C}\to{\mathbb H}\to{\mathbb O}',
                radian_form='scan violation for R, C, H, O at given psi_norms',
                confidence='THEORETICAL',
                code_verified=True,
                params=['psi_norms', 'g'],
                compute=None,
                display_options=['text', '3d_cartesian'],
            ),
            Equation(
                name='resonance_artifacts',
                display='Resonance artifact detection (J history)',
                latex=r'\text{oscillation in } J^0_l \Rightarrow \text{boundary artifact}',
                radian_form='zero crossings in J[0] across layer history',
                confidence='THEORETICAL',
                code_verified=True,
                params=['n_steps', 'g', 'algebra'],
                compute=None,
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='blockchain_record',
                display='Record violation to NoetherLedger (blockchain)',
                latex=r'\text{block}_{i} = H\bigl(\text{block}_{i-1}\|J^a\|\Delta\bigr)',
                radian_form='SHA-256 hash chain of violation events',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['algebra', 'violation', 'g'],
                compute=None,
                display_options=['text'],
            ),
            Equation(
                name='blockchain_verify',
                display='Verify NoetherLedger chain integrity',
                latex=r'h_i = H(\text{content}_i),\quad h_{i-1} = \text{prev\_hash}_i',
                radian_form='SHA-256 hash verification of full chain',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: get_ledger().verify(),
                display_options=['text'],
            ),
            Equation(
                name='blockchain_summary',
                display='NoetherLedger summary',
                latex=r'\#\text{blocks}, \#\text{violations}, \text{valid}',
                radian_form='summary of ledger: blocks, violations, passes, validity',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: get_ledger().summary(),
                display_options=['text'],
            ),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in noether module")

        psi   = self._get_psi(params)
        g     = float(params.get('g', 0.01))
        alg   = int(params.get('algebra', ALG_C))

        if equation_name == 'conservation_diagnostic':
            result = conservation_diagnostic(psi, g, alg)

        elif equation_name == 'violation_scan':
            result = {}
            for a in (ALG_R, ALG_C, ALG_H, ALG_O):
                d = conservation_diagnostic(psi, g, a)
                result[ALG_NAME[a]] = {
                    'violation': d['violation'],
                    'status':    d['status'],
                    'J':         d['J'],
                }

        elif equation_name == 'resonance_artifacts':
            n_steps = int(params.get('n_steps', 20))
            # Simulate J history: psi_norms decay geometrically over n_steps
            history = []
            for s in range(n_steps):
                decay = 0.9 ** s
                psi_s = [p * decay for p in psi]
                history.append(activation_current(psi_s, g, alg))
            result = resonance_artifacts(history)
            result['history_length'] = n_steps

        elif equation_name == 'blockchain_record':
            viol = float(params.get('violation', 0.0))
            J    = activation_current(psi, g, alg)
            block = get_ledger().record(alg, viol, J)
            result = {'block_index': block['index'], 'hash': block['hash'][:16] + '…',
                      'status': block['status'], 'violation': viol}

        elif eq.compute is not None:
            result = eq.compute()
        else:
            result = {'note': 'no compute path'}

        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str,
                    params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)
        r = result['result']

        if display_mode == 'text':
            return {'text': self._fmt(equation_name, r)}

        elif display_mode == 'complex_plane':
            return self._complex_data(equation_name, params, r)

        elif display_mode == '3d_cartesian':
            return self._3d_data(equation_name, params, r)

        return {'text': self._fmt(equation_name, r)}

    def _fmt(self, name: str, result) -> str:
        if isinstance(result, dict):
            lines = [f"  {name}"]
            for k, v in result.items():
                if isinstance(v, float):
                    lines.append(f"  {k:22s} = {v:.8f}")
                elif isinstance(v, list) and v and isinstance(v[0], float):
                    lines.append(f"  {k:22s} = [{', '.join(f'{x:.4f}' for x in v[:6])}{'...' if len(v)>6 else ''}]")
                elif isinstance(v, dict):
                    lines.append(f"  {k}:")
                    for kk, vv in v.items():
                        lines.append(f"    {kk:20s} = {vv}")
                else:
                    lines.append(f"  {k:22s} = {v}")
            return '\n'.join(lines)
        return f"  {name}: {result}"

    def _get_psi(self, params) -> List[float]:
        psi = params.get('psi_norms', [0.5, 0.4, 0.3, 0.2])
        if isinstance(psi, (int, float)):
            psi = [float(psi)]
        return psi

    def _complex_data(self, name, params, result) -> Dict:
        if name == 'conservation_diagnostic':
            J = result.get('J', [])
            # Plot J^a as points on unit circle (one per generator)
            n = len(J)
            import math as _m
            cartesian = [
                (J[i] * _m.cos(2 * _m.pi * i / n),
                 J[i] * _m.sin(2 * _m.pi * i / n))
                for i in range(n)
            ]
            return {
                'type':       'polar_trajectory',
                'trajectory': [(i, J[i]) for i in range(n)],
                'cartesian':  cartesian,
            }
        elif name == 'resonance_artifacts':
            # Simulated J[0] history as polar trajectory
            n_steps = int(params.get('n_steps', 20))
            g   = float(params.get('g', 0.01))
            alg = int(params.get('algebra', ALG_C))
            pts = []
            psi = self._get_psi(params)
            import math as _m
            for s in range(n_steps):
                decay = 0.9 ** s
                psi_s = [p * decay for p in psi]
                J = activation_current(psi_s, g, alg)
                j0 = J[0] if J else 0.0
                theta = 2 * _m.pi * s / n_steps
                pts.append((j0 * _m.cos(theta), j0 * _m.sin(theta)))
            return {'type': 'polar_trajectory', 'cartesian': pts, 'trajectory': [(i, pts[i][0]) for i in range(n_steps)]}
        return {'text': self._fmt(name, result)}

    def _3d_data(self, name, params, result) -> Dict:
        if name == 'violation_scan':
            pts = []
            psi = self._get_psi(params)
            g   = float(params.get('g', 0.01))
            for alg in (ALG_R, ALG_C, ALG_H, ALG_O):
                d = conservation_diagnostic(psi, g, alg)
                pts.append((float(alg), d['violation'], d['delta_J']))
            return {
                'type':   '3d_flow',
                'points': pts,
                'axes':   ('algebra_stratum', 'violation', 'delta_J'),
            }
        return {'text': self._fmt(name, result)}

    def shell_commands(self) -> Dict:
        return {
            'noether':   lambda psi=None, g=0.01, alg=ALG_C:
                             conservation_diagnostic(psi or [0.5,0.4,0.3], g, alg),
            'ledger':    lambda: get_ledger().summary(),
            'verify':    lambda: get_ledger().verify(),
        }
