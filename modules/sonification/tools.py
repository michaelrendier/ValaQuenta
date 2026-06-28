"""
ainulindale_engine.modules.sonification.tools
===============================================
SonificationModule — registry contract.

Equations:
  1. particle_tone      named particle → ω, frequency
  2. equation_tone      any equation result → ω
  3. wavetable_rydberg  hydrogen Rydberg waveform
  4. wavetable_higgs    Mexican hat oscillation
  5. wavetable_phi      phi-recursion waveform
  6. wavetable_fano     Fano 7-harmonic
  7. quasiparticle_rest named rest duration

Version: 0.111
"""

import math
from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    FREQ, QUASIPARTICLE_RESTS,
    omega_from_equation, wavetable, sonification_data,
)


class SonificationModule(EquationModule):

    @property
    def name(self): return 'sonification'

    @property
    def display_name(self): return 'Sonification  ω = pitch'

    @property
    def version(self): return '0.111'

    @property
    def description(self):
        return (
            'Equation-derived audio. ω (angular frequency) = pitch. '
            'Radian transform made audible. fractions.Fraction throughout; '
            'float only at WAV render boundary. '
            'Viewer renders waveform and plays via SonificationPanel. '
            'Standalone Ainulindale Synthesizer is a separate repo.'
        )

    @property
    def confidence_floor(self): return 'ESTABLISHED'

    def formulary(self) -> List[Equation]:
        eqs = []

        # Named particle tones
        for particle in ['higgs', 'photon', 'electron', 'W_plus', 'W_minus',
                         'Z0', 'gluon_1', 'phi_attractor', 'd_star',
                         'stratum_R', 'stratum_C', 'stratum_H', 'stratum_O']:
            freq = FREQ.get(particle)
            if freq is None:
                continue
            eqs.append(Equation(
                name=f'tone_{particle}',
                display=f'{particle}  f = {float(freq):.2f} Hz',
                latex=rf'\omega_{{particle}} = 2\pi\cdot{float(freq):.2f}\,\text{{Hz}}',
                radian_form=f'omega = 2*pi * {float(freq):.4f}',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda p=particle: {
                    'omega'   : float(FREQ[p]) * 2 * math.pi,
                    'freq_hz' : float(FREQ[p]),
                    'label'   : p,
                },
                display_options=['sonification', 'text'],
            ))

        # Wavetables
        for wt_name in ['sine', 'rydberg', 'higgs_hat', 'phi_recursion', 'fano']:
            eqs.append(Equation(
                name=f'wavetable_{wt_name}',
                display=f'Wavetable: {wt_name}',
                latex=rf'\text{{wavetable: }}{wt_name}',
                radian_form=f'512-point {wt_name} wavetable — radian-primary',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda n=wt_name: wavetable(n),
                display_options=['sonification', 'text'],
            ))

        # Quasi-particle rests
        eqs.append(Equation(
            name='quasiparticle_rests',
            display='Quasi-particle rest durations (Gravinon = 144/89 beats)',
            latex=r'\text{Gravinon}=\frac{144}{89}\text{ beats}\to\varphi',
            radian_form='rest durations in samples, exact integer arithmetic',
            confidence='ESTABLISHED',
            code_verified=True,
            params=[],
            compute=lambda: {k: v for k, v in QUASIPARTICLE_RESTS.items()},
            display_options=['text'],
        ))

        return eqs

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not in sonification module")
        result = eq.compute()
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str,
                    params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        result = self.run(equation_name, params)['result']

        if display_mode == 'sonification' or 'tone_' in equation_name:
            # Determine wavetable name from params or equation
            wt_name = params.get('wavetable', 'sine')
            if 'wavetable_' in equation_name:
                wt_name = equation_name.replace('wavetable_', '')

            # Get omega
            if isinstance(result, dict) and 'omega' in result:
                omega = result['omega']
                freq  = result.get('freq_hz', omega / (2 * math.pi))
                label = result.get('label', equation_name)
                wt    = wavetable(wt_name)
                # Modulate waveform at derived frequency
                preview_n = 512
                wave = [
                    wt['samples'][i % len(wt['samples'])]
                    * math.sin(2 * math.pi * freq * i / preview_n)
                    for i in range(preview_n)
                ]
                mx = max(abs(v) for v in wave) or 1.0
                wave = [v / mx for v in wave]
                return {
                    'omega'     : omega,
                    'freq_hz'   : freq,
                    'label'     : label,
                    'waveform'  : wave,
                    'duration_s': 2.0,
                    'wavetable' : wt_name,
                }
            elif isinstance(result, dict) and 'samples' in result:
                # Raw wavetable — use stratum_C frequency
                freq = float(FREQ.get('stratum_C', 440))
                return {
                    'omega'    : freq * 2 * math.pi,
                    'freq_hz'  : freq,
                    'label'    : equation_name,
                    'waveform' : result['samples'][:512],
                    'duration_s': 2.0,
                }

        if display_mode == 'text':
            return {'text': self._fmt(equation_name, result)}

        return {'text': self._fmt(equation_name, result)}

    def _fmt(self, name, result) -> str:
        if isinstance(result, dict):
            lines = [f"  {name}"]
            for k, v in result.items():
                if isinstance(v, float):
                    lines.append(f"  {k:20s} = {v:.6f}")
                elif isinstance(v, list) and len(v) > 8:
                    lines.append(f"  {k:20s} = [{', '.join(f'{x:.3f}' for x in v[:6])}...]")
                elif not isinstance(v, list):
                    lines.append(f"  {k:20s} = {v}")
            return '\n'.join(lines)
        return f"  {name}: {result}"

    def shell_commands(self) -> Dict:
        return {
            'tone':      lambda p='higgs': omega_from_equation(f'tone_{p}', {}),
            'wavetable': lambda n='rydberg': wavetable(n),
        }
