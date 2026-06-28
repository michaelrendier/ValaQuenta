"""
ainulindale_engine.modules.sonification.maths
===============================================
Equation-derived audio. Every sound is a derivation.

ω (angular frequency) = pitch.
Radian transform made audible.
fractions.Fraction throughout; float only at WAV render boundary.

Particle-frequency table (just intonation, A=440 Hz):
  Higgs     → A2 = 110 Hz   (cello, ground state)
  Photon    → A6 = 1760 Hz  (flute, massless)
  Electron  → C#5 = 550 Hz  (oboe)
  W+        → E5 = 660 Hz   (french horn, ascending)
  W-        → D5 = 586 Hz   (french horn, descending)
  Z0        → A1 = 55 Hz    (tuba, neutral massive)
  Gluon(1)  → A3 = 220 Hz   (percussion voice 1)

Quasi-particle rests (exact integer samples):
  Phonon    = SR/4    (short decay)
  Gravinon  = SR × 144/89  (Fibonacci/phi convergent)

This module feeds the viewer's sonification display mode.
The standalone Ainulindale Synthesizer is a separate repo.

Version: 0.111
"""

import math
from fractions import Fraction
from typing import Dict, List, Any, Optional, Tuple


# ── Constants ──────────────────────────────────────────────────────────────────

SAMPLE_RATE   = 44100
MAX_AMP       = 28000
CONCERT_A     = Fraction(440)
BEAT_SAMPLES  = 22050   # half second

# Fibonacci/phi convergent for Gravinon rest
FIB_NUM       = 144
FIB_DEN       = 89
GRAVINON_SAMPLES = (BEAT_SAMPLES * FIB_NUM) // FIB_DEN

PHONON_SAMPLES  = BEAT_SAMPLES // 4
EXCITON_SAMPLES = BEAT_SAMPLES // 2
MAGNON_SAMPLES  = BEAT_SAMPLES * 3 // 8
ROTON_SAMPLES   = BEAT_SAMPLES * 3 // 4
PLASMON_SAMPLES = BEAT_SAMPLES

# Just intonation ratios — exact Fraction arithmetic
def _jf(num, den, octave=0) -> Fraction:
    base = CONCERT_A * Fraction(num, den)
    if octave > 0:
        return base * (2 ** octave)
    elif octave < 0:
        return base * Fraction(1, 2 ** (-octave))
    return base


FREQ: Dict[str, Fraction] = {
    'higgs'    : _jf(1, 1, -2),       # A2 = 110 Hz
    'photon'   : _jf(1, 1,  2),       # A6 = 1760 Hz
    'electron' : _jf(5, 4,  0),       # C#5 = 550 Hz
    'positron' : _jf(5, 4,  0),       # same, inverted phase
    'nu_e'     : _jf(9, 8,  1),       # B5
    'nu_mu'    : _jf(4, 3,  1),       # D6
    'nu_tau'   : _jf(3, 2,  1),       # E6
    'W_plus'   : _jf(3, 2,  0),       # E5 = 660 Hz
    'W_minus'  : _jf(4, 3,  0),       # D5 ≈ 586 Hz
    'Z0'       : _jf(1, 1, -3),       # A1 = 55 Hz
    'gluon_1'  : _jf(1, 1, -1),       # A3 = 220 Hz
    'gluon_2'  : _jf(9, 8, -1),       # B3
    'gluon_3'  : _jf(5, 4, -1),       # C#4
    'gluon_4'  : _jf(4, 3, -1),       # D4
    'gluon_5'  : _jf(3, 2, -1),       # E4
    'gluon_6'  : _jf(5, 3, -1),       # F#4
    'gluon_7'  : _jf(15, 8, -1),      # G#4
    'gluon_8'  : _jf(2, 1, -1),       # A4 = 440 Hz
    'up'       : _jf(5, 4,  1),       # C#6
    'down'     : _jf(4, 3,  1),       # D6
    'strange'  : _jf(45, 32, 0),      # F#5 (tritone)
    'charm'    : _jf(3, 2,  1),       # E6
    'bottom'   : _jf(5, 3,  0),       # F#5
    'top'      : _jf(2, 1,  2),       # A7 = 3520 Hz (brief, massive)
    # SMNNIP algebra strata
    'stratum_R': _jf(1, 1, -2),       # A2
    'stratum_C': _jf(5, 4, -1),       # C#4
    'stratum_H': _jf(3, 2, -1),       # E4
    'stratum_O': _jf(2, 1,  0),       # A5 = 880 Hz
    # Inversion fixed point and attractor
    'phi_attractor': _jf(5, 3, 0),    # F#5 — golden ratio approximant
    'd_star'       : _jf(5, 4, -2),   # C#3 — Berry-Keating
}

QUASIPARTICLE_RESTS: Dict[str, int] = {
    'phonon' : PHONON_SAMPLES,
    'exciton': EXCITON_SAMPLES,
    'magnon' : MAGNON_SAMPLES,
    'roton'  : ROTON_SAMPLES,
    'plasmon': PLASMON_SAMPLES,
    'gravinon': GRAVINON_SAMPLES,
}


# ── Omega from equation result ─────────────────────────────────────────────────

def omega_from_equation(equation_name: str,
                         result: Any) -> Dict[str, Any]:
    """
    Derive ω (angular frequency, rad/s) from an equation result.

    Strategy:
      1. If result is a float, map it to a frequency via log-scaling
         relative to concert A = 440 Hz.
      2. If result is a dict, look for known keys: 'phi', 'r', 'alpha_nn',
         'd_star', 'gap', 'violation', 'I_info'.
      3. If the equation name matches a particle, return that FREQ.
    """
    freq: Optional[Fraction] = None
    label = equation_name

    # Named particle match
    for particle, f in FREQ.items():
        if particle in equation_name.lower():
            freq = f
            label = particle
            break

    if freq is None:
        # Extract a float from result
        val = None
        if isinstance(result, float):
            val = result
        elif isinstance(result, dict):
            for key in ('phi', 'r', 'alpha_nn', 'd_star', 'gap',
                        'violation', 'I_info', 'total', 'final_r'):
                if key in result and isinstance(result[key], (int, float)):
                    val = float(result[key])
                    label = key
                    break

        if val is not None and val > 0:
            # Map val to frequency: f = A4 * 2^(log2(val))  clamped to [20, 20000]
            raw_freq = 440.0 * (2.0 ** (math.log2(abs(val)) / 8.0))
            raw_freq = max(20.0, min(20000.0, raw_freq))
            freq = Fraction(raw_freq).limit_denominator(100)
        else:
            freq = FREQ.get('stratum_C', Fraction(440))

    omega = freq * Fraction(2) * Fraction(math.floor(math.pi * 1000000), 1000000)
    omega_float = float(freq) * 2.0 * math.pi

    return {
        'omega'     : omega_float,
        'freq_hz'   : float(freq),
        'freq_frac' : str(freq),
        'label'     : label,
        'equation'  : equation_name,
        'duration_s': 2.0,
    }


def wavetable(name: str, n_samples: int = 512) -> Dict[str, Any]:
    """
    Generate a named wavetable.

    Available:
      'sine'         pure sine
      'rydberg'      hydrogen Rydberg waveform (1/n² superposition)
      'higgs_hat'    Mexican hat oscillation (SSB potential)
      'phi_recursion' r → 1+1/r spiral waveform
      'fano'         Fano-plane 7-harmonic superposition
    """
    if n_samples < 2:
        n_samples = 512

    t = [i / n_samples for i in range(n_samples)]

    if name == 'rydberg':
        # Superposition of first 4 Rydberg harmonics: f_n ~ 1/n²
        wave = [
            sum(
                math.sin(2 * math.pi * n * n * ti) / (n * n)
                for n in range(1, 5)
            )
            for ti in t
        ]
    elif name == 'higgs_hat':
        # Oscillation around Mexican hat minimum: V(β)=μ²β²/2 - λβ⁴/4, μ²<0
        # Small oscillations at β=vev: ω² = 2|μ²|
        mu_sq = -1.0
        lam   = 0.5
        vev   = math.sqrt(abs(mu_sq) / lam)
        omega_h = math.sqrt(2 * abs(mu_sq))
        wave  = [math.cos(omega_h * 2 * math.pi * ti) for ti in t]
    elif name == 'phi_recursion':
        # r_{n+1} = 1 + 1/r_n trajectory → periodic orbit around phi
        phi  = (1 + math.sqrt(5)) / 2
        r    = 2.0
        vals = []
        for _ in range(n_samples):
            vals.append(r - phi)   # deviation from attractor
            r = 1.0 + 1.0 / r
        mx = max(abs(v) for v in vals) or 1.0
        wave = [v / mx for v in vals]
    elif name == 'fano':
        # 7-harmonic Fano plane superposition (one per octonion generator)
        fano_ratios = [Fraction(n+1, 1) for n in range(7)]
        wave = [
            sum(
                math.sin(2 * math.pi * float(r) * ti) / (i+1)
                for i, r in enumerate(fano_ratios)
            )
            for ti in t
        ]
    else:
        # pure sine
        wave = [math.sin(2 * math.pi * ti) for ti in t]

    # Normalise to [-1, 1]
    mx = max(abs(v) for v in wave) or 1.0
    wave = [v / mx for v in wave]

    return {
        'name'    : name,
        'samples' : wave,
        'n'       : n_samples,
        'note'    : f'Wavetable: {name}',
    }


def sonification_data(equation_name: str,
                       params: Dict[str, Any],
                       result: Any,
                       wavetable_name: str = 'sine') -> Dict[str, Any]:
    """
    Produce the full sonification viewer_data dict.
    Combines omega_from_equation + wavetable.
    """
    omega_info = omega_from_equation(equation_name, result)
    wt         = wavetable(wavetable_name)

    # Modulate the wavetable by the derived frequency
    freq  = omega_info['freq_hz']
    omega = omega_info['omega']
    dur   = omega_info['duration_s']
    sr    = SAMPLE_RATE
    n     = int(sr * dur)
    t     = [i / sr for i in range(n)]

    # Preview waveform (downsample to 512 pts for viewer)
    preview_n = 512
    preview   = [
        wt['samples'][int(i * len(wt['samples']) / preview_n) % len(wt['samples'])]
        * math.sin(2 * math.pi * freq * i / preview_n)
        for i in range(preview_n)
    ]
    mx = max(abs(v) for v in preview) or 1.0
    preview = [v / mx for v in preview]

    return {
        'omega'          : omega,
        'freq_hz'        : freq,
        'freq_frac'      : omega_info['freq_frac'],
        'label'          : omega_info['label'],
        'equation'       : equation_name,
        'wavetable'      : wavetable_name,
        'waveform'       : preview,
        'duration_s'     : dur,
        'sample_rate'    : sr,
        'note'           : 'Viewer plays via SonificationPanel. Synth export via standalone repo.',
    }
