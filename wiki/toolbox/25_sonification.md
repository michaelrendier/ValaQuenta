# Sonification  ω = pitch

**Module:** `ValaQuenta.modules.sonification`
**Import:** `from ValaQuenta.modules.sonification.tools import SonificationModule`
**Theory page:** [`../sonification.md`](../sonification.md)

---

`sonification` · v0.111 · confidence floor **ESTABLISHED**

Equation-derived audio. ω (angular frequency) = pitch. Radian transform made audible. fractions.Fraction throughout; float only at WAV render boundary. Viewer renders waveform and plays via SonificationPanel. Standalone Ainulindale Synthesizer is a separate repo.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`tone_higgs`** — higgs  f = 110.00 Hz
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(p='higgs')`
```python
>>> module.run('tone_higgs', {})['result']
{'omega': 691.1503837897545, 'freq_hz': 110.0, 'label': 'higgs'}
```

**`tone_photon`** — photon  f = 1760.00 Hz
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(p='photon')`
```python
>>> module.run('tone_photon', {})['result']
{'omega': 11058.406140636072, 'freq_hz': 1760.0, 'label': 'photon'}
```

**`tone_electron`** — electron  f = 550.00 Hz
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(p='electron')`
```python
>>> module.run('tone_electron', {})['result']
{'omega': 3455.7519189487725, 'freq_hz': 550.0, 'label': 'electron'}
```

**`tone_W_plus`** — W_plus  f = 660.00 Hz
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(p='W_plus')`
```python
>>> module.run('tone_W_plus', {})['result']
{'omega': 4146.9023027385265, 'freq_hz': 660.0, 'label': 'W_plus'}
```

**`tone_W_minus`** — W_minus  f = 586.67 Hz
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(p='W_minus')`
```python
>>> module.run('tone_W_minus', {})['result']
{'omega': 3686.135380212024, 'freq_hz': 586.6666666666666, 'label': 'W_minus'}
```

**`tone_Z0`** — Z0  f = 55.00 Hz
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(p='Z0')`
```python
>>> module.run('tone_Z0', {})['result']
{'omega': 345.57519189487726, 'freq_hz': 55.0, 'label': 'Z0'}
```

**`tone_gluon_1`** — gluon_1  f = 220.00 Hz
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(p='gluon_1')`
```python
>>> module.run('tone_gluon_1', {})['result']
{'omega': 1382.300767579509, 'freq_hz': 220.0, 'label': 'gluon_1'}
```

**`tone_phi_attractor`** — phi_attractor  f = 733.33 Hz
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(p='phi_attractor')`
```python
>>> module.run('tone_phi_attractor', {})['result']
{'omega': 4607.66922526503, 'freq_hz': 733.3333333333334, 'label': 'phi_attractor'}
```

**`tone_d_star`** — d_star  f = 137.50 Hz
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(p='d_star')`
```python
>>> module.run('tone_d_star', {})['result']
{'omega': 863.9379797371931, 'freq_hz': 137.5, 'label': 'd_star'}
```

**`tone_stratum_R`** — stratum_R  f = 110.00 Hz
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(p='stratum_R')`
```python
>>> module.run('tone_stratum_R', {})['result']
{'omega': 691.1503837897545, 'freq_hz': 110.0, 'label': 'stratum_R'}
```

**`tone_stratum_C`** — stratum_C  f = 275.00 Hz
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(p='stratum_C')`
```python
>>> module.run('tone_stratum_C', {})['result']
{'omega': 1727.8759594743863, 'freq_hz': 275.0, 'label': 'stratum_C'}
```

**`tone_stratum_H`** — stratum_H  f = 330.00 Hz
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(p='stratum_H')`
```python
>>> module.run('tone_stratum_H', {})['result']
{'omega': 2073.4511513692632, 'freq_hz': 330.0, 'label': 'stratum_H'}
```

**`tone_stratum_O`** — stratum_O  f = 880.00 Hz
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(p='stratum_O')`
```python
>>> module.run('tone_stratum_O', {})['result']
{'omega': 5529.203070318036, 'freq_hz': 880.0, 'label': 'stratum_O'}
```

**`wavetable_sine`** — Wavetable: sine
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(n='sine')`
```python
>>> module.run('wavetable_sine', {})['result']
{'name': 'sine', 'samples': [0.0, 0.012271538285719925, 0.024541228522912288, 0.03680722294135883, 0.049067674327418015, 0.06132073630220858, 0.07356456359966743, 0.0857973123444399, 0.0980171403295606, 0.11022220729388306, 0.1224106751992162, 0.13458070850712617, 0.14673047445536175, 0.158858143...
```

**`wavetable_rydberg`** — Wavetable: rydberg
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(n='rydberg')`
```python
>>> module.run('wavetable_rydberg', {})['result']
{'name': 'rydberg', 'samples': [0.0, 0.04002023527729629, 0.07950999640342718, 0.11795506721919254, 0.15487316386631306, 0.18982846368069003, 0.22244447000019799, 0.25241475674939334, 0.27951121627897213, 0.3035895275994927, 0.3245916662850452, 0.3425453879637104, 0.35756073024270163, 0.369823688...
```

**`wavetable_higgs_hat`** — Wavetable: higgs_hat
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(n='higgs_hat')`
```python
>>> module.run('wavetable_higgs_hat', {})['result']
{'name': 'higgs_hat', 'samples': [1.0, 0.9998494055682458, 0.9993976676303487, 0.998644922244745, 0.9975913961299618, 0.9962374065963323, 0.9945833614504255, 0.9926297588722188, 0.9903771872650526, 0.9878263250784094, 0.984977940603572, 0.9818328917422232, 0.9783921257480552, 0.9746566789414676, ...
```

**`wavetable_phi_recursion`** — Wavetable: phi_recursion
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(n='phi_recursion')`
```python
>>> module.run('wavetable_phi_recursion', {})['result']
{'name': 'phi_recursion', 'samples': [1.0, -0.3090169943749476, 0.12732200375003455, -0.04721359549995786, 0.018237254218789294, -0.00693614951919038, 0.002653718571468543, -0.0010129956984892806, 0.0003870224773126917, -0.0001478159269263816, 5.646263024841786e-05, -2.156651820018057e-05, 8.2377...
```

**`wavetable_fano`** — Wavetable: fano
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(n='fano')`
```python
>>> module.run('wavetable_fano', {})['result']
{'name': 'fano', 'samples': [0.0, 0.05198921484745657, 0.103821958304852, 0.15534254545838208, 0.20639685966859042, 0.2568331250422495, 0.30650266499002826, 0.3552606423714998, 0.4029667768475085, 0.44948603520650066, 0.49468929060512984, 0.5384539468631224, 0.5806645241766716, 0.6212132028620304...
```

**`quasiparticle_rests`** — Quasi-particle rest durations (Gravinon = 144/89 beats)
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('quasiparticle_rests', {})['result']
{'phonon': 5512, 'exciton': 11025, 'magnon': 8268, 'roton': 16537, 'plasmon': 22050, 'gravinon': 35676}
```

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`tone`, `wavetable`

---

### Running via the registry

```python
from ValaQuenta.modules.sonification.tools import SonificationModule

m = SonificationModule()
m.formulary()                              # list every Equation this module exposes
m.run('tone_higgs', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('tone_higgs', {}, 'text')     # -> {'text': '...formatted...'}
```
